<!-- .slide: data-background="./rusty-lock.jpg" -->

<div class=boxed>
  <h4>Building a lock-free MPMC queue for tcmalloc</h4>
  <p style="font-size: 1.1rem;">https://github.com/fowles/building-a-lock-free-mpmc-queue</p>
  <h5>by Matt Kulukundis</h5>
</div>

NOTES:

- SLOW DOWN
- Introduce yourself
- Mention Speaker notes with links
- Mention diving into my sources of inspiration/learning


-----

<!-- .slide: data-background-color="black" -->
<!-- .slide: data-background="./epoch-time-model-rich-hickey.jpg" -->
<!-- .slide: data-background-size="contain" -->

NOTES:

- SLOW DOWN
- Rich Hickey's talk [Are We There Yet](https://www.infoq.com/presentations/Are-We-There-Yet-Rich-Hickey/) at JVM Language Summit in 2009
- Provides a high level lexicon for understanding concurrency
- More a mental model and a design principle that can be followed in the future
- Underscores that all values might be stale values


-----

<!-- .slide: data-background-color="black" -->
<!-- .slide: data-background="./java-memory-model-jeremy-manson.png" -->
<!-- .slide: data-background-size="contain" -->

NOTES:

- SLOW DOWN
- Jeremy Manson's talk [Advanced Topics in Programming Languages: The Java Memory Model](https://www.youtube.com/watch?v=1FX4zco0ziY) at Google NY in 2007
- Provides a low level lexicon for talking about concurrency
- Underscores the importance of using happens-before/happens-after terminology
- Sapir-Whorf hypothesis

-----

<!-- .slide: data-background="./disruptor-trisha-gee.png" -->
<!-- .slide: data-background-size="contain" -->

NOTES:

- SLOW DOWN
- May 2011 Martin Thompson (amone others) introduced Disruptors
- [Trisha Gee's blog](https://trishagee.github.io/post/disruptor_20__all_change_please/) is where I learned

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
    "CPU Cache";
    "Transfer Cache";
    "Central Free List";
  }
  "malloc/free" -> "CPU Cache" [dir="both"];
  "CPU Cache" -> "Transfer Cache" [dir="both"];
  "Transfer Cache" -> "Central Free List" [dir="both"];
  "Central Free List" -> "Operating System" [dir="both"];
}
```

-----

```language-plantuml
digraph g {
  bgcolor = "transparent";
  node [ fontname = "courier"; shape = none; ];
  q [
    label=<
      <table border="0" cellborder="1" cellspacing="0" cellpadding="4">
        <tr>
          <td> </td>
          <td> </td>
          <td> </td>
          <td>0</td>
          <td>1</td>
          <td>2</td>
          <td>3</td>
          <td> </td>
          <td> </td>
          <td> </td>
        </tr>
      </table>
    >
  ];
}
```

pain<!-- .element: class="absolute bottom-0 left-0" -->

Note:
asdf qwer
