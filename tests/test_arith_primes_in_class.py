from erdos_straus.arith import is_prime, primes_in_class


def test_primes_in_class_matches_trial_on_tiny_529_range():
    start, stop, residue, modulus = 5569, 20000, 529, 840
    got = primes_in_class(start, stop, residue, modulus)
    n = start + (residue - start % modulus) % modulus
    if n < start:
        n += modulus
    want = []
    while n < stop:
        if is_prime(n):
            want.append(n)
        n += modulus
    assert got == want
    assert 5569 in got


def test_primes_in_class_empty_and_small():
    assert primes_in_class(10, 10, 529, 840) == []
    assert primes_in_class(8, 30, 1, 4) == [13, 17, 29]
