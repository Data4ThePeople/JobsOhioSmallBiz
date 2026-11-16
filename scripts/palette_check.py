#!/usr/bin/env python3
"""Check a categorical palette for colour-vision separation, in OKLab.

The dataviz guidance this project follows says the colour question is
computable and must not be eyeballed, and ships a Node validator. There is no
Node on this machine, so the same checks are implemented here.

What it does, per pair of colours:
  * converts sRGB to OKLab
  * simulates deuteranopia, protanopia and tritanopia with the Brettel/
    Vienot-style LMS transforms
  * reports Delta E (OKLab distance, times 100) for normal vision and for each
    simulation

The thresholds the guidance sets: CVD Delta E of 8 or more is the target, 6 to
8 is a floor that is legal only with a second encoding such as shape or a
label, and a normal-vision Delta E below 15 is a hard failure because
full-colour readers cannot tell the pair apart either.

Also reports WCAG contrast against a given surface, for anything that carries
text or a thin outline.

**Categorical and sequential are different tests and must not be confused.**
The Delta E floors above are for categorical hues, which have to be told apart
as identities. A sequential ramp is built from deliberately small steps and
fails that test by design; the first run of this script reported a perfectly
good income ramp as four failures because it was asked the wrong question.
`--sequential` asks the right one: lightness has to move in one direction, the
steps have to be roughly even, and the two ends have to be far apart.

Usage: palette_check.py "#1F6F6B,#C8501E" [--surface "#fcfcfb"]
       palette_check.py "#EDF2F0,...,#1F6F6B" --sequential
"""
import sys


def hex_rgb(h):
    h = h.strip().lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def oklab(rgb):
    r, g, b = (lin(x) for x in rgb)
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


# LMS matrices and the dichromat projections
_TO = ((0.31399022, 0.63951294, 0.04649755),
       (0.15537241, 0.75789446, 0.08670142),
       (0.01775239, 0.10944209, 0.87256922))
_FROM = ((5.47221206, -4.6419601, 0.16963708),
         (-1.1252419, 2.29317094, -0.1678952),
         (0.02980165, -0.19318073, 1.16364789))
_SIM = {
    "deuteranopia": ((1, 0, 0), (0.9513092, 0, 0.04866992), (0, 0, 1)),
    "protanopia": ((0, 1.05118294, -0.05116099), (0, 1, 0), (0, 0, 1)),
    "tritanopia": ((1, 0, 0), (0, 1, 0), (-0.86744736, 1.86727089, 0)),
}


def mul(m, v):
    return tuple(sum(m[i][j] * v[j] for j in range(3)) for i in range(3))


def simulate(rgb, kind):
    v = tuple(lin(c) for c in rgb)
    out = mul(_FROM, mul(_SIM[kind], mul(_TO, v)))
    def unlin(c):
        c = max(0.0, min(1.0, c))
        return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
    return tuple(unlin(c) for c in out)


def de(a, b):
    la, lb = oklab(a), oklab(b)
    return 100 * sum((x - y) ** 2 for x, y in zip(la, lb)) ** 0.5


def relum(rgb):
    r, g, b = (lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = relum(a), relum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def sequential(cols, rgbs):
    """A ramp is good when lightness moves one way, the steps are even, and the
    ends are far apart. Adjacent steps being close is the point, not a fault."""
    ls = [oklab(r)[0] for r in rgbs]
    steps = [ls[i + 1] - ls[i] for i in range(len(ls) - 1)]
    mono = all(s > 0 for s in steps) or all(s < 0 for s in steps)
    span = 100 * abs(ls[-1] - ls[0])
    ev = max(abs(s) for s in steps) / max(1e-9, min(abs(s) for s in steps))
    print(f"{len(cols)} step ramp\n")
    for c, l in zip(cols, ls):
        print(f"  {c}  lightness {l*100:5.1f}")
    print(f"\n  lightness monotonic : {'yes' if mono else 'NO, the ramp reverses'}")
    print(f"  end to end span     : {span:5.1f}" +
          ("" if span >= 35 else "   WARN under 35, the ends will look alike"))
    print(f"  most uneven step    : {ev:5.2f}x" +
          ("" if ev <= 2.0 else "   WARN steps are lumpy, some bands will vanish"))
    worst = min(min(de(simulate(rgbs[i], k), simulate(rgbs[i + 1], k)) for k in _SIM)
                for i in range(len(rgbs) - 1))
    print(f"  worst adjacent step under colour blindness: {worst:4.1f}" +
          ("" if worst >= 3 else "   WARN adjacent bands merge"))
    ok = mono and span >= 35 and ev <= 2.0 and worst >= 3
    print("\n" + ("the ramp reads as an ordering" if ok else "the ramp needs work"))
    return 0 if ok else 1


def main(argv):
    cols = [c for c in argv[0].split(",") if c.strip()]
    if "--sequential" in argv:
        return sequential(cols, [hex_rgb(c) for c in cols])
    surface = "#fcfcfb"
    if "--surface" in argv:
        surface = argv[argv.index("--surface") + 1]
    rgbs = [hex_rgb(c) for c in cols]
    srgb = hex_rgb(surface)
    bad = []
    print(f"{len(cols)} colours against surface {surface}\n")
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            a, b = rgbs[i], rgbs[j]
            normal = de(a, b)
            sims = {k: de(simulate(a, k), simulate(b, k)) for k in _SIM}
            worst = min(sims.values())
            verdict = ("FAIL normal vision" if normal < 15 else
                       "FAIL cvd" if worst < 6 else
                       "needs a second encoding" if worst < 8 else "ok")
            if verdict != "ok":
                bad.append((cols[i], cols[j], verdict))
            print(f"  {cols[i]} vs {cols[j]}")
            print(f"    normal {normal:6.1f}   " +
                  "  ".join(f"{k[:5]} {v:5.1f}" for k, v in sims.items()) +
                  f"   -> {verdict}")
    print()
    for c, rgb in zip(cols, rgbs):
        r = contrast(rgb, srgb)
        print(f"  {c} on surface: contrast {r:.2f}" +
              ("" if r >= 3 else "   WARN below 3:1, needs a label or outline"))
    print("\n" + ("every pair separates" if not bad else
                  f"{len(bad)} pair(s) need work: " +
                  "; ".join(f"{a}/{b} {v}" for a, b, v in bad)))
    return 1 if any(v.startswith("FAIL") for *_, v in bad) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
