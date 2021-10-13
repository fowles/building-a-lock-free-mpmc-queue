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

-----

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

-----

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

[fa3b5ab](https://github.com/google/tcmalloc/blob/fa3b5ab3e914483757fadd393a8db9263a3e926a/tcmalloc/transfer_cache_test.cc#L45-L47) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Suddenly we can write unit tests for all of out things!
- This may not seem ground breaking, but architecting a low-level component like
  tcmalloc so its internals can be tested outside the remainder of the system
  with no overhead can be rough.  Especially if the system already exists.  That
  said, the time spent making these refactors pays for itself easily when you
  then try to change the implementation.
