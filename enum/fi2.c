/* Type I enumerator with the Opus turn-7 constraints:
 *   x = n * a * b * d
 *   a <= b, y = a*c*d, n/4 < y <= 2n/3
 *   gcd(a, c) = 1  (equivalent to gcd(a,b,c)=1 because b = c*e - a)
 * f_I(n) counts both (x,y,z) and (x,z,y) when a < b.
 *
 * Reconstructs the missing fi2 harvest binary from those reductions.
 * A matching census is a measurement, not a Mordell-class cover.
 *
 * Usage:
 *   ./fi2 N [n_lo n_hi] [--a-lo A] [--a-hi B] [--dump file.bin]
 *   ./fi2 --merge N dump1.bin dump2.bin ...
 *
 * --a-lo/--a-hi/--dump checkpoint an a-range shard (same count).
 * --merge adds dumps and prints the usual JSON. Not a redesign.
 */
#define _POSIX_C_SOURCE 200809L
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#ifdef _OPENMP
#include <omp.h>
#endif

static const int MORDELL[6] = {1, 121, 169, 289, 361, 529};

static int mordell_index(int r) {
    for (int i = 0; i < 6; i++)
        if (r == MORDELL[i])
            return i;
    return -1;
}

static uint64_t isqrt_u64(uint64_t n) {
    uint64_t x = (uint64_t)sqrt((double)n);
    while (x > 0 && x * x > n)
        x--;
    while (x < UINT64_MAX && (x + 1) * (x + 1) <= n)
        x++;
    return x;
}

static uint64_t gcd_u64(uint64_t a, uint64_t b) {
    while (b) {
        uint64_t t = a % b;
        a = b;
        b = t;
    }
    return a;
}

static uint64_t modinv_u64(uint64_t a, uint64_t m) {
    int64_t t = 0, newt = 1;
    int64_t r = (int64_t)m, newr = (int64_t)(a % m);
    while (newr != 0) {
        int64_t q = r / newr;
        int64_t tmp = newt;
        newt = t - q * newt;
        t = tmp;
        tmp = newr;
        newr = r - q * newr;
        r = tmp;
    }
    if (r > 1)
        return 0;
    if (t < 0)
        t += (int64_t)m;
    return (uint64_t)t;
}

static uint64_t cdiv_u64(uint64_t num, uint64_t den) {
    return (num + den - 1) / den;
}

static int *sieve_primes(uint64_t limit, int *out_n) {
    if (limit < 2) {
        *out_n = 0;
        return NULL;
    }
    uint8_t *mark = calloc(limit + 1, 1);
    if (!mark)
        return NULL;
    mark[0] = mark[1] = 1;
    uint64_t lim = isqrt_u64(limit);
    for (uint64_t i = 2; i <= lim; i++) {
        if (mark[i])
            continue;
        for (uint64_t j = i * i; j <= limit; j += i)
            mark[j] = 1;
    }
    int n = 0;
    for (uint64_t i = 2; i <= limit; i++)
        if (!mark[i])
            n++;
    int *pr = malloc((size_t)n * sizeof(int));
    if (!pr) {
        free(mark);
        return NULL;
    }
    int k = 0;
    for (uint64_t i = 2; i <= limit; i++)
        if (!mark[i])
            pr[k++] = (int)i;
    free(mark);
    *out_n = n;
    return pr;
}

static uint8_t *sieve_is_prime(uint64_t N) {
    uint8_t *ip = malloc((size_t)(N + 1));
    if (!ip)
        return NULL;
    memset(ip, 1, (size_t)(N + 1));
    ip[0] = ip[1] = 0;
    uint64_t lim = isqrt_u64(N);
    for (uint64_t i = 2; i <= lim; i++) {
        if (!ip[i])
            continue;
        for (uint64_t j = i * i; j <= N; j += i)
            ip[j] = 0;
    }
    return ip;
}

#define MAX_PF 16
#define MAX_DIV 4096

static int build_divisors(const uint64_t *pf, const int *pe, int np, uint64_t *divs) {
    int nd = 1;
    divs[0] = 1;
    for (int i = 0; i < np; i++) {
        int base = nd;
        uint64_t mul = 1;
        for (int e = 1; e <= pe[i]; e++) {
            mul *= pf[i];
            for (int j = 0; j < base; j++) {
                if (nd >= MAX_DIV)
                    return -1;
                divs[nd++] = divs[j] * mul;
            }
        }
    }
    return nd;
}

static uint64_t mulmod_u64(uint64_t a, uint64_t b, uint64_t m) {
    return (uint64_t)(((__uint128_t)a * b) % m);
}

static uint64_t modpow_u64(uint64_t a, uint64_t e, uint64_t m) {
    uint64_t r = 1;
    a %= m;
    while (e) {
        if (e & 1)
            r = mulmod_u64(r, a, m);
        a = mulmod_u64(a, a, m);
        e >>= 1;
    }
    return r;
}

/* Deterministic Miller–Rabin for all 64-bit n (witnesses 2,3,5,7,11,13,23). */
static int is_prime_u64(uint64_t n) {
    if (n < 2)
        return 0;
    if ((n & 1ull) == 0)
        return n == 2;
    static const uint64_t small[] = {3, 5, 7, 11, 13, 17, 19, 23, 0};
    for (int i = 0; small[i]; i++) {
        if (n == small[i])
            return 1;
        if (n % small[i] == 0)
            return 0;
    }
    uint64_t d = n - 1;
    int s = 0;
    while ((d & 1ull) == 0) {
        d >>= 1;
        s++;
    }
    static const uint64_t W[] = {2, 3, 5, 7, 11, 13, 23, 0};
    for (int i = 0; W[i]; i++) {
        uint64_t a = W[i];
        if (a >= n)
            continue;
        uint64_t x = modpow_u64(a, d, n);
        if (x == 1 || x == n - 1)
            continue;
        int ok = 0;
        for (int r = 1; r < s; r++) {
            x = mulmod_u64(x, x, n);
            if (x == n - 1) {
                ok = 1;
                break;
            }
        }
        if (!ok)
            return 0;
    }
    return 1;
}

static uint64_t pollard_rho(uint64_t n) {
    if ((n & 1ull) == 0)
        return 2;
    for (uint64_t c = 1; c < 64; c++) {
        uint64_t x = 2, y = 2, d = 1;
        uint64_t steps = 0;
        while (d == 1 && steps < (1ull << 18)) {
            x = (mulmod_u64(x, x, n) + c) % n;
            y = (mulmod_u64(y, y, n) + c) % n;
            y = (mulmod_u64(y, y, n) + c) % n;
            uint64_t diff = x > y ? x - y : y - x;
            d = gcd_u64(diff, n);
            if (d == n)
                break;
            steps++;
        }
        if (d > 1 && d < n)
            return d;
    }
    return n;
}

static void add_prime_power(uint64_t p, int e, uint64_t *pf, int *pe, int *np) {
    for (int i = 0; i < *np; i++) {
        if (pf[i] == p) {
            pe[i] += e;
            return;
        }
    }
    pf[*np] = p;
    pe[*np] = e;
    (*np)++;
}

static int factor_trial(uint64_t n, uint64_t *pf, int *pe, const int *primes, int npr) {
    int np = 0;
    for (int i = 0; i < npr; i++) {
        uint64_t p = (uint64_t)primes[i];
        if (p > 4000ull)
            break;
        if (p * p > n)
            break;
        if (n % p)
            continue;
        int e = 0;
        while (n % p == 0) {
            n /= p;
            e++;
        }
        add_prime_power(p, e, pf, pe, &np);
    }
    /* Trial to 4000 proves primality below 16e6. MR handles the rest. */
    if (n > 1 && (n < 4000ull * 4000ull || is_prime_u64(n))) {
        add_prime_power(n, 1, pf, pe, &np);
        n = 1;
    }
    uint64_t stack[32];
    int ns = 0;
    if (n > 1)
        stack[ns++] = n;
    while (ns) {
        uint64_t m = stack[--ns];
        if (m < 2)
            continue;
        if (m < 4000ull * 4000ull || is_prime_u64(m)) {
            add_prime_power(m, 1, pf, pe, &np);
            continue;
        }
        uint64_t r = isqrt_u64(m);
        if (r * r == m) {
            stack[ns++] = r;
            stack[ns++] = r;
            continue;
        }
        uint64_t f = pollard_rho(m);
        if (f == m || f == 0) {
            add_prime_power(m, 1, pf, pe, &np);
        } else {
            stack[ns++] = f;
            stack[ns++] = m / f;
        }
    }
    return np;
}

static void apply_divisors(uint64_t a, uint64_t d, uint64_t F, const uint64_t *divs, int nd,
                           uint64_t nlo, uint64_t nhi, uint64_t M, uint32_t *acc) {
    uint64_t ad = a * d;
    if (ad == 0)
        return;
    for (int j = 0; j < nd; j++) {
        uint64_t f = divs[j];
        if (f == 0 || F % f)
            continue;
        uint64_t e = F / f;
        /* n = 4*a*c*d - f ∈ [nlo, nhi] */
        uint64_t cmin = 1;
        uint64_t tmp;
        tmp = cdiv_u64(nlo + f, 4 * ad);
        if (tmp > cmin)
            cmin = tmp;
        tmp = cdiv_u64(2 * a, e); /* a <= b  <=>  2a <= c*e */
        if (tmp > cmin)
            cmin = tmp;
        tmp = cdiv_u64(2 * f, 5 * ad); /* y <= 2n/3  <=>  f <= (5/2) a c d */
        if (tmp > cmin)
            cmin = tmp;
        uint64_t cmax = (nhi + f) / (4 * ad);
        tmp = M / ad;
        if (tmp < cmax)
            cmax = tmp;
        if (cmin < 1)
            cmin = 1;
        if (cmin > cmax)
            continue;
        if (a == 1) {
            for (uint64_t c = cmin; c <= cmax; c++) {
                uint64_t n = 4 * ad * c - f;
                uint32_t delta = (2 * a == c * e) ? 1u : 2u;
                acc[n] += delta;
            }
        } else {
            for (uint64_t c = cmin; c <= cmax; c++) {
                if (gcd_u64(a, c) != 1)
                    continue;
                uint64_t n = 4 * ad * c - f;
                uint32_t delta = (2 * a == c * e) ? 1u : 2u;
                acc[n] += delta;
            }
        }
    }
}

static int write_dump(const char *path, uint64_t N, uint64_t alo, uint64_t ahi, const uint32_t *fi) {
    FILE *fp = fopen(path, "wb");
    if (!fp) {
        perror(path);
        return 1;
    }
    char mag[4] = {'F', 'I', '2', 'A'};
    if (fwrite(mag, 1, 4, fp) != 4 || fwrite(&N, sizeof N, 1, fp) != 1 ||
        fwrite(&alo, sizeof alo, 1, fp) != 1 || fwrite(&ahi, sizeof ahi, 1, fp) != 1 ||
        fwrite(fi, sizeof(uint32_t), (size_t)(N + 1), fp) != (size_t)(N + 1)) {
        fprintf(stderr, "write dump failed: %s\n", path);
        fclose(fp);
        return 1;
    }
    fclose(fp);
    return 0;
}

static int load_dump(const char *path, uint64_t N, uint32_t *fi) {
    FILE *fp = fopen(path, "rb");
    if (!fp) {
        perror(path);
        return 1;
    }
    char mag[4];
    uint64_t n2, alo, ahi;
    if (fread(mag, 1, 4, fp) != 4 || mag[0] != 'F' || mag[1] != 'I' || mag[2] != '2' ||
        mag[3] != 'A' || fread(&n2, sizeof n2, 1, fp) != 1 || n2 != N ||
        fread(&alo, sizeof alo, 1, fp) != 1 || fread(&ahi, sizeof ahi, 1, fp) != 1) {
        fprintf(stderr, "bad dump header: %s\n", path);
        fclose(fp);
        return 1;
    }
    uint32_t *buf = malloc((size_t)(N + 1) * sizeof(uint32_t));
    if (!buf) {
        fclose(fp);
        return 1;
    }
    if (fread(buf, sizeof(uint32_t), (size_t)(N + 1), fp) != (size_t)(N + 1)) {
        fprintf(stderr, "short dump: %s\n", path);
        free(buf);
        fclose(fp);
        return 1;
    }
    fclose(fp);
    for (uint64_t i = 0; i <= N; i++)
        fi[i] += buf[i];
    free(buf);
    fprintf(stderr, "loaded %s a=[%llu,%llu]\n", path, (unsigned long long)alo,
            (unsigned long long)ahi);
    return 0;
}

int main(int argc, char **argv) {
    setvbuf(stderr, NULL, _IONBF, 0);
    if (argc < 2) {
        fprintf(stderr, "usage: %s N [n_lo n_hi] [--a-lo A --a-hi B] [--dump file]\n", argv[0]);
        fprintf(stderr, "       %s --merge N dump1.bin dump2.bin ...\n", argv[0]);
        return 2;
    }

    int merge_mode = 0;
    uint64_t N = 0, nlo = 2, nhi = 0;
    uint64_t alo = 1, ahi = 0;
    const char *dump_path = NULL;
    const char *merge_files[64];
    int nmerge = 0;
    int pos = 0;

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--merge") == 0) {
            merge_mode = 1;
        } else if (strcmp(argv[i], "--a-lo") == 0 && i + 1 < argc) {
            alo = strtoull(argv[++i], NULL, 10);
        } else if (strcmp(argv[i], "--a-hi") == 0 && i + 1 < argc) {
            ahi = strtoull(argv[++i], NULL, 10);
        } else if (strcmp(argv[i], "--dump") == 0 && i + 1 < argc) {
            dump_path = argv[++i];
        } else if (merge_mode && pos >= 1) {
            if (nmerge >= 64) {
                fprintf(stderr, "too many dumps\n");
                return 2;
            }
            merge_files[nmerge++] = argv[i];
        } else {
            if (pos == 0)
                N = strtoull(argv[i], NULL, 10);
            else if (pos == 1)
                nlo = strtoull(argv[i], NULL, 10);
            else if (pos == 2)
                nhi = strtoull(argv[i], NULL, 10);
            else {
                fprintf(stderr, "unexpected arg %s\n", argv[i]);
                return 2;
            }
            pos++;
        }
    }

    if (N < 2) {
        fprintf(stderr, "N must be >= 2\n");
        return 2;
    }
    if (nhi == 0)
        nhi = N;
    if (nlo < 2)
        nlo = 2;
    if (nhi > N)
        nhi = N;
    if (nlo > nhi) {
        fprintf(stderr, "empty range\n");
        return 2;
    }

    uint64_t M = (2 * N) / 3;
    if (ahi == 0 || ahi > M)
        ahi = M;
    if (alo < 1)
        alo = 1;
    if (alo > ahi && !merge_mode) {
        fprintf(stderr, "empty a-range\n");
        return 2;
    }
    uint64_t maxF = 4 * M * M + 1;
    uint64_t primelimit = isqrt_u64(maxF) + 2;
    if (primelimit < 3)
        primelimit = 3;

    fprintf(stderr, "fi2 N=%llu range=[%llu,%llu] a=[%llu,%llu] M=%llu primelimit=%llu%s\n",
            (unsigned long long)N, (unsigned long long)nlo, (unsigned long long)nhi,
            (unsigned long long)alo, (unsigned long long)ahi, (unsigned long long)M,
            (unsigned long long)primelimit, merge_mode ? " merge" : "");

    int npr = 0;
    int *primes = sieve_primes(primelimit, &npr);
    if (!primes) {
        fprintf(stderr, "prime sieve failed\n");
        return 1;
    }
    uint8_t *is_prime = sieve_is_prime(N);
    if (!is_prime) {
        fprintf(stderr, "is_prime sieve failed\n");
        return 1;
    }
    uint32_t *fi = calloc((size_t)(N + 1), sizeof(uint32_t));
    if (!fi) {
        fprintf(stderr, "fi[] alloc failed\n");
        return 1;
    }

    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

#ifdef _OPENMP
#pragma omp parallel
#endif
    {
        uint32_t *acc = fi;
#ifdef _OPENMP
        acc = calloc((size_t)(N + 1), sizeof(uint32_t));
        if (!acc) {
            fprintf(stderr, "thread-local fi alloc failed\n");
        } else
#endif
        if (merge_mode) {
            /* skip the a-loop; dumps are loaded below */
        } else
#ifdef _OPENMP
#pragma omp for schedule(dynamic, 1)
#endif
        for (uint64_t a = alo; a <= ahi; a++) {
        uint64_t Dmax = M / a;
        uint64_t step = 4 * a * a;
        uint64_t pf[MAX_PF];
        int pe[MAX_PF];
        uint64_t divs[MAX_DIV];
        const uint64_t BLOCK = 65536;

        if (Dmax < 256) {
            for (uint64_t d = 1; d <= Dmax; d++) {
                uint64_t F = step * d + 1;
                int np = factor_trial(F, pf, pe, primes, npr);
                int nd = build_divisors(pf, pe, np, divs);
                if (nd < 0)
                    continue;
                apply_divisors(a, d, F, divs, nd, nlo, nhi, M, acc);
            }
        } else {
            uint64_t *val = malloc((size_t)BLOCK * sizeof(uint64_t));
            uint8_t *nfac = malloc((size_t)BLOCK);
            uint64_t *spf = malloc((size_t)BLOCK * MAX_PF * sizeof(uint64_t));
            int *spe = malloc((size_t)BLOCK * MAX_PF * sizeof(int));
            if (!val || !nfac || !spf || !spe) {
                free(val);
                free(nfac);
                free(spf);
                free(spe);
                continue;
            }
            for (uint64_t d0 = 1; d0 <= Dmax; d0 += BLOCK) {
                uint64_t d1 = d0 + BLOCK - 1;
                if (d1 > Dmax)
                    d1 = Dmax;
                uint64_t blen = d1 - d0 + 1;
                uint64_t maxFb = step * d1 + 1;
                uint64_t lim = isqrt_u64(maxFb);
                for (uint64_t i = 0; i < blen; i++) {
                    val[i] = step * (d0 + i) + 1;
                    nfac[i] = 0;
                }
                for (int ip = 0; ip < npr; ip++) {
                    uint64_t p = (uint64_t)primes[ip];
                    if (p > lim)
                        break;
                    if (step % p == 0)
                        continue;
                    uint64_t inv = modinv_u64(step % p, p);
                    if (inv == 0)
                        continue;
                    uint64_t dfirst = (p - inv) % p;
                    if (dfirst == 0)
                        dfirst = p;
                    if (dfirst < d0) {
                        uint64_t k = (d0 - dfirst + p - 1) / p;
                        dfirst += k * p;
                    }
                    for (uint64_t d = dfirst; d <= d1; d += p) {
                        uint64_t i = d - d0;
                        if (val[i] % p)
                            continue;
                        int k = nfac[i];
                        if (k >= MAX_PF)
                            continue;
                        int e = 0;
                        while (val[i] % p == 0) {
                            val[i] /= p;
                            e++;
                        }
                        spf[i * MAX_PF + k] = p;
                        spe[i * MAX_PF + k] = e;
                        nfac[i] = (uint8_t)(k + 1);
                    }
                }
                for (uint64_t i = 0; i < blen; i++) {
                    if (val[i] > 1 && nfac[i] < MAX_PF) {
                        spf[i * MAX_PF + nfac[i]] = val[i];
                        spe[i * MAX_PF + nfac[i]] = 1;
                        nfac[i]++;
                    }
                    int nd = build_divisors(&spf[i * MAX_PF], &spe[i * MAX_PF], nfac[i], divs);
                    if (nd < 0)
                        continue;
                    uint64_t F = step * (d0 + i) + 1;
                    apply_divisors(a, d0 + i, F, divs, nd, nlo, nhi, M, acc);
                }
            }
            free(val);
            free(nfac);
            free(spf);
            free(spe);
        }
        if (a == alo || ((a - alo) & 4095ull) == 0)
            fprintf(stderr, "a=%llu / %llu (shard %llu..%llu)\n", (unsigned long long)a,
                    (unsigned long long)M, (unsigned long long)alo, (unsigned long long)ahi);
        }
#ifdef _OPENMP
        if (acc && acc != fi) {
#pragma omp critical
            {
                for (uint64_t n = nlo; n <= nhi; n++)
                    fi[n] += acc[n];
            }
            free(acc);
        }
#endif
    }

    if (merge_mode) {
        for (int i = 0; i < nmerge; i++) {
            if (load_dump(merge_files[i], N, fi))
                return 1;
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &t1);
    double secs = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9;

    if (dump_path) {
        if (write_dump(dump_path, N, alo, ahi, fi))
            return 1;
        fprintf(stderr, "wrote %s\n", dump_path);
    }

    unsigned long long sum_n = 0, sum_p = 0;
    int nprimes = 0;
    struct {
        int r, primes, hits, misses, min_f, max_f;
    } mc[6];
    for (int i = 0; i < 6; i++) {
        mc[i].r = MORDELL[i];
        mc[i].primes = mc[i].hits = mc[i].misses = 0;
        mc[i].min_f = 1 << 30;
        mc[i].max_f = 0;
    }

    for (uint64_t n = nlo; n <= nhi; n++) {
        uint32_t v = fi[n];
        sum_n += v;
        if (!is_prime[n])
            continue;
        nprimes++;
        sum_p += v;
        int idx = mordell_index((int)(n % 840));
        if (idx < 0)
            continue;
        mc[idx].primes++;
        if (v > 0) {
            mc[idx].hits++;
            if ((int)v < mc[idx].min_f)
                mc[idx].min_f = (int)v;
            if ((int)v > mc[idx].max_f)
                mc[idx].max_f = (int)v;
        } else {
            mc[idx].misses++;
        }
    }

    printf("{\n");
    printf("  \"N\": %llu,\n", (unsigned long long)N);
    printf("  \"n_lo\": %llu,\n", (unsigned long long)nlo);
    printf("  \"n_hi\": %llu,\n", (unsigned long long)nhi);
    printf("  \"runtime_seconds\": %.3f,\n", secs);
    printf("  \"sums\": {\"f_I_n\": %llu, \"f_I_p\": %llu, \"primes\": %d},\n", sum_n, sum_p,
           nprimes);
    printf("  \"mordell_primes\": {\n");
    printf("    \"zero_misses_is_not_a_cover\": true,\n");
    printf("    \"classes\": [\n");
    int tot_p = 0, tot_h = 0, tot_m = 0;
    for (int i = 0; i < 6; i++) {
        if (mc[i].hits == 0)
            mc[i].min_f = 0;
        tot_p += mc[i].primes;
        tot_h += mc[i].hits;
        tot_m += mc[i].misses;
        printf("      {\"residue_mod_840\": %d, \"primes\": %d, \"hits\": %d, \"misses\": %d, "
               "\"min_f_I\": %d, \"max_f_I\": %d}%s\n",
               mc[i].r, mc[i].primes, mc[i].hits, mc[i].misses, mc[i].min_f, mc[i].max_f,
               i == 5 ? "" : ",");
    }
    printf("    ],\n");
    printf("    \"totals\": {\"primes\": %d, \"hits\": %d, \"misses\": %d}\n", tot_p, tot_h, tot_m);
    printf("  },\n");
    printf("  \"constraints\": {\"y_max\": \"2n/3\", \"x\": \"n*a*b*d\", \"a_le_b\": true, "
           "\"primitive_ac\": true},\n");
    printf("  \"esc_proved\": false,\n");
    printf("  \"cover_claimed\": false\n");
    printf("}\n");

    if (N >= 3049 && nlo <= 3049 && nhi >= 3049)
        fprintf(stderr, "f_I(3049)=%u (want 30)\n", fi[3049]);
    if (N >= 2521 && nlo <= 2521 && nhi >= 2521)
        fprintf(stderr, "f_I(2521)=%u (want 12)\n", fi[2521]);
    if (N >= 1009 && nlo <= 1009 && nhi >= 1009)
        fprintf(stderr, "f_I(1009)=%u (want 22)\n", fi[1009]);

    free(fi);
    free(is_prime);
    free(primes);
    return 0;
}
