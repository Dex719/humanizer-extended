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
    aggregate_corpus,
    compare_texts,
    count_phrases,
    content_function_ratio,
    dangling_russian_participle,
    detect_language,
    digit_density,
    format_compare,
    human_marker_floor,
    immutable_token_audit,
    load_corpus,
    metrics,
    participial_stack_rate,
    punctuation_entropy,
    split_sentences,
    that_clause_subject_rate,
    windowed_ttr,
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
    assert en["compliance"]["checks"]["em_dashes"]["applicable"] is False
    assert en["compliance"]["checks"]["em_dashes"]["passed"] is None
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
    assert "immutable_token_audit" in result["integrity"]
    report = format_compare(result)
    assert "STRUCTURAL" in report
    assert "COMPLIANCE" in report


def test_ru_corpus_has_six_contentful_genres() -> None:
    pairs = load_corpus(DEFAULT_CORPUS)
    ru_pairs = [item for item in pairs if item.get("language") == "ru"]
    assert len(ru_pairs) >= 6
    assert {item["genre"] for item in ru_pairs} >= {
        "vc-habr",
        "landing",
        "bio",
        "review",
        "science-pop",
        "readme",
    }
    for item in ru_pairs:
        if item["genre"] == "scientific":
            assert item["id"] == "ru-dangling-kanclit"
        else:
            assert len(item["before"].split()) >= 65
            assert len(item["after"].split()) >= 55


def test_aggregate_smoke_and_improvement() -> None:
    result = aggregate_corpus(DEFAULT_CORPUS)
    assert result["schema_version"] == 1
    assert result["command"] == "aggregate"
    assert result["corpus"]["pairs"] >= 8
    assert result["corpus"]["languages"]["ru"] >= 7
    assert result["corpus"]["languages"]["en"] >= 1
    assert sum(result["corpus"]["languages"].values()) == result["corpus"]["pairs"]
    assert result["structural"]["after_score"]["rate"] >= result["structural"]["before_score"]["rate"]
    assert result["compliance"]["after_score"]["rate"] > result["compliance"]["before_score"]["rate"]
    assert result["integrity"]["immutable_token_audit"]["total_violations"] == 0
    assert result["tells"]["after_total"] < result["tells"]["before_total"]
    for diagnostic in result["diagnostics"]["metrics"].values():
        assert diagnostic["paired_applicable"] <= min(
            diagnostic["before_applicable"], diagnostic["after_applicable"]
        )


def test_aggregate_warns_on_length_mismatch(tmp_path: Path) -> None:
    pair = {
        "id": "length-mismatch",
        "language": "en",
        "genre": "essay",
        "before": "The documented procedure remains within the supplied scope. " * 25,
        "after": "The procedure remains within scope.",
    }
    (tmp_path / "pair.json").write_text(json.dumps(pair), encoding="utf-8")
    result = aggregate_corpus(tmp_path)
    assert result["diagnostics"]["length_matching"][0]["id"] == "length-mismatch"
    assert result["warnings"] and "length mismatch" in result["warnings"][0]


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


# ---- v2.21 metrics tests ----

LONG_EN = (
    "The study found that 42% of users preferred option A in 2023. "
    "See https://example.com for details of the protocol and its scope. "
) * 8


def test_immutable_no_change() -> None:
    result = immutable_token_audit(LONG_EN, LONG_EN)
    assert not result["abstained"] and result["total_violations"] == 0


def test_immutable_removed_number() -> None:
    after = LONG_EN.replace("42%", "most").replace("2023", "recently")
    result = immutable_token_audit(LONG_EN, after)
    assert not result["abstained"] and result["total_violations"] > 0


def test_immutable_audits_url_name_negation_and_modality() -> None:
    before = (
        "Ada Lovelace may not publish the protocol at https://example.com/v1. "
        "The research team will review the documented procedure and record its scope. "
    ) * 8
    after = before.replace("Ada Lovelace", "Ada Byron").replace(
        "may not publish", "will publish"
    ).replace("https://example.com/v1", "https://example.com/v2")
    result = immutable_token_audit(before, after)
    assert not result["abstained"]
    for category in ("urls", "names", "negations", "modality"):
        assert result["categories"][category]["violations"] > 0


def test_immutable_short_abstain() -> None:
    assert immutable_token_audit("Short text.", "Short text.")["abstained"]


def test_marker_present() -> None:
    text = (
        "Well, the results were clear. No answer is complete without context, "
        "though it suggests a trend. The manner in which the system runs matters. "
    ) * 5
    result = human_marker_floor(text, "en")
    assert not result["abstained"] and result["count"] >= 3


def test_marker_absent() -> None:
    text = (
        "The system demonstrates significant improvements. "
        "The platform showcases enhanced capabilities across environments. "
    ) * 10
    result = human_marker_floor(text, "en")
    assert not result["abstained"] and result["count"] == 0


def test_marker_ru() -> None:
    text = (
        "Впрочем, результат оказался неожиданным. Ведь выборка была мала, "
        "а метод-то новый. Пожалуй, стоит повторить эксперимент на большей выборке. "
    ) * 6
    result = human_marker_floor(text, "ru")
    assert not result["abstained"] and result["count"] >= 3


def test_entropy_uniform_low() -> None:
    text = "The system works. The platform runs. The code executes. The test passes. " * 10
    result = punctuation_entropy(text, "en")
    assert not result["abstained"] and result["entropy"] < 2.0


def test_entropy_varied() -> None:
    text = (
        "Results were clear: 42% better. However, the sample was small (n=10). "
        "Expected? Yes — and no. The team, led by Dr. Smith, published in 2023. "
    ) * 5
    result = punctuation_entropy(text, "en")
    assert not result["abstained"] and result["entropy"] >= 2.0


def test_ttr_windows() -> None:
    text = "alpha beta gamma delta epsilon zeta eta theta iota kappa " * 40
    result = windowed_ttr(text)
    assert not result["abstained"] and result["num_windows"] >= 3


def test_ttr_short_abstain() -> None:
    assert windowed_ttr("one two three " * 10)["abstained"]


def test_cf_ratio_range() -> None:
    result = content_function_ratio(LONG_EN, "en")
    assert not result["abstained"] and 0.3 < result["ratio"] < 3.5


def test_digit_density_zero_is_signal() -> None:
    text = (
        "The system demonstrates significant improvements in overall performance "
        "and reliability across multiple operational environments. "
    ) * 10
    result = digit_density(text, "en", "scientific")
    assert not result["abstained"] and result["density_per_1000"] == 0


def test_digit_density_genre_gate() -> None:
    assert digit_density(LONG_EN, "en", "essay")["abstained"]


def test_participials_flagged() -> None:
    text = (
        "The system, leveraging advanced algorithms, processing real-time data, "
        "achieves high throughput under load in production. "
    ) * 12
    result = participial_stack_rate(text, "academic", "en")
    assert not result["abstained"] and result["stack_count"] >= 2


def test_participials_news_abstain() -> None:
    text = "The system, leveraging algorithms, processing data, works. " * 20
    assert participial_stack_rate(text, "news", "en")["abstained"]
    assert metrics(text, genre="news", language="en")["structural"]["checks"][
        "participial_clauses_per_250_words"
    ]["applicable"] is False


def test_that_subjects() -> None:
    text = (
        "That the system failed is concerning. That the budget was exceeded is "
        "problematic. Ordinary prose follows here with no such constructions at all. "
    ) * 5
    result = that_clause_subject_rate(text, "academic", "en")
    assert not result["abstained"] and result["count"] >= 2


def test_dangling_ru_detected() -> None:
    text = (
        "Используя этот метод, результаты были улучшены на 15%. "
        "Применяя новый подход, эффективность была повышена."
    )
    result = dangling_russian_participle(text, "ru")
    assert not result["abstained"] and result["count"] >= 1


def test_dangling_ru_correct_usage() -> None:
    text = (
        "Используя этот метод, мы улучшили результаты на 15%. "
        "Применяя новый подход, команда повысила эффективность."
    )
    result = dangling_russian_participle(text, "ru")
    assert result["count"] <= 1


def test_dangling_ru_does_not_treat_adjective_as_gerund() -> None:
    result = dangling_russian_participle(
        "Высокая точность, результаты стабильны во всех сериях.", "ru"
    )
    assert result["count"] == 0


def test_dangling_en_abstain() -> None:
    assert dangling_russian_participle("Using this method, results improved.", "en")[
        "abstained"
    ]
