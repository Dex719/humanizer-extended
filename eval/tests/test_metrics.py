from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from eval.metrics import (
    BOOSTERS,
    CONNECTORS,
    DEFAULT_CORPUS,
    EN_HEDGES,
    HEDGES,
    RU_FRAME_PHRASES,
    aggregate_corpus,
    compare_texts,
    count_phrases,
    detect_language,
    format_compare,
    load_corpus,
    metrics,
    split_sentences,
)


ROOT = Path(__file__).resolve().parents[2]
METRICS_CLI = ROOT / "eval" / "metrics.py"
PROFILE_CLI = ROOT / "eval" / "profile.py"
BASELINE = ROOT / "eval" / "baseline.json"


def test_language_detection_uses_cyrillic_share() -> None:
    assert detect_language("API v2: отчёты, поиск и очередь задач") == "ru"
    assert detect_language("An API with one пример token") == "en"
    assert detect_language("123 -- https://example.test") == "en"


def test_language_word_lists_have_required_en_and_ru_entries() -> None:
    assert {"однако", "кроме того", "таким образом", "следовательно", "в связи с этим"} <= set(
        CONNECTORS["ru"]
    )
    assert {"however", "moreover", "therefore"} <= set(CONNECTORS["en"])
    assert {"возможно", "вероятно", "может"} <= set(HEDGES["ru"])
    assert {"безусловно", "действительно", "на самом деле"} <= set(BOOSTERS["ru"])


def test_count_phrases_does_not_treat_month_may_as_hedge() -> None:
    text = "The May release shipped on 12 May. It may change, and the fix might help."
    profile = metrics(text, language="en")
    assert count_phrases(text, EN_HEDGES) == 2  # lowercase modal may + might; two month names excluded
    assert profile["lexical"]["hedges"]["may"] == 1
    assert profile["lexical"]["hedges_total"] == 2


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Сохраняем логи, метрики и т. д. Потом строим отчёт.", 2),
        ("Это, т. е. по сути, один этап. Следующий этап короче.", 2),
        ("Use e.g. Python or Rust. Then run it.", 2),
        ("The cache is shared, i.e. all workers see it. Retry once.", 2),
        ("А. С. Пушкин родился в Москве. Это второе предложение.", 2),
        ("J. R. R. Tolkien wrote the novel. It became famous.", 2),
    ],
)
def test_sentence_splitter_preserves_abbreviations_and_initials(text: str, expected: int) -> None:
    assert len(split_sentences(text)) == expected


def test_ru_tell_detectors() -> None:
    text = (
        'В современном мире сервис играет ключевую роль. Однако, команда продолжила работу. '
        'Преимущества: Высокая скорость и простота. Автор назвал это "новым подходом".'
    )
    profile = metrics(text)
    assert profile["language"] == "ru"
    assert profile["tells"]["ru_odnako_comma"] == 1
    assert profile["tells"]["ru_capital_after_colon"] == 1
    assert profile["tells"]["ru_non_guillemets"] == 1
    assert profile["tells"]["ru_frame_phrases"] >= 2


def test_ru_inverted_targets_allow_dash_and_do_not_penalize_passive() -> None:
    ru = metrics(
        "Москва — столица России. Можно сделать вывод после проверки. Результат был получен утром.",
        language="ru",
    )
    en = metrics("One — two. This is a test.", language="en")
    assert ru["compliance"]["checks"]["em_dashes"]["target"] > 0
    assert ru["compliance"]["checks"]["em_dashes"]["passed"] is True
    assert en["compliance"]["checks"]["em_dashes"]["passed"] is False
    passive = ru["structural"]["checks"]["agentless_passive_per_100_words"]
    assert passive["applicable"] is False
    assert passive["passed"] is None
    assert ru["structural"]["checks"]["sentence_length_sd"]["target"] < metrics(
        "One. This sentence has several words. A much longer sentence follows because rhythm varies.",
        language="en",
    )["structural"]["checks"]["sentence_length_sd"]["target"]
    assert ru["structural"]["long_sentence_threshold"] > en["structural"]["long_sentence_threshold"]


def test_booster_compliance_is_genre_gated() -> None:
    readme = metrics("Короткая техническая справка без оценки.", genre="readme", language="ru")
    review = metrics("Короткий обзор без оценки.", genre="review", language="ru")
    assert readme["compliance"]["checks"]["boosters"]["applicable"] is False
    assert readme["compliance"]["checks"]["boosters"]["passed"] is None
    assert review["compliance"]["checks"]["boosters"]["applicable"] is True
    assert review["compliance"]["checks"]["boosters"]["passed"] is False


def test_compare_has_separate_structural_and_compliance_blocks() -> None:
    result = compare_texts(
        "Однако, это важный текст. В заключение он играет ключевую роль.",
        "Это текст. Он действительно важен по указанной причине.",
        genre="review",
        language="ru",
    )
    assert result["command"] == "compare"
    assert "sentence_length_sd" in result["structural"]["metrics"]
    assert "em_dashes" in result["compliance"]["metrics"]
    report = format_compare(result)
    assert "STRUCTURAL" in report
    assert "COMPLIANCE" in report


def test_ru_corpus_has_six_contentful_genres() -> None:
    pairs = load_corpus(DEFAULT_CORPUS)
    assert len(pairs) >= 6
    assert {item["genre"] for item in pairs} >= {
        "vc-habr",
        "landing",
        "bio",
        "review",
        "science-pop",
        "readme",
    }
    for item in pairs:
        assert item.get("language") == "ru"
        assert len(item["before"].split()) >= 65
        assert len(item["after"].split()) >= 55


def test_aggregate_smoke_and_improvement() -> None:
    result = aggregate_corpus(DEFAULT_CORPUS)
    assert result["schema_version"] == 1
    assert result["command"] == "aggregate"
    assert result["corpus"]["pairs"] >= 6
    assert result["corpus"]["languages"] == {"ru": result["corpus"]["pairs"]}
    assert result["structural"]["after_score"]["rate"] >= result["structural"]["before_score"]["rate"]
    assert result["compliance"]["after_score"]["rate"] > result["compliance"]["before_score"]["rate"]
    assert result["tells"]["after_total"] < result["tells"]["before_total"]


def test_aggregate_cli_json_is_deterministic() -> None:
    command = [sys.executable, str(METRICS_CLI), "aggregate", "--corpus", str(DEFAULT_CORPUS), "--json"]
    first = subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True).stdout
    second = subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True).stdout
    assert first == second
    assert json.loads(first)["command"] == "aggregate"


def test_baseline_gate_passes_and_regressions_exit_nonzero(tmp_path: Path) -> None:
    command = [
        sys.executable,
        str(METRICS_CLI),
        "aggregate",
        "--corpus",
        str(DEFAULT_CORPUS),
        "--check-baseline",
        str(BASELINE),
        "--json",
    ]
    passing = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True)
    assert passing.returncode == 0
    assert json.loads(passing.stdout)["baseline_check"]["passed"] is True

    impossible = json.loads(BASELINE.read_text(encoding="utf-8"))
    impossible["compliance"]["after_score"]["rate"] = 1.1
    impossible_path = tmp_path / "impossible-baseline.json"
    impossible_path.write_text(json.dumps(impossible), encoding="utf-8")
    failing_command = command.copy()
    failing_command[failing_command.index(str(BASELINE))] = str(impossible_path)
    failing = subprocess.run(failing_command, cwd=ROOT, check=False, capture_output=True, text=True)
    assert failing.returncode == 1
    result = json.loads(failing.stdout)
    assert result["baseline_check"]["passed"] is False
    assert result["baseline_check"]["regressions"]


def test_profile_wrapper_finds_corpus_outside_repo_cwd(tmp_path: Path) -> None:
    completed = subprocess.run(
        [sys.executable, str(PROFILE_CLI), "--json"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(completed.stdout)["corpus"]["pairs"] >= 6


def test_empty_input_is_safe() -> None:
    profile = metrics("")
    assert profile["language"] == "en"
    assert profile["word_count"] == 0
    assert profile["sentence_count"] == 0
    assert profile["structural"]["sentence_burstiness"] == 0.0
