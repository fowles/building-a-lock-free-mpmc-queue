
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
          <td port="r10"> </td>
          <td port="r11"> </td>
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
  "head\ncommitted" -> q:r11;
  "head\npending" -> q:r14;
}
```

Note:

- SLOW DOWN
- Ages come and pass

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
          <td port="r0" style="dotted" sides="TBR">...</td>
          <td port="r1" style="dotted" sides="TBR"> </td>
          <td port="r2" style="dotted" sides="TBR"> </td>
          <td port="r3" style="dotted" sides="TBR"> </td>
          <td port="r4" style="dotted" sides="TBR"> </td>
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
          <td port="r9" style="dotted" sides="TBR"> </td>
          <td port="r10"> </td>
          <td port="r11"> </td>
          <td port="r12" style="dotted" sides="TBR"> </td>
          <td port="r13" style="dotted" sides="TBR"> </td>
          <td port="r14" style="dotted" sides="TBR"> </td>
          <td port="r15" style="dotted" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r10;
  "tail\npending" -> q:r10;
  "head\ncommitted" -> q:r11;
  "head\npending" -> q:r14;
}
```

Note:

- SLOW DOWN
- leaving memories that become legend

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
          <td port="r0" sides="TBR">...</td>
          <td port="r1" sides="TBR"> </td>
          <td port="r2" sides="TBR"> </td>
          <td port="r3" sides="TBR"> </td>
          <td port="r4" sides="TBR"> </td>
          <td port="r5" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
          <td port="r9" style="dotted" sides="TBR"> </td>
          <td port="r10" style="dotted" sides="TBR"> </td>
          <td port="r11" style="dotted" sides="TBR"> </td>
          <td port="r12" style="dotted" sides="TBR"> </td>
          <td port="r13" style="dotted" sides="TBR"> </td>
          <td port="r14"> </td>
          <td port="r15" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r10;
  "tail\npending" -> q:r14;
  "head\ncommitted" -> q:r5;
  "head\npending" -> q:r6;
}
```

Note:

- SLOW DOWN
- Legend fades to myth

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
          <td port="r0" style="dotted" sides="TBR">...</td>
          <td port="r1" style="dotted" sides="TBR"> </td>
          <td port="r2" style="dotted" sides="TBR"> </td>
          <td port="r3"> </td>
          <td port="r4"> </td>
          <td port="r5"> </td>
          <td port="r6"> </td>
          <td port="r7"> </td>
          <td port="r8"> </td>
          <td port="r9" style="dotted" sides="TBR"> </td>
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
  "tail\ncommitted" -> q:r14;
  "tail\npending" -> q:r3;
  "head\ncommitted" -> q:r8;
  "head\npending" -> q:r11;
}
```

Note:

- SLOW DOWN
- and even myth is long forgotten

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
```

Note:

- SLOW DOWN
- when the Age that gave it birth comes again.
