"""Score the full-vs-slim outputs in this folder with the eval metrics."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from eval.metrics import compare_texts  # noqa: E402

HERE = Path(__file__).resolve().parent


def main() -> None:
    rows = []
    for lang in ("en", "ru"):
        inputs = {
            item["id"]: item
            for item in json.loads((HERE / f"cmp_inputs_{lang}.json").read_text(encoding="utf-8"))
        }
        for variant in ("full", "slim"):
            outputs = json.loads((HERE / f"out_{variant}_{lang}.json").read_text(encoding="utf-8"))
            for out in outputs:
                item = inputs[out["id"]]
                c = compare_texts(
                    item["text"], out["output"], genre=item["genre"], language=lang, pair_id=out["id"]
                )
                audit = c["integrity"]["immutable_token_audit"]
                cats = audit.get("categories", {})
                rows.append(
                    {
                        "lang": lang,
                        "variant": variant,
                        "id": out["id"],
                        "words": f'{c["counts"]["before_words"]}->{c["counts"]["after_words"]}',
                        "viol": audit["total_violations"],
                        "contrast_in": c["compliance"]["metrics"]["contrast_frames"]["before"]["value"],
                        "contrast": c["compliance"]["metrics"]["contrast_frames"]["after"]["value"],
                        "struct": c["structural"]["after_score"]["rate"],
                        "compl": c["compliance"]["after_score"]["rate"],
                        "lost": {k: v["missing"] for k, v in cats.items() if v.get("missing")},
                        "added": {k: v["added"] for k, v in cats.items() if v.get("added")},
                    }
                )
    for lang in ("en", "ru"):
        for variant in ("full", "slim"):
            sub = [r for r in rows if r["lang"] == lang and r["variant"] == variant]
            n = len(sub)
            print(
                f"{lang} {variant}: n={n} violations={sum(r['viol'] for r in sub)} "
                f"contrast_left={sum(r['contrast'] for r in sub)} "
                f"structural={sum(r['struct'] for r in sub) / n:.3f} "
                f"compliance={sum(r['compl'] for r in sub) / n:.3f}"
            )
    (HERE / "scores.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n"
    )


if __name__ == "__main__":
    main()
