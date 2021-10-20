<!-- .slide: data-background="./rusty-lock.png" -->

<div class="background" style="border-radius: 10px">
  <h4 style="margin-bottom: 0;">Building a lock-free MPMC queue for tcmalloc</h4>
  <a style="font-size: 1.1rem;" href="https://github.com/fowles/building-a-lock-free-mpmc-queue">https://github.com/fowles/building-a-lock-free-mpmc-queue</a>
  <h5>by Matt Kulukundis</h5>
</div>
<div style="font-size: 0.8rem; color: white" class="absolute bottom-0">press "S" for speaker view</div>

[tcmalloc](https://github.com/google/tcmalloc) <!-- .element: class="github" -->

NOTES:

- SLOW DOWN
- Introduce yourself
- Mention Speaker notes with links
- TALK ABOUT THE GITHUB CHIP

-----

<!-- .slide: data-background-color="black" -->
<!-- .slide: data-background="./overview.png" -->

NOTES:

- SLOW DOWN
- I learned about tcmalloc at Chris Kennelly's cppcon talk in 2019, which
  inspired me to hack on it.  tcmalloc is an implementaiton of the memory
  allocator for your process.  It handles getting raw memory from the OS and
  handing back raw memory to the OS (with many layers of caching).  You can
  think of it as the thing that implements malloc/free and/or new/delete.
- This talk is more of a journey then a destination.  I am going to explain how
  I go about iterating in a difficult design space like this.  What steps I use
  to inform next actions and leasons learned along the way, including real world
  bugs, benchmarks, and results on full systems.  Naturally, I wanted to dive
  write in and start improving it.

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
- [tcmalloc][1] is best thought of as a series of layered caches, so I started
  by diving into those layers.
- [cpu cache][2] is the fastest.  It uses restartable sequences to do per-cpu
  magic. Internally, it stores its data in a very simple stack so that it can
  hand that data out to users very fast.  It uses a lot of assembly and is
  highly optimized.  I briefly looked at this but it was clear to me that this
  was way too advanced.  
- [central free list][4] is the component that interacts with the operating
  system.  It uses a very complex structure that it embeds inside the memory it
  manages for maximum efficiency.  It has a lot of complicated code to handle os
  specific things like page sizes.  It was clear to me that this was too
  advanced for me to play with easily.
- [transfer cache][3] is a kinda simple stack that sits between the two of
  these.  It keeps the data in a simple format so it can hand it to cpu caches
  easily.  It's primary purpose is to vend data between cpu caches as they
  overflow or underflow.
- Fortunately, I have a bit of experience with concurrent data structures from a
  previous life.

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

