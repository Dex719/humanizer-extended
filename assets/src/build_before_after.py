#!/usr/bin/env python3
"""Build the README before/after images from the eval corpus pairs.

The texts come verbatim from ``eval/corpus/*_blog_weekly_releases.json``; this
script only adds highlight markup to the ``before`` side. Render the HTML with
any headless Chromium, for example::

    chrome --headless --hide-scrollbars --force-device-scale-factor=2 \
        --window-size=1200,760 --screenshot=assets/before-after-en.png \
        assets/src/before-after-en.html
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

KINDS = {
    "contrast": ("#fde2e1", "#b42318", "Not X but Y"),
    "closer": ("#fef0c7", "#b54708", "Closer / fragments"),
    "inflation": ("#ece4fd", "#6941c6", "Inflation"),
    "chat": ("#dbeafe", "#1d4ed8", "Chatbot residue / run-up"),
    "defense": ("#d1fadf", "#067647", "Arguing with no one"),
    "grammar": ("#cffafe", "#0e7490", "Dangling participle"),
    "calque": ("#fce7f6", "#c11574", "Calque"),
}

KIND_LABELS_RU = {
    "contrast": "Не X, а Y",
    "closer": "Концовки и обрывки",
    "inflation": "Раздувание",
    "chat": "Остатки чата и разгон",
    "defense": "Спор с никем",
    "grammar": "Висячее деепричастие",
    "calque": "Калька",
}

HIGHLIGHTS = {
    "en": [
        ("Great question! Here's a look at", "chat"),
        ("isn't just a process change — it's a cultural shift", "contrast"),
        ("the goal wasn't speed. It was predictability.", "contrast"),
        ("The results speak for themselves.", "chat"),
        ("Faster feedback. Smaller diffs. Fewer surprises.", "closer"),
        ("To be clear,", "defense"),
        ("this isn't about working harder. It's about", "contrast"),
        ("a pivotal shift that underscores our commitment to quality, fostering trust across the team.", "inflation"),
        ("And that's the real win.", "closer"),
        ("I hope this helps! Let me know if you'd like a template for your own release calendar.", "chat"),
    ],
    "ru": [
        ("Отличный вопрос! Давайте разберёмся,", "chat"),
        ("это не просто изменение процесса, а", "contrast"),
        ("настоящая смена культуры", "calque"),
        ("Переходя", "grammar"),
        ("нашей целью была не скорость. Это про предсказуемость.", "contrast"),
        ("Результаты говорят сами за себя:", "chat"),
        ("Быстрая обратная связь. Маленькие диффы. Меньше сюрпризов.", "closer"),
        ("Важно отметить:", "chat"),
        ("речь не о том, чтобы работать больше. Дело в том,", "contrast"),
        ("играет ключевую роль", "inflation"),
        ("И в этом вся суть.", "closer"),
        ("Надеюсь, это поможет! Если хотите, могу подготовить шаблон календаря релизов.", "chat"),
    ],
}

COPY = {
    "en": {
        "title": "Before and after",
        "before": "Before",
        "after": "After · humanizer-slim",
        "foot": "Kept: March, monthly → weekly, predictability over speed, 9 → 2 rollbacks, 1.5 vs 4 days, faster feedback, smaller diffs, fewer surprises, smaller steps, trust. Added: nothing.",
        "model": "Unedited output, Claude Sonnet 5.5",
    },
    "ru": {
        "title": "До и после",
        "before": "До",
        "after": "После · humanizer-slim",
        "foot": "Сохранено: март, ежемесячный → еженедельный цикл, предсказуемость вместо скорости, 9 → 2 отката, 1,5 дня вместо 4, быстрая обратная связь, маленькие диффы, меньше сюрпризов, маленькие шаги. Калька «смена культуры» заменена на «команда стала работать иначе». Добавлено: ничего.",
        "model": "Вывод без правок, Claude Sonnet 5.5",
    },
}


def paragraphs(text: str) -> list[str]:
    return [part for part in text.split("\n\n") if part.strip()]


def mark(paragraph: str, language: str) -> str:
    escaped = html.escape(paragraph)
    for phrase, kind in HIGHLIGHTS[language]:
        needle = html.escape(phrase)
        if needle in escaped:
            bg, fg, _ = KINDS[kind]
            escaped = escaped.replace(
                needle,
                f'<mark style="background:{bg};box-shadow:inset 0 -2px 0 {fg}">{needle}</mark>',
                1,
            )
    return escaped


def build(language: str, corpus_file: str) -> str:
    pair = json.loads((ROOT / "eval" / "corpus" / corpus_file).read_text(encoding="utf-8"))
    copy = COPY[language]
    before_html = "".join(f"<p>{mark(p, language)}</p>" for p in paragraphs(pair["before"]))
    after_html = "".join(f"<p>{html.escape(p)}</p>" for p in paragraphs(pair["after"]))
    used = []
    for _, kind in HIGHLIGHTS[language]:
        if kind not in used:
            used.append(kind)
    legend = "".join(
        f'<span class="chip"><i style="background:{KINDS[k][0]};border-color:{KINDS[k][1]}"></i>'
        f"{html.escape(KIND_LABELS_RU[k] if language == 'ru' else KINDS[k][2])}</span>"
        for k in used
    )
    return f"""<!doctype html>
<html lang="{language}"><head><meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: #f2f4f7; font-family: "Segoe UI", system-ui, sans-serif; color: #101828; }}
  .card {{ margin: 24px; background: #fff; border-radius: 16px; padding: 28px 32px 22px;
          box-shadow: 0 1px 3px rgba(16,24,40,.08), 0 8px 24px rgba(16,24,40,.06); }}
  header {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 14px; }}
  h1 {{ font-size: 22px; margin: 0; letter-spacing: -.01em; }}
  .model {{ font-size: 13px; color: #667085; }}
  .legend {{ display: flex; flex-wrap: wrap; gap: 8px 16px; margin-bottom: 18px; font-size: 13px; color: #344054; }}
  .chip i {{ display: inline-block; width: 12px; height: 12px; border-radius: 3px; border: 1.5px solid; margin-right: 6px; vertical-align: -1px; }}
  .cols {{ display: grid; grid-template-columns: 1.15fr 1fr; gap: 20px; }}
  .col {{ border: 1px solid #eaecf0; border-radius: 12px; padding: 16px 20px; }}
  .col h2 {{ font-size: 13px; text-transform: uppercase; letter-spacing: .06em; margin: 0 0 8px; color: #667085; }}
  .after {{ background: #f6fef9; border-color: #abefc6; }}
  .after h2 {{ color: #067647; }}
  p {{ font-size: 15.5px; line-height: 1.55; margin: 0 0 10px; }}
  mark {{ color: inherit; border-radius: 3px; padding: 0 2px; }}
  footer {{ margin-top: 16px; font-size: 13px; color: #475467; }}
</style></head>
<body><div class="card" id="card">
  <header><h1>{html.escape(copy["title"])}</h1><span class="model">{html.escape(copy["model"])}</span></header>
  <div class="legend">{legend}</div>
  <div class="cols">
    <section class="col"><h2>{html.escape(copy["before"])}</h2>{before_html}</section>
    <section class="col after"><h2>{html.escape(copy["after"])}</h2>{after_html}</section>
  </div>
  <footer>{html.escape(copy["foot"])}</footer>
</div></body></html>
"""


def main() -> None:
    for language, corpus_file in (
        ("en", "en_blog_weekly_releases.json"),
        ("ru", "ru_blog_weekly_releases.json"),
    ):
        page = build(language, corpus_file)
        missing = [p for p, _ in HIGHLIGHTS[language] if html.escape(p) not in page]
        if missing:
            raise SystemExit(f"{language}: highlight phrases not found: {missing}")
        (OUT / f"before-after-{language}.html").write_text(page, encoding="utf-8", newline="\n")
        print(f"wrote {OUT / f'before-after-{language}.html'}")


if __name__ == "__main__":
    main()
