#!/usr/bin/env python3
"""Find polynomial Type I/II parameters for Mordell's mod-5 and mod-7 classes."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import sympy as sp

from erdos_straus.parametric import type_I, type_II
from erdos_straus.verifier import verify


def search_constant_ab_linear_e(mod: int, residue: int) -> None:
    t = sp.symbols("t", integer=True, nonnegative=True)
    n = mod * t + residue
    print(f"\n=== n = {mod}t+{residue} : constant a,b, polynomial e,d ===")
    # Try a,b small constants; e linear; require 4ab | n+e identically
    # i.e. n+e = 4ab * d(t) for a polynomial d.
    for a in range(1, 8):
        for b in range(a, 8):
            for e0 in range(0, 12):
                for e1 in range(0, 8):
                    e = e0 + e1 * t
                    if e == 0:
                        continue
                    # e | a+b for all t: e must be a constant divisor of a+b
                    if e1 != 0:
                        continue
                    if e0 == 0 or (a + b) % e0 != 0:
                        continue
                    expr = n + e
                    # Type II: 4ab | n+e
                    if (expr / (4 * a * b)).is_polynomial(t):
                        d = sp.simplify(expr / (4 * a * b))
                        if d.is_polynomial(t) and sp.Poly(sp.together(d), t).domain.is_ZZ:
                            # check positivity for t=0,1,2
                            ok = True
                            for tv in range(0, 6):
                                nv = int(n.subs(t, tv))
                                if nv < 2:
                                    continue
                                trip = type_II(nv, a, b, e0)
                                if trip is None or not verify(nv, trip.x, trip.y, trip.z):
                                    ok = False
                                    break
                            if ok:
                                print(f"  Type II a={a} b={b} e={e0}  d={d}")


def search_linear_params(mod: int, residue: int) -> None:
    """Assume a=a0+a1 t, etc., require the Type II equations identically."""
    t = sp.symbols("t", integer=True, nonnegative=True)
    n = mod * t + residue
    print(f"\n=== linear-parameter scan for n={mod}t+{residue} ===")
    # Keep it cheap: a constant, b linear, e constant dividing a+b(t) for all t
    # is impossible unless b is constant. So try a,b,e all linear with
    # a+b = e * c and c constant or linear, and 4ab divides n+e.
    hits = 0
    for a0 in range(1, 4):
        for a1 in range(0, 3):
            for b0 in range(1, 4):
                for b1 in range(0, 3):
                    for e0 in range(1, 6):
                        for e1 in range(0, 4):
                            a = a0 + a1 * t
                            b = b0 + b1 * t
                            e = e0 + e1 * t
                            s = sp.expand(a + b)
                            # e | a+b as polynomials: a+b = e * c
                            q, r = sp.div(s, e, t)
                            if r != 0:
                                continue
                            c = q
                            if c == 0:
                                continue
                            num = sp.expand(n + e)
                            den = sp.expand(4 * a * b)
                            q2, r2 = sp.div(num, den, t)
                            if r2 != 0:
                                continue
                            d = q2
                            # evaluate a few t
                            ok = True
                            for tv in range(0, 8):
                                av, bv, ev, dv, cv = (
                                    int(a.subs(t, tv)),
                                    int(b.subs(t, tv)),
                                    int(e.subs(t, tv)),
                                    int(d.subs(t, tv)),
                                    int(c.subs(t, tv)),
                                )
                                nv = int(n.subs(t, tv))
                                if min(av, bv, ev, dv, cv, nv) < 1:
                                    if nv < 2:
                                        continue
                                    ok = False
                                    break
                                x, y, z = av * bv * dv, av * cv * dv * nv, bv * cv * dv * nv
                                if not verify(nv, x, y, z):
                                    ok = False
                                    break
                            if ok:
                                print(f"  HIT Type II a={a} b={b} e={e} c={c} d={d}")
                                hits += 1
                                if hits >= 8:
                                    return
    if hits == 0:
        print("  no linear Type II hit")


def interpolate_from_solver(mod: int, residue: int, count: int = 10) -> None:
    from erdos_straus.solver import solve

    print(f"\n=== solver triples for n≡{residue} mod {mod} ===")
    xs, ys, zs, ts = [], [], [], []
    t = 0
    while len(ts) < count:
        n = mod * t + residue
        t += 1
        if n < 2:
            continue
        # skip those already covered by even / 3 mod 4 / 2 mod 3 / 5 mod 8
        if n % 2 == 0 or n % 4 == 3 or n % 3 == 2 or n % 8 == 5:
            continue
        sol = solve(n)
        if sol is None:
            print("  unsolved", n)
            continue
        trip = tuple(sorted((sol.x, sol.y, sol.z)))
        print(f"  t={(n-residue)//mod:3d} n={n:4d} {trip} via {sol.method}")
        ts.append((n - residue) // mod)
        xs.append(trip[0])
        ys.append(trip[1])
        zs.append(trip[2])
    # try to interpolate x as a polynomial in t of deg ≤ 2
    if len(ts) >= 4:
        tt = sp.symbols("t")
        for name, seq in (("x", xs), ("y", ys), ("z", zs)):
            try:
                poly = sp.interpolating_poly(3, tt, X=ts[:4], Y=seq[:4])
                poly = sp.simplify(sp.expand(poly))
                print(f"  interp deg≤2 {name}(t) = {poly}")
                # check remaining
                ok = all(int(poly.subs(tt, ts[i])) == seq[i] for i in range(len(ts)))
                print(f"    fits all samples: {ok}")
            except Exception as exc:
                print(f"  interp {name} failed: {exc}")


def main() -> None:
    for mod, res in [(5, 2), (5, 3), (7, 3), (7, 5), (7, 6)]:
        search_constant_ab_linear_e(mod, res)
        search_linear_params(mod, res)
        interpolate_from_solver(mod, res)


if __name__ == "__main__":
    main()
