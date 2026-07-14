# Evaluation corpus and methodology

The `eval/` harness measures editing outcomes; it does not determine authorship. Treat every threshold as a regression heuristic that must be calibrated by language, genre, text length, and corpus provenance.

## Pair schema

Each `eval/corpus/**/*.json` file contains one before/after pair.

| Field | Required | Type | Meaning |
|---|---:|---|---|
| `id` | yes | string | Stable, unique identifier used for sorting and aggregate output. |
| `genre` | yes | string | Genre gate passed to the metrics. |
| `before` | yes | string | Source text, including every fact and qualification the rewrite must preserve. |
| `after` | yes | string | Expected edited text. |
| `language` | no | `"en"` or `"ru"` | Explicit language; omitted values are detected automatically. |
| `title` | no | string | Human-readable label. |
| `name` | no | string | Descriptive alias; never a substitute for `id`. |
| `source` | no | `"human"` or `"ai"` | Optional 2×2 provenance axis. Use only when provenance is documented. |
| `transform` | no | `"original"` or `"humanized"` | Optional 2×2 transformation axis. Use only when the transformation is documented. |

Keep the input immutable during evaluation. A rewrite may change wording and structure, but it must preserve numbers, dates, URLs, names, negation, modality, and other substantive claims. Do not add a source label merely because prose looks human- or machine-written.

## Methodological checks

- **2×2 test.** When `source` and `transform` are available, evaluate the four `human|ai × original|humanized` cells separately. Reject or demote a rule whose hits concentrate in only one off-diagonal cell; that usually signals a transformation artifact rather than a robust source distinction.
- **CoAT false-positive regression.** After human-written CoAT texts are vendored under `eval/corpus/coat_human/` with their dataset provenance intact, demote any pattern that fires on more than 10% of those human texts to corroboration-only. CoAT spans six Russian domains and explicitly reports weak transfer to unseen domains, so report per-domain as well as aggregate rates.
- **Length matching for Russian.** Aggregate runs should warn when the before/after word-count difference exceeds 35%. AINL-Eval 2025 contains a strong length confound: human abstracts average 126.4 words, while model outputs average 49.6–85.7 tokens. Do not interpret a length-driven score change as a style improvement.
- **No single-metric verdict.** Use metrics to locate passages for review. Aggressive editing requires convergence across independent lexical, structural, grammatical, or sourcing families.

## Corpus debt

The twelve English pairs removed before v2.20 remain outstanding. Their original source files and provenance are not present in this repository, so v2.21 does **not** recreate them from memory or synthetic substitutes. Restore them only from verifiable originals with source and licensing notes. Until then, English aggregate coverage is limited to the explicitly specified v2.21 pair now present in `eval/corpus/`.

Primary methodology references are recorded in [`../references/research.md`](../references/research.md#v221-evidence-register).
