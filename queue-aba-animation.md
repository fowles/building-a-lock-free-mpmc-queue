
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
          <td port="r5" > </td>
          <td port="r6" > </td>
          <td port="r7" > </td>
          <td port="r8" > </td>
          <td port="r9" > </td>
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
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r5" > </td>
          <td port="r6" > </td>
          <td port="r7" > </td>
          <td port="r8" > </td>
          <td port="r9" > </td>
          <td port="r10" > </td>
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
  "head\ncommitted" -> q:r10;
  "head\npending" -> q:r13;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" > </td>
          <td port="r7" > </td>
          <td port="r8" > </td>
          <td port="r9" > </td>
          <td port="r10" > </td>
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
  "tail\npending" -> q:r6;
  "head\ncommitted" -> q:r10;
  "head\npending" -> q:r13;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" > </td>
          <td port="r7" > </td>
          <td port="r8" > </td>
          <td port="r9" > </td>
          <td port="r10" > </td>
          <td port="r11" > </td>
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
  "tail\npending" -> q:r6;
  "head\ncommitted" -> q:r11;
  "head\npending" -> q:r13;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" > </td>
          <td port="r8" > </td>
          <td port="r9" > </td>
          <td port="r10" > </td>
          <td port="r11" > </td>
          <td port="r12" style="dotted" sides="TBR"> </td>
          <td port="r13" style="dotted" sides="TBR"> </td>
          <td port="r14" style="dotted" sides="TBR"> </td>
          <td port="r15" style="dotted" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r4;
  "tail\npending" -> q:r7;
  "head\ncommitted" -> q:r11;
  "head\npending" -> q:r13;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" > </td>
          <td port="r8" > </td>
          <td port="r9" > </td>
          <td port="r10" > </td>
          <td port="r11" > </td>
          <td port="r12" > </td>
          <td port="r13" style="dotted" sides="TBR"> </td>
          <td port="r14" style="dotted" sides="TBR"> </td>
          <td port="r15" style="dotted" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r4;
  "tail\npending" -> q:r7;
  "head\ncommitted" -> q:r12;
  "head\npending" -> q:r1;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" > </td>
          <td port="r9" > </td>
          <td port="r10" > </td>
          <td port="r11" > </td>
          <td port="r12" > </td>
          <td port="r13" style="dotted" sides="TBR"> </td>
          <td port="r14" style="dotted" sides="TBR"> </td>
          <td port="r15" style="dotted" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r6;
  "tail\npending" -> q:r8;
  "head\ncommitted" -> q:r12;
  "head\npending" -> q:r1;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
          <td port="r9" > </td>
          <td port="r10" > </td>
          <td port="r11" > </td>
          <td port="r12" > </td>
          <td port="r13" style="dotted" sides="TBR"> </td>
          <td port="r14" style="dotted" sides="TBR"> </td>
          <td port="r15" style="dotted" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r7;
  "tail\npending" -> q:r9;
  "head\ncommitted" -> q:r12;
  "head\npending" -> q:r1;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
          <td port="r9" > </td>
          <td port="r10" > </td>
          <td port="r11" > </td>
          <td port="r12" > </td>
          <td port="r13" > </td>
          <td port="r14" style="dotted" sides="TBR"> </td>
          <td port="r15" style="dotted" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r7;
  "tail\npending" -> q:r9;
  "head\ncommitted" -> q:r13;
  "head\npending" -> q:r1;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
          <td port="r9" > </td>
          <td port="r10" > </td>
          <td port="r11" > </td>
          <td port="r12" > </td>
          <td port="r13" > </td>
          <td port="r14" > </td>
          <td port="r15" style="dotted" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r7;
  "tail\npending" -> q:r9;
  "head\ncommitted" -> q:r14;
  "head\npending" -> q:r1;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
          <td port="r9" style="dotted" sides="TBR"> </td>
          <td port="r10" > </td>
          <td port="r11" > </td>
          <td port="r12" > </td>
          <td port="r13" > </td>
          <td port="r14" > </td>
          <td port="r15" style="dotted" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r7;
  "tail\npending" -> q:r10;
  "head\ncommitted" -> q:r14;
  "head\npending" -> q:r1;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
          <td port="r9" style="dotted" sides="TBR"> </td>
          <td port="r10" style="dotted" sides="TBR"> </td>
          <td port="r11" > </td>
          <td port="r12" > </td>
          <td port="r13" > </td>
          <td port="r14" > </td>
          <td port="r15" style="dotted" sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r9;
  "tail\npending" -> q:r11;
  "head\ncommitted" -> q:r14;
  "head\npending" -> q:r1;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r0"  sides="TBR">...</td>
          <td port="r1" > </td>
          <td port="r2" style="dotted" sides="TBR"> </td>
          <td port="r3" style="dotted" sides="TBR"> </td>
          <td port="r4" style="dotted" sides="TBR"> </td>
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
          <td port="r9" style="dotted" sides="TBR"> </td>
          <td port="r10" style="dotted" sides="TBR"> </td>
          <td port="r11" > </td>
          <td port="r12" > </td>
          <td port="r13" > </td>
          <td port="r14" > </td>
          <td port="r15"  sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r9;
  "tail\npending" -> q:r11;
  "head\ncommitted" -> q:r1;
  "head\npending" -> q:r4;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r0"  sides="TBR">...</td>
          <td port="r1" > </td>
          <td port="r2" style="dotted" sides="TBR"> </td>
          <td port="r3" style="dotted" sides="TBR"> </td>
          <td port="r4" style="dotted" sides="TBR"> </td>
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
          <td port="r9" style="dotted" sides="TBR"> </td>
          <td port="r10" style="dotted" sides="TBR"> </td>
          <td port="r11" style="dotted" sides="TBR"> </td>
          <td port="r12" > </td>
          <td port="r13" > </td>
          <td port="r14" > </td>
          <td port="r15"  sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r10;
  "tail\npending" -> q:r12;
  "head\ncommitted" -> q:r1;
  "head\npending" -> q:r4;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r0"  sides="TBR">...</td>
          <td port="r1" > </td>
          <td port="r2" > </td>
          <td port="r3" style="dotted" sides="TBR"> </td>
          <td port="r4" style="dotted" sides="TBR"> </td>
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
          <td port="r9" style="dotted" sides="TBR"> </td>
          <td port="r10" style="dotted" sides="TBR"> </td>
          <td port="r11" style="dotted" sides="TBR"> </td>
          <td port="r12" > </td>
          <td port="r13" > </td>
          <td port="r14" > </td>
          <td port="r15"  sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r10;
  "tail\npending" -> q:r12;
  "head\ncommitted" -> q:r2;
  "head\npending" -> q:r4;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r0"  sides="TBR">...</td>
          <td port="r1" > </td>
          <td port="r2" > </td>
          <td port="r3" > </td>
          <td port="r4" style="dotted" sides="TBR"> </td>
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
          <td port="r9" style="dotted" sides="TBR"> </td>
          <td port="r10" style="dotted" sides="TBR"> </td>
          <td port="r11" style="dotted" sides="TBR"> </td>
          <td port="r12" > </td>
          <td port="r13" > </td>
          <td port="r14" > </td>
          <td port="r15"  sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r10;
  "tail\npending" -> q:r12;
  "head\ncommitted" -> q:r3;
  "head\npending" -> q:r6;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r0"  sides="TBR">...</td>
          <td port="r1" > </td>
          <td port="r2" > </td>
          <td port="r3" > </td>
          <td port="r4" style="dotted" sides="TBR"> </td>
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
          <td port="r9" style="dotted" sides="TBR"> </td>
          <td port="r10" style="dotted" sides="TBR"> </td>
          <td port="r11" style="dotted" sides="TBR"> </td>
          <td port="r12" style="dotted" sides="TBR"> </td>
          <td port="r13" > </td>
          <td port="r14" > </td>
          <td port="r15"  sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r11;
  "tail\npending" -> q:r13;
  "head\ncommitted" -> q:r3;
  "head\npending" -> q:r6;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r0"  sides="TBR">...</td>
          <td port="r1" > </td>
          <td port="r2" > </td>
          <td port="r3" > </td>
          <td port="r4" style="dotted" sides="TBR"> </td>
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
          <td port="r9" style="dotted" sides="TBR"> </td>
          <td port="r10" style="dotted" sides="TBR"> </td>
          <td port="r11" style="dotted" sides="TBR"> </td>
          <td port="r12" style="dotted" sides="TBR"> </td>
          <td port="r13" style="dotted" sides="TBR"> </td>
          <td port="r14" > </td>
          <td port="r15"  sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r12;
  "tail\npending" -> q:r14;
  "head\ncommitted" -> q:r3;
  "head\npending" -> q:r6;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r0"  sides="TBR">...</td>
          <td port="r1" > </td>
          <td port="r2" > </td>
          <td port="r3" > </td>
          <td port="r4" > </td>
          <td port="r5" style="dotted" sides="TBR"> </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
          <td port="r9" style="dotted" sides="TBR"> </td>
          <td port="r10" style="dotted" sides="TBR"> </td>
          <td port="r11" style="dotted" sides="TBR"> </td>
          <td port="r12" style="dotted" sides="TBR"> </td>
          <td port="r13" style="dotted" sides="TBR"> </td>
          <td port="r14" > </td>
          <td port="r15"  sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r12;
  "tail\npending" -> q:r14;
  "head\ncommitted" -> q:r4;
  "head\npending" -> q:r7;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r0"  sides="TBR">...</td>
          <td port="r1" > </td>
          <td port="r2" > </td>
          <td port="r3" > </td>
          <td port="r4" > </td>
          <td port="r5" > </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
          <td port="r9" style="dotted" sides="TBR"> </td>
          <td port="r10" style="dotted" sides="TBR"> </td>
          <td port="r11" style="dotted" sides="TBR"> </td>
          <td port="r12" style="dotted" sides="TBR"> </td>
          <td port="r13" style="dotted" sides="TBR"> </td>
          <td port="r14" > </td>
          <td port="r15"  sides="TB">...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\nhead committed" [dir="back"];
  "tail\ncommitted" -> q:r12;
  "tail\npending" -> q:r14;
  "head\ncommitted" -> q:r5;
  "head\npending" -> q:r7;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r1" > </td>
          <td port="r2" > </td>
          <td port="r3" > </td>
          <td port="r4" > </td>
          <td port="r5" > </td>
          <td port="r6" style="dotted" sides="TBR"> </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
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
  "tail\npending" -> q:r1;
  "head\ncommitted" -> q:r5;
  "head\npending" -> q:r7;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r1" > </td>
          <td port="r2" > </td>
          <td port="r3" > </td>
          <td port="r4" > </td>
          <td port="r5" > </td>
          <td port="r6" > </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
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
  "tail\npending" -> q:r1;
  "head\ncommitted" -> q:r6;
  "head\npending" -> q:r8;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r2" > </td>
          <td port="r3" > </td>
          <td port="r4" > </td>
          <td port="r5" > </td>
          <td port="r6" > </td>
          <td port="r7" style="dotted" sides="TBR"> </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
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
  "tail\npending" -> q:r2;
  "head\ncommitted" -> q:r6;
  "head\npending" -> q:r8;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r2" > </td>
          <td port="r3" > </td>
          <td port="r4" > </td>
          <td port="r5" > </td>
          <td port="r6" > </td>
          <td port="r7" > </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
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
  "tail\npending" -> q:r2;
  "head\ncommitted" -> q:r7;
  "head\npending" -> q:r9;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r3" > </td>
          <td port="r4" > </td>
          <td port="r5" > </td>
          <td port="r6" > </td>
          <td port="r7" > </td>
          <td port="r8" style="dotted" sides="TBR"> </td>
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
  "tail\ncommitted" -> q:r1;
  "tail\npending" -> q:r3;
  "head\ncommitted" -> q:r7;
  "head\npending" -> q:r9;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r3" > </td>
          <td port="r4" > </td>
          <td port="r5" > </td>
          <td port="r6" > </td>
          <td port="r7" > </td>
          <td port="r8" > </td>
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
  "tail\ncommitted" -> q:r1;
  "tail\npending" -> q:r3;
  "head\ncommitted" -> q:r8;
  "head\npending" -> q:r11;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r4" > </td>
          <td port="r5" > </td>
          <td port="r6" > </td>
          <td port="r7" > </td>
          <td port="r8" > </td>
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
  "tail\ncommitted" -> q:r1;
  "tail\npending" -> q:r4;
  "head\ncommitted" -> q:r8;
  "head\npending" -> q:r11;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r5" > </td>
          <td port="r6" > </td>
          <td port="r7" > </td>
          <td port="r8" > </td>
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
  "tail\ncommitted" -> q:r3;
  "tail\npending" -> q:r5;
  "head\ncommitted" -> q:r8;
  "head\npending" -> q:r11;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r5" > </td>
          <td port="r6" > </td>
          <td port="r7" > </td>
          <td port="r8" > </td>
          <td port="r9" > </td>
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
  "head\npending" -> q:r12;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.

-----

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
          <td port="r5" > </td>
          <td port="r6" > </td>
          <td port="r7" > </td>
          <td port="r8" > </td>
          <td port="r9" > </td>
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
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.
