<!-- .slide: data-background="./race-drag.png" -->

NOTES:

- SLOW DOWN
- Now that we have pounded out the bugs it is time to see how fast our creation
  is.  First thing we are going to need our benchmarks.

---

<!-- .slide: data-background="./race-drag.png" -->

```cc []
using TransferCacheEnv =
    FakeTransferCacheEnvironment<TransferCache<
        MinimalFakeCentralFreeList,
        FakeTransferCacheManager>>;

using LockFreeEnv =
    FakeTransferCacheEnvironment<TransferCache<
        MinimalFakeCentralFreeList,
        FakeTransferCacheManager>>;
```

[9587e53](https://github.com/google/tcmalloc/blob/9587e53228f6a578745fd424bafd4d90267e3060/tcmalloc/transfer_cache_benchmark.cc#L26-L32) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Fortunately, we put in all that work be able to fake parts of our environment
  efficiently.
- And glue it together for some direct comparisons

---

<!-- .slide: data-background="./race-drag.png" -->

```cc []
template <typename Env>
void BM_Draining(benchmark::State& state) {
  Env e;
  int src = state.thread_index % 2;
  int dst = (src + 1) % 2;
  for (auto iter : state) {
    benchmark::DoNotOptimize(batch);
    e.cache[src].RemoveRange(batch, kBatchSize);
    benchmark::DoNotOptimize(batch);
    e.cache[dst].InsertRange(batch, kBatchSize);
    benchmark::DoNotOptimize(batch);
  }
}
```

[9587e53](https://github.com/google/tcmalloc/blob/9587e53228f6a578745fd424bafd4d90267e3060/tcmalloc/transfer_cache_benchmark.cc#L35) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Fair warning, this code is more slide ware than previous ones.  Turns out the
  setup require just doesn't fit on a slide.  The real code is on github.
- Now we can look at some nice comparisons.

---

<!-- .slide: data-background="./race-drag.png" -->

```json [|2-3,8-9|6-7,12-13]
name                                        cpu/op
BM_Draining<TransferCacheEnv>/threads:2     292ns ± 5%
BM_Draining<TransferCacheEnv>/threads:4     888ns ± 8%
BM_Draining<TransferCacheEnv>/threads:8    2.25µs ± 7%
BM_Draining<TransferCacheEnv>/threads:16   4.66µs ± 5%
BM_Draining<TransferCacheEnv>/threads:32   9.34µs ± 6%
BM_Draining<TransferCacheEnv>/threads:64   29.5µs ± 6%
BM_Draining<LockFreeEnv>/threads:2          286ns ±24%
BM_Draining<LockFreeEnv>/threads:4          793ns ±11%
BM_Draining<LockFreeEnv>/threads:8         1.79µs ± 4%
BM_Draining<LockFreeEnv>/threads:16        3.37µs ±21%
BM_Draining<LockFreeEnv>/threads:32        5.94µs ±32%
BM_Draining<LockFreeEnv>/threads:64        11.6µs ± 7%
```

[9587e53](https://github.com/google/tcmalloc/commit/9587e53228f6a578745fd424bafd4d90267e3060) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- ADVANCE: at low contention our numbers are broadly similar, although the lock free
  version has a higher variance.  That is interesting, but not something I am
  going to worry about right now.
- Importantly, it is not significantly worse at low contention.  The goal of all
  of this was to reduce contention and increase parallelism after.
- ADVANCE: at high contention it is 2x faster!!  I can just taste the promo I am
  going to get from these wins!
- Let's see how this does if we plug it into websearch!

---

<!-- .slide: data-background="./race-drag.png" -->

```json
-- total:qps --
base: XXXXX.XX ±XX (8 trials, 8.0 robust values)
test: YYYYY.YY ±XX (8 trials, 7.0 robust values)
diff: -17.29% ±1.333%
Possible significant effect (p=0.000)
```

NOTES:

- SLOW DOWN
- That is very, very not good.
- qps is Queries Per Second which is a mesaure of throughput.  That number is
  suppose to go up.  Also 17% is a really large loss.

-----

<!-- .slide: data-background="./race-drag.png" -->

NOTES:

- SLOW DOWN
- The problem with benchmarks is that they can be quite artificial.  You may
  think you are doing this.

---

<!-- .slide: data-background="./race-autocross.png" -->

NOTES:

- SLOW DOWN
- The problem with benchmarks is that they can be quite artificial.  You may
  think you are doing this.
- But in fact you are doing this.
- Don't get me wrong, both have value, but it is important to understand what
  you are doing.


---

<!-- .slide: data-background="./race-autocross.png" -->

```cc [|3,8]
using TransferCacheEnv =
    FakeTransferCacheEnvironment<TransferCache<
        MinimalFakeCentralFreeList,
        FakeTransferCacheManager>>;

using LockFreeEnv =
    FakeTransferCacheEnvironment<TransferCache<
        MinimalFakeCentralFreeList,
        FakeTransferCacheManager>>;
```

[9587e53](https://github.com/google/tcmalloc/blob/9587e53228f6a578745fd424bafd4d90267e3060/tcmalloc/transfer_cache_benchmark.cc#L26-L32) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Remember this part it?  
- ADVANCE: Perhaps those fakes aren't actually modelling the overall system's
  behavior very well..

---

<!-- .slide: data-background="./treachery-magritte.png" -->

```cc [3,8]
using TransferCacheEnv =
    FakeTransferCacheEnvironment<TransferCache<
        MinimalFakeCentralFreeList,
        FakeTransferCacheManager>>;

using LockFreeEnv =
    FakeTransferCacheEnvironment<TransferCache<
        MinimalFakeCentralFreeList,
        FakeTransferCacheManager>>;
```

[Post Modern](https://www.youtube.com/watch?v=QTLn3goa3A8) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- One of the hardest things to remember in software is that the referant is not
  the referred.  
- My `MinimalFakeCentralFreeList` behaves like the actual `CentralFreeList` exactly as
  much as this picture of a pipe behaves like a pipe.

---

<!-- .slide: data-background="./treachery-magritte.png" -->

```cc []
class MinimalFakeCentralFreeList {
  void AllocateBatch(void** batch, int n) {
    for (int i = 0; i < n; ++i) {
      batch[i] = &batch[i];
    }
  }

  void FreeBatch(void** batch, int n) {
    for (int i = 0; i < n; ++i) {
      CHECK_CONDITION(batch[i] != nullptr);
    }
  }
};
```

[fa9db8b](https://github.com/google/tcmalloc/blob/fa9db8bb2f564d6ad667fabea793fb336135c442/tcmalloc/mock_central_freelist.cc#L21-L27) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- I said it was minimal didn't I?  The real `CentralFreelist` is a very large
  heavy weight object.

-----

<!-- .slide: data-background="./treachery-magritte.png" -->

```json [6-7,12-13]
name                                        cpu/op
BM_Draining<TransferCacheEnv>/threads:2     292ns ± 5%
BM_Draining<TransferCacheEnv>/threads:4     888ns ± 8%
BM_Draining<TransferCacheEnv>/threads:8    2.25µs ± 7%
BM_Draining<TransferCacheEnv>/threads:16   4.66µs ± 5%
BM_Draining<TransferCacheEnv>/threads:32   9.34µs ± 6%
BM_Draining<TransferCacheEnv>/threads:64   29.5µs ± 6%
BM_Draining<LockFreeEnv>/threads:2          286ns ±24%
BM_Draining<LockFreeEnv>/threads:4          793ns ±11%
BM_Draining<LockFreeEnv>/threads:8         1.79µs ± 4%
BM_Draining<LockFreeEnv>/threads:16        3.37µs ±21%
BM_Draining<LockFreeEnv>/threads:32        5.94µs ±32%
BM_Draining<LockFreeEnv>/threads:64        11.6µs ± 7%
```

[9587e53](https://github.com/google/tcmalloc/commit/9587e53228f6a578745fd424bafd4d90267e3060) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Let's think about what is actually going on when we are highly contended.
- The old system will hold a mutex and force people to go one at a time.

---

<!-- .slide: data-background="./treachery-magritte.png" -->

```cc [3]
void InsertRange(absl::Span<void*> batch, int n) {
  ASSERT(0 < n && n <= batch_size_);
  absl::MutexLock l(&mu_);
  if (IsFull()) {
    freelist_.InsertRange(batch.data(), n);
    return;
  }

  CopyIntoSlots(batch.data(), head_, n);
  head_ += n;
}
```

[9587e53](https://github.com/google/tcmalloc/commit/9587e53228f6a578745fd424bafd4d90267e3060) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- The old system will hold a mutex and force people to go one at a time.
  quickly shunt the remainder directly to the central free list

---

<!-- .slide: data-background="./treachery-magritte.png" -->

```cc [3-7]
void InsertRange(absl::Span<void*> batch, int n) {
  ASSERT(0 < n && n <= batch_size_);
  absl::optional<Range> r = ClaimInsert(n);
  if (!r.has_value()) {
    freelist_.InsertRange(batch.data(), n);
    return;
  }

  CopyIntoSlots(batch.data(), *r);
  AdvanceCommitLine(&head_committed_, *r);
}
```

[9587e53](https://github.com/google/tcmalloc/commit/9587e53228f6a578745fd424bafd4d90267e3060) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- The new system will allow a bunch of threads to start operating and then will
  quickly shunt the remainder directly to the central free list

-----

<!-- .slide: data-background="./race-drag.png" -->

NOTES:

- SLOW DOWN
- Ok, we now have a theory.  In our micro benchmark we are incredibly fast at
  moving something to a light weight operation, so it is a big win.

---

<!-- .slide: data-background="./race-autocross.png" -->

NOTES:

- SLOW DOWN
- And in our system tests we are incredibly fast at moving something to a
  very expensive operation, so it is a big loss.
- We have a theory and it fits the data.  The question is how do we evaluate
  this theory?
- One option is to try and make our micro benchmark resemble the full system
  more accurately.  Of course, we didn't do that in the first place because it
  is hard.
- Another option is to look at different or more specific stats for our micro
  benchmark.  That seems like it will be a bit easier, so let's start there.

---

<!-- .slide: data-background="./race-drag.png" -->

```cc []
template <typename Env>
void BM_Draining(benchmark::State& state) {
  // ...
  auto stats = env.GetHitRateStats();
  state.counters["insert_hit_ratio"] =
    static_cast<double>(stats.insert_hits) /
    (stats.insert_hits + stats.insert_misses);
  state.counters["remove_hit_ratio"] =
    static_cast<double>(stats.remove_hits) /
    (stats.remove_hits + stats.remove_misses);
}
```

[fa9db8b](https://github.com/google/tcmalloc/blob/fa9db8bb2f564d6ad667fabea793fb336135c442/tcmalloc/transfer_cache_benchmark.cc#L75-L91) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Now we can look at these stats and see how our theory holds up

---

<!-- .slide: data-background="./race-drag.png" -->

```json
BM_Draining<TransferCacheEnv>
  threads:2   insert_hit_ratio=0.944 remove_hit_ratio=0.943
  threads:4   insert_hit_ratio=0.813 remove_hit_ratio=0.813
  threads:8   insert_hit_ratio=0.923 remove_hit_ratio=0.923
  threads:16  insert_hit_ratio=0.918 remove_hit_ratio=0.918
  threads:32  insert_hit_ratio=0.925 remove_hit_ratio=0.924
  threads:64  insert_hit_ratio=0.891 remove_hit_ratio=0.890
```
```json
BM_Draining<LockFreeEnv>
  threads:2   insert_hit_ratio=0.808 remove_hit_ratio=0.808
  threads:4   insert_hit_ratio=0.833 remove_hit_ratio=0.833
  threads:8   insert_hit_ratio=0.803 remove_hit_ratio=0.803
  threads:16  insert_hit_ratio=0.617 remove_hit_ratio=0.617
  threads:32  insert_hit_ratio=0.713 remove_hit_ratio=0.712
  threads:64  insert_hit_ratio=0.542 remove_hit_ratio=0.541
```

[fa9db8b](https://github.com/google/tcmalloc/blob/fa9db8bb2f564d6ad667fabea793fb336135c442/tcmalloc/transfer_cache_benchmark.cc#L75-L91) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Seems plausible.  As we see more action on the cache it become ever more
  efficient and tell people it is busy and go talk to the `CentralFreeList`
- There may even be systems for which this behavior is desirable.  Just not
  ours.
  
-----

<!-- .slide: data-background="./dog-sniffing-tail.png" -->

NOTES:

- SLOW DOWN
- I guess the easy answer is to try sniffing at the other end of the queue to
  see if there is activety.

-----

<!-- .slide: data-background="./dog-sniffing-tail.png" -->

```cc [|4-6]
absl::optional<Range> ClaimRemove(int n) {
  uint32_t new_t, old_t = tail_.load(order_relaxed);
  do {
    uint32_t h = head_committed_.load(order_acquire);
    uint32_t s = size_from_pos(h, old_t);
    if (s < n) return absl::nullopt;
    new_t = old_t + n;
  } while (!tail_.compare_exchange_weak(
      old_t, new_t, order_relaxed, order_relaxed));
  return Range{old_t, new_t};
}

```

NOTES:

- SLOW DOWN
- Here is the spot we sniff the other side to see if we have space.  Now we can
  just adjust how we handle it on error.

---

<!-- .slide: data-background="./dog-sniffing-tail.png" -->

```cc [|5|6]
absl::optional<Range> ClaimRemove(int n) {
  // ...
    uint32_t h = head_committed_.load(order_acquire);
    if (s < n) {
      if (head != head_.load(std::memory_order_relaxed)) {
        AwaitChange(head_committed_, head);
        return ClaimRemove(n);
      }
      return absl::nullopt;
    }
  // ...
}
```

[f97cacc](https://github.com/google/tcmalloc/blob/f97cacc6fc09876e12b55f7987d444820047f083/tcmalloc/transfer_cache_internals.h#L816-L825) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Now we look to see if our pending line has gotten ahead of our commit line.
  If it has, someone else is working on it, so we simply need to wait for them
  to finish!

---

<!-- .slide: data-background="./dog-sniffing-tail.png" -->

```cc
void AwaitChange(std::atomic<uint32_t> &v, uint32_t actual) {
  while (v.load(std::memory_order_relaxed) != actual) {
    _mm_pause();
  }
}
```

[f97cacc](https://github.com/google/tcmalloc/blob/f97cacc6fc09876e12b55f7987d444820047f083/tcmalloc/transfer_cache_internals.h#L861-L875) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Now we look to see if our pending line has gotten ahead of our commit line.
  If it has, someone else is working on it, so we simply need to wait for them
  to finish!

