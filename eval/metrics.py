#!/usr/bin/env python3
"""Deterministic EN/RU style metrics for humanizer-extended.

This module deliberately uses only the Python standard library.  The numbers are
heuristics, not an AI detector: they make before/after edits observable and keep
the Russian-specific rules in the skill from regressing unnoticed.

Public API:

* ``detect_language(text)`` -> ``"en"`` or ``"ru"``
* ``split_sentences(text)`` -> list of sentences
* ``count_phrases(text, phrases)`` -> phrase occurrence count
* ``immutable_token_audit(before, after)`` -> fact-lock diagnostic
* ``human_marker_floor(text, language)`` -> language-gated marker count
* ``punctuation_entropy(text, language)`` -> punctuation Shannon entropy
* ``windowed_ttr(text)`` -> non-overlapping 100-token TTR windows
* ``content_function_ratio(text, language)`` -> stdlib Biber approximation
* ``digit_density(text, language, genre)`` -> scientific-genre digit density
* ``participial_stack_rate(text, genre, language)`` -> gated EN -ing stacks
* ``that_clause_subject_rate(text, genre, language)`` -> gated EN subjects
* ``dangling_russian_participle(text, language)`` -> RU grammar heuristic
* ``metrics(text, genre=None, language=None)`` -> stable profile dictionary
* ``compare_texts(before, after, ...)`` -> grouped before/after comparison
* ``aggregate_corpus(path)`` -> aggregate for JSON corpus pairs

CLI examples::

    python eval/metrics.py profile article.txt
    python eval/metrics.py compare before.txt after.txt --json
    python eval/metrics.py aggregate --corpus eval/corpus --json
    python eval/metrics.py aggregate --corpus eval/corpus \
        --check-baseline eval/baseline.json --json
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


SCHEMA_VERSION = 1
EVAL_DIR = Path(__file__).resolve().parent
DEFAULT_CORPUS = EVAL_DIR / "corpus"
DEFAULT_BASELINE = EVAL_DIR / "baseline.json"
CYRILLIC_THRESHOLD = 0.30
SHORT_TEXT_WORDS = 100
LENGTH_MISMATCH_THRESHOLD = 0.35


EN_CONNECTORS = (
    "however",
    "moreover",
    "furthermore",
    "additionally",
    "in addition",
    "consequently",
    "as a result",
    "therefore",
    "thus",
    "that said",
    "nevertheless",
)

RU_CONNECTORS = (
    "однако",
    "кроме того",
    "таким образом",
    "следовательно",
    "в связи с этим",
    "помимо этого",
    "в результате",
    "вместе с тем",
    "тем не менее",
    "итак",
)

EN_HEDGES = (
    "may",
    "might",
    "could",
    "possibly",
    "potentially",
    "perhaps",
    "probably",
    "likely",
    "appears to",
    "seems to",
    "suggests that",
    "arguably",
)

RU_HEDGES = (
    "может",
    "могут",
    "могло бы",
    "возможно",
    "вероятно",
    "по-видимому",
    "предположительно",
    "кажется",
    "скорее всего",
    "можно предположить",
    "есть основания полагать",
)

EN_BOOSTERS = (
    "clearly",
    "definitely",
    "certainly",
    "undoubtedly",
    "in fact",
    "of course",
    "indeed",
    "demonstrably",
)

RU_BOOSTERS = (
    "безусловно",
    "несомненно",
    "определённо",
    "определенно",
    "очевидно",
    "действительно",
    "конечно",
    "на самом деле",
    "без сомнения",
)

CONNECTORS = {"en": EN_CONNECTORS, "ru": RU_CONNECTORS}
HEDGES = {"en": EN_HEDGES, "ru": RU_HEDGES}
BOOSTERS = {"en": EN_BOOSTERS, "ru": RU_BOOSTERS}

RU_FRAME_PHRASES = (
    "важно отметить",
    "важно понимать",
    "следует учитывать",
    "стоит подчеркнуть",
    "нельзя не заметить",
    "в современном мире",
    "в современных условиях",
    "в условиях",
    "в связи с этим",
    "на сегодняшний день",
    "в заключение",
    "играет ключевую роль",
    "играют ключевую роль",
    "ключевой момент",
    "нельзя переоценить важность",
    "расположен в самом сердце",
    "расположенный в самом сердце",
)

EN_AI_PHRASES = (
    "it is important to note",
    "it is worth noting",
    "in today's rapidly evolving",
    "in conclusion",
    "plays a crucial role",
    "delve into",
    "ever-evolving landscape",
    "a testament to",
    "at its core",
)

NEUTRAL_BOOSTER_GENRES = {
    "documentation",
    "docs",
    "encyclopedia",
    "encyclopedic",
    "methodology",
    "reference",
    "readme",
    "scientific-methods",
    "technical-documentation",
    "документация",
    "методология",
    "справка",
    "энциклопедия",
}

# A lexical booster is a meaningful compliance target only in voice-led genres.
# In neutral or unknown genres, forcing one would manufacture stance rather than
# measure editing quality.
BOOSTER_TARGET_GENRES = frozenset(
    {
        "blog",
        "commentary",
        "essay",
        "opinion",
        "personal-blog",
        "review",
        "блог",
        "мнение",
        "обзор",
        "эссе",
    }
)

_WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё]+(?:[-'][A-Za-zА-Яа-яЁё]+)*|\d+(?:[.,]\d+)*")
_CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
_LETTER_RE = re.compile(r"[A-Za-zА-Яа-яЁё]")
_PROTECTED_DOT = "\ue000"


# These lists intentionally approximate function-word classes without claiming
# POS accuracy.  They are kept explicit and deterministic so corpus baselines do
# not depend on a tagger version or a network resource.
EN_FUNCTION_WORDS = frozenset(
    """
    a an the and or but nor so yet if because although though while whereas
    as than that whether when whenever where wherever why how of to in on at
    by for from with without into onto over under between among through during
    before after above below about against around near since until within
    i me my mine myself we us our ours ourselves you your yours yourself
    yourselves he him his himself she her hers herself it its itself they them
    their theirs themselves this these those who whom whose which what
    am is are was were be been being have has had having do does did doing
    can could may might must shall should will would not no nor never
    here there then also only even very too just more most less least much many
    some any each every either neither both all few several own same such
    """.split()
)

RU_FUNCTION_WORDS = frozenset(
    """
    а без более бы был была были было быть в во вот вы да даже для до его её ее
    если есть ещё еще же за и из или им их к как ко когда кто ли либо мне может
    мы на над не него неё нее нет ни но ну о об от по под при про с со так также
    такой там те тем то того тоже той только том тут ты у уже хотя чем что чтобы
    эта эти это этой этот я он она оно они мы вы ты вас вам ваш ваша ваши наше
    наш нас мне меня мой моя мои ему ей их ими который которая которые которых
    который где куда откуда почему потому пока после перед между через около
    можно нельзя нужно следует должен должна должны мог могла могли могут
    """.split()
)

FUNCTION_WORDS = {"en": EN_FUNCTION_WORDS, "ru": RU_FUNCTION_WORDS}

EN_HUMAN_MARKERS = (
    "well",
    "no answer is complete without",
    "the manner in which",
    "though",
    "after all",
    "for one thing",
    "mind you",
)

RU_HUMAN_MARKERS = (
    "впрочем",
    "ведь",
    "пожалуй",
    "в конце концов",
    "между прочим",
)

HUMAN_MARKERS = {"en": EN_HUMAN_MARKERS, "ru": RU_HUMAN_MARKERS}

SCIENTIFIC_DIGIT_GENRES = frozenset(
    {
        "academic",
        "experiment",
        "methodology",
        "research",
        "science",
        "science-pop",
        "scientific",
        "scientific-methods",
        "technical-report",
        "научный",
        "исследование",
        "методология",
    }
)

PARTICIPIAL_NEUTRAL_GENRES = frozenset(
    {
        "journalism",
        "news",
        "press-news",
        "resume",
        "résumé",
        "cv",
        "cover-letter",
        "журналистика",
        "новости",
        "резюме",
    }
)

PARTICIPIAL_TECH_GENRES = frozenset(
    {
        "documentation",
        "docs",
        "readme",
        "technical",
        "technical-documentation",
        "tech-docs",
    }
)

THAT_SUBJECT_NEUTRAL_GENRES = frozenset(
    {
        "argumentative",
        "formal-argumentative",
        "legal",
        "официально-деловой",
        "юридический",
    }
)


def _rounded(value: float, digits: int = 4) -> float:
    """Return JSON-friendly, stable rounded floats (and never negative zero)."""

    result = round(float(value), digits)
    return 0.0 if result == 0 else result


def _mean(values: Sequence[float | int]) -> float:
    return _rounded(statistics.fmean(values)) if values else 0.0


def _pstdev(values: Sequence[float | int]) -> float:
    return _rounded(statistics.pstdev(values)) if len(values) > 1 else 0.0


def detect_language(text: str, threshold: float = CYRILLIC_THRESHOLD) -> str:
    """Detect Russian by the share of Cyrillic characters among letters.

    A ratio rather than an absolute count keeps short Russian snippets working and
    prevents URLs, Markdown punctuation, and numbers from diluting the signal.
    The threshold is intentionally exported and deterministic; there is no model
    or locale dependency.
    """

    letters = _LETTER_RE.findall(text)
    if not letters:
        return "en"
    cyrillic = sum(1 for char in letters if _CYRILLIC_RE.fullmatch(char))
    return "ru" if cyrillic / len(letters) >= threshold else "en"


def cyrillic_ratio(text: str) -> float:
    letters = _LETTER_RE.findall(text)
    if not letters:
        return 0.0
    return _rounded(sum(1 for char in letters if _CYRILLIC_RE.fullmatch(char)) / len(letters))


def words(text: str) -> list[str]:
    """Tokenize English/Russian words and numbers without external packages."""

    return _WORD_RE.findall(text)


def _phrase_pattern(phrase: str) -> re.Pattern[str]:
    escaped = re.escape(phrase).replace(r"\ ", r"\s+")
    return re.compile(rf"(?<!\w){escaped}(?!\w)", re.IGNORECASE | re.UNICODE)


def count_phrase_details(text: str, phrases: Iterable[str]) -> dict[str, int]:
    """Count phrases with Unicode word boundaries and longest-phrase semantics.

    The English modal ``may`` is case-sensitive by design.  This excludes the
    month in ``released in May`` while still counting ``it may change``.  Longer
    phrases are counted independently because the lists contain no nested items.
    """

    result: dict[str, int] = {}
    for phrase in phrases:
        if phrase == "may":
            pattern = re.compile(r"(?<!\w)may(?!\w)", re.UNICODE)
        else:
            pattern = _phrase_pattern(phrase)
        count = sum(1 for _ in pattern.finditer(text))
        if count:
            result[phrase] = count
    return dict(sorted(result.items()))


def count_phrases(text: str, phrases: Iterable[str]) -> int:
    """Return the total occurrences of ``phrases`` in ``text``."""

    return sum(count_phrase_details(text, phrases).values())


def _resolve_language(text: str, language: str | None) -> str:
    chosen = detect_language(text) if language in (None, "auto") else language
    if chosen not in {"en", "ru"}:
        raise ValueError("language must be 'en', 'ru', 'auto', or None")
    return chosen


def _abstained(word_count: int, reason: str, **values: Any) -> dict[str, Any]:
    """Build the common, JSON-stable abstention envelope."""

    return {
        "abstained": True,
        "reason": reason,
        "word_count": word_count,
        **values,
    }


_URL_RE = re.compile(r"https?://[^\s<>\[\]{}]+", re.IGNORECASE)
_NUMBER_DATE_RE = re.compile(
    r"(?<![\w])(?:[+-]?\d{1,4}(?:[./-]\d{1,4}){1,2}|[+-]?\d+(?:[.,]\d+)?%?)(?![\w])"
)
_CAPITALIZED_RE = re.compile(r"(?<!\w)[A-ZА-ЯЁ][a-zа-яё]{2,}(?!\w)")
_MULTI_NAME_RE = re.compile(
    r"(?<!\w)(?:[A-ZА-ЯЁ][a-zа-яё]+[ \t]+){1,3}"
    r"[A-ZА-ЯЁ][a-zа-яё]+(?!\w)"
)
_ACRONYM_RE = re.compile(r"(?<!\w)[A-ZА-ЯЁ]{2,}(?:-[A-ZА-ЯЁ0-9]{2,})?(?!\w)")
_QUOTED_NAME_RE = re.compile(
    r"[«“\"]\s*(?P<name>[A-ZА-ЯЁ][^»”\"\n]{0,79}?)\s*[»”\"]"
)

_NEGATION_PATTERNS = {
    "en": ("not", "no", "never", "neither", "nor", "without"),
    "ru": ("не", "ни", "нет", "никогда", "без", "нельзя"),
}
_MODALITY_PATTERNS = {
    "en": (
        "may",
        "might",
        "could",
        "can",
        "must",
        "should",
        "shall",
        "will",
        "would",
        "ought to",
        "perhaps",
        "possibly",
        "probably",
        "likely",
        "appears to",
        "seems to",
    ),
    "ru": (
        "может",
        "могут",
        "мог",
        "могла",
        "могло",
        "могли",
        "можно",
        "возможно",
        "вероятно",
        "по-видимому",
        "предположительно",
        "должен",
        "должна",
        "должно",
        "должны",
        "следует",
        "нужно",
        "необходимо",
    ),
}


def _trim_url(value: str) -> str:
    return value.rstrip(".,;:!?)]}»”\"'")


def _immutable_inventory(text: str) -> dict[str, Counter[str]]:
    """Extract a conservative multiset for the fact-lock audit.

    The name rule intentionally favors precision: acronyms and multi-token names
    are always kept, while a single capitalized token is kept only away from a
    sentence boundary.  This avoids treating every sentence opener as a person.
    """

    urls = [_trim_url(match.group(0)) for match in _URL_RE.finditer(text)]
    without_urls = list(text)
    for match in _URL_RE.finditer(text):
        without_urls[match.start() : match.end()] = " " * (match.end() - match.start())
    number_source = "".join(without_urls)
    numbers_dates = [match.group(0) for match in _NUMBER_DATE_RE.finditer(number_source)]

    quoted_matches = list(_QUOTED_NAME_RE.finditer(text))
    names: list[str] = [match.group("name").strip().casefold() for match in quoted_matches]
    names.extend(match.group(0).casefold() for match in _MULTI_NAME_RE.finditer(text))
    names.extend(match.group(0).casefold() for match in _ACRONYM_RE.finditer(text))
    occupied = [(match.start(), match.end()) for match in _MULTI_NAME_RE.finditer(text)]
    occupied.extend((match.start(), match.end()) for match in _ACRONYM_RE.finditer(text))
    occupied.extend((match.start(), match.end()) for match in quoted_matches)
    for match in _CAPITALIZED_RE.finditer(text):
        if any(start <= match.start() < end for start, end in occupied):
            continue
        line_start = text.rfind("\n", 0, match.start()) + 1
        line_prefix = text[line_start : match.start()]
        if re.fullmatch(r"\s*(?:#{1,6}\s*|[-*+]\s+|\d+[.)]\s+)?", line_prefix):
            continue
        prefix = text[: match.start()].rstrip()
        if not prefix or prefix[-1:] in ".!?…\n:;,«“\"":
            continue
        names.append(match.group(0).casefold())

    language = detect_language(text)
    negations = count_phrase_details(text, _NEGATION_PATTERNS[language])
    # English contracted negation is not covered by word-boundary phrase lists.
    if language == "en":
        contracted = len(re.findall(r"\b[A-Za-z]+n't\b", text, flags=re.IGNORECASE))
        if contracted:
            negations["n't"] = contracted
    modality = count_phrase_details(text, _MODALITY_PATTERNS[language])

    def present(details: Mapping[str, int]) -> Counter[str]:
        return Counter({key.casefold(): 1 for key, value in details.items() if value})

    return {
        "urls": Counter(urls),
        "numbers_dates": Counter(numbers_dates),
        # Presence semantics avoid treating harmless repetition compaction as a
        # factual change. Numbers, dates, and URLs remain multisets because each
        # repeated occurrence may encode a separate datum.
        "names": Counter(set(names)),
        "negations": present(negations),
        "modality": present(modality),
    }


def _counter_json(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted((key, value) for key, value in counter.items() if value))


def immutable_token_audit(before: str, after: str) -> dict[str, Any]:
    """Audit numbers/dates, URLs, names, negations, and modality after editing.

    The source text controls the short-text gate.  A long source that was
    accidentally truncated must still be audited rather than hidden by an
    after-text abstention. Numbers, dates, and URLs use multiset occurrences;
    names, negation forms, and modality forms use normalized presence so normal
    deduplication does not become a false integrity failure.
    """

    before_word_count = len(words(before))
    after_word_count = len(words(after))
    if before_word_count < SHORT_TEXT_WORDS:
        return _abstained(
            before_word_count,
            f"source has fewer than {SHORT_TEXT_WORDS} words",
            before_word_count=before_word_count,
            after_word_count=after_word_count,
            categories={},
            total_violations=0,
        )

    before_inventory = _immutable_inventory(before)
    after_inventory = _immutable_inventory(after)
    categories: dict[str, Any] = {}
    total = 0
    for name in ("numbers_dates", "urls", "names", "negations", "modality"):
        before_values = before_inventory[name]
        after_values = after_inventory[name]
        missing = before_values - after_values
        added = after_values - before_values
        violations = sum(missing.values()) + sum(added.values())
        total += violations
        categories[name] = {
            "before": _counter_json(before_values),
            "after": _counter_json(after_values),
            "missing": _counter_json(missing),
            "added": _counter_json(added),
            "violations": violations,
        }
    return {
        "abstained": False,
        "reason": None,
        "word_count": before_word_count,
        "before_word_count": before_word_count,
        "after_word_count": after_word_count,
        "categories": categories,
        "total_violations": total,
        "passed": total == 0,
    }


def human_marker_floor(text: str, language: str | None = "auto") -> dict[str, Any]:
    """Count a small EN/RU set of discourse markers associated with human prose.

    This is an observational corroboration feature, never an authorship verdict.
    It abstains below 100 words and uses only the list for the selected language.
    """

    chosen = _resolve_language(text, language)
    word_count = len(words(text))
    if word_count < SHORT_TEXT_WORDS:
        return _abstained(
            word_count,
            f"text has fewer than {SHORT_TEXT_WORDS} words",
            language=chosen,
            count=0,
            markers={},
            density_per_1000=0.0,
            floor_count=None,
            meets_floor=None,
        )
    details = count_phrase_details(text, HUMAN_MARKERS[chosen])
    if chosen == "ru":
        particle_to = len(re.findall(r"(?<=[А-Яа-яЁё])-(?:то)\b", text, flags=re.IGNORECASE))
        if particle_to:
            details["-то"] = particle_to
    details = dict(sorted(details.items()))
    count = sum(details.values())
    floor_count = max(1, math.ceil(word_count / 500))
    return {
        "abstained": False,
        "reason": None,
        "word_count": word_count,
        "language": chosen,
        "count": count,
        "markers": details,
        "density_per_1000": _rounded(count * 1000 / word_count),
        "floor_count": floor_count,
        "meets_floor": count >= floor_count,
    }


def punctuation_entropy(text: str, language: str | None = "auto") -> dict[str, Any]:
    """Return base-2 Shannon entropy over coarse punctuation categories."""

    chosen = _resolve_language(text, language)
    word_count = len(words(text))
    if word_count < SHORT_TEXT_WORDS:
        return _abstained(
            word_count,
            f"text has fewer than {SHORT_TEXT_WORDS} words",
            language=chosen,
            entropy=0.0,
            punctuation_total=0,
            distribution={},
        )
    # URLs have their own punctuation conventions and would otherwise inflate a
    # prose-style metric.  ASCII hyphens inside words are excluded for the same
    # reason.
    cleaned = _URL_RE.sub("", text)
    distribution: Counter[str] = Counter()
    categories = {
        ".": "period",
        "…": "ellipsis",
        ",": "comma",
        ";": "semicolon",
        ":": "colon",
        "?": "question",
        "!": "exclamation",
        "—": "dash",
        "–": "dash",
        "(": "parenthesis",
        ")": "parenthesis",
        "[": "bracket",
        "]": "bracket",
        "{": "brace",
        "}": "brace",
        '"': "quote",
        "'": "quote",
        "«": "quote",
        "»": "quote",
        "“": "quote",
        "”": "quote",
        "„": "quote",
        "‘": "quote",
        "’": "quote",
    }
    for char in cleaned:
        if char in categories:
            distribution[categories[char]] += 1
    distribution["dash"] += len(re.findall(r"(?<!\w)-(?!\w)", cleaned))
    if not distribution["dash"]:
        del distribution["dash"]
    total = sum(distribution.values())
    entropy = (
        -sum((count / total) * math.log2(count / total) for count in distribution.values())
        if total
        else 0.0
    )
    return {
        "abstained": False,
        "reason": None,
        "word_count": word_count,
        "language": chosen,
        "entropy": _rounded(entropy),
        "punctuation_total": total,
        "distribution": _counter_json(distribution),
    }


def windowed_ttr(
    text: str,
    window_size: int = 100,
    step: int | None = None,
) -> dict[str, Any]:
    """Compute case-folded TTR over deterministic full token windows.

    The default uses non-overlapping 100-token windows.  A partial tail is not a
    window because its systematically higher TTR would create a length confound.
    """

    if window_size <= 0:
        raise ValueError("window_size must be positive")
    if step is None:
        step = window_size
    if step <= 0:
        raise ValueError("step must be positive")
    token_list = [token.casefold() for token in words(text)]
    word_count = len(token_list)
    if word_count < SHORT_TEXT_WORDS or word_count < window_size:
        return _abstained(
            word_count,
            f"text has fewer than {max(SHORT_TEXT_WORDS, window_size)} words",
            window_size=window_size,
            step=step,
            num_windows=0,
            windows=[],
            mean_ttr=0.0,
            ttr_sd=0.0,
        )
    values = [
        _rounded(len(set(token_list[start : start + window_size])) / window_size)
        for start in range(0, word_count - window_size + 1, step)
    ]
    return {
        "abstained": False,
        "reason": None,
        "word_count": word_count,
        "window_size": window_size,
        "step": step,
        "num_windows": len(values),
        "windows": values,
        "mean_ttr": _mean(values),
        "ttr_sd": _pstdev(values),
        "min_ttr": min(values),
        "max_ttr": max(values),
    }


def content_function_ratio(text: str, language: str | None = "auto") -> dict[str, Any]:
    """Approximate content/function ratio with explicit stdlib word lists.

    This is not a true POS/Biber feature.  Alphabetic tokens absent from the
    selected function-word list are treated as content words.
    """

    chosen = _resolve_language(text, language)
    token_list = [token.casefold() for token in words(text) if token[0].isalpha()]
    word_count = len(words(text))
    if word_count < SHORT_TEXT_WORDS:
        return _abstained(
            word_count,
            f"text has fewer than {SHORT_TEXT_WORDS} words",
            language=chosen,
            ratio=None,
            content_words=0,
            function_words=0,
        )
    function_count = sum(1 for token in token_list if token in FUNCTION_WORDS[chosen])
    content_count = len(token_list) - function_count
    if function_count == 0:
        return _abstained(
            word_count,
            "no recognized function words",
            language=chosen,
            ratio=None,
            content_words=content_count,
            function_words=0,
        )
    return {
        "abstained": False,
        "reason": None,
        "word_count": word_count,
        "language": chosen,
        "ratio": _rounded(content_count / function_count),
        "content_words": content_count,
        "function_words": function_count,
        "classified_words": len(token_list),
        "approximation": "explicit function-word list; no POS tagger",
    }


def _normalized_genre(genre: str | None) -> str | None:
    return genre.casefold().strip() if genre else None


def digit_density(
    text: str,
    language: str | None = "auto",
    genre: str | None = None,
) -> dict[str, Any]:
    """Measure digit characters per 1,000 words in scientific genres only."""

    chosen = _resolve_language(text, language)
    word_count = len(words(text))
    normalized_genre = _normalized_genre(genre)
    base = {
        "language": chosen,
        "genre": genre,
        "digit_count": 0,
        "numeric_token_count": 0,
        "density_per_1000": 0.0,
    }
    if word_count < SHORT_TEXT_WORDS:
        return _abstained(
            word_count, f"text has fewer than {SHORT_TEXT_WORDS} words", **base
        )
    if normalized_genre not in SCIENTIFIC_DIGIT_GENRES:
        return _abstained(word_count, "genre gate: scientific genres only", **base)
    digit_count = sum(char.isdigit() for char in text)
    numeric_tokens = sum(1 for token in words(text) if token[0].isdigit())
    return {
        "abstained": False,
        "reason": None,
        "word_count": word_count,
        "language": chosen,
        "genre": genre,
        "digit_count": digit_count,
        "numeric_token_count": numeric_tokens,
        "density_per_1000": _rounded(digit_count * 1000 / word_count),
        "zero_digit_signal": digit_count == 0,
    }


def participial_stack_rate(
    text: str,
    genre: str | None = None,
    language: str | None = "auto",
) -> dict[str, Any]:
    """Count EN sentences with multiple comma-linked present participles.

    News/journalism and résumé genres abstain.  Technical documentation uses the
    stricter three-clause threshold required by pattern ##68; other genres use
    two.  Russian abstains because ``-ing`` is an English-only fingerprint.
    """

    chosen = _resolve_language(text, language)
    word_count = len(words(text))
    normalized_genre = _normalized_genre(genre)
    stack_threshold = 3 if normalized_genre in PARTICIPIAL_TECH_GENRES else 2
    base = {
        "language": chosen,
        "genre": genre,
        "stack_threshold": stack_threshold,
        "clause_count": 0,
        "stack_count": 0,
        "rate_per_500": 0.0,
        "sentence_clause_counts": [],
        "flagged": None,
    }
    if word_count < SHORT_TEXT_WORDS:
        return _abstained(
            word_count, f"text has fewer than {SHORT_TEXT_WORDS} words", **base
        )
    if chosen != "en":
        return _abstained(word_count, "language gate: English only", **base)
    if normalized_genre in PARTICIPIAL_NEUTRAL_GENRES:
        return _abstained(word_count, "genre gate: neutral participial rate", **base)

    sentence_counts: list[int] = []
    pattern = re.compile(
        r"(?:^|[,;:]\s+)(?:(?:by|while|when|thereby)\s+)?[A-Za-z]+ing\b",
        flags=re.IGNORECASE,
    )
    for sentence in split_sentences(text):
        sentence_counts.append(len(pattern.findall(sentence)))
    clause_count = sum(sentence_counts)
    stack_count = sum(1 for count in sentence_counts if count >= stack_threshold)
    return {
        "abstained": False,
        "reason": None,
        "word_count": word_count,
        "language": chosen,
        "genre": genre,
        "stack_threshold": stack_threshold,
        "clause_count": clause_count,
        "stack_count": stack_count,
        "rate_per_500": _rounded(stack_count * 500 / word_count),
        "sentence_clause_counts": sentence_counts,
        "flagged": stack_count > 0,
    }


def that_clause_subject_rate(
    text: str,
    genre: str | None = None,
    language: str | None = "auto",
) -> dict[str, Any]:
    """Count sentence-initial English ``That [clause] is/was ...`` subjects."""

    chosen = _resolve_language(text, language)
    word_count = len(words(text))
    normalized_genre = _normalized_genre(genre)
    threshold_per_500 = 2.0 if normalized_genre in {"academic", "scientific"} else 1.0
    base = {
        "language": chosen,
        "genre": genre,
        "count": 0,
        "rate_per_500": 0.0,
        "threshold_per_500": threshold_per_500,
        "flagged": None,
    }
    if word_count < SHORT_TEXT_WORDS:
        return _abstained(
            word_count, f"text has fewer than {SHORT_TEXT_WORDS} words", **base
        )
    if chosen != "en":
        return _abstained(word_count, "language gate: English only", **base)
    if normalized_genre in THAT_SUBJECT_NEUTRAL_GENRES:
        return _abstained(word_count, "genre gate: formal argumentative register", **base)

    pattern = re.compile(
        r"^\s*[\"'“‘(\[]*That\s+"
        r"(?:[A-Za-z][A-Za-z'-]*\s+){2,20}"
        r"(?:is|are|was|were|seems|appears|remains)\b",
        flags=re.IGNORECASE,
    )
    count = sum(1 for sentence in split_sentences(text) if pattern.search(sentence))
    rate = _rounded(count * 500 / word_count)
    return {
        "abstained": False,
        "reason": None,
        "word_count": word_count,
        "language": chosen,
        "genre": genre,
        "count": count,
        "rate_per_500": rate,
        "threshold_per_500": threshold_per_500,
        "flagged": rate > threshold_per_500,
    }


_RU_GERUND_LEAD_RE = re.compile(
    r"^\s*[«\"“'(\[]*(?:не\s+)?"
    r"(?P<gerund>[А-ЯЁа-яё-]{3,})\b"
    r"(?P<modifier>[^,]{0,160}),\s*(?P<main>.+)$",
    flags=re.IGNORECASE,
)
_RU_GERUND_SUFFIX_RE = re.compile(
    r"(?:[аяеиоуыю]в(?:ши)?(?:сь)?|ши(?:сь)?|уя(?:сь)?|яя(?:сь)?|"
    r"учи(?:сь)?|ючи(?:сь)?)$",
    flags=re.IGNORECASE,
)
_RU_COMMON_GERUNDS = frozenset(
    {
        "благодаря",
        "ведя",
        "глядя",
        "говоря",
        "делая",
        "идя",
        "исходя",
        "лежа",
        "начиная",
        "неся",
        "сидя",
        "стоя",
        "судя",
    }
)
_RU_ANIMATE_MAIN_RE = re.compile(
    r"^(?:я|мы|ты|вы|он|она|они|автор(?:ы)?|команда|исследовател[ьи]|"
    r"участни(?:к|ки)|разработчи(?:к|ки)|редактор(?:ы)?|врач(?:и)?|учён(?:ый|ые)|учен(?:ый|ые))\b",
    flags=re.IGNORECASE,
)
_RU_INANIMATE_MAIN_RE = re.compile(
    r"^(?:результат(?:ы)?|эффективность|значени[ея]|данные|метод|методика|"
    r"система|показател[ьи]|точность|скорость|качество|уровень|ошибк[аи]|"
    r"выборка|гипотеза|задача|модель|таблица|оценка|производительность)\b",
    flags=re.IGNORECASE,
)
_RU_IMPERSONAL_RE = re.compile(
    r"\b(?:можно|нужно|необходимо|следует|удалось|оказалось|получилось|"
    r"был[аио]?|были|будет|будут)\b|\b[а-яё]+(?:ется|ются)\b",
    flags=re.IGNORECASE,
)


def dangling_russian_participle(
    text: str,
    language: str | None = "auto",
) -> dict[str, Any]:
    """Flag likely dangling Russian adverbial-participle constructions.

    Unlike distributional style metrics, this local grammar check deliberately
    does not abstain below 100 words: pattern ##70 applies to a single sentence
    in every genre.  It still has a hard language gate and reports evidence so a
    reviewer can dismiss false positives.
    """

    chosen = _resolve_language(text, language)
    word_count = len(words(text))
    if chosen != "ru":
        return _abstained(
            word_count,
            "language gate: Russian only",
            language=chosen,
            count=0,
            matches=[],
        )

    matches: list[dict[str, Any]] = []
    for index, sentence in enumerate(split_sentences(text), start=1):
        match = _RU_GERUND_LEAD_RE.match(sentence)
        if not match:
            continue
        gerund = match.group("gerund")
        if not (
            _RU_GERUND_SUFFIX_RE.search(gerund)
            or gerund.casefold() in _RU_COMMON_GERUNDS
        ):
            continue
        main = match.group("main").strip()
        if _RU_ANIMATE_MAIN_RE.match(main):
            continue
        inanimate = _RU_INANIMATE_MAIN_RE.match(main)
        impersonal = _RU_IMPERSONAL_RE.search(main)
        if not inanimate and not impersonal:
            continue
        matches.append(
            {
                "sentence_index": index,
                "gerund": gerund,
                "main_clause": main,
                "reason": (
                    "inanimate matrix subject"
                    if inanimate
                    else "impersonal/passive matrix clause"
                ),
            }
        )
    return {
        "abstained": False,
        "reason": None,
        "word_count": word_count,
        "language": chosen,
        "count": len(matches),
        "matches": matches,
    }


def _protect_abbreviations(text: str) -> str:
    """Hide dots inside common abbreviations and name initials from splitting."""

    protected = text

    def hide_all_dots(match: re.Match[str]) -> str:
        return match.group(0).replace(".", _PROTECTED_DOT)

    # In Russian, ``т. д.`` / ``т. е.`` may also finish a sentence.  Preserve
    # the final dot when an uppercase sentence clearly follows, while hiding it
    # in the ordinary mid-sentence case.
    russian_abbreviation = re.compile(r"(?<!\w)(?:т\.\s*д\.|т\.\s*е\.|т\.\s*п\.)(?!\w)", re.IGNORECASE)

    def hide_russian_abbreviation(match: re.Match[str]) -> str:
        value = match.group(0).replace(".", _PROTECTED_DOT)
        following = match.string[match.end() :]
        if re.match(r"\s+[А-ЯЁ]", following):
            last = value.rfind(_PROTECTED_DOT)
            value = value[:last] + "." + value[last + 1 :]
        return value

    protected = russian_abbreviation.sub(hide_russian_abbreviation, protected)

    abbreviation_patterns = (
        r"(?<!\w)(?:e\.\s*g\.|i\.\s*e\.)(?!\w)",
        r"(?<!\w)(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St)\.",
        r"(?<!\w)(?:г|ул|стр|рис|им|тов)\.(?=\s*[А-ЯЁ0-9])",
    )
    for pattern in abbreviation_patterns:
        protected = re.sub(pattern, hide_all_dots, protected, flags=re.IGNORECASE)

    # One to four initials before a surname: A. S. Pushkin / А. С. Пушкин.
    initials_before_surname = re.compile(
        r"(?<!\w)(?:[A-ZА-ЯЁ]\.[ \t]*){1,4}(?=[A-ZА-ЯЁ][a-zа-яё])"
    )
    protected = initials_before_surname.sub(hide_all_dots, protected)
    return protected


def split_sentences(text: str) -> list[str]:
    """Split prose without breaking e.g., i.e., т. д., т. е., or initials.

    The splitter is conservative: it needs terminal punctuation followed by an
    uppercase letter, a digit, a Markdown list marker, or a paragraph boundary.
    This is preferable for evaluation because a false split distorts every rhythm
    metric that follows.
    """

    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        return []
    protected = _protect_abbreviations(normalized)
    pieces: list[str] = []
    start = 0

    for match in re.finditer(r"\s+", protected):
        left = protected[start : match.start()].rstrip()
        right = protected[match.end() :]
        if not left or not right:
            continue

        terminal_probe = re.sub(r"[»”\"')\]}]+$", "", left)
        terminal = terminal_probe[-1:] in ".!?…"
        paragraph_break = "\n\n" in match.group(0)
        next_probe = right.lstrip("«“\"'([{ ")
        starts_sentence = bool(re.match(r"(?:[-*+]\s+|\d+[.)]\s+)?[A-ZА-ЯЁ0-9]", next_probe))
        if terminal and (starts_sentence or paragraph_break):
            pieces.append(left.replace(_PROTECTED_DOT, ".").strip())
            start = match.end()

    tail = protected[start:].strip()
    if tail:
        pieces.append(tail.replace(_PROTECTED_DOT, "."))
    return [piece for piece in pieces if piece]


def split_paragraphs(text: str) -> list[str]:
    """Return non-empty Markdown/prose paragraphs."""

    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    return [part.strip() for part in re.split(r"\n\s*\n+", normalized) if part.strip()]


def _sentence_opener_counts(sentences: Sequence[str], phrases: Sequence[str]) -> tuple[int, dict[str, int]]:
    details: Counter[str] = Counter()
    ordered = sorted(phrases, key=lambda item: (-len(item), item))
    for sentence in sentences:
        candidate = sentence.lstrip(" \t\n\r«“\"'([{-*").casefold()
        for phrase in ordered:
            pattern = re.compile(rf"^{re.escape(phrase.casefold()).replace(r'\ ', r'\s+')}\b")
            if pattern.search(candidate):
                details[phrase] += 1
                break
    return sum(details.values()), dict(sorted(details.items()))


def _count_non_guillemets(text: str) -> int:
    straight_pairs = text.count('"') // 2
    english_curly_pairs = min(text.count("“"), text.count("”"))
    low_high_pairs = min(text.count("„"), text.count("“"))
    return straight_pairs + english_curly_pairs + low_high_pairs


def _count_ru_odnako_comma(sentences: Sequence[str]) -> int:
    return sum(
        1
        for sentence in sentences
        if re.match(r"^\s*[«“\"'(\[]*однако\s*,", sentence, flags=re.IGNORECASE)
    )


def _count_capital_after_colon(text: str) -> int:
    # Quote/list starts are excluded: a quotation after a colon may start uppercase.
    return len(re.findall(r":\s+(?![«“\"'\n\-*])[А-ЯЁA-Z](?=[а-яёa-z])", text))


def _count_participial_clauses(text: str, language: str) -> int:
    if language == "en":
        return len(re.findall(r",\s+(?:thereby\s+)?[a-z]+ing\b", text, flags=re.IGNORECASE))
    # Russian adverbial participles following a comma.  Requiring a comma avoids
    # treating ordinary words ending in -я/-в as clauses.
    return len(
        re.findall(
            r",\s+(?:не\s+)?[а-яё]{3,}(?:в|вши|ши|я)(?:сь)?\b",
            text,
            flags=re.IGNORECASE,
        )
    )


def _count_nominalizations(text: str, language: str) -> int:
    tokens = [token.casefold() for token in words(text) if token[0].isalpha()]
    if language == "ru":
        pattern = re.compile(r"(?:ция|ции|ций|ние|ния|ний|ость|ости|остей|изация|изации)$")
    else:
        pattern = re.compile(r"(?:tion|sion|ment|ance|ence|ity|ness)s?$")
    return sum(1 for token in tokens if pattern.search(token))


def _count_agentless_passive(text: str, language: str) -> int:
    if language == "ru":
        impersonal = re.findall(
            r"\b(?:можно|нужно|следует|необходимо|принято|решено|установлено|показано|"
            r"обнаружено|получено|разработано|предложено|рассмотрено)\b",
            text,
            flags=re.IGNORECASE,
        )
        analytic = re.findall(
            r"\b(?:был|была|было|были|будет|будут)\s+[а-яё]+(?:н|т)[аоыи]\b",
            text,
            flags=re.IGNORECASE,
        )
        return len(impersonal) + len(analytic)
    return len(
        re.findall(
            r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+\s+){0,2}\w+(?:ed|en)\b",
            text,
            flags=re.IGNORECASE,
        )
    )


def _check(
    value: float | int,
    operator: str,
    target: float | int | None,
    *,
    applicable: bool = True,
    description: str,
) -> dict[str, Any]:
    if not applicable or target is None:
        passed: bool | None = None
    elif operator == ">=":
        passed = value >= target
    elif operator == "<=":
        passed = value <= target
    elif operator == "==":
        passed = value == target
    else:  # pragma: no cover - internal programming error
        raise ValueError(f"unsupported operator: {operator}")
    return {
        "value": value,
        "operator": operator,
        "target": target,
        "applicable": applicable,
        "passed": passed,
        "description": description,
    }


def _check_score(checks: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    applicable = [item for item in checks.values() if item["applicable"]]
    passed = sum(1 for item in applicable if item["passed"])
    return {
        "passed": passed,
        "applicable": len(applicable),
        "rate": _rounded(passed / len(applicable)) if applicable else 1.0,
    }


def metrics(text: str, genre: str | None = None, language: str | None = None) -> dict[str, Any]:
    """Profile one text and return a stable JSON-serializable dictionary."""

    language = _resolve_language(text, language)
    normalized_genre = _normalized_genre(genre)

    sentence_list = split_sentences(text)
    paragraph_list = split_paragraphs(text)
    token_list = words(text)
    sentence_lengths = [len(words(sentence)) for sentence in sentence_list]
    paragraph_lengths = [len(words(paragraph)) for paragraph in paragraph_list]
    word_count = len(token_list)
    sentence_count = len(sentence_list)

    connector_details = count_phrase_details(text, CONNECTORS[language])
    hedge_details = count_phrase_details(text, HEDGES[language])
    booster_details = count_phrase_details(text, BOOSTERS[language])
    connector_openers, connector_opener_details = _sentence_opener_counts(
        sentence_list, CONNECTORS[language]
    )

    participial_clauses = _count_participial_clauses(text, language)
    nominalizations = _count_nominalizations(text, language)
    agentless_passive = _count_agentless_passive(text, language)
    em_dashes = text.count("—") + text.count("–")
    curly_quotes = sum(text.count(char) for char in "“”‘’")

    sentence_sd = _pstdev(sentence_lengths)
    sentence_mean = _mean(sentence_lengths)
    paragraph_sd = _pstdev(paragraph_lengths)
    paragraph_mean = _mean(paragraph_lengths)
    burstiness = _rounded(sentence_sd / sentence_mean) if sentence_mean else 0.0
    connector_density = _rounded(connector_openers / sentence_count) if sentence_count else 0.0
    participial_rate = _rounded(participial_clauses * 250 / word_count) if word_count else 0.0
    passive_rate = _rounded(agentless_passive * 100 / word_count) if word_count else 0.0

    # Russian deliberately receives softer rhythm thresholds.  Long sentences are
    # reported but never penalized; Pattern 40's short-sentence pressure is not
    # portable to Russian prose.
    sd_target = 5.0 if language == "ru" else 8.0
    paragraph_sd_target = 18.0 if language == "ru" else 25.0
    long_threshold = 32 if language == "ru" else 25
    short_threshold = 7 if language == "ru" else 5

    structural_checks = {
        "sentence_length_sd": _check(
            sentence_sd,
            ">=",
            sd_target,
            applicable=sentence_count >= 3,
            description="sentence-length variation; Russian uses a softer floor",
        ),
        "paragraph_length_sd": _check(
            paragraph_sd,
            ">=",
            paragraph_sd_target,
            applicable=len(paragraph_list) >= 3,
            description="visible paragraph-length variation",
        ),
        "connector_opener_density": _check(
            connector_density,
            "<=",
            0.35,
            applicable=sentence_count >= 2,
            description="share of sentences opened by an explicit connector",
        ),
        "participial_clauses_per_250_words": _check(
            participial_rate,
            "<=",
            1.5
            if language == "ru" or normalized_genre in PARTICIPIAL_TECH_GENRES
            else 1.0,
            applicable=(
                word_count >= 40
                and not (
                    language == "en"
                    and normalized_genre in PARTICIPIAL_NEUTRAL_GENRES
                )
            ),
            description=(
                "trailing participial/deverbal clauses per 250 words; "
                "English news, journalism, résumés, and cover letters are neutral"
            ),
        ),
        "agentless_passive_per_100_words": _check(
            passive_rate,
            "<=",
            None if language == "ru" else 2.5,
            applicable=language == "en" and word_count >= 40,
            description=(
                "informational for Russian: agentless passive is not penalized"
                if language == "ru"
                else "English agentless-passive density"
            ),
        ),
    }

    ru_odnako = _count_ru_odnako_comma(sentence_list) if language == "ru" else 0
    ru_colon_capital = _count_capital_after_colon(text) if language == "ru" else 0
    ru_non_guillemets = _count_non_guillemets(text) if language == "ru" else 0
    ru_frames = count_phrases(text, RU_FRAME_PHRASES) if language == "ru" else 0
    en_ai_phrases = count_phrases(text, EN_AI_PHRASES) if language == "en" else 0
    tell_total = ru_odnako + ru_colon_capital + ru_non_guillemets + ru_frames + en_ai_phrases

    booster_applicable = normalized_genre in BOOSTER_TARGET_GENRES
    ru_dash_limit = max(1, math.ceil(max(sentence_count, 1) * 0.75))
    compliance_checks = {
        "em_dashes": _check(
            em_dashes,
            "<=",
            ru_dash_limit if language == "ru" else None,
            applicable=language == "ru",
            description=(
                "Russian dashes are allowed up to an overuse guard"
                if language == "ru"
                else "legacy corroboration only for English; no pass/fail target"
            ),
        ),
        "curly_quotes": _check(
            curly_quotes,
            "==",
            0,
            description="skill-level English curly-quote compliance",
        ),
        "boosters": _check(
            sum(booster_details.values()),
            ">=",
            1,
            applicable=booster_applicable,
            description=(
                "genre-gated confidence marker; only voice-led genres are scored"
            ),
        ),
        "ru_quote_style": _check(
            ru_non_guillemets,
            "==",
            0,
            applicable=language == "ru",
            description="Russian quotations use «ёлочки», not straight/English curly pairs",
        ),
        "ru_capital_after_colon": _check(
            ru_colon_capital,
            "==",
            0,
            applicable=language == "ru",
            description="lowercase after a Russian colon unless quoted/proper",
        ),
        "ru_odnako_comma": _check(
            ru_odnako,
            "==",
            0,
            applicable=language == "ru",
            description="sentence-initial «Однако» is not followed by a comma",
        ),
    }

    diagnostics = {
        "short_text_abstention": word_count < SHORT_TEXT_WORDS,
        "human_marker_floor": human_marker_floor(text, language),
        "punctuation_entropy": punctuation_entropy(text, language),
        "windowed_ttr": windowed_ttr(text),
        "content_function_ratio": content_function_ratio(text, language),
        "digit_density": digit_density(text, language, genre),
        "participial_stack_rate": participial_stack_rate(text, genre, language),
        "that_clause_subject_rate": that_clause_subject_rate(text, genre, language),
        "dangling_russian_participle": dangling_russian_participle(text, language),
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "language": language,
        "cyrillic_ratio": cyrillic_ratio(text),
        "genre": genre,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "paragraph_count": len(paragraph_list),
        "structural": {
            "sentence_lengths": sentence_lengths,
            "paragraph_lengths": paragraph_lengths,
            "sentence_length_mean": sentence_mean,
            "sentence_length_sd": sentence_sd,
            "sentence_burstiness": burstiness,
            "paragraph_length_mean": paragraph_mean,
            "paragraph_length_sd": paragraph_sd,
            "short_sentence_threshold": short_threshold,
            "long_sentence_threshold": long_threshold,
            "short_sentences": sum(1 for value in sentence_lengths if value <= short_threshold),
            "long_sentences": sum(1 for value in sentence_lengths if value >= long_threshold),
            "connectors_total": sum(connector_details.values()),
            "connector_openers": connector_openers,
            "connector_opener_density": connector_density,
            "participial_clauses": participial_clauses,
            "participial_clauses_per_250_words": participial_rate,
            "nominalizations": nominalizations,
            "agentless_passive": agentless_passive,
            "agentless_passive_per_100_words": passive_rate,
            "checks": structural_checks,
            "score": _check_score(structural_checks),
        },
        "lexical": {
            "connectors_total": sum(connector_details.values()),
            "connectors": connector_details,
            "connector_openers": connector_openers,
            "connector_opener_phrases": connector_opener_details,
            "hedges_total": sum(hedge_details.values()),
            "hedges": hedge_details,
            "boosters_total": sum(booster_details.values()),
            "boosters": booster_details,
        },
        "tells": {
            "ru_odnako_comma": ru_odnako,
            "ru_capital_after_colon": ru_colon_capital,
            "ru_non_guillemets": ru_non_guillemets,
            "ru_frame_phrases": ru_frames,
            "en_ai_phrases": en_ai_phrases,
            "total": tell_total,
        },
        "compliance": {
            "em_dashes": em_dashes,
            "curly_quotes": curly_quotes,
            "boosters_total": sum(booster_details.values()),
            "checks": compliance_checks,
            "score": _check_score(compliance_checks),
        },
        # Additive schema-v1 diagnostics: existing structural/compliance keys and
        # score semantics remain unchanged, so v2.20 baselines stay comparable.
        "diagnostics": diagnostics,
    }


def _comparison_block(
    before_checks: Mapping[str, Mapping[str, Any]],
    after_checks: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    items: dict[str, Any] = {}
    for name in sorted(set(before_checks) | set(after_checks)):
        before = before_checks[name]
        after = after_checks[name]
        delta = _rounded(float(after["value"]) - float(before["value"]))
        operator = after["operator"]
        improved = None
        if before["applicable"] or after["applicable"]:
            if operator == ">=":
                improved = delta > 0
            elif operator in {"<=", "=="}:
                improved = delta < 0
            if before["passed"] is False and after["passed"] is True:
                improved = True
            elif before["passed"] is True and after["passed"] is False:
                improved = False
        items[name] = {
            "before": before,
            "after": after,
            "delta": delta,
            "improved": improved,
        }
    return {
        "before_score": _check_score(before_checks),
        "after_score": _check_score(after_checks),
        "score_delta": _rounded(
            _check_score(after_checks)["rate"] - _check_score(before_checks)["rate"]
        ),
        "metrics": items,
    }


_DIAGNOSTIC_VALUE_FIELDS = {
    "human_marker_floor": "count",
    "punctuation_entropy": "entropy",
    "windowed_ttr": "mean_ttr",
    "content_function_ratio": "ratio",
    "digit_density": "density_per_1000",
    "participial_stack_rate": "rate_per_500",
    "that_clause_subject_rate": "rate_per_500",
    "dangling_russian_participle": "count",
}


def _diagnostic_comparison(
    before_diagnostics: Mapping[str, Any],
    after_diagnostics: Mapping[str, Any],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name, value_field in _DIAGNOSTIC_VALUE_FIELDS.items():
        before = before_diagnostics[name]
        after = after_diagnostics[name]
        before_value = before.get(value_field)
        after_value = after.get(value_field)
        applicable = (
            not before.get("abstained", False)
            and not after.get("abstained", False)
            and before_value is not None
            and after_value is not None
        )
        delta = (
            _rounded(float(after_value) - float(before_value)) if applicable else None
        )
        result[name] = {
            "value_field": value_field,
            "applicable": applicable,
            "before_value": before_value,
            "after_value": after_value,
            "delta": delta,
            "before": before,
            "after": after,
        }
    return result


def compare_texts(
    before: str,
    after: str,
    genre: str | None = None,
    language: str | None = None,
    *,
    pair_id: str | None = None,
) -> dict[str, Any]:
    """Compare two texts using one detected/forced language and grouped blocks."""

    chosen_language = _resolve_language(before + "\n" + after, language)
    before_profile = metrics(before, genre=genre, language=chosen_language)
    after_profile = metrics(after, genre=genre, language=chosen_language)
    immutable_audit = immutable_token_audit(before, after)
    tell_names = sorted(set(before_profile["tells"]) | set(after_profile["tells"]))
    tells = {
        name: {
            "before": before_profile["tells"].get(name, 0),
            "after": after_profile["tells"].get(name, 0),
            "delta": after_profile["tells"].get(name, 0) - before_profile["tells"].get(name, 0),
        }
        for name in tell_names
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "command": "compare",
        "id": pair_id,
        "genre": genre,
        "language": chosen_language,
        "counts": {
            "before_words": before_profile["word_count"],
            "after_words": after_profile["word_count"],
            "before_sentences": before_profile["sentence_count"],
            "after_sentences": after_profile["sentence_count"],
        },
        "structural": _comparison_block(
            before_profile["structural"]["checks"], after_profile["structural"]["checks"]
        ),
        "compliance": _comparison_block(
            before_profile["compliance"]["checks"], after_profile["compliance"]["checks"]
        ),
        "integrity": {"immutable_token_audit": immutable_audit},
        "diagnostics": _diagnostic_comparison(
            before_profile["diagnostics"], after_profile["diagnostics"]
        ),
        "tells": tells,
        "profiles": {"before": before_profile, "after": after_profile},
    }


def load_corpus(corpus: str | Path = DEFAULT_CORPUS) -> list[dict[str, Any]]:
    """Load deterministic ``*.json`` corpus pairs, sorted by id/path."""

    corpus_path = Path(corpus)
    if not corpus_path.is_dir():
        raise ValueError(f"corpus directory does not exist: {corpus_path}")
    pairs: list[dict[str, Any]] = []
    for path in sorted(corpus_path.rglob("*.json"), key=lambda item: item.as_posix().casefold()):
        with path.open("r", encoding="utf-8") as handle:
            item = json.load(handle)
        missing = [key for key in ("id", "genre", "before", "after") if not item.get(key)]
        if missing:
            raise ValueError(f"{path}: missing non-empty fields: {', '.join(missing)}")
        item = dict(item)
        item["_path"] = path
        pairs.append(item)
    pairs.sort(key=lambda item: (str(item["id"]).casefold(), item["_path"].as_posix().casefold()))
    if not pairs:
        raise ValueError(f"no JSON corpus pairs found in: {corpus_path}")
    duplicate_ids = [name for name, count in Counter(str(item["id"]) for item in pairs).items() if count > 1]
    if duplicate_ids:
        raise ValueError(f"duplicate corpus ids: {', '.join(sorted(duplicate_ids))}")
    return pairs


def _aggregate_check_block(comparisons: Sequence[Mapping[str, Any]], block_name: str) -> dict[str, Any]:
    names = sorted(
        {
            name
            for comparison in comparisons
            for name in comparison[block_name]["metrics"].keys()
        }
    )
    result: dict[str, Any] = {}
    before_passed = before_applicable = after_passed = after_applicable = 0
    for name in names:
        entries = [comparison[block_name]["metrics"][name] for comparison in comparisons]
        before_entries = [entry["before"] for entry in entries if entry["before"]["applicable"]]
        after_entries = [entry["after"] for entry in entries if entry["after"]["applicable"]]
        b_passed = sum(1 for entry in before_entries if entry["passed"])
        a_passed = sum(1 for entry in after_entries if entry["passed"])
        before_passed += b_passed
        before_applicable += len(before_entries)
        after_passed += a_passed
        after_applicable += len(after_entries)
        before_mean = _mean([entry["value"] for entry in before_entries])
        after_mean = _mean([entry["value"] for entry in after_entries])
        result[name] = {
            "before_mean": before_mean,
            "after_mean": after_mean,
            "delta": _rounded(after_mean - before_mean),
            "before_passed": b_passed,
            "before_applicable": len(before_entries),
            "before_pass_rate": _rounded(b_passed / len(before_entries)) if before_entries else None,
            "after_passed": a_passed,
            "after_applicable": len(after_entries),
            "after_pass_rate": _rounded(a_passed / len(after_entries)) if after_entries else None,
        }
    before_rate = _rounded(before_passed / before_applicable) if before_applicable else 1.0
    after_rate = _rounded(after_passed / after_applicable) if after_applicable else 1.0
    return {
        "before_score": {
            "passed": before_passed,
            "applicable": before_applicable,
            "rate": before_rate,
        },
        "after_score": {
            "passed": after_passed,
            "applicable": after_applicable,
            "rate": after_rate,
        },
        "score_delta": _rounded(after_rate - before_rate),
        "metrics": result,
    }


def _aggregate_diagnostic_block(comparisons: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Aggregate applicable diagnostic values without inventing pass targets."""

    result: dict[str, Any] = {}
    for name, value_field in _DIAGNOSTIC_VALUE_FIELDS.items():
        entries = [comparison["diagnostics"][name] for comparison in comparisons]
        paired_entries = [entry for entry in entries if entry["applicable"]]
        before_values = [
            entry["before_value"]
            for entry in entries
            if not entry["before"].get("abstained", False)
            and entry["before_value"] is not None
        ]
        after_values = [
            entry["after_value"]
            for entry in entries
            if not entry["after"].get("abstained", False)
            and entry["after_value"] is not None
        ]
        before_mean = _mean(before_values)
        after_mean = _mean(after_values)
        result[name] = {
            "value_field": value_field,
            "before_mean": before_mean,
            "after_mean": after_mean,
            # Compute change only on pairs for which both sides are applicable;
            # otherwise short-text or genre abstention would confound the delta.
            "delta": _mean([entry["delta"] for entry in paired_entries])
            if paired_entries
            else None,
            "paired_applicable": len(paired_entries),
            "before_applicable": len(before_values),
            "after_applicable": len(after_values),
            "before_abstained": len(comparisons) - len(before_values),
            "after_abstained": len(comparisons) - len(after_values),
        }
    return result


def aggregate_corpus(corpus: str | Path = DEFAULT_CORPUS) -> dict[str, Any]:
    """Aggregate all JSON pairs in ``corpus`` with separate metric families."""

    pairs = load_corpus(corpus)
    comparisons = [
        compare_texts(
            item["before"],
            item["after"],
            genre=item.get("genre"),
            language=item.get("language", "auto"),
            pair_id=str(item["id"]),
        )
        for item in pairs
    ]
    language_counts = Counter(str(comparison["language"]) for comparison in comparisons)
    genre_counts = Counter(str(item["genre"]) for item in pairs)
    tell_names = sorted(
        {name for comparison in comparisons for name in comparison["tells"] if name != "total"}
    )
    tell_metrics: dict[str, Any] = {}
    for name in tell_names:
        before_values = [comparison["tells"][name]["before"] for comparison in comparisons]
        after_values = [comparison["tells"][name]["after"] for comparison in comparisons]
        tell_metrics[name] = {
            "before_total": sum(before_values),
            "after_total": sum(after_values),
            "delta": sum(after_values) - sum(before_values),
            "before_mean": _mean(before_values),
            "after_mean": _mean(after_values),
        }
    before_tells = sum(comparison["tells"]["total"]["before"] for comparison in comparisons)
    after_tells = sum(comparison["tells"]["total"]["after"] for comparison in comparisons)

    length_matching: list[dict[str, Any]] = []
    warnings: list[str] = []
    for comparison in comparisons:
        before_words = comparison["counts"]["before_words"]
        after_words = comparison["counts"]["after_words"]
        denominator = max(before_words, after_words)
        difference_ratio = (
            _rounded(abs(before_words - after_words) / denominator) if denominator else 0.0
        )
        if difference_ratio > LENGTH_MISMATCH_THRESHOLD:
            item = {
                "id": comparison["id"],
                "before_words": before_words,
                "after_words": after_words,
                "difference_ratio": difference_ratio,
                "threshold": LENGTH_MISMATCH_THRESHOLD,
            }
            length_matching.append(item)
            warnings.append(
                f"{comparison['id']}: length mismatch {difference_ratio:.1%} > "
                f"{LENGTH_MISMATCH_THRESHOLD:.0%} "
                f"(before={before_words}, after={after_words} words)"
            )

    audits = [comparison["integrity"]["immutable_token_audit"] for comparison in comparisons]
    applicable_audits = [audit for audit in audits if not audit["abstained"]]
    integrity = {
        "immutable_token_audit": {
            "applicable": len(applicable_audits),
            "abstained": len(audits) - len(applicable_audits),
            "passed": sum(1 for audit in applicable_audits if audit["passed"]),
            "total_violations": sum(audit["total_violations"] for audit in applicable_audits),
        }
    }

    pair_summaries = [
        {
            "id": comparison["id"],
            "genre": comparison["genre"],
            "language": comparison["language"],
            "structural_before_rate": comparison["structural"]["before_score"]["rate"],
            "structural_after_rate": comparison["structural"]["after_score"]["rate"],
            "compliance_before_rate": comparison["compliance"]["before_score"]["rate"],
            "compliance_after_rate": comparison["compliance"]["after_score"]["rate"],
            "immutable_token_violations": comparison["integrity"]["immutable_token_audit"][
                "total_violations"
            ],
            "immutable_token_audit_abstained": comparison["integrity"][
                "immutable_token_audit"
            ]["abstained"],
            "tells_before": comparison["tells"]["total"]["before"],
            "tells_after": comparison["tells"]["total"]["after"],
        }
        for comparison in comparisons
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "command": "aggregate",
        "corpus": {
            "path": Path(corpus).as_posix(),
            "pairs": len(pairs),
            "languages": dict(sorted(language_counts.items())),
            "genres": dict(sorted(genre_counts.items())),
        },
        "structural": _aggregate_check_block(comparisons, "structural"),
        "compliance": _aggregate_check_block(comparisons, "compliance"),
        "integrity": integrity,
        "diagnostics": {
            "metrics": _aggregate_diagnostic_block(comparisons),
            "length_matching": length_matching,
        },
        "warnings": warnings,
        "tells": {
            "before_total": before_tells,
            "after_total": after_tells,
            "delta": after_tells - before_tells,
            "metrics": tell_metrics,
        },
        "pairs": pair_summaries,
    }


def check_baseline(current: Mapping[str, Any], baseline_path: str | Path) -> dict[str, Any]:
    """Compare aggregate quality gates and list every regression."""

    path = Path(baseline_path)
    with path.open("r", encoding="utf-8") as handle:
        baseline = json.load(handle)
    if baseline.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(
            f"baseline schema {baseline.get('schema_version')!r} != {SCHEMA_VERSION}"
        )
    regressions: list[str] = []
    if current["corpus"]["pairs"] < baseline["corpus"]["pairs"]:
        regressions.append(
            f"corpus pairs {current['corpus']['pairs']} < baseline {baseline['corpus']['pairs']}"
        )
    target_overrides = baseline.get("targets", {})
    for block_name in ("structural", "compliance"):
        actual = current[block_name]["after_score"]["rate"]
        expected = target_overrides.get(
            f"{block_name}_after_score_rate",
            baseline[block_name]["after_score"]["rate"],
        )
        if actual + 1e-9 < expected:
            regressions.append(f"{block_name} after score {actual} < baseline {expected}")
        baseline_metrics = baseline[block_name].get("metrics", {})
        current_metrics = current[block_name].get("metrics", {})
        for name, expected_metric in sorted(baseline_metrics.items()):
            if name not in current_metrics:
                regressions.append(f"{block_name}.{name} missing")
                continue
            expected_rate = expected_metric.get("after_pass_rate")
            actual_rate = current_metrics[name].get("after_pass_rate")
            if expected_rate is not None and (actual_rate is None or actual_rate + 1e-9 < expected_rate):
                regressions.append(
                    f"{block_name}.{name} after pass rate {actual_rate} < baseline {expected_rate}"
                )
    integrity_limit = target_overrides.get("immutable_token_violations_max")
    if integrity_limit is not None:
        actual_integrity = current["integrity"]["immutable_token_audit"]["total_violations"]
        if actual_integrity > integrity_limit:
            regressions.append(
                f"immutable-token violations {actual_integrity} > target {integrity_limit}"
            )
    actual_tells = current["tells"]["after_total"]
    expected_tells = baseline["tells"]["after_total"]
    if actual_tells > expected_tells:
        regressions.append(f"tells after total {actual_tells} > baseline {expected_tells}")
    return {
        "path": path.as_posix(),
        "passed": not regressions,
        "regressions": regressions,
    }


def _status(check: Mapping[str, Any]) -> str:
    if not check["applicable"]:
        return "n/a"
    return "PASS" if check["passed"] else "FAIL"


def format_profile(profile: Mapping[str, Any]) -> str:
    lines = [
        f"PROFILE [{profile['language'].upper()}]",
        f"words={profile['word_count']} sentences={profile['sentence_count']} "
        f"paragraphs={profile['paragraph_count']} cyrillic={profile['cyrillic_ratio']:.1%}",
        "",
        "STRUCTURAL",
    ]
    for name, check in profile["structural"]["checks"].items():
        lines.append(
            f"  {_status(check):4} {name}: {check['value']} {check['operator']} {check['target']}"
        )
    score = profile["structural"]["score"]
    lines.append(f"  score: {score['passed']}/{score['applicable']} ({score['rate']:.1%})")
    lines.extend(["", "COMPLIANCE"])
    for name, check in profile["compliance"]["checks"].items():
        lines.append(
            f"  {_status(check):4} {name}: {check['value']} {check['operator']} {check['target']}"
        )
    score = profile["compliance"]["score"]
    lines.append(f"  score: {score['passed']}/{score['applicable']} ({score['rate']:.1%})")
    lines.extend(
        [
            "",
            "LEXICAL / TELLS",
            f"  connectors={profile['lexical']['connectors_total']} "
            f"hedges={profile['lexical']['hedges_total']} "
            f"boosters={profile['lexical']['boosters_total']}",
            f"  tells={profile['tells']['total']} ({profile['tells']})",
        ]
    )
    diagnostics = profile.get("diagnostics", {})
    if diagnostics:
        lines.extend(["", "V2.21 DIAGNOSTICS"])
        for name, value_field in _DIAGNOSTIC_VALUE_FIELDS.items():
            item = diagnostics[name]
            value = item.get(value_field)
            status = f"abstain: {item['reason']}" if item["abstained"] else str(value)
            lines.append(f"  {name}: {status}")
    return "\n".join(lines)


def format_compare(comparison: Mapping[str, Any]) -> str:
    lines = [
        f"COMPARE [{comparison['language'].upper()}]"
        + (f" id={comparison['id']}" if comparison.get("id") else ""),
        f"words {comparison['counts']['before_words']} -> {comparison['counts']['after_words']}; "
        f"sentences {comparison['counts']['before_sentences']} -> {comparison['counts']['after_sentences']}",
    ]
    for block_name, heading in (("structural", "STRUCTURAL"), ("compliance", "COMPLIANCE")):
        block = comparison[block_name]
        lines.extend(["", heading])
        for name, item in block["metrics"].items():
            lines.append(
                f"  {name}: {item['before']['value']} [{_status(item['before'])}] -> "
                f"{item['after']['value']} [{_status(item['after'])}] (delta {item['delta']:+g})"
            )
        lines.append(
            f"  score: {block['before_score']['rate']:.1%} -> "
            f"{block['after_score']['rate']:.1%} (delta {block['score_delta']:+.1%})"
        )
    lines.extend(["", "TELLS"])
    for name, item in comparison["tells"].items():
        lines.append(f"  {name}: {item['before']} -> {item['after']} (delta {item['delta']:+d})")
    audit = comparison.get("integrity", {}).get("immutable_token_audit")
    if audit:
        status = "abstained" if audit["abstained"] else str(audit["total_violations"])
        lines.extend(["", "INTEGRITY", f"  immutable_token_audit: {status}"])
    diagnostics = comparison.get("diagnostics", {})
    if diagnostics:
        lines.extend(["", "V2.21 DIAGNOSTICS"])
        for name, item in diagnostics.items():
            if item["applicable"]:
                lines.append(
                    f"  {name}: {item['before_value']} -> {item['after_value']} "
                    f"(delta {item['delta']:+g})"
                )
            else:
                lines.append(f"  {name}: n/a (abstained or gated)")
    return "\n".join(lines)


def format_aggregate(aggregate: Mapping[str, Any]) -> str:
    corpus = aggregate["corpus"]
    lines = [
        f"AGGREGATE pairs={corpus['pairs']} corpus={corpus['path']}",
        f"languages={corpus['languages']} genres={corpus['genres']}",
    ]
    for block_name, heading in (("structural", "STRUCTURAL"), ("compliance", "COMPLIANCE")):
        block = aggregate[block_name]
        lines.extend(["", heading])
        for name, item in block["metrics"].items():
            before_rate = "n/a" if item["before_pass_rate"] is None else f"{item['before_pass_rate']:.1%}"
            after_rate = "n/a" if item["after_pass_rate"] is None else f"{item['after_pass_rate']:.1%}"
            lines.append(
                f"  {name}: mean {item['before_mean']} -> {item['after_mean']}; "
                f"pass {before_rate} -> {after_rate}"
            )
        lines.append(
            f"  score: {block['before_score']['rate']:.1%} -> "
            f"{block['after_score']['rate']:.1%} (delta {block['score_delta']:+.1%})"
        )
    tells = aggregate["tells"]
    lines.extend(
        [
            "",
            "TELLS",
            f"  total: {tells['before_total']} -> {tells['after_total']} (delta {tells['delta']:+d})",
        ]
    )
    integrity = aggregate.get("integrity", {}).get("immutable_token_audit")
    if integrity:
        lines.extend(
            [
                "",
                "INTEGRITY",
                f"  immutable_token_audit: {integrity['passed']}/{integrity['applicable']} pass; "
                f"violations={integrity['total_violations']}; abstained={integrity['abstained']}",
            ]
        )
    diagnostics = aggregate.get("diagnostics", {}).get("metrics", {})
    if diagnostics:
        lines.extend(["", "V2.21 DIAGNOSTICS"])
        for name, item in diagnostics.items():
            before = (
                str(item["before_mean"])
                if item["before_applicable"]
                else "n/a"
            )
            after = str(item["after_mean"]) if item["after_applicable"] else "n/a"
            delta = f"{item['delta']:+g}" if item["delta"] is not None else "n/a"
            lines.append(
                f"  {name}: mean {before} -> {after}; "
                f"paired delta {delta} (n={item['paired_applicable']}); "
                f"applicable {item['before_applicable']} -> {item['after_applicable']}"
            )
    if aggregate.get("warnings"):
        lines.extend(["", "WARNINGS"])
        lines.extend(f"  - {warning}" for warning in aggregate["warnings"])
    if "baseline_check" in aggregate:
        check = aggregate["baseline_check"]
        lines.extend(["", f"BASELINE: {'PASS' if check['passed'] else 'FAIL'} ({check['path']})"])
        lines.extend(f"  - {item}" for item in check["regressions"])
    return "\n".join(lines)


def _emit(data: Mapping[str, Any], as_json: bool, text_report: str) -> None:
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(text_report)


def _read_source(path: str | None, literal: str | None, label: str) -> tuple[str, str]:
    if literal is not None and path is not None:
        raise ValueError(f"provide either {label} path or --{label}-text, not both")
    if literal is not None:
        return literal, "<literal>"
    if path is None:
        raise ValueError(f"missing {label} path (use '-' for stdin)")
    if path == "-":
        return sys.stdin.read(), "<stdin>"
    return Path(path).read_text(encoding="utf-8"), Path(path).as_posix()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    profile_parser = subparsers.add_parser("profile", help="profile one file or literal text")
    profile_parser.add_argument("source", nargs="?", help="UTF-8 file path, or '-' for stdin")
    profile_parser.add_argument("--text", help="literal text instead of a file")
    profile_parser.add_argument("--genre")
    profile_parser.add_argument("--language", choices=("auto", "en", "ru"), default="auto")
    profile_parser.add_argument("--json", action="store_true", help="emit stable JSON")

    compare_parser = subparsers.add_parser("compare", help="compare before and after files")
    compare_parser.add_argument("before", nargs="?", help="before UTF-8 file")
    compare_parser.add_argument("after", nargs="?", help="after UTF-8 file")
    compare_parser.add_argument("--before-text")
    compare_parser.add_argument("--after-text")
    compare_parser.add_argument("--genre")
    compare_parser.add_argument("--language", choices=("auto", "en", "ru"), default="auto")
    compare_parser.add_argument("--json", action="store_true", help="emit stable JSON")

    aggregate_parser = subparsers.add_parser("aggregate", help="aggregate JSON corpus pairs")
    aggregate_parser.add_argument("--corpus", default=str(DEFAULT_CORPUS), help="corpus directory")
    aggregate_parser.add_argument("--check-baseline", help="fail with exit 1 on aggregate regression")
    aggregate_parser.add_argument("--json", action="store_true", help="emit stable JSON")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "profile":
            text, source = _read_source(args.source, args.text, "text")
            profile = metrics(text, genre=args.genre, language=args.language)
            result = {
                "schema_version": SCHEMA_VERSION,
                "command": "profile",
                "source": source,
                "profile": profile,
            }
            _emit(result, args.json, format_profile(profile))
            return 0

        if args.command == "compare":
            before, before_source = _read_source(args.before, args.before_text, "before")
            after, after_source = _read_source(args.after, args.after_text, "after")
            result = compare_texts(before, after, genre=args.genre, language=args.language)
            result["sources"] = {"before": before_source, "after": after_source}
            _emit(result, args.json, format_compare(result))
            return 0

        aggregate = aggregate_corpus(args.corpus)
        exit_code = 0
        if args.check_baseline:
            aggregate["baseline_check"] = check_baseline(aggregate, args.check_baseline)
            exit_code = 0 if aggregate["baseline_check"]["passed"] else 1
        _emit(aggregate, args.json, format_aggregate(aggregate))
        return exit_code
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    return 2  # pragma: no cover


if __name__ == "__main__":
    raise SystemExit(main())
