#!/usr/bin/env python3
"""Reference Type I counter matching the Opus fi2 checksums.

f_I(n) = number of ordered Type I triples (x,y,z) with x = n*a*b*d,
i.e. twice the number of primitive (gcd(a,b,c)=1) solutions with a ≤ b
and n/4 < acd ≤ 2n/3 (min(y,z) ≤ 2n/3). a=b contributes 1.

Do not use this for the 1e8 harvest; it is the correctness oracle.
"""

from __future__ import annotations

from math import gcd


def _divisors(m: int) -> list[int]:
    ds: list[int] = []
    i = 1
    while i * i <= m:
        if m % i == 0:
            ds.append(i)
            if i * i != m:
                ds.append(m // i)
        i += 1
    return ds


def f_I(n: int) -> int:
    """Canonical f_I(n) used by the 1e6/1e7 harvest."""
    if n < 2:
        return 0
    lo = n // 4 + 1
    hi = (2 * n) // 3
    count = 0
    seen: set[tuple[int, int, int]] = set()
    for y in range(lo, hi + 1):
        f = 4 * y - n
        if f <= 0:
            continue
        for a in _divisors(y):
            y1 = y // a
            for c in _divisors(y1):
                d = y1 // c
                F = 4 * a * a * d + 1
                if F % f:
                    continue
                e = F // f
                if e < 1 or (n * a + c) % f:
                    continue
                b = (n * a + c) // f
                if b < 1 or a > b:
                    continue
                if a + b != c * e:
                    continue
                if gcd(gcd(a, b), c) != 1:
                    continue
                x = a * b * d * n
                z = b * c * d
                key = (x, y, z)
                if key in seen:
                    continue
                seen.add(key)
                count += 1 if a == b else 2
    return count


if __name__ == "__main__":
    assert f_I(3049) == 30
    assert f_I(2521) == 12
    assert f_I(1009) == 22
    assert f_I(1801) == 24
    assert f_I(1129) == 28
    assert f_I(1201) == 14
    print("reference checksums ok")
