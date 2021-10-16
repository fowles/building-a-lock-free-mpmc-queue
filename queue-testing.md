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

<img class="fragment absolute transform rotate-12 -translate-y-10 -translate-x-10" src="./deepwater-horizon.png" style="width: 60%;" data-fragment-index="1" />

<img class="fragment absolute transform -rotate-12 translate-x-10" src="./sir-not-appearing.png" style="width: 60%;" data-fragment-index="2" />


[ce9370a](https://github.com/google/tcmalloc/commit/ce9370ad2d603801d82cf28935ea29ad28b5e91c) <!-- .element: class="github fragment" style="background-color: rgb(229 231 225)" data-fragment-index="2" -->


NOTES:

- SLOW DOWN
- just put a giant lock on it.  Does it still happen?
- ADVANCE: yes.  But now I can stop looking at the atomics and start looking at
  the main logic.
- ADVANCE: the fix is a little hard to fit on a slide, but essentially I needed
  to handle cache growth more correctly.

-----

<!-- .slide: data-background="./clouds.png" -->

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
<!-- .element: class="fragment" -->

NOTES:

- SLOW DOWN
- Now that we have handled that bug and the test passes we are good right?
- Narrator: they weren't
- ADVANCE: Anyone remember this code?  I warned you that there was a bug.
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
<!-- .element: class="fragment" -->

NOTES:

- SLOW DOWN
- how do we know there is a problem, let alone track it down?
- ADVANCE: first run our fuzz tests many, many times.
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
- welp, there we are... we have a bug.
- before we go buck wild trying to figure this out...

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

FAILED in 4 out of 5000 in 39.8s
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

<div class="background fragment">
<pre><code class="language-plantuml"><script type="text/template">
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
</script></code></pre>
</div>

NOTES:

- SLOW DOWN
- now comes the hardest part of debugging.  I have exausted all of the tricks
  except just thinking more.
- let's go back to considering our queue.
- What happens if I acquire head committed and then go to sleep for a while...

---

<!-- .slide: data-background="./thinker.png" -->
<!-- .slide: data-background-size="contain" -->
<!-- .slide: data-background-color="black" -->

<div class="background">
<pre><code class="language-plantuml"><script type="text/template">
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
</script></code></pre>
</div>

Note:

- SLOW DOWN
- ANIMATION STARTS ON NEXT SLIDE!!!!

