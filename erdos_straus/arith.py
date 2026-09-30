"""Integer arithmetic helpers: factorisation and divisor enumeration."""

from __future__ import annotations

from functools import lru_cache
from math import gcd, isqrt


def factorize(n: int) -> dict[int, int]:
    """Trial-division factorisation. Returns {prime: exponent}."""
    if n <= 0:
        raise ValueError("factorize expects a positive integer")
    factors: dict[int, int] = {}
    remaining = n
    while remaining % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        remaining //= 2
    p = 3
    limit = isqrt(remaining)
    while p <= limit:
        if remaining % p == 0:
            while remaining % p == 0:
                factors[p] = factors.get(p, 0) + 1
                remaining //= p
            limit = isqrt(remaining)
        p += 2
    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1
    return factors


@lru_cache(maxsize=65536)
def divisors(n: int) -> tuple[int, ...]:
    """Positive divisors of n, sorted."""
    if n <= 0:
        raise ValueError("divisors expects a positive integer")
    facts = factorize(n)
    divs = [1]
    for p, exp in facts.items():
        next_divs = []
        mul = 1
        for _ in range(exp + 1):
            next_divs.extend(d * mul for d in divs)
            mul *= p
        divs = next_divs
    return tuple(sorted(divs))


def _small_primes(limit: int) -> list[int]:
    """Primes p <= limit via an odd sieve."""
    if limit < 2:
        return []
    if limit < 3:
        return [2]
    n_odd = (limit - 1) // 2
    sieve = bytearray(b"\x01") * (n_odd + 1)
    for i in range((isqrt(limit) - 1) // 2 + 1):
        if not sieve[i]:
            continue
        p = 2 * i + 3
        start = (p * p - 3) // 2
        sieve[start::p] = b"\x00" * (((n_odd - start) // p) + 1)
    out = [2]
    out.extend(2 * i + 3 for i in range(n_odd + 1) if sieve[i])
    return out


def primes_in_class(start: int, stop: int, residue: int, modulus: int) -> list[int]:
    """Primes n in [start, stop) with n ≡ residue (mod modulus).

    Sieves the arithmetic progression. Used by the first-R scanner so
    large leftover-class ranges do not trial-divide every candidate.
    """
    if stop <= start or modulus < 2:
        return []
    residue %= modulus
    n0 = start + (residue - start % modulus) % modulus
    if n0 < start:
        n0 += modulus
    while n0 < 2:
        n0 += modulus
    if n0 >= stop:
        return []
    count = (stop - 1 - n0) // modulus + 1
    if count <= 0:
        return []
    # Tiny ranges: trial is cheaper than sieving to sqrt(stop).
    if count < 64:
        return [n0 + i * modulus for i in range(count) if is_prime(n0 + i * modulus)]

    mark = bytearray(b"\x01") * count
    lim = isqrt(stop - 1)
    for p in _small_primes(lim):
        # first index i with (n0 + i*mod) ≡ 0 (mod p)
        rem = n0 % p
        if rem == 0:
            first = 0
        else:
            # n0 + i*mod ≡ 0 (mod p) => i*mod ≡ -n0 (mod p)
            inv = pow(modulus % p, -1, p) if modulus % p else 0
            if inv == 0:
                # p | modulus. Then either every term or no term is 0 mod p.
                if rem == 0:
                    first = 0
                else:
                    continue
            else:
                first = ((p - rem) * inv) % p
        if first >= count:
            continue
        # Do not unmark the prime p itself.
        if n0 + first * modulus == p:
            first += p
        if first >= count:
            continue
        mark[first::p] = b"\x00" * (((count - 1 - first) // p) + 1)
    out: list[int] = []
    for i, ok in enumerate(mark):
        if ok:
            n = n0 + i * modulus
            if n >= 2:
                out.append(n)
    return out


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    if n % 3 == 0:
        return n == 3
    r = isqrt(n)
    f = 5
    while f <= r:
        if n % f == 0 or n % (f + 2) == 0:
            return False
        f += 6
    return True


def jacobi(a: int, n: int) -> int:
    """Jacobi symbol (a/n). n must be a positive odd integer."""
    if n <= 0 or n % 2 == 0:
        raise ValueError("Jacobi symbol requires a positive odd n")
    a = a % n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            n4 = n % 8
            if n4 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def quadratic_residues(mod: int) -> frozenset[int]:
    """Squares in 0..mod-1, including 0."""
    return frozenset((i * i) % mod for i in range(mod))


def lcm(a: int, b: int) -> int:
    return a // gcd(a, b) * b
