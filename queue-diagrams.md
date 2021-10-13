```cc []
class TransferCache {
  void InsertRange(absl::Span<void *> batch, int n);
  int RemoveRange(void** batch, int n);
};
```

Note:

- SLOW DOWN
- Let's start with a single writer queue
- For simplicity we are only going to look at one end.


-----

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
          <td sides="TBR">...</td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td port="h0"> </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  head -> q:h0;
}
```

```cc []
void InsertRange(absl::Span<void *> batch, int n) {
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

Note:

- SLOW DOWN
- Let's start with a single writer queue
- For simplicity we are only going to look at one end.

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
          <td sides="TBR">...</td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td port="h0"> </td>
          <td> </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  head -> q:h0;
}
```

```cc [3,9]
void InsertRange(absl::Span<void *> batch, int n) {
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

Note:

- SLOW DOWN
- fill in the new value

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
          <td sides="TBR">...</td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td port="h0"> </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  head -> q:h0;
}
```

```cc [3,10]
void InsertRange(absl::Span<void *> batch, int n) {
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

Note:

- SLOW DOWN
- and advanced the head pointer
- but how does this work with multiple producers?

-----

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
          <td sides="TBR">...</td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td port="h0"> </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  "head\ncommitted" -> q:h0;
  "head\npending" -> q:h0;
}
```

```cc []
void InsertRange(absl::Span<void *> batch, int n) {
  ASSERT(0 < n && n <= batch_size_);
  absl::optional<Range> r = ClaimInsert(n);
  if (!r.has_value()) {
    freelist_.InsertRange(batch.data(), n);
    return;
  }

  CopyIntoSlots(batch.data(), *r);
  head_committed_.AdvanceCommitLine(*r);
}
```

[9ca447](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L584) <!-- .element: class="github" -->

Note:

- SLOW DOWN
- instead of a single head pointer we keep a pending pointer
- when a new thread wants to push an element

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
          <td sides="TBR">...</td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td port="h0"> </td>
          <td port="h1" style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  "head\ncommitted" -> q:h0;
  "head\npending" -> q:h1;
}
```

```cc [3]
void InsertRange(absl::Span<void *> batch, int n) {
  ASSERT(0 < n && n <= batch_size_);
  absl::optional<Range> r = ClaimInsert(n);
  if (!r.has_value()) {
    freelist_.InsertRange(batch.data(), n);
    return;
  }

  CopyIntoSlots(batch.data(), *r);
  head_committed_.AdvanceCommitLine(*r);
}
```

[9ca447](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L584) <!-- .element: class="github" -->

Note:

- SLOW DOWN
- it advances the pending pointer

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
          <td sides="TBR">...</td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td port="h0"> </td>
          <td port="h1" style="dotted" sides="TBR" > </td>
          <td port="h2" style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  "head\ncommitted" -> q:h0;
  "head\npending" -> q:h2;
}
```

```cc [3]
void InsertRange(absl::Span<void *> batch, int n) {
  ASSERT(0 < n && n <= batch_size_);
  absl::optional<Range> r = ClaimInsert(n);
  if (!r.has_value()) {
    freelist_.InsertRange(batch.data(), n);
    return;
  }

  CopyIntoSlots(batch.data(), *r);
  head_committed_.AdvanceCommitLine(*r);
}
```

[9ca447](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L584) <!-- .element: class="github" -->

Note:

- SLOW DOWN
- even if the committed pointer has not yet caught up

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
          <td sides="TBR">...</td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td port="h0"> </td>
          <td port="h1" style="dotted" sides="TBR" > </td>
          <td port="h2" style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  "head\ncommitted" -> q:h0;
  "head\npending" -> q:h2;
}
```

```cc [9]
void InsertRange(absl::Span<void *> batch, int n) {
  ASSERT(0 < n && n <= batch_size_);
  absl::optional<Range> r = ClaimInsert(n);
  if (!r.has_value()) {
    freelist_.InsertRange(batch.data(), n);
    return;
  }

  CopyIntoSlots(batch.data(), *r);
  head_committed_.AdvanceCommitLine(*r);
}
```

[9ca447](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L584) <!-- .element: class="github" -->

Note:

- SLOW DOWN
- at this point two threads are running in parallel on this line!

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
          <td sides="TBR">...</td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td port="h0"> </td>
          <td port="h1" style="dotted" sides="TBR" > </td>
          <td port="h2" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  "head\ncommitted" -> q:h0;
  "head\npending" -> q:h2;
}
```

```cc [10]
void InsertRange(absl::Span<void *> batch, int n) {
  ASSERT(0 < n && n <= batch_size_);
  absl::optional<Range> r = ClaimInsert(n);
  if (!r.has_value()) {
    freelist_.InsertRange(batch.data(), n);
    return;
  }

  CopyIntoSlots(batch.data(), *r);
  head_committed_.AdvanceCommitLine(*r);
}
```

[9ca447](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L584) <!-- .element: class="github" -->


Note:

- SLOW DOWN
- for the sake of argument, let's say the thread2 finishes first
- it wants to advance the fill pointer, but it has to wait until it has reached the position before it.

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
          <td sides="TBR">...</td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td port="h0"> </td>
          <td port="h1" sides="TBR" > </td>
          <td port="h2" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  "head\ncommitted" -> q:h0;
  "head\npending" -> q:h2;
}
```

```cc [10]
void InsertRange(absl::Span<void *> batch, int n) {
  ASSERT(0 < n && n <= batch_size_);
  absl::optional<Range> r = ClaimInsert(n);
  if (!r.has_value()) {
    freelist_.InsertRange(batch.data(), n);
    return;
  }

  CopyIntoSlots(batch.data(), *r);
  head_committed_.AdvanceCommitLine(*r);
}
```

[9ca447](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L584) <!-- .element: class="github" -->

Note:

- SLOW DOWN
- once thread1 has finished pending its element, it can advance head

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
          <td sides="TBR">...</td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td port="h0"> </td>
          <td port="h1" sides="TBR" > </td>
          <td port="h2" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  "head\ncommitted" -> q:h1;
  "head\npending" -> q:h2;
}
```

```cc [10]
void InsertRange(absl::Span<void *> batch, int n) {
  ASSERT(0 < n && n <= batch_size_);
  absl::optional<Range> r = ClaimInsert(n);
  if (!r.has_value()) {
    freelist_.InsertRange(batch.data(), n);
    return;
  }

  CopyIntoSlots(batch.data(), *r);
  head_committed_.AdvanceCommitLine(*r);
}
```

[9ca447](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L584) <!-- .element: class="github" -->

Note:

- SLOW DOWN
- and now that head has advanced, thread2 can advance the committed line.

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
          <td sides="TBR">...</td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td port="h0"> </td>
          <td port="h1" sides="TBR" > </td>
          <td port="h2" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  "head\ncommitted" -> q:h2;
  "head\npending" -> q:h2;
}
```

```cc [10]
void InsertRange(absl::Span<void *> batch, int n) {
  ASSERT(0 < n && n <= batch_size_);
  absl::optional<Range> r = ClaimInsert(n);
  if (!r.has_value()) {
    freelist_.InsertRange(batch.data(), n);
    return;
  }

  CopyIntoSlots(batch.data(), *r);
  head_committed_.AdvanceCommitLine(*r);
}
```

[9ca447](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L584) <!-- .element: class="github" -->

Note:

- SLOW DOWN
- and now that head has advanced, thread2 can advance the committed line.

-----

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
          <td style="dotted"> </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td port="h0"> </td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  "tail\ncommitted" -> q:h0;
  "tail\npending" -> q:h0;
}
```

```cc []
int RemoveRange(void **batch, int n) {
  ASSERT(n > 0);
  absl::optional<Range> r = ClaimRemove(n);
  if (!r.has_value()) {
    return freelist_.RemoveRange(batch, n);
  }

  CopyFromSlots(batch, *r);
  tail_committed_.AdvanceCommitLine(*r, batch_size_);
  return n;
}
```

[9ca447](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L602) <!-- .element: class="github" -->

Note:

- SLOW DOWN
- removing from the queue is analagous

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
          <td style="dotted"> </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td port="h0"> </td>
          <td port="h1"> </td>
          <td port="h2"> </td>
          <td> </td>
          <td> </td>
          <td sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  "tail\ncommitted" -> q:h0;
  "tail\npending" -> q:h1;
}
```

```cc [3]
int RemoveRange(void **batch, int n) {
  ASSERT(n > 0);
  absl::optional<Range> r = ClaimRemove(n);
  if (!r.has_value()) {
    return freelist_.RemoveRange(batch, n);
  }

  CopyFromSlots(batch, *r);
  tail_committed_.AdvanceCommitLine(*r, batch_size_);
  return n;
}
```

[9ca447](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L602) <!-- .element: class="github" -->

Note:

- SLOW DOWN
- each thread advances pending line

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
          <td style="dotted"> </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td port="h0"> </td>
          <td port="h1"> </td>
          <td port="h2"> </td>
          <td> </td>
          <td> </td>
          <td sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  "tail\ncommitted" -> q:h0;
  "tail\npending" -> q:h2;
}
```

```cc [3]
int RemoveRange(void **batch, int n) {
  ASSERT(n > 0);
  absl::optional<Range> r = ClaimRemove(n);
  if (!r.has_value()) {
    return freelist_.RemoveRange(batch, n);
  }

  CopyFromSlots(batch, *r);
  tail_committed_.AdvanceCommitLine(*r, batch_size_);
  return n;
}
```

[9ca447](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L602) <!-- .element: class="github" -->

Note:

- SLOW DOWN
- potentially in parallel

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
          <td style="dotted"> </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td port="h0"> </td>
          <td port="h1" style="dotted" sides="TBR"> </td>
          <td port="h2"> </td>
          <td> </td>
          <td> </td>
          <td sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  "tail\ncommitted" -> q:h0;
  "tail\npending" -> q:h2;
}
```

```cc [8]
int RemoveRange(void **batch, int n) {
  ASSERT(n > 0);
  absl::optional<Range> r = ClaimRemove(n);
  if (!r.has_value()) {
    return freelist_.RemoveRange(batch, n);
  }

  CopyFromSlots(batch, *r);
  tail_committed_.AdvanceCommitLine(*r, batch_size_);
  return n;
}
```

[9ca447](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L602) <!-- .element: class="github" -->

Note:

- SLOW DOWN
- then they actually remove the elements

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
          <td style="dotted"> </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td port="h0" style="dotted" sides="TBR"> </td>
          <td port="h1" style="dotted" sides="TBR"> </td>
          <td port="h2"> </td>
          <td> </td>
          <td> </td>
          <td sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  "tail\ncommitted" -> q:h0;
  "tail\npending" -> q:h2;
}
```

```cc [8]
int RemoveRange(void **batch, int n) {
  ASSERT(n > 0);
  absl::optional<Range> r = ClaimRemove(n);
  if (!r.has_value()) {
    return freelist_.RemoveRange(batch, n);
  }

  CopyFromSlots(batch, *r);
  tail_committed_.AdvanceCommitLine(*r, batch_size_);
  return n;
}
```

[9ca447](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L602) <!-- .element: class="github" -->


Note:

- SLOW DOWN
- and then they start to advance the commit lines

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
          <td style="dotted"> </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td port="h0" style="dotted" sides="TBR"> </td>
          <td port="h1" style="dotted" sides="TBR"> </td>
          <td port="h2"> </td>
          <td> </td>
          <td> </td>
          <td sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  "tail\ncommitted" -> q:h1;
  "tail\npending" -> q:h2;
}
```

```cc [9]
int RemoveRange(void **batch, int n) {
  ASSERT(n > 0);
  absl::optional<Range> r = ClaimRemove(n);
  if (!r.has_value()) {
    return freelist_.RemoveRange(batch, n);
  }

  CopyFromSlots(batch, *r);
  tail_committed_.AdvanceCommitLine(*r, batch_size_);
  return n;
}
```

[9ca447](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L602) <!-- .element: class="github" -->


Note:

- SLOW DOWN
- but each thread can only advance from the previous line to the next

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
          <td style="dotted"> </td>
          <td style="dotted" sides="TBR" > </td>
          <td style="dotted" sides="TBR" > </td>
          <td port="h0" style="dotted" sides="TBR"> </td>
          <td port="h1" style="dotted" sides="TBR"> </td>
          <td port="h2"> </td>
          <td> </td>
          <td> </td>
          <td sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  "tail\ncommitted" -> q:h2;
  "tail\npending" -> q:h2;
}
```

```cc [9]
int RemoveRange(void **batch, int n) {
  ASSERT(n > 0);
  absl::optional<Range> r = ClaimRemove(n);
  if (!r.has_value()) {
    return freelist_.RemoveRange(batch, n);
  }

  CopyFromSlots(batch, *r);
  tail_committed_.AdvanceCommitLine(*r, batch_size_);
  return n;
}
```

[9ca447](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L602) <!-- .element: class="github" -->

Note:

- SLOW DOWN
- until they are all done

-----

<!-- .slide: data-background-color="white" -->
<!-- .slide: data-background="./axo.png" -->
<!-- .slide: data-background-size="contain" -->

NOTES:

- SLOW DOWN
- so far we have shown you the bits in isolation, but not how they fit together

-----

##### Normal

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
          <td style="dotted" sides="TBR">...</td>
          <td style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td port="tc" style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td port="tp"> </td>
          <td> </td>
          <td> </td>
          <td> </td>
          <td port="hc"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td port="hp" style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  "head\ncommitted" -> q:hc;
  "head\npending" -> q:hp;
  "tail\ncommitted" -> q:tc;
  "tail\npending" -> q:tp;
}
```

Note:

- SLOW DOWN
- here is a view in standard operation
- there are 2 threads inserting and 2 threads removing

---

##### Full

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
          <td sides="TBR">...</td>
          <td> </td>
          <td> </td>
          <td port="hc"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td port="hp" style="dotted" sides="TBR"> </td>
          <td port="tc" style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td port="tp"> </td>
          <td> </td>
          <td> </td>
          <td sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  "head\ncommitted" -> q:hc;
  "head\npending" -> q:hp;
  "tail\ncommitted" -> q:tc;
  "tail\npending" -> q:tp;
}
```

Note:

- SLOW DOWN
- here it is logically full
- there are active threads both filling and draining it
- but there is no space for new things right now

---

##### Empty

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
          <td style="dotted" sides="TBR">...</td>
          <td style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR" port="p"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TBR"> </td>
          <td style="dotted" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  "head\ncommitted" -> q:p;
  "head\npending" -> q:p;
  "tail\ncommitted" -> q:p;
  "tail\npending" -> q:p;
}
```

Note:

- SLOW DOWN
- here is it completely empty
- no active threads are operating on this queue

-----

##### Invariants

```md
Offsets are ordered (when viewed circularly):
  * `tail_committed <= tail_pending`
  * `tail_pending <= head_committed`
  * `head_committed <= head_pending`

Special states for empty/full:
  * Empty when `tail_committed == head_committed`
  * Full when `head_pending + 1 == tail_committed`

When there are no active threads:
  *  `tail_committed == tail`
  *  `head_committed == head`
```

NOTES:

- SLOW DOWN
- all of this is of course, when viewed circularly.

