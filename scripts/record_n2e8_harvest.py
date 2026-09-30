#!/usr/bin/env python3
"""Write notes/tests from a finished N=2e8 Type I merge. Not a cover."""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "data" / "typeI_mordell_2e8.json"
PARTIAL = ROOT / "data" / "typeI_partial"
MINS = {1: 12, 121: 24, 169: 22, 289: 28, 361: 14, 529: 30}


def ratio(p: int) -> float:
    # Same convention as the 1e7–1e8 tables: P / (N ln^2 N).
    n = 200_000_000
    return p / (n * (math.log(n) ** 2))


def load() -> dict:
    data = json.loads(JSON_PATH.read_text())
    assert data["N"] == 200_000_000
    assert data["cover_claimed"] is False
    assert data["esc_proved"] is False
    assert data["mordell_primes"]["zero_misses_is_not_a_cover"] is True
    assert data["sums"]["primes"] == 11_078_937
    mins = {c["residue_mod_840"]: c["min_f_I"] for c in data["mordell_primes"]["classes"]}
    assert mins == MINS, mins
    assert data["mordell_primes"]["totals"]["misses"] == 0
    assert data["mordell_primes"]["totals"]["hits"] == data["mordell_primes"]["totals"]["primes"]
    return data


def shard_rows() -> list[tuple[str, int, int, int, float]]:
    rows = []
    for line in (ROOT / "enum" / "n2e8_shards.tsv").read_text().splitlines():
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
    lines = [
        "# Type I enumerator harvest at \(N = 2\\times 10^8\) (wave 4)",
        "",
        "Source: same reconstructed `enum/fi2.c` as the \(10^6\) / \(10^7\) /",
        "\(2\\times 10^7\) / \(5\\times 10^7\) / \(10^8\) harvests, 2026-09-06.",
        "Checkpointed as a-range dumps and merged. Same turn-7 constraints.",
        "Structured copy: `data/typeI_mordell_2e8.json`.",
        "",
        "This is a **measurement**. ESC is unproved. Zero Type I misses among",
        "Mordell primes \(p \\le 2\\times 10^8\) is **not** a full-class cover.",
        "Elsholtz–Tao Prop. 1.6 still forbids a Type I/II cover of the full",
        "classes \(n \\equiv 169\) or \(529 \\pmod{840}\).",
        "",
        "Do **not** rerun \(10^6\), \(10^7\), \(2\\times 10^7\), \(5\\times 10^7\),",
        "\(10^8\), or this \(2\\times 10^8\) bound.",
        "",
        "## Totals",
        "",
        "| bound | \(\\sum_n f_I(n)\) | \(\\sum_p f_I(p)\) | observed \(P/(M\\ln^2 M)\) |",
        "| --- | ---: | ---: | ---: |",
        "| \(N=10^6\) | 165374532 | 34276274 | — |",
        "| \(N=10^7\) | 2559629008 | 454495120 | 0.17495 |",
        "| \(N=2\\times 10^7\) | 5772274472 | 982580024 | 0.17384 |",
        "| \(N=5\\times 10^7\) | 16795310188 | 2709141549 | 0.17241 |",
        "| \(N=10^8\) | 37494215304 | 5818322818 | 0.17147 |",
        f"| \(N=2\\times 10^8\) | {nsum} | {p} | {r:.5f} |",
        "",
        "Checksums on the merge: \(f_I(3049)=30\), \(f_I(2521)=12\),",
        "\(f_I(1009)=22\). \(\\pi(2\\times 10^8)=11078937\). Shard \(\\sum_n\)",
        "values add to the merge total.",
        "",
        "## Mordell primes \(p \\le 2\\times 10^8\)",
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
        "`Dmax = M/a` with \(M=2N/3=133333333\), so \(a\) runs through \(M\).",
        "Sixteen a-range dumps (gitignored under `data/typeI_partial/`) cover",
        "\([1,M]\) with no gaps. List: `enum/n2e8_shards.tsv`.",
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
        "scripts/merge_n2e8.sh",
        "```",
        "",
        "Same factoring path as the \(10^8\) harvest (trial to",
        "\(p\\le 4000\), then Miller–Rabin / Pollard). Not an enumerator rebuild.",
        "",
        "## What this wave did not do",
        "",
        "- Did not invent a covering family.",
        "- Did not claim a Mordell-class cover.",
        "- Did not rerun any finished smaller bound.",
        "",
    ]
    (ROOT / "notes" / "HARVEST-2e8.md").write_text("\n".join(lines))


def write_partial_done() -> None:
    (ROOT / "notes" / "HARVEST-partial-2e8.md").write_text(
        """# Type I census toward \(2\\times 10^8\) — complete (wave 4)

The \(N=2\\times 10^8\) harvest is **done**. See `notes/HARVEST-2e8.md` and
`data/typeI_mordell_2e8.json`.

Do **not** rerun \(N=10^6\), \(10^7\), \(2\\times 10^7\),
\(5\\times 10^7\), \(10^8\), or \(2\\times 10^8\).

Pickup if someone still has the gitignored dumps:

```bash
scripts/merge_n2e8.sh
```

Zero misses through \(2\\times 10^8\) stay a measurement, not a cover.
"""
    )


def write_next() -> None:
    (ROOT / "notes" / "NEXT.md").write_text(
        """# Next leftover spend

The Type I harvest at \(N = 2\\times 10^8\) is **done**. Do **not**
rerun \(10^6\), \(10^7\), \(2\\times 10^7\), \(5\\times 10^7\),
\(10^8\), or \(2\\times 10^8\).

Optional leftover burns (none of these is a cover):

1. Same `enum/fi2` at a **larger** complete bound (\(N=5\\times 10^8\))
   with a-range dumps + merge. Checkpoint hard. Do not rebuild `fi2`.
2. Continue the 529 first-R scanner from \(8.00\\times 10^8\)
   (`scripts/scan_first_r.py`). Search, not a cover.

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
"""
    )
    # append the 2e8 row from JSON at call time
    data = json.loads(JSON_PATH.read_text())
    path = ROOT / "notes" / "NEXT.md"
    path.write_text(
        path.read_text()
        + f"| \(2\\times 10^8\) | {data['sums']['f_I_n']} | {data['sums']['f_I_p']} |\n"
        + "\nKeep \(y\\le 2n/3\), \(x=n\\cdot a\\cdot b\\cdot d\), \(a\\le b\),\n"
        + "\\(\\gcd(a,c)=1\).\n"
    )


def patch_closed(data: dict) -> None:
    path = ROOT / "notes" / "CLOSED.md"
    text = path.read_text()
    text = text.replace(
        "(`notes/HARVEST-5e7.md`, `notes/HARVEST-1e8.md`). Next leftover spend\n"
        "is `notes/NEXT.md` (same constraints — not a rebuild).",
        "(`notes/HARVEST-5e7.md`, `notes/HARVEST-1e8.md`). The `2×10⁸` harvest\n"
        "is also done (`notes/HARVEST-2e8.md`). Next leftover spend is\n"
        "`notes/NEXT.md` (same constraints — not a rebuild).",
    )
    marker = "## Type I harvest at `2×10⁸` is measurement, not a cover (wave 4)"
    if marker not in text:
        p = data["sums"]["f_I_p"]
        block = f"""
## Type I harvest at `2×10⁸` is measurement, not a cover (wave 4)

Same `enum/fi2`, checkpointed a-range merge. Full table:
`notes/HARVEST-2e8.md`, `data/typeI_mordell_2e8.json`.

- `Σ_{{n≤2×10⁸}} f_I(n) = {data["sums"]["f_I_n"]}`
- `Σ_{{p≤2×10⁸}} f_I(p) = {p}`
- observed `P/(M ln² M) = {ratio(p):.5f}` (was 0.17147 at `10⁸`)
- All **{data["mordell_primes"]["totals"]["primes"]}** Mordell primes `p ≤ 2×10⁸` had `f_I(p) > 0` (zero misses)
- Checksums: `f_I(3049)=30`, `f_I(2521)=12`, `f_I(1009)=22`

**Zero Type I misses through 2×10⁸ is not a full-class cover.**
Do not harvest `2×10⁸` again. Next leftover spend is `notes/NEXT.md`.

"""
        text = text.replace(
            "**Zero Type I misses through 10⁸ is not a full-class cover.**\n"
            "Do not harvest `10⁸` again. Next leftover spend is `notes/NEXT.md`.\n",
            "**Zero Type I misses through 10⁸ is not a full-class cover.**\n"
            "Do not harvest `10⁸` again.\n"
            + block,
        )
    path.write_text(text)


def patch_test(data: dict) -> None:
    path = ROOT / "tests" / "test_typeI_harvest.py"
    text = path.read_text()
    if "HARVEST_2E8" not in text:
        text = text.replace(
            'HARVEST_1E8 = REPO / "data" / "typeI_mordell_1e8.json"\n',
            'HARVEST_1E8 = REPO / "data" / "typeI_mordell_1e8.json"\n'
            'HARVEST_2E8 = REPO / "data" / "typeI_mordell_2e8.json"\n',
        )
    tot = data["mordell_primes"]["totals"]
    fn = f"""


def test_typeI_2e8_harvest_is_measurement():
    data = json.loads(HARVEST_2E8.read_text())
    assert data["N"] == 200_000_000
    assert data["sums"]["f_I_n"] == {data["sums"]["f_I_n"]}
    assert data["sums"]["f_I_p"] == {data["sums"]["f_I_p"]}
    assert data["sums"]["primes"] == 11_078_937
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
    if "test_typeI_2e8_harvest_is_measurement" in text:
        text = re.sub(
            r"\n\ndef test_typeI_2e8_harvest_is_measurement\(\):[\s\S]*$",
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
        "and \(N = 10^8\) are also done. At \(10^8\):",
        "\(N = 10^8\), and \(N = 2\\times 10^8\) are also done. At \(10^8\):",
    )
    if "typeI_mordell_2e8" not in t:
        t = t.replace(
            "`notes/HARVEST-1e8.md`.\n\n"
            "Next leftover burn: finish \\(N=2\\times 10^8\\) on the same `fi2`\n"
            "(`notes/NEXT.md`, `notes/HARVEST-partial-2e8.md`,\n"
            "`enum/n2e8_shards.tsv`). **Do not rebuild** `fi2`. **Do not rerun**\n"
            "\\(\\le 10^8\\).\n",
            "`notes/HARVEST-1e8.md`. At \(2\\times 10^8\): "
            f"\\(\\sum_n f_I = {data['sums']['f_I_n']}\\), "
            f"\\(\\sum_p f_I = {data['sums']['f_I_p']}\\). "
            "That is a measurement, **not** a class cover. Details:\n"
            "`notes/HARVEST-2e8.md`.\n\n"
            "Next leftover burn: optional larger Type I bound or first-R from\n"
            "\\(8.00\\times 10^8\\) (`notes/NEXT.md`). **Do not rebuild**\n"
            "`fi2`. **Do not rerun** \\(\\le 2\\times 10^8\\).\n",
        )
    t = t.replace(
        "notes/HARVEST-partial-2e8.md  2e8 Type I shards (wave 4)\n",
        "notes/HARVEST-2e8.md  Type I census at 2e8 (this machine)\n"
        "notes/HARVEST-partial-2e8.md  2e8 shards (complete; see HARVEST-2e8)\n",
    )
    t = t.replace(
        "notes/NEXT.md     finish 2e8; optional first-R continue from 8e8\n",
        "notes/NEXT.md     optional larger Type I or first-R from 8e8\n",
    )
    readme.write_text(t)

    conv = ROOT / "CONVENTIONS.md"
    ct = conv.read_text()
    ct = ct.replace(
        "- The Type I enumerator census through `10⁸` is done. Wave 4 extends\n"
        "  the same `enum/fi2` to `2×10⁸` (`y ≤ 2n/3`, `x = n·a·b·d`). Do not\n"
        "  rerun `10⁶`, `10⁷`, `2×10⁷`, `5×10⁷`, or `10⁸`.\n",
        "- The Type I enumerator census through `2×10⁸` is done (`y ≤ 2n/3`,\n"
        "  `x = n·a·b·d`). Do not rerun `10⁶`, `10⁷`, `2×10⁷`, `5×10⁷`,\n"
        "  `10⁸`, or `2×10⁸`.\n",
    )
    conv.write_text(ct)

    data_readme = ROOT / "data" / "README.md"
    dr = data_readme.read_text()
    if "typeI_mordell_2e8" not in dr:
        dr = dr.replace(
            "`typeI_mordell_1e8.json` is the wave-3 complete bound \\(N=10^8\\).\n",
            "`typeI_mordell_1e8.json` is the wave-3 complete bound \\(N=10^8\\).\n"
            "`typeI_mordell_2e8.json` is the wave-4 complete bound \\(N=2\\times 10^8\\).\n",
        )
    data_readme.write_text(dr)

    enum_readme = ROOT / "enum" / "README.md"
    er = enum_readme.read_text()
    if "2\\times10^8" not in er and "2\\times 10^8" not in er:
        er = er.replace(
            "| \\(10^8\\) | 37494215304 | 5818322818 | 30 |\n",
            "| \\(10^8\\) | 37494215304 | 5818322818 | 30 |\n"
            f"| \\(2\\times 10^8\\) | {data['sums']['f_I_n']} | {data['sums']['f_I_p']} | 30 |\n",
        )
    enum_readme.write_text(er)


def main() -> None:
    data = load()
    write_harvest(data)
    write_partial_done()
    write_next()
    patch_closed(data)
    patch_test(data)
    patch_readmes(data)
    print("recorded 2e8 harvest notes and tests")
    print(f"f_I_n={data['sums']['f_I_n']} f_I_p={data['sums']['f_I_p']}")
    print(f"P/(M ln^2 M)={ratio(data['sums']['f_I_p']):.5f}")


if __name__ == "__main__":
    main()
