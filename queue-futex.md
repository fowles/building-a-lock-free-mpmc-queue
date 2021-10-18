<!-- .slide: data-background="./rusty-lock.png" -->

NOTES:

- SLOW DOWN
- So the observant of you will notice that I now have two little spin lock.

---

<!-- .slide: data-background="./rusty-lock.png" -->

```cc [2,4]
void AwaitChange(std::atomic<uint32_t> &v, uint32_t actual) {
  while (v.load(std::memory_order_relaxed) != actual) {
    _mm_pause();
  }
}
```

NOTES:

- SLOW DOWN
- One here where we sniff our tail and wait for things to proceed so we can retry

---

<!-- .slide: data-background="./rusty-lock.png" -->

```cc [4-6,8]
void AdvanceCommitLine(
    std::atomic<uint32_t> *commit, Range r) {
  uint32_t temp_pos;
  while (!commit->compare_exchange_weak(
            temp_pos = r.from, r.to,
            order_release, order_relaxed)) {
    _mm_pause();
  }
}
```

NOTES:

- SLOW DOWN
- and another one here where we spin waiting for people before us to commit
- That is a lot of spinning where we could be saving CPU and letting other
  threads do real work

-----

<!-- .slide: data-background="./rusty-lock.png" -->

NOTES:

- SLOW DOWN
- While I try to think of a way to improve this, why don't you talk amonst
  yourselves.  I will give you a topic.
- Futex is neither fast, nor userspace, nor a mutex.  Discuss.

---

<!-- .slide: data-background="./rusty-lock.png" -->

```cc [|3]
long syscall(SYS_futex,
             uint32_t *uaddr,
             int futex_op,
             uint32_t val,
             const struct timespec *timeout,
             uint32_t *uaddr2,
             uint32_t val3);
```

NOTES:

- SLOW DOWN
- It is actually a low level utility thing that you can use to build a mutex
  that is fast and entirely in user space for the non-contended cases.
- It is a bit like calling a supply of nails, lumber, roofing, and cement,
  "churahouse" because you can use all of these parts to build a cheap durable
  house.
- It is better to think of `futex` as a number of distinct operations that
  relate to each other as good building blocks.

---

<!-- .slide: data-background="./rusty-lock.png" -->

```cc [|5|7|6|8]
class Futex {
  std::atomic<uint32_t> val_;

 public:
  bool Wait(uint32_t expected);
  bool WaitBitset(uint32_t expected, uint32_t bitset);
  bool Wake(uint32_t num_to_wake);
  bool WakeBitset(uint32_t num_to_wake, uint32_t bitset);
};
```

NOTES:

- SLOW DOWN
- You can notionally think of it this way.
- ADVANCE: `Wait` is the core operation.  It is an atomic "compare-and-sleep"
  operation.
- ADVANCE: `Wake` pairs with `Wait` and specifies how many sleepers to wake up
  as well.  Usually you want 1 or all.
- ADVANCE: `WaitBitset` is still an atomic "compare-and-sleep", but the sleeper
  keep a bitset that will be used for selective wake ups.
- ADVANCE: `WakeBitset` specifies a mask that will be `&`ed with the the
  sleepers' bitset value.  Only sleepers with a bit in common will be woken.
- There are actually a few more advanced operations, including options for
  controlling timeouts and the like, but I am not going to cover them in this
  talk.

---

<!-- .slide: data-background="./rusty-lock.png" -->

```cc [|2]
long syscall(SYS_futex,
             uint32_t *uaddr,
             int futex_op,
             uint32_t val,
             const struct timespec *timeout,
             uint32_t *uaddr2,
             uint32_t val3);
```

NOTES:

- SLOW DOWN
- The nice thing about futex is that you can reuse any atomic you happen to
  already have lying around.  Heck, you can even use 4 bytes from an
  `atomic<T*>` if you are feeling spicy.
- Let's see how that fits in here.

-----

<!-- .slide: data-background="./rusty-lock.png" -->

```cc []
void AwaitChange(std::atomic<uint32_t> &v, uint32_t actual) {
  while (v.load(std::memory_order_relaxed) != actual) {
    _mm_pause();
  }
}
```

```cc []
void AwaitChange(std::atomic<uint32_t> &v, uint32_t actual) {
  FutexWait(v, cur);
}
```

[9ca447c](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L793-L808) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Notionally this should work, but it is good practice to spin just a little
  bit before going straight to a kernel sleep.  That said, you are in a land of
  careful dragons here and should not take my slides as golden.

---

<!-- .slide: data-background="./rusty-lock.png" -->

```cc []
void AwaitChange(std::atomic<uint32_t> &v, uint32_t actual) {
    while (true) {
      for (int i = 1024; i > 0; --i) {
        if (v_.load(std::memory_order_relaxed) != actual) {
          return;
        }
        _mm_pause();
      }

      FutexWait(v, actual);
    }
}
```

[9ca447c](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L793-L808) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Here is a very slightly improved version, which is basically what we do.

---

<!-- .slide: data-background="./rusty-lock.png" -->

```cc []
void AdvanceCommitLine(
    std::atomic<uint32_t> *commit, Range r) {
  uint32_t temp_pos;
  while (!commit->compare_exchange_weak(
            temp_pos = r.from, r.to,
            order_release, order_relaxed)) {
    _mm_pause();
  }
}
```

NOTES:

- SLOW DOWN
- this one gets a slightly larger overhaul

---

<!-- .slide: data-background="./rusty-lock.png" -->

```cc []
void AdvanceCommitLine(
    std::atomic<uint32_t> *commit, Range r) {
  uint32_t temp_pos;
  while (!commit->compare_exchange_weak(
            temp_pos = r.from, r.to,
            order_release, order_relaxed)) {
    _mm_pause();
  }
}
```

```cc []
void AdvanceCommitLine(
    std::atomic<uint32_t> *commit, Range r) {
  AwaitEqual(commit, r.from);
  commit->store(r.to, order_release);
  FutexWake(commit);
}
```

[9ca447c](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L793-L808) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- We introduce a small helper to keep it clean

---

<!-- .slide: data-background="./rusty-lock.png" -->

```cc []
void AwaitEqual(std::atomic<uint32_t> &v, uint32_t desired) {
    uint32_t cur;
    while (true) {
      for (int i = 1024; i > 0; --i) {
        cur = v_.load(std::memory_order_relaxed);
        if (cur == actual) return;
        _mm_pause();
      }

      FutexWait(v, cur);
    }
}
```

NOTES:

- SLOW DOWN
- Same basic idea here though.
- Wait a moment (no pun intended). 
- When we are waiting to advance the commit line, there is only a single value
  that will make us happy.  We shouldn't need to wake up for any old change to
  the value.
- Let's go back to the Futex API and see if we can do anything clever.

-----

<!-- .slide: data-background="./rusty-lock.png" -->

```cc [6,8]
class Futex {
  std::atomic<uint32_t> val_;

 public:
  bool Wait(uint32_t expected);
  bool WaitBitset(uint32_t expected, uint32_t bitset);
  bool Wake(uint32_t num_to_wake);
  bool WakeBitset(uint32_t num_to_wake, uint32_t bitset);
};
```

NOTES:

- SLOW DOWN
- It's odd that the narrator put those two methods into the API when talking
  about these things.  I bet we can do something clever with that.

---

<!-- .slide: data-background="./rusty-lock.png" -->

```cc [10]
void AwaitChange(std::atomic<uint32_t> &v, uint32_t actual) {
    while (true) {
      for (int i = 1024; i > 0; --i) {
        if (v_.load(std::memory_order_relaxed) != actual) {
          return;
        }
        _mm_pause();
      }

      FutexWait(v, actual);
    }
}
```

NOTES:

- SLOW DOWN
- In this case we want to wake up for any value at all.  So I guess we just set
  all the bits.

---

<!-- .slide: data-background="./rusty-lock.png" -->

```cc [10]
void AwaitChange(std::atomic<uint32_t> &v, uint32_t actual) {
    while (true) {
      for (int i = 1024; i > 0; --i) {
        if (v_.load(std::memory_order_relaxed) != actual) {
          return;
        }
        _mm_pause();
      }

      FutexWaitBitset(v, actual, FUTEX_BITSET_MATCH_ANY);
    }
}
```

NOTES:

- SLOW DOWN
- Seems simple enough.

---

<!-- .slide: data-background="./rusty-lock.png" -->

```cc [10]
void AwaitEqual(std::atomic<uint32_t> &v, uint32_t desired) {
    uint32_t cur;
    while (true) {
      for (int i = 1024; i > 0; --i) {
        cur = v_.load(std::memory_order_relaxed);
        if (cur == actual) return;
        _mm_pause();
      }

      FutexWait(v, cur);
    }
}
```

NOTES:

- SLOW DOWN
- In this case we want to wait on something related to our desired value.
  Let's just assume we can figure that out later.

---

<!-- .slide: data-background="./rusty-lock.png" -->

```cc [10]
void AwaitEqual(std::atomic<uint32_t> &v, uint32_t desired) {
    uint32_t cur;
    while (true) {
      for (int i = 1024; i > 0; --i) {
        cur = v_.load(std::memory_order_relaxed);
        if (cur == actual) return;
        _mm_pause();
      }

      FutexWaitBitset(v, cur, ComputeBitset(desired));
    }
}
```

NOTES:

- SLOW DOWN
- seems reasonable assuming we can figure out that function later.

---

<!-- .slide: data-background="./rusty-lock.png" -->

```cc []
void AdvanceCommitLine(
    std::atomic<uint32_t> *commit, Range r) {
  AwaitEqual(commit, r.from);
  commit->store(r.to, order_release);
  FutexWake(commit);
}
```

NOTES:

- SLOW DOWN
- lastly, we need to wake up things based on the bitset.  Fortunately we can
  simply reuse our assumption.

---

<!-- .slide: data-background="./rusty-lock.png" -->

```cc []
void AdvanceCommitLine(
    std::atomic<uint32_t> *commit, Range r) {
  AwaitEqual(commit, r.from);
  commit->store(r.to, order_release);
  FutexWakeBitset(commit, ComputeBitset(r.to));
}
```

NOTES:

- SLOW DOWN
- lastly, we need to wake up things based on the bitset.  Fortunately we can
  simply reuse our assumption.

-----

<!-- .slide: data-background="./rusty-lock.png" -->

NOTES:

- SLOW DOWN
- Now we only need to figure out our function.
- Since these are bits that will be masked to each other we want as little
  overlap as possible.  Also, we each subsequent value to be unique.


---

<!-- .slide: data-background="./rusty-lock.png" -->

```cc
0b00000000000000000000000000000001
0b00000000000000000000000000000010
0b00000000000000000000000000000100
0b00000000000000000000000000001000
...
```

NOTES:

- SLOW DOWN
- Actually, that is a really easy function to compute...

---

<!-- .slide: data-background="./rusty-lock.png" -->

```cc
uint32_t ComputeBitset(uint32_t value) {
  uint32_t shift = value % 32;
  return uint32_t{1} << shift;
}
```

[9ca447c](https://github.com/google/tcmalloc/blob/9ca447ccc18bf70e33ac1efa292911590e539e08/tcmalloc/transfer_cache_internals.h#L934-L944) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- We will get collisions, but that was unavoidable since we are trying to map
  the full space of a uint32_t down to 32 unique values.  The important part is
  that the bits are maximally spaced out for our domain.

-----

<!-- .slide: data-background="./deepwater-horizon.png" -->

NOTES:

- SLOW DOWN
- In truth it took me a few tries and I had to track down some bugs, but it
  wasn't really that bad.
