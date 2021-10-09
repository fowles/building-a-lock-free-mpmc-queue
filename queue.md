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
          <td port="head"> </td>
          <td style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  head -> q:head;
}
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
          <td port="head"> </td>
          <td> </td>
          <td style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  head -> q:head;
}
```

Note:

- SLOW DOWN
- fill in the new value

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
          <td port="head"> </td>
          <td style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  filled -> q:head;
  filling -> q:head;
}
```

Note:

- SLOW DOWN
- instead of a single head pointer we keep a filling pointer
- when a new thread wants to push an element

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
          <td port="head"> </td>
          <td port="h1" style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  filled -> q:head;
  filling -> q:h1;
}
```

Note:

- SLOW DOWN
- it advances the filling pointer

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
          <td port="head"> </td>
          <td port="h1" style="dashed" sides="TBR" > </td>
          <td port="h2" style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  filled -> q:head;
  filling -> q:h2;
}
```

Note:

- SLOW DOWN
- even if the filled pointer has not yet caught up

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
          <td port="head"> </td>
          <td port="h1" style="dashed" sides="TBR" > </td>
          <td port="h2" > </td>
          <td style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  filled -> q:head;
  filling -> q:h2;
}
```

Note:

- SLOW DOWN
- for the sake of argument, let's say the thread2 finishes first
- it wants to advance the fill pointer, but it has to wait until it has reached the position before it.

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
          <td port="head"> </td>
          <td port="h1" sides="TBR" > </td>
          <td port="h2" > </td>
          <td style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  filled -> q:head;
  filling -> q:h2;
}
```

Note:

- SLOW DOWN
- once thread1 has finished filling its element, it can advance head

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
          <td port="head"> </td>
          <td port="h1" sides="TBR" > </td>
          <td port="h2" > </td>
          <td style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  filled -> q:h1;
  filling -> q:h2;
}
```

Note:

- SLOW DOWN
- and now that head has advanced, thread2 can advance the filled line.

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
          <td port="head"> </td>
          <td port="h1" sides="TBR" > </td>
          <td port="h2" > </td>
          <td style="dashed" sides="TBR" > </td>
          <td style="dashed" sides="TBR" > </td>
        </tr>
      </table>
    >;
  ];
  filled -> q:h2;
  filling -> q:h2;
}
```

Note:

- SLOW DOWN
- and now that head has advanced, thread2 can advance the filled line.
