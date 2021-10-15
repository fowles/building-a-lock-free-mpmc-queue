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
