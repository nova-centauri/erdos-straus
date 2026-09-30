# Conventions for leftover-credit agents

This repo is Steve Barrett’s durable Erdős–Straus **workbench**
for leftover LLM credits. It is not a proof grind. The conjecture stays
open. There is **no** full Mordell-class cover.

## Models and spend

- **Never Fable.**
- **Claude Opus 5 High** on leftover Anthropic credit only. Cap the
  spend at about **80%** of whatever leftover is on the account. Do
  **not** start a fresh Anthropic week to continue this work.
- **SuperGrok Heavy**. Cap at about **70%** of leftover.
- Chat continuity stays in the leftover sessions; durable facts
  (notes, CSV rows, harvest JSON) live in this repository.

## What you may do

- The Type I enumerator census through `2×10⁸` is done (`y ≤ 2n/3`,
  `x = n·a·b·d`). Do not rerun `10⁶`, `10⁷`, `2×10⁷`, `5×10⁷`,
  `10⁸`, or `2×10⁸`.
- The first-R scanner (`erdos_straus/first_r.py`) may be extended
  from `8.00×10⁹` on `n ≡ 529 (mod 840)`. It is a search, not a cover.
- Type I toward `5×10⁸` may continue from `enum/n5e8_shards.tsv`.
  Do not claim that bound complete unless the merge exists.
- Independently verify triples with exact arithmetic
  (`4xyz − n(xy + xz + yz) = 0` or `fractions.Fraction`).
- Commit notes and any new verified rows to `data/triples.csv`.
- Keep the first-pass identities, algebra proofs, and solver if they
  still check. Wire new data into them. Do not delete a working
  verifier to start over.

## What you must not do

- Do not try to prove the conjecture.
- Do not invent new covering families.
- Do not repeat anything in `notes/CLOSED.md`.
- Do not claim a full Mordell-class cover. None exists. Chat work from
  27–29 Aug 2026 supersedes stale cover claims.
- Do not rebuild the Type I enumerator (Opus turn 7 BUILD is done).
- Do not add a web app or Vercel deploy. This repository is the
  public workbench; keep facts in git, not in a chat.
- Do not rewrite unrelated first-pass files (`IDENTITIES.md` algebra,
  the solver, the sympy proofs) unless a leftover harvest needs a
  hook.

## Arithmetic

Never floats. A triple is accepted only when

```
4*x*y*z - n*(x*y + x*z + y*z) == 0
```

with `n ≥ 2` and `x, y, z ≥ 1`. The verifier also checks
`fractions.Fraction`. Print `n % 840` whenever you report a triple.

## Commit habit

Every leftover session that produces a fact should leave that fact in
git: notes, CSV rows, and the `make check` / `erdos-straus check-csv`
pass. Chat-only results evaporate (the Claude sandbox was not durable).
