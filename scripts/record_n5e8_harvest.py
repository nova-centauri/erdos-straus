#!/usr/bin/env python3
"""Write notes/tests from a finished N=5e8 Type I merge. Not a cover."""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "data" / "typeI_mordell_5e8.json"
PARTIAL = ROOT / "data" / "typeI_partial"
MINS = {1: 12, 121: 24, 169: 22, 289: 28, 361: 14, 529: 30}
PI = 26_355_867


def ratio(p: int) -> float:
    n = 500_000_000
    return p / (n * (math.log(n) ** 2))


def load() -> dict:
    data = json.loads(JSON_PATH.read_text())
    assert data["N"] == 500_000_000
    assert data["cover_claimed"] is False
    assert data["esc_proved"] is False
    assert data["mordell_primes"]["zero_misses_is_not_a_cover"] is True
    assert data["sums"]["primes"] == PI
    mins = {c["residue_mod_840"]: c["min_f_I"] for c in data["mordell_primes"]["classes"]}
    assert mins == MINS, mins
    assert data["mordell_primes"]["totals"]["misses"] == 0
    assert data["mordell_primes"]["totals"]["hits"] == data["mordell_primes"]["totals"]["primes"]
    return data


def shard_rows() -> list[tuple[str, int, int, int, float]]:
    rows = []
    for line in (ROOT / "enum" / "n5e8_shards.tsv").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        name, lo, hi = line.split()
        js = PARTIAL / f"{name}.json"
        sum_n = -1
        secs = -1.0
        if js.is_file():
            d = json.loads(js.read_text())
            sum_n = int(d["sums"]["f_I_n"])
            secs = float(d["runtime_seconds"])
        rows.append((name, int(lo), int(hi), sum_n, secs))
    return rows


def write_harvest(data: dict) -> None:
    p = data["sums"]["f_I_p"]
    nsum = data["sums"]["f_I_n"]
    r = ratio(p)
    classes = data["mordell_primes"]["classes"]
    tot = data["mordell_primes"]["totals"]
    nshards = len(shard_rows())
    lines = [
        "# Type I enumerator harvest at \(N = 5\\times 10^8\) (wave 6)",
        "",
        "Source: same reconstructed `enum/fi2.c` as the \(10^6\)–\(2\\times 10^8\)",
        "harvests, 2026-09-07. Checkpointed as a-range dumps and merged.",
        "Same turn-7 constraints. Structured copy:",
        "`data/typeI_mordell_5e8.json`.",
        "",
        "This is a **measurement**. ESC is unproved. Zero Type I misses among",
        "Mordell primes \(p \\le 5\\times 10^8\) is **not** a full-class cover.",
        "Elsholtz–Tao Prop. 1.6 still forbids a Type I/II cover of the full",
        "classes \(n \\equiv 169\) or \(529 \\pmod{840}\).",
        "",
        "Do **not** rerun \(10^6\), \(10^7\), \(2\\times 10^7\), \(5\\times 10^7\),",
        "\(10^8\), \(2\\times 10^8\), or this \(5\\times 10^8\) bound.",
        "",
        "## Totals",
        "",
        "| bound | \(\\sum_n f_I(n)\) | \(\\sum_p f_I(p)\) | observed \(P/(N\\ln^2 N)\) |",
        "| --- | ---: | ---: | ---: |",
        "| \(N=10^6\) | 165374532 | 34276274 | — |",
        "| \(N=10^7\) | 2559629008 | 454495120 | 0.17495 |",
        "| \(N=2\\times 10^7\) | 5772274472 | 982580024 | 0.17384 |",
        "| \(N=5\\times 10^7\) | 16795310188 | 2709141549 | 0.17241 |",
        "| \(N=10^8\) | 37494215304 | 5818322818 | 0.17147 |",
        "| \(N=2\\times 10^8\) | 83381351012 | 12463112814 | 0.17057 |",
        f"| \(N=5\\times 10^8\) | {nsum} | {p} | {r:.5f} |",
        "",
        "The ratio column is \(P/(N\\ln^2 N)\) with \(N\) the bound (same",
        "convention as the \(10^7\)–\(2\\times 10^8\) tables). Checksums on",
        "the merge: \(f_I(3049)=30\), \(f_I(2521)=12\), \(f_I(1009)=22\).",
        f"\\(\\pi(5\\times 10^8)={PI}\\). Shard \(\\sum_n\) / \(\\sum_p\) add to",
        "the merge totals exactly.",
        "",
        "## Mordell primes \(p \\le 5\\times 10^8\)",
        "",
        "Every prime in each leftover class had \(f_I(p) > 0\) (zero misses).",
        "",
        "| residue mod 840 | #primes | hits | misses | min \(f_I\) | max \(f_I\) |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for c in classes:
        lines.append(
            f"| {c['residue_mod_840']} | {c['primes']} | {c['hits']} | {c['misses']} | "
            f"{c['min_f_I']} | {c['max_f_I']} |"
        )
    lines.append(
        f"| **total** | **{tot['primes']}** | **{tot['hits']}** | **{tot['misses']}** | | |"
    )
    lines += [
        "",
        "Class minima are unchanged from \(10^7\) (still realised at the small",
        "checksum primes: \(f_I(2521)=12\), \(f_I(1801)=24\), \(f_I(1009)=22\),",
        "\(f_I(1129)=28\), \(f_I(1201)=14\), \(f_I(3049)=30\)).",
        "",
        "## How it was run",
        "",
        "`Dmax = M/a` with \(M=2N/3=333333333\), so \(a\) runs through \(M\).",
        f"{nshards} a-range dumps (gitignored under `data/typeI_partial/`) cover",
        "\([1,M]\) with no gaps. List: `enum/n5e8_shards.tsv`.",
        "",
        "| shard | \(a\)-range | shard \(\\sum_n f_I\) | shard seconds |",
        "| ---: | --- | ---: | ---: |",
    ]
    for name, lo, hi, sum_n, secs in shard_rows():
        sn = str(sum_n) if sum_n >= 0 else "?"
        sc = f"{secs:.0f}" if secs >= 0 else "?"
        lines.append(f"| {name} | {lo}–{hi} | {sn} | {sc} |")
    lines += [
        "",
        "```bash",
        "scripts/merge_n5e8.sh",
        "```",
        "",
        "Same factoring path as the \(2\\times 10^8\) harvest (trial to",
        "\(p\\le 4000\), then Miller–Rabin / Pollard). Not an enumerator rebuild.",
        "",
        "## What this wave did not do",
        "",
        "- Did not invent a covering family.",
        "- Did not claim a Mordell-class cover.",
        "- Did not rerun any finished smaller bound.",
        "",
    ]
    (ROOT / "notes" / "HARVEST-5e8.md").write_text("\n".join(lines))


def write_partial_done() -> None:
    (ROOT / "notes" / "HARVEST-partial-5e8.md").write_text(
        """# Type I census toward \(5\\times 10^8\) — complete (wave 6)

The \(N=5\\times 10^8\) harvest is **done**. See `notes/HARVEST-5e8.md` and
`data/typeI_mordell_5e8.json`.

Do **not** rerun \(N=10^6\), \(10^7\), \(2\\times 10^7\),
\(5\\times 10^7\), \(10^8\), \(2\\times 10^8\), or \(5\\times 10^8\).

Pickup if someone still has the gitignored dumps:

```bash
scripts/merge_n5e8.sh
```

Zero misses through \(5\\times 10^8\) stay a measurement, not a cover.
"""
    )


def write_next(data: dict) -> None:
    (ROOT / "notes" / "NEXT.md").write_text(
        f"""# Next leftover spend

The Type I harvest at \(N = 5\\times 10^8\) is **done**. Do **not**
rerun \(10^6\), \(10^7\), \(2\\times 10^7\), \(5\\times 10^7\),
\(10^8\), \(2\\times 10^8\), or \(5\\times 10^8\).

The 529 first-R scan through \(8.00\\times 10^9\) is **done**
(no first-R \(\\ge 108\); max 83 at \(3434195209\)). Continue from
\(8.00\\times 10^9\) if you want more scan, not a cover.

Optional leftover burns (none of these is a cover):

1. Continue `scripts/scan_first_r.py` from \(8.00\\times 10^9\).
   Checkpoint slices under `data/first_r_slices/`.
2. Same `enum/fi2` at a **larger** complete bound, a-range dumps +
   merge. Checkpoint hard. Do not rebuild `fi2`.

**Do not do this:** rebuild `fi2`; invent a covering family; claim a
Type I/II full-class cover; try to prove ESC; reopen
`notes/CLOSED.md`; spend a fresh Anthropic week; use Fable; rerun
any finished Type I bound.

## Recorded complete totals (do not harvest again)

| \(N\) | \(\\sum_n f_I\) | \(\\sum_p f_I\) |
| ---: | ---: | ---: |
| \(10^6\) | 165374532 | 34276274 |
| \(10^7\) | 2559629008 | 454495120 |
| \(2\\times 10^7\) | 5772274472 | 982580024 |
| \(5\\times 10^7\) | 16795310188 | 2709141549 |
| \(10^8\) | 37494215304 | 5818322818 |
| \(2\\times 10^8\) | 83381351012 | 12463112814 |
| \(5\\times 10^8\) | {data['sums']['f_I_n']} | {data['sums']['f_I_p']} |

Keep \(y\\le 2n/3\), \(x=n\\cdot a\\cdot b\\cdot d\), \(a\\le b\),
\\(\\gcd(a,c)=1\\).
"""
    )


def patch_closed(data: dict) -> None:
    path = ROOT / "notes" / "CLOSED.md"
    text = path.read_text()
    marker = "## Type I harvest at `5×10⁸` is measurement, not a cover (wave 6)"
    if marker in text:
        return
    p = data["sums"]["f_I_p"]
    block = f"""
## Type I harvest at `5×10⁸` is measurement, not a cover (wave 6)

Same `enum/fi2`, checkpointed a-range merge. Full table:
`notes/HARVEST-5e8.md`, `data/typeI_mordell_5e8.json`.

- `Σ_{{n≤5×10⁸}} f_I(n) = {data["sums"]["f_I_n"]}`
- `Σ_{{p≤5×10⁸}} f_I(p) = {p}`
- observed `P/(N ln² N) = {ratio(p):.5f}` (was 0.17057 at `2×10⁸`)
- All **{data["mordell_primes"]["totals"]["primes"]}** Mordell primes `p ≤ 5×10⁸` had `f_I(p) > 0` (zero misses)
- Checksums: `f_I(3049)=30`, `f_I(2521)=12`, `f_I(1009)=22`

**Zero Type I misses through 5×10⁸ is not a full-class cover.**
Do not harvest `5×10⁸` again. Next leftover spend is `notes/NEXT.md`.

"""
    text = text.replace(
        "**Zero Type I misses through 2×10⁸ is not a full-class cover.**\n"
        "Do not harvest `2×10⁸` again. Next leftover spend is `notes/NEXT.md`.\n",
        "**Zero Type I misses through 2×10⁸ is not a full-class cover.**\n"
        "Do not harvest `2×10⁸` again.\n"
        + block,
    )
    path.write_text(text)


def patch_test(data: dict) -> None:
    path = ROOT / "tests" / "test_typeI_harvest.py"
    text = path.read_text()
    if "HARVEST_5E8" not in text:
        text = text.replace(
            'HARVEST_2E8 = REPO / "data" / "typeI_mordell_2e8.json"\n',
            'HARVEST_2E8 = REPO / "data" / "typeI_mordell_2e8.json"\n'
            'HARVEST_5E8 = REPO / "data" / "typeI_mordell_5e8.json"\n',
        )
    tot = data["mordell_primes"]["totals"]
    fn = f"""


def test_typeI_5e8_harvest_is_measurement():
    data = json.loads(HARVEST_5E8.read_text())
    assert data["N"] == 500_000_000
    assert data["sums"]["f_I_n"] == {data["sums"]["f_I_n"]}
    assert data["sums"]["f_I_p"] == {data["sums"]["f_I_p"]}
    assert data["sums"]["primes"] == {PI}
    assert data["cover_claimed"] is False
    assert data["esc_proved"] is False
    assert data["mordell_primes"]["zero_misses_is_not_a_cover"] is True
    assert data["mordell_primes"]["totals"] == {{
        "primes": {tot["primes"]},
        "hits": {tot["hits"]},
        "misses": 0,
    }}
    mins = {{c["residue_mod_840"]: c["min_f_I"] for c in data["mordell_primes"]["classes"]}}
    assert mins == {{1: 12, 121: 24, 169: 22, 289: 28, 361: 14, 529: 30}}
"""
    if "test_typeI_5e8_harvest_is_measurement" in text:
        text = re.sub(
            r"\n\ndef test_typeI_5e8_harvest_is_measurement\(\):[\s\S]*$",
            fn,
            text,
        )
    else:
        text = text.rstrip() + fn
    path.write_text(text if text.endswith("\n") else text + "\n")


def patch_readmes(data: dict) -> None:
    readme = ROOT / "README.md"
    t = readme.read_text()
    t = t.replace(
        "Next leftover burn: optional first-R from \\(8.00\\times 10^9\\) or\n"
        "Type I toward \\(5\\times 10^8\\) (`notes/NEXT.md`). **Do not rebuild**\n"
        "`fi2`. **Do not rerun** \\(\\le 2\\times 10^8\\).\n",
        "Next leftover burn: optional first-R from \\(8.00\\times 10^9\\) or a\n"
        "larger Type I bound (`notes/NEXT.md`). **Do not rebuild** `fi2`.\n"
        "**Do not rerun** \\(\\le 5\\times 10^8\\).\n",
    )
    if "typeI_mordell_5e8" not in t and "HARVEST-5e8.md" not in t:
        t = t.replace(
            "`notes/HARVEST-2e8.md`.\n",
            "`notes/HARVEST-2e8.md`. At \\(5\\times 10^8\\): "
            f"\\(\\sum_n f_I = {data['sums']['f_I_n']}\\), "
            f"\\(\\sum_p f_I = {data['sums']['f_I_p']}\\). "
            "Measurement, not a cover: `notes/HARVEST-5e8.md`.\n",
        )
    t = t.replace(
        "notes/HARVEST-partial-5e8.md  5e8 Type I shards (not complete)\n",
        "notes/HARVEST-5e8.md  Type I census at 5e8 (this machine)\n"
        "notes/HARVEST-partial-5e8.md  5e8 shards (complete; see HARVEST-5e8)\n",
    )
    t = t.replace(
        "notes/NEXT.md     first-R from 8e9 or Type I toward 5e8\n",
        "notes/NEXT.md     first-R from 8e9 or larger Type I\n",
    )
    readme.write_text(t)

    conv = ROOT / "CONVENTIONS.md"
    ct = conv.read_text()
    ct = ct.replace(
        "- The Type I enumerator census through `2×10⁸` is done (`y ≤ 2n/3`,\n"
        "  `x = n·a·b·d`). Do not rerun `10⁶`, `10⁷`, `2×10⁷`, `5×10⁷`,\n"
        "  `10⁸`, or `2×10⁸`.\n",
        "- The Type I enumerator census through `5×10⁸` is done (`y ≤ 2n/3`,\n"
        "  `x = n·a·b·d`). Do not rerun `10⁶`, `10⁷`, `2×10⁷`, `5×10⁷`,\n"
        "  `10⁸`, `2×10⁸`, or `5×10⁸`.\n",
    )
    ct = ct.replace(
        "- Type I toward `5×10⁸` may continue from `enum/n5e8_shards.tsv`.\n"
        "  Do not claim that bound complete unless the merge exists.\n",
        "",
    )
    conv.write_text(ct)

    data_readme = ROOT / "data" / "README.md"
    dr = data_readme.read_text()
    if "typeI_mordell_5e8" not in dr:
        dr = dr.replace(
            "`typeI_mordell_2e8.json` is the wave-4 complete bound \\(N=2\\times 10^8\\).\n",
            "`typeI_mordell_2e8.json` is the wave-4 complete bound \\(N=2\\times 10^8\\).\n"
            "`typeI_mordell_5e8.json` is the wave-6 complete bound \\(N=5\\times 10^8\\).\n",
        )
    data_readme.write_text(dr)

    enum_readme = ROOT / "enum" / "README.md"
    er = enum_readme.read_text()
    if "5\\times 10^8" not in er:
        er = er.replace(
            "| \\(2\\times 10^8\\) | 83381351012 | 12463112814 | 30 |\n",
            "| \\(2\\times 10^8\\) | 83381351012 | 12463112814 | 30 |\n"
            f"| \\(5\\times 10^8\\) | {data['sums']['f_I_n']} | {data['sums']['f_I_p']} | 30 |\n",
        )
    er = er.replace(
        "# N=5e8 (not complete unless every n5e8 dump exists)\n",
        "# N=5e8 (complete; do not rerun)\n",
    )
    enum_readme.write_text(er)


def main() -> None:
    data = load()
    write_harvest(data)
    write_partial_done()
    write_next(data)
    patch_closed(data)
    patch_test(data)
    patch_readmes(data)
    print("recorded 5e8 harvest notes and tests")
    print(f"f_I_n={data['sums']['f_I_n']} f_I_p={data['sums']['f_I_p']}")
    print(f"P/(N ln^2 N)={ratio(data['sums']['f_I_p']):.5f}")


if __name__ == "__main__":
    main()
