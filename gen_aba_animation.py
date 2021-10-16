#!python3

import random

slide_template = '''
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
          <td port="r0" %(0)s>...</td>
          <td port="r1" %(1)s> </td>
          <td port="r2" %(2)s> </td>
          <td port="r3" %(3)s> </td>
          <td port="r4" %(4)s> </td>
          <td port="r5" %(5)s> </td>
          <td port="r6" %(6)s> </td>
          <td port="r7" %(7)s> </td>
          <td port="r8" %(8)s> </td>
          <td port="r9" %(9)s> </td>
          <td port="r10" %(10)s> </td>
          <td port="r11" %(11)s> </td>
          <td port="r12" %(12)s> </td>
          <td port="r13" %(13)s> </td>
          <td port="r14" %(14)s> </td>
          <td port="r15" %(15)s>...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\\nhead committed" [dir="back"];
  "tail\\ncommitted" -> q:r%(tc)s;
  "tail\\npending" -> q:r%(tp)s;
  "head\\ncommitted" -> q:r%(hc)s;
  "head\\npending" -> q:r%(hp)s;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.
'''

slide_template = '''
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
          <td port="r0" %(0)s>...</td>
          <td port="r1" %(1)s> </td>
          <td port="r2" %(2)s> </td>
          <td port="r3" %(3)s> </td>
          <td port="r4" %(4)s> </td>
          <td port="r5" %(5)s> </td>
          <td port="r6" %(6)s> </td>
          <td port="r7" %(7)s> </td>
          <td port="r8" %(8)s> </td>
          <td port="r9" %(9)s> </td>
          <td port="r10" %(10)s> </td>
          <td port="r11" %(11)s> </td>
          <td port="r12" %(12)s> </td>
          <td port="r13" %(13)s> </td>
          <td port="r14" %(14)s> </td>
          <td port="r15" %(15)s>...</td>
        </tr>
      </table>
    >;
  ];
  q:r9 -> "my view of\\nhead committed" [dir="back"];
  "tail\\ncommitted" -> q:r%(tc)s;
  "tail\\npending" -> q:r%(tp)s;
  "head\\ncommitted" -> q:r%(hc)s;
  "head\\npending" -> q:r%(hp)s;
}
</script></code></pre>
</div>

Note:

- SLOW DOWN
- Ages come and pass, leaving memories that become legend. Legend fades to myth,
  and even myth is long forgotten when the Age that gave it birth comes again.
'''

def style(pos, filled):
  r = ''
  if not filled:
    r += 'style="dotted"'
  if pos == 0:
    r += ' sides="TBR"'
  elif pos == 15:
    r += ' sides="TB"'
  elif not filled:
    r += ' sides="TBR"'
  return r

def diagram(tc, tp, hc, hp):
  style_rules = {
      "tc" : tc,
      "tp" : tp,
      "hc" : hc,
      "hp" : hp,
  }

  if tp < hc:
    for i in range(0, tp):
      style_rules[str(i)] = style(i, False)
    for i in range(tp, hc+1):
      style_rules[str(i)] = style(i, True)
    for i in range(hc+1, 16):
      style_rules[str(i)] = style(i, False)
  else:
    for i in range(0, hc+1):
      style_rules[str(i)] = style(i, True)
    for i in range(hc+1, tp):
      style_rules[str(i)] = style(i, False)
    for i in range(tp, 16):
      style_rules[str(i)] = style(i, True)
  return slide_template % style_rules

def clip(p):
  p %= 16
  if p >= 15 or p == 0: p = 1
  return p

def gen_all():
  diagrams = []
  tc = 3
  tp = 5
  hc = 9
  hp = 11
  diagrams.append(diagram(tc, tp, hc, hp))
  for i in range(14):
    if random.choice([True, False]):
      hc = clip(hc + 1)
      hp = clip(hc + random.choice([2,3]))
      diagrams.append(diagram(tc, tp, hc, hp))
      tp = clip(tp + 1)
      tc = clip(tp - random.choice([2,3]))
      if tp == 1 or tp == 2: tc = 14  # avoid configurations that cause the diagram to jank
      diagrams.append(diagram(tc, tp, hc, hp))
    else:
      tp = clip(tp + 1)
      tc = clip(tp - random.choice([2,3]))
      if tp == 1 or tp == 2: tc = 14  # avoid configurations that cause the diagram to jank
      diagrams.append(diagram(tc, tp, hc, hp))
      hc = clip(hc + 1)
      hp = clip(hc + random.choice([2,3]))
      diagrams.append(diagram(tc, tp, hc, hp))
  diagrams.append(diagram(3, 5, 9, 11))
  return diagrams

def write_md(f):
  slides = gen_all()
  with open(f, "w") as file:
    file.write("\n-----\n".join(slides))

