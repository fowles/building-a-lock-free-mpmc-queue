<!-- .slide: data-background="./thinker.png" -->
<!-- .slide: data-background-size="contain" -->
<!-- .slide: data-background-color="black" -->
<!-- .slide: data-transition="none" -->

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
- ANIMATION ENDED

-----

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
<!-- .element: class="fragment" -->

NOTES:

- SLOW DOWN
- welcome to the canonical ABA bug.
- ADVANCE: empires can rise fand all around me while I wait here.
- ADVANCE: and as long as this contains the value it contained before I went to sleep
- I can be none the wiser

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

[398b03c](https://github.com/google/tcmalloc/commit/398b03cf62804b24559b15422b2aea9b710fdb97#diff-fe2f8ee3b392be2f61ca686947bb43adffc4bbb12dde9dfac7bbf7edb219b824L757-R766) <!-- .element: class="github" -->

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

[398b03c](https://github.com/google/tcmalloc/commit/398b03cf62804b24559b15422b2aea9b710fdb97#diff-fe2f8ee3b392be2f61ca686947bb43adffc4bbb12dde9dfac7bbf7edb219b824R746-R747) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- We also have to update CopyIntoSlots to chop the domain to our range.

