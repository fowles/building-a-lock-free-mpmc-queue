<!-- .slide: data-background="./treasure.png" -->

NOTES:

- SLOW DOWN
- Thus far, this talk has been a bit like a treasure map in a video game.  When
  you find yourself in just the right place at the right time.  Look here for
  treasure.  But it doesn't really tell you how to get here or even where you
  are.

-----

##### Before

```language-plantuml
digraph g {
  bgcolor = "transparent";
  rankdir=LR;
  node [
    fontname = "courier";
    shape = box;
  ];
  subgraph cluster_0 {
    label="Per Size Class";
    subgraph cluster_1 {
      label="Per CPU";
      "CPU Cache";
    }
    "Transfer Cache";
    "Central Free List";
  }
  "malloc/free" -> "CPU Cache" [dir="both"];
  "CPU Cache" -> "Transfer Cache" [dir="both"];
  "Transfer Cache" -> "Central Free List" [dir="both"];
  "Central Free List" -> "Operating System" [dir="both"];
}
```

##### After

```language-plantuml
digraph g {
  bgcolor = "transparent";
  rankdir=LR;
  node [
    fontname = "courier";
    shape = box;
  ];
  subgraph cluster_0 {
    label="Per Size Class";
    subgraph cluster_00 {
      label="Per CPU";
      "CPU Cache";
    }
  }

  subgraph cluster_1 {
    label="Transfer Cache Manager";
    subgraph cluster_10 {
      label="Per Size Class";
      "Transfer Cache";
      "Central Free List";
    }
  }
  "malloc/free" -> "CPU Cache" [dir="both"];
  "CPU Cache" -> "Transfer Cache" [dir="both"];
  "Transfer Cache" -> "Central Free List" [dir="both"];
  "Central Free List" -> "Operating System" [dir="both"];
}
```


[76aefd7](https://github.com/google/tcmalloc/commit/76aefd7ea46feff1a086bf7294645d9abb01863e#diff-52870df7d7556e2041487d72448260c02e2de55aa1212ad8c0fc783304f83957) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Our first step was to encapsulate these things a bit better so that fewer
  people accessed globals.
- This may seem like a silly step, but now very few users spell the exact type
  of `TransferCache`.  Intead they spell `TransferCacheManager` which contains
  all the `TransferCache` objects.  Now I can change the type in one place when
  experimenting.

---

##### Before

```cc []
class TransferCacheManager {
  TransferCache cache_[kNumClasses];
};
```

##### After

```cc []
class TransferCacheManager {
  using TransferCache =
      internal::TransferCache<CentralFreeList,
                              TransferCacheManager>;

  TransferCache cache_[kNumClasses];
};
```


[73697c7](https://github.com/google/tcmalloc/commit/73697c73cfa445300e8447c3de84f4a4211e37cf#diff-52870df7d7556e2041487d72448260c02e2de55aa1212ad8c0fc783304f83957) <!-- .element: class="github" -->


NOTES:

- SLOW DOWN
- Next step is to statically inject the dependencies of the type we want.
- In a less performance sensitive context, we could probably use a virtual
  dispatch here to decoupl things.  Sadly, tcmalloc does not want to pay the
  cost of an indirect function call here, so we do this entirely with templates.

---

```cc []
using TransferCache = internal::TransferCache<
    MockCentralFreeList, MockTransferCacheManager>;

TEST(TransferCache, IsolatedSmoke) {
  const int b = 32;
  MockTransferCacheManager manager;
  TransferCache cache(&manager);
  cache.Init(1);
  Batch in, out;
  cache.InsertRange(absl::MakeSpan(in.objs, b), b);
  cache.InsertRange(absl::MakeSpan(in.objs + b, b), b);
  ASSERT_EQ(cache.RemoveRange(out.objs, b), b);
  ASSERT_EQ(cache.RemoveRange(out.objs + b, b), b);
}
```

[fa3b5ab](https://github.com/google/tcmalloc/blob/fa3b5ab3e914483757fadd393a8db9263a3e926a/tcmalloc/transfer_cache_test.cc#L45-L74) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Suddenly we can write unit tests for all of out things!
- This may not seem ground breaking, but architecting a low-level component like
  tcmalloc so its internals can be tested outside the remainder of the system
  with no overhead can be rough.  Especially if the system already exists.  That
  said, the time spent making these refactors pays for itself easily when you
  then try to change the implementation.

---

```cc [|9]
template <typename TransferCache>
class FakeTransferCacheEnvironment {
 public:
  void Shrink();
  void Grow();
  void Insert(int n);
  void Remove(int n);
  void Drain();
  void RandomlyPoke();
};
```

[5aba75b](https://github.com/google/tcmalloc/blob/5aba75bf076d85c0e3c01128f88d6b15a96bb643/tcmalloc/mock_transfer_cache.h#L66) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Now that we have a functional thing, we exctract the guts of that into a small
  library with a simplified API, so we can write a ton of tests with much less
  bolierplate.
- ADVANCE: What is that?  Foreshadow.  I promise it becomes interesting later.

---

```cc []
TEST(TransferCache, IsolatedSmoke) {
  Env e;
  EXPECT_CALL(e.central_freelist(), InsertRange).Times(0);
  EXPECT_CALL(e.central_freelist(), RemoveRange).Times(0);
  e.Insert(kBatchSize);
  e.Remove(kBatchSize);
}

TEST(TransferCache, FetchesFromFreelist) {
  Env e;
  EXPECT_CALL(e.central_freelist(), InsertRange).Times(0);
  EXPECT_CALL(e.central_freelist(), RemoveRange).Times(1);
  e.Remove(kBatchSize);
}
```

[5aba75b](https://github.com/google/tcmalloc/blob/5aba75bf076d85c0e3c01128f88d6b15a96bb643/tcmalloc/transfer_cache_test.cc#L44-L61) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Now that we have a functional thing, we exctract the guts of that into a small
  library with a simplified API, so we can write a ton of tests with much less
  bolierplate.

-----

<!-- .slide: data-background="./miho-nonaka.png" -->
<!-- .slide: data-background-size="contain" -->


NOTES:

- SLOW DOWN
- Now I have simple and easy unit tests for both the old and new versions of the
  `TransferCache`.  That is nice, but how do I test this.
- Aside: this is Miho Nonaka who won silver in the olympic
  combined climbing event this year.  But really, I just think her facial
  expression captures my feeling when I hit this point in a problem.  I am in a
  kinda stable place, and I need to move somewhere else, but how do I get there.
- Fortunately, I learned a trick for this.

---

<!-- .slide: data-background="./tribbles.png" -->
<!-- .slide: data-background-size="contain" -->

```cc [9]
template <typename TransferCache>
class FakeTransferCacheEnvironment {
 public:
  void Shrink();
  void Grow();
  void Insert(int n);
  void Remove(int n);
  void Drain();
  void RandomlyPoke();
};
```
<!-- .element: class="fragment" -->


NOTES:

- SLOW DOWN
- Here is a small hint.  Also, DS9 is the best StarTrek and no one will ever
  convince me otherwise.
- ADVANCE: here is a slightly larger hint and a callback to our earlier
  foreshadow.

---

```cc []
void RandomlyPoke() {
  absl::BitGen gen;
  double choice = absl::Uniform(gen, 0.0, 1.0);
  if (choice < 0.1) {
    Shrink();
  } else if (choice < 0.2) {
    Grow();
  } else if (choice < 0.6) {
    Insert(absl::Uniform(gen, 1, kBatchSize));
  } else {
    Remove(absl::Uniform(gen, 1, kBatchSize));
  }
}
```

[e4834bd](https://github.com/google/tcmalloc/blob/e4834bdb1a026994cfebbe6fad2191dea42566fb/tcmalloc/mock_transfer_cache.h#L128-L145) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Fuzz testing to the answer.
- RandomlyPoke allows us to just interact with the thing.  Existing assertions
  catch many of our issues.

---

```cc [|8]
TEST(LockFreeTransferCache, MultiThreadedUnbiased) {
  LockFreeEnv env;
  ThreadManager threads;
  threads.Start(10, [&]() { env.RandomlyPoke(); });

  auto start = absl::Now();
  while (start + absl::Seconds(0.3) > absl::Now()) {
    env.RandomlyPoke();
  }
  threads.Stop();
}
```

[e4834bd](https://github.com/google/tcmalloc/blob/e4834bdb1a026994cfebbe6fad2191dea42566fb/tcmalloc/transfer_cache_test.cc#L190-L198) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Here is a simple test that should catch things, eventually.  But we know that
  there are corner cases.  Can we bias this towards some of our corners?
- ADVANCE: actually it is pretty easy

---

```cc [8]
TEST(LockFreeTransferCache, MultiThreadedBiasedInsert) {
  LockFreeEnv env;
  ThreadManager threads;
  threads.Start(10, [&]() { env.RandomlyPoke(); });

  auto start = absl::Now();
  while (start + absl::Seconds(0.3) > absl::Now()) {
    env.Insert(kBatchSize);
  }
  threads.Stop();
}
```

[e4834bd](https://github.com/google/tcmalloc/blob/e4834bdb1a026994cfebbe6fad2191dea42566fb/tcmalloc/transfer_cache_test.cc#L190-L198) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Here we bias towards a full cache by leaving one thread spinning on insert.

---

```cc [8]
TEST(LockFreeTransferCache, MultiThreadedBiasedRemove) {
  LockFreeEnv env;
  ThreadManager threads;
  threads.Start(10, [&]() { env.RandomlyPoke(); });

  auto start = absl::Now();
  while (start + absl::Seconds(0.3) > absl::Now()) {
    env.Remove(kBatchSize);
  }
  threads.Stop();
}
```

[e4834bd](https://github.com/google/tcmalloc/blob/e4834bdb1a026994cfebbe6fad2191dea42566fb/tcmalloc/transfer_cache_test.cc#L190-L198) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- or towards an empty cache

---

```cc [8]
TEST(LockFreeTransferCache, MultiThreadedBiasedShrink) {
  LockFreeEnv env;
  ThreadManager threads;
  threads.Start(10, [&]() { env.RandomlyPoke(); });

  auto start = absl::Now();
  while (start + absl::Seconds(0.3) > absl::Now()) {
    env.Shrink();
  }
  threads.Stop();
}
```

[e4834bd](https://github.com/google/tcmalloc/blob/e4834bdb1a026994cfebbe6fad2191dea42566fb/tcmalloc/transfer_cache_test.cc#L190-L198) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- or towards a small cache

---

```cc [8]
TEST(LockFreeTransferCache, MultiThreadedBiasedGrow) {
  LockFreeEnv env;
  ThreadManager threads;
  threads.Start(10, [&]() { env.RandomlyPoke(); });

  auto start = absl::Now();
  while (start + absl::Seconds(0.3) > absl::Now()) {
    env.Grow();
  }
  threads.Stop();
}
```

[e4834bd](https://github.com/google/tcmalloc/blob/e4834bdb1a026994cfebbe6fad2191dea42566fb/tcmalloc/transfer_cache_test.cc#L190-L198) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- or a large one

-----

<!-- .slide: data-background="./dragon-pony.png" -->
<!-- .slide: data-background-size="contain" -->

[llvm sanitizers](https://github.com/google/sanitizers) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- remember the great care we took to isolate the components so they could run in
  a fully controlled environment?
- now we get to really reap the rewards of this.  Now we can use debug
  allocators and specialized system libraries like asan/msan/tsan and run our
  tests under those configurations.

-----

<!-- .slide: data-background="./deepwater-horizon.png" -->

NOTES:

- SLOW DOWN
- I don't really know what I expected.  Actually I do and it was basically this.
- I spent a lot of time trying to figure out this bug.  Staring at my atomics,
  reading and re-reading the code.  Trying to produce smaller repros.  Until one
  of my coworkers Andy Soffer had a suggestion.

---

<!-- .slide: data-background="./rusty-lock.jpg" -->

<img class="fragment transform rotate-12 -translate-y-10 -translate-x-10" src="./deepwater-horizon.png" style="width: 60%;" />


[ce9370a](https://github.com/google/tcmalloc/commit/ce9370ad2d603801d82cf28935ea29ad28b5e91c) <!-- .element: class="github fragment" style="background-color: rgb(229 231 225)" -->


NOTES:

- SLOW DOWN
- just put a giant lock on it.  Does it still happen?
- ADVANCE: yes.  But now I can stop looking at the atomics and start looking at
  the main logic.
- ADVANCE: the fix is a little hard to fit on a slide, but essentially I needed
  to handle cache growth more correctly.

-----

<!-- .slide: data-background="./clouds.png" -->

NOTES:

- SLOW DOWN
- Now that we have handled that bug and the test passes we are good right?
- Narrator: they weren't

---

```cc [|8]
absl::optional<Range> ClaimInsert(int n) {
  int32_t new_h, old_h = head_.load(order_relaxed);
  do {
    int32_t t = tail_committed_.load(order_acquire);
    size_t size = size_from_pos(old_h, t);
    if (!EnsureCacheSpace(size + n)) return absl::nullopt;

    new_h = (old_h + n) % slots_size();
  } while (!head_.compare_exchange_weak(
        old_h, new_h, order_relaxed, order_relaxed));
  return Range{old_h, new_h};
}
```

Note:

- SLOW DOWN
- Anyone remember this code?  I warned you that there was a bug.
- ADVANCE: here's a hint

---

<!-- .slide: data-background="./letter-a.png" -->

```cc [8]
absl::optional<Range> ClaimInsert(int n) {
  int32_t new_h, old_h = head_.load(order_relaxed);
  do {
    int32_t t = tail_committed_.load(order_acquire);
    size_t size = size_from_pos(old_h, t);
    if (!EnsureCacheSpace(size + n)) return absl::nullopt;

    new_h = (old_h + n) % slots_size();
  } while (!head_.compare_exchange_weak(
        old_h, new_h, order_relaxed, order_relaxed));
  return Range{old_h, new_h};
}
```
<!-- .element: class="fragment" style="opacity: 0.8;" -->

NOTES:

- SLOW DOWN
- here's another hint
- ADVANCE: here they are together in case that helps.

---

<!-- .slide: data-background="./letter-a.png" -->

```shell [|3|2]
$ bazel test \
    --config=tsan \
    --runs_per_test=5000 --jobs=5000 \
    tcmalloc:transfer_cache_test
```

NOTES:

- SLOW DOWN
- let's start with how do we even begin to track this down.
- step one is to run our fuzz tests many, many times.
- when I worked at startups I would create tests that ran in a loop for hours to
  days.
- ADVANCE: at google I just run them on 5000 machines at the same time
- ADVANCE: don't forget to use tsan to give you all the friendly warnings

---

<!-- .slide: data-background="./letter-a.png" -->

```shell [6-7]
$ bazel test \
    --config=tsan \
    --runs_per_test=5000 --jobs=5000 \
    tcmalloc:transfer_cache_test

FAILED in 5 out of 5000 in 39.8s
  Stats over 5000 runs: max = 39.8s, min = 1.2s, avg = 2.3s
```

NOTES:

- SLOW DOWN
- let's start with how do we even begin to track this down.
- step one is to run our fuzz tests many, many times.
- when I worked at startups I would create tests that ran in a loop for hours to
  days.
- ADVANCE: at google I just run them on 5000 machines at the same time
- ADVANCE: don't forget to use tsan to give you all the friendly warnings


---

<!-- .slide: data-background="./letter-a.png" -->

```shell [5]
$ bazel test \
    --config=tsan \
    --runs_per_test=5000 --jobs=5000 \
    tcmalloc:transfer_cache_test \
    --test_env TSAN_OPTIONS="force_seq_cst_atomics=1"
```

NOTES:

- SLOW DOWN
- we have a quick test to tell us if our problem is associated with not having a
  strong enough memory order on our existing atomic ops.

---

<!-- .slide: data-background="./letter-a.png" -->

```shell [7-8]
$ bazel test \
    --config=tsan \
    --runs_per_test=5000 --jobs=5000 \
    tcmalloc:transfer_cache_test \
    --test_env TSAN_OPTIONS="force_seq_cst_atomics=1"

FAILED in 5 out of 5000 in 39.8s
  Stats over 5000 runs: max = 39.8s, min = 1.2s, avg = 2.3s
```

NOTES:

- SLOW DOWN
- Nope, that wasn't it.  Guess we have to look at the actual error message.

---

<!-- .slide: data-background="./letter-a.png" -->

```json []
WARNING: ThreadSanitizer: data race (pid=6510)
...
Write of size 8 at 0x7ba4000029b8 by thread T7:
  #2 LockFreeTransferCache::InsertRange
     third_party/tcmalloc/transfer_cache_internals.h:585
...
Previous read of size 8 at 0x7ba4000029b8 by thread T8:
    #2 LockFreeTransferCache::RemoveRange
       third_party/tcmalloc/transfer_cache_internals.h:602
...
```

NOTES:

- SLOW DOWN
- a data race.  Can't say I am entirely surprised, but I really thought I did a
  good job avoiding those.


---

<!-- .slide: data-background="./letter-a.png" -->

```cc [9|10]
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

```cc [8|3]
int RemoveRange(void** batch, int n) {
  ASSERT(n > 0);
  absl::optional<Range> r = ClaimRemove(n);
  if (!r.has_value()) {
    return freelist_.RemoveRange(batch, n);
  }

  CopyFromSlots(batch, *r);
  AdvanceCommitLine(&tail_committed_, *r);
  return n;
}
```

NOTES:

- SLOW DOWN
- this is essentially the pair of lines I am staring at.
- but I took so much care!  I used the right words and everything!
- ADVANCE: see `AdvanceCommitLine` is supposed to release the memory
- ADVANCE: that is aquired by `ClaimRemove`

---
<!-- .slide: data-background="./letter-a.png" -->

```cc []
class TransferCache {
  // *Acquires* tail and claims space for insert.
  absl::optional<Range> ClaimInsert(int n);

  // *Acquires* head and claims space for remove.
  absl::optional<Range> ClaimRemove(int n);

  // *Releases* `c` and advances its position.
  void AdvanceCommitLine(std::atomic<int32_t>* c, Range r);

 public:
  void InsertRange(absl::Span<void*> batch, int n);
  int RemoveRange(void** batch, int n);
};
```

NOTES:

- SLOW DOWN
- It even says so in the docs!
- I guess we have to go into the code a stare more...

---
<!-- .slide: data-background="./letter-a.png" -->

```cc [|4-6]
ABSL_ATTRIBUTE_ALWAYS_INLINE void AdvanceCommitLine(
    std::atomic<int32_t> *commit, Range r) {
  int32_t temp_pos;
  while (!commit->compare_exchange_weak(
            temp_pos = r.from, r.to,
            order_release, order_relaxed)) {
#ifdef __x86_64__
    _mm_pause();
#endif
  }
}
```

```cc [|4]
absl::optional<Range> ClaimRemove(int n) {
  int32_t new_t, old_t = tail_.load(order_relaxed);
  do {
    int32_t h = head_committed_.load(order_acquire);
    int32_t s = size_from_pos(h, old_t);
    if (s < n) return absl::nullopt;
    new_t = (old_t + n) % slots_size();
  } while (!tail_.compare_exchange_weak(
      old_t, new_t, order_relaxed, order_relaxed));
  return Range{old_t, new_t};
}

```

NOTES:

- SLOW DOWN
- zooming in on that code
- ADVANCE: you can even see the release here
- ADVANCE: pairing with the acquire here
- This only fails about one a thousand times too... If I got it really wrong, it
  would be much worse.

-----

<!-- .slide: data-background="./thinker.png" -->
<!-- .slide: data-background-size="contain" -->
<!-- .slide: data-background-color="black" -->

NOTES:

- SLOW DOWN
- now comes the hardest part of debugging.  I have exausted all of the tricks
  except just thinking more.
- let's go back to considering our queue.

---

```language-plantuml
digraph g {
  bgcolor = "transparent";
  rankdir = BT;
  node [
    fontname = "courier";
    shape = none;
  ];
  q [
    fontsize=30;
    label=<
      <table border="0" cellborder="1" cellspacing="0" cellpadding="4">
        <tr>
          <td port="r0" style="dotted" sides="TBR">...</td>
          <td port="r1" style="dotted" sides="TBR"> </td>
          <td port="r2" style="dotted" sides="TBR"> </td>
          <td port="r3" style="dotted" sides="TBR"> </td>
          <td port="r4" style="dotted" sides="TBR"> </td>
          <td port="r5"> </td>
          <td port="r6"> </td>
          <td port="r7"> </td>
          <td port="r8"> </td>
          <td port="r9"> </td>
          <td port="r10" style="dotted" sides="TBR"> </td>
          <td port="r11" style="dotted" sides="TBR"> </td>
          <td port="r12" style="dotted" sides="TBR"> </td>
          <td port="r13" style="dotted" sides="TBR"> </td>
          <td port="r14" style="dotted" sides="TBR"> </td>
          <td port="r15" style="dotted" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  "tail\ncommitted" -> q:r3;
  "tail\npending" -> q:r5;
  "head\ncommitted" -> q:r9;
  "head\npending" -> q:r11;
}
```

Note:

- SLOW DOWN
- What happens if I acquire head committed and then go to sleep for a while...

---

```language-plantuml
digraph g {
  bgcolor = "transparent";
  rankdir = BT;
  node [
    fontname = "courier";
    shape = none;
  ];
  q [
    fontsize=30;
    label=<
      <table border="0" cellborder="1" cellspacing="0" cellpadding="4">
        <tr>
          <td port="r0" style="dotted" sides="TBR">...</td>
          <td port="r1" style="dotted" sides="TBR"> </td>
          <td port="r2" style="dotted" sides="TBR"> </td>
          <td port="r3" style="dotted" sides="TBR"> </td>
          <td port="r4" style="dotted" sides="TBR"> </td>
          <td port="r5"> </td>
          <td port="r6"> </td>
          <td port="r7"> </td>
          <td port="r8"> </td>
          <td port="r9"> </td>
          <td port="r10" style="dotted" sides="TBR"> </td>
          <td port="r11" style="dotted" sides="TBR"> </td>
          <td port="r12" style="dotted" sides="TBR"> </td>
          <td port="r13" style="dotted" sides="TBR"> </td>
          <td port="r14" style="dotted" sides="TBR"> </td>
          <td port="r15" style="dotted" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r3;
  "tail\npending" -> q:r5;
  "head\ncommitted" -> q:r9;
  "head\npending" -> q:r11;
}
```

Note:

- SLOW DOWN
- What happens if I acquire head committed and then go to sleep for a while...

---

```language-plantuml
digraph g {
  bgcolor = "transparent";
  rankdir = BT;
  node [
    fontname = "courier";
    shape = none;
  ];
  q [
    fontsize=30;
    label=<
      <table border="0" cellborder="1" cellspacing="0" cellpadding="4">
        <tr>
          <td port="r0" style="dotted" sides="TBR">...</td>
          <td port="r1" style="dotted" sides="TBR"> </td>
          <td port="r2" style="dotted" sides="TBR"> </td>
          <td port="r3" style="dotted" sides="TBR"> </td>
          <td port="r4" style="dotted" sides="TBR"> </td>
          <td port="r5"> </td>
          <td port="r6"> </td>
          <td port="r7"> </td>
          <td port="r8"> </td>
          <td port="r9"> </td>
          <td port="r10"> </td>
          <td port="r11"> </td>
          <td port="r12" style="dotted" sides="TBR"> </td>
          <td port="r13" style="dotted" sides="TBR"> </td>
          <td port="r14" style="dotted" sides="TBR"> </td>
          <td port="r15" style="dotted" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r3;
  "tail\npending" -> q:r5;
  "head\ncommitted" -> q:r11;
  "head\npending" -> q:r14;
}
```

Note:

- SLOW DOWN
- Ages come and pass

---

```language-plantuml
digraph g {
  bgcolor = "transparent";
  rankdir = BT;
  node [
    fontname = "courier";
    shape = none;
  ];
  q [
    fontsize=30;
    label=<
      <table border="0" cellborder="1" cellspacing="0" cellpadding="4">
        <tr>
          <td port="r0" style="dotted" sides="TBR">...</td>
          <td port="r1" style="dotted" sides="TBR"> </td>
          <td port="r2" style="dotted" sides="TBR"> </td>
          <td port="r3" style="dotted" sides="TBR"> </td>
          <td port="r4" style="dotted" sides="TBR"> </td>
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
          <td port="r9" style="dotted" sides="TBR"> </td>
          <td port="r10"> </td>
          <td port="r11"> </td>
          <td port="r12" style="dotted" sides="TBR"> </td>
          <td port="r13" style="dotted" sides="TBR"> </td>
          <td port="r14" style="dotted" sides="TBR"> </td>
          <td port="r15" style="dotted" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r10;
  "tail\npending" -> q:r10;
  "head\ncommitted" -> q:r11;
  "head\npending" -> q:r14;
}
```

Note:

- SLOW DOWN
- leaving memories that become legend

---

```language-plantuml
digraph g {
  bgcolor = "transparent";
  rankdir = BT;
  node [
    fontname = "courier";
    shape = none;
  ];
  q [
    fontsize=30;
    label=<
      <table border="0" cellborder="1" cellspacing="0" cellpadding="4">
        <tr>
          <td port="r0" sides="TBR">...</td>
          <td port="r1" sides="TBR"> </td>
          <td port="r2" sides="TBR"> </td>
          <td port="r3" sides="TBR"> </td>
          <td port="r4" sides="TBR"> </td>
          <td port="r5" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
          <td port="r9" style="dotted" sides="TBR"> </td>
          <td port="r10" style="dotted" sides="TBR"> </td>
          <td port="r11" style="dotted" sides="TBR"> </td>
          <td port="r12" style="dotted" sides="TBR"> </td>
          <td port="r13" style="dotted" sides="TBR"> </td>
          <td port="r14"> </td>
          <td port="r15" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r10;
  "tail\npending" -> q:r14;
  "head\ncommitted" -> q:r5;
  "head\npending" -> q:r6;
}
```

Note:

- SLOW DOWN
- Legend fades to myth

---

```language-plantuml
digraph g {
  bgcolor = "transparent";
  rankdir = BT;
  node [
    fontname = "courier";
    shape = none;
  ];
  q [
    fontsize=30;
    label=<
      <table border="0" cellborder="1" cellspacing="0" cellpadding="4">
        <tr>
          <td port="r0" style="dotted" sides="TBR">...</td>
          <td port="r1" style="dotted" sides="TBR"> </td>
          <td port="r2" style="dotted" sides="TBR"> </td>
          <td port="r3"> </td>
          <td port="r4"> </td>
          <td port="r5"> </td>
          <td port="r6"> </td>
          <td port="r7"> </td>
          <td port="r8"> </td>
          <td port="r9" style="dotted" sides="TBR"> </td>
          <td port="r10" style="dotted" sides="TBR"> </td>
          <td port="r11" style="dotted" sides="TBR"> </td>
          <td port="r12" style="dotted" sides="TBR"> </td>
          <td port="r13" style="dotted" sides="TBR"> </td>
          <td port="r14" style="dotted" sides="TBR"> </td>
          <td port="r15" style="dotted" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r14;
  "tail\npending" -> q:r3;
  "head\ncommitted" -> q:r8;
  "head\npending" -> q:r11;
}
```

Note:

- SLOW DOWN
- and even myth is long forgotten

---

```language-plantuml
digraph g {
  bgcolor = "transparent";
  rankdir = BT;
  node [
    fontname = "courier";
    shape = none;
  ];
  q [
    fontsize=30;
    label=<
      <table border="0" cellborder="1" cellspacing="0" cellpadding="4">
        <tr>
          <td port="r0" style="dotted" sides="TBR">...</td>
          <td port="r1" style="dotted" sides="TBR"> </td>
          <td port="r2" style="dotted" sides="TBR"> </td>
          <td port="r3" style="dotted" sides="TBR"> </td>
          <td port="r4" style="dotted" sides="TBR"> </td>
          <td port="r5"> </td>
          <td port="r6"> </td>
          <td port="r7"> </td>
          <td port="r8"> </td>
          <td port="r9"> </td>
          <td port="r10" style="dotted" sides="TBR"> </td>
          <td port="r11" style="dotted" sides="TBR"> </td>
          <td port="r12" style="dotted" sides="TBR"> </td>
          <td port="r13" style="dotted" sides="TBR"> </td>
          <td port="r14" style="dotted" sides="TBR"> </td>
          <td port="r15" style="dotted" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r3;
  "tail\npending" -> q:r5;
  "head\ncommitted" -> q:r9;
  "head\npending" -> q:r11;
}
```

Note:

- SLOW DOWN
- when the Age that gave it birth comes again.

---

<!-- .slide: data-background="./thinker.png" -->
<!-- .slide: data-background-size="contain" -->
<!-- .slide: data-background-color="black" -->

---

<!-- .slide: data-background="./thinker.png" -->
<!-- .slide: data-background-size="contain" -->
<!-- .slide: data-background-color="black" -->

```cc [4|8-9]
absl::optional<Range> ClaimRemove(int n) {
  int32_t new_t, old_t = tail_.load(order_relaxed);
  do {
    int32_t h = head_committed_.load(order_acquire);
    int32_t s = size_from_pos(h, old_t);
    if (s < n) return absl::nullopt;
    new_t = (old_t + n) % slots_size();
  } while (!tail_.compare_exchange_weak(
      old_t, new_t, order_relaxed, order_relaxed));
  return Range{old_t, new_t};
}
```

NOTES:

- SLOW DOWN
- empires can rise fand all around me while I wait here.
- and as long as this contains the value it contained before I went to sleep
- I can be none the wiser
- welcome to the canonical ABA bug.

---

<!-- .slide: data-background="./letter-a.png" -->

NOTES:

- SLOW DOWN
- I read A

---

<!-- .slide: data-background="./thinker.png" -->
<!-- .slide: data-background-size="contain" -->
<!-- .slide: data-background-color="black" -->

NOTES:

- SLOW DOWN
- went to sleep for an era when B occurred

---

<!-- .slide: data-background="./letter-a.png" -->

NOTES:

- SLOW DOWN
- And woke up to see A again and assumed nothing had changed.  It is an illusion
  of object permanence
- the usual fix to this is to keep an epoch counter, so you know when ages come
  and go.  I however do not wish to waste the extra 4 bytes and associated
  atomic operations.  Fortunately, there is a cheat I can use.

---

<!-- .slide: data-background="./letter-a.png" -->

```cc [7]
absl::optional<Range> ClaimRemove(int n) {
  int32_t new_t, old_t = tail_.load(order_relaxed);
  do {
    int32_t h = head_committed_.load(order_acquire);
    int32_t s = size_from_pos(h, old_t);
    if (s < n) return absl::nullopt;
    new_t = (old_t + n) % slots_size();
  } while (!tail_.compare_exchange_weak(
      old_t, new_t, order_relaxed, order_relaxed));
  return Range{old_t, new_t};
}
```

NOTES:

- SLOW DOWN
- by taking the modulus here, I am discarding a whole bunch of high bits.  What
  if instead, I just leave them unharmed.

---

<!-- .slide: data-background="./letter-a.png" -->

```cc [7]
absl::optional<Range> ClaimRemove(int n) {
  int32_t new_t, old_t = tail_.load(order_relaxed);
  do {
    int32_t h = head_committed_.load(order_acquire);
    int32_t s = size_from_pos(h, old_t);
    if (s < n) return absl::nullopt;
    new_t = old_t + n;
  } while (!tail_.compare_exchange_weak(
      old_t, new_t, order_relaxed, order_relaxed));
  return Range{old_t, new_t};
}
```

[398b03c](https://github.com/google/tcmalloc/commit/398b03cf62804b24559b15422b2aea9b710fdb97#diff-fe2f8ee3b392be2f61ca686947bb43adffc4bbb12dde9dfac7bbf7edb219b824L757-R766) <!-- .element: class="github" style="background-color: rgb(229 231 225)" -->

NOTES:

- SLOW DOWN
- now instead of overflowing once to return to the original age, I have to
  overflow `2**32` times.  That seems like a lot.

---

<!-- .slide: data-background="./letter-a.png" -->

```cc [2]
void CopyIntoSlots(Span<void*> batch, Range r) {
  r.start %= slots_size(); r.end %= slots_size();
  if (ABSL_PREDICT_TRUE(r.start < r.end)) {
    memcpy(GetSlot(r.start), batch.data(),
           sizeof(void*) * (r.end - r.start));
  } else {
    int32_t overhang = slots_size() + 1 - r.start;
    memcpy(GetSlot(r.start), batch.data(),
           sizeof(void*) * overhang);
    memcpy(GetSlot(0), batch.data() + overhang,
           sizeof(void*) * r.end);
  }
}
```

[398b03c](https://github.com/google/tcmalloc/commit/398b03cf62804b24559b15422b2aea9b710fdb97#diff-fe2f8ee3b392be2f61ca686947bb43adffc4bbb12dde9dfac7bbf7edb219b824R746-R747) <!-- .element: class="github" style="background-color: rgb(229 231 225)" -->

NOTES:

- SLOW DOWN
- We also have to update CopyIntoSlots to chop the domain to our range.

