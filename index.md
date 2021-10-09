<!-- .slide: data-background="./rusty-lock.jpg" -->

<div class="boxed">
  <h4 style="margin-bottom: 0;">Building a lock-free MPMC queue for tcmalloc</h4>
  <a style="font-size: 1.1rem;" href="https://github.com/fowles/building-a-lock-free-mpmc-queue"> https://github.com/fowles/building-a-lock-free-mpmc-queue </a>
  <h5>by Matt Kulukundis</h5>
</div>
<div style="font-size: 0.8rem; color: white" class="absolute bottom-0">press "S" for speaker view</div>

NOTES:

- SLOW DOWN
- Introduce yourself
- Mention Speaker notes with links
- Mention diving into my sources of inspiration/learning

-----

<!-- .slide: data-background-color="black" -->
<!-- .slide: data-background="./overview.png" -->

NOTES:

- SLOW DOWN
- Steel yourselves, I am told that I have a tendency to jump into technical things pretty hot.
- This talk has a few sections
  - overview of tcmalloc
  - recommendations for talks and blogs where I learned a lot of this stuff
  - explanation of LMAX disruptors
  - re-architecting tcmalloc for unit tests
  - diving into the new algorithm
  - adding fuzz tests
  - adding benchmarks
  - fixing race conditions
  - improving benchmarks

-----

## `tcmalloc`

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

NOTES:

- SLOW DOWN
- [tcmalloc][1] is best thought of as a series of layered caches
- [cpu cache][2] is fastest and unique to both the CPU and size class
- [transfer cache][3] is unique to the size class but shared for all cpus
- transfer cache stores data in a format well suited to the cpu cache
- [central free list][4] stores data in a more memory efficient format

[1]: https://github.com/google/tcmalloc
[2]: https://github.com/google/tcmalloc/blob/master/tcmalloc/cpu_cache.h
[3]: https://github.com/google/tcmalloc/blob/master/tcmalloc/transfer_cache.h
[4]: https://github.com/google/tcmalloc/blob/master/tcmalloc/central_freelist.h


-----

<!-- .slide: data-background-color="black" -->
<!-- .slide: data-background="./epoch-time-model-rich-hickey.jpg" -->
<!-- .slide: data-background-size="contain" -->

NOTES:

- SLOW DOWN
- Rich Hickey's talk [Are We There Yet][1] at JVM Language Summit in 2009
- Provides a high level lexicon for understanding concurrency
- More a mental model and a design principle that can be followed in the future
- Underscores that all values might be stale values

[1]: https://www.infoq.com/presentations/Are-We-There-Yet-Rich-Hickey/

-----

<!-- .slide: data-background-color="black" -->
<!-- .slide: data-background="./java-memory-model-jeremy-manson.png" -->
<!-- .slide: data-background-size="contain" -->

NOTES:

- SLOW DOWN
- Jeremy Manson's talk [Advanced Topics in Programming Languages: The Java Memory Model][1] at Google NY in 2007
- Provides a low level lexicon for talking about concurrency
- Underscores the importance of using happens-before/happens-after terminology

[1]: https://www.youtube.com/watch?v=1FX4zco0ziY

-----

<!-- .slide: data-background="./sapir-whorf.png" -->
<!-- .slide: data-background-size="contain" -->

NOTES:

- SLOW DOWN
- You might pick out a theme between these two talks defining our lexicon and mental model.
- Concurrent programming is hard.  Hard to do, hard to think about.
- If you nail down your language it can be a really big aid.

-----

<!-- .slide: data-background="./disruptor-trisha-gee.png" -->
<!-- .slide: data-background-size="contain" -->
<img class="absolute bottom-0 left-0" src="./trisha-gee.png" style="width: 20%;" />

NOTES:

- SLOW DOWN
- May 2011 Martin Thompson (amone others) introduced Disruptors
- [Trisha Gee's blog][1] is where I learned

[1]: https://trishagee.github.io/post/disruptor_20__all_change_please/

