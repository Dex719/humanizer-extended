# Russian-language patterns

Read this file whenever the input or requested output is predominantly Russian. These rules override conflicting English defaults in `SKILL.md`.

## Contents

- [44. Russian AI vocabulary and frame phrases](#44-russian-ai-vocabulary-and-frame-phrases)
- [45. Russian syntactic calques from English](#45-russian-syntactic-calques-from-english)
- [46. Russian punctuation tells](#46-russian-punctuation-tells)
- [70. Висячий деепричастный оборот](#70-висячий-деепричастный-оборот)
- [71. Дидактические дисклеймеры](#71-дидактические-дисклеймеры)
- [72. Формульные зачины](#72-формульные-зачины)
- [73. Формульное «Заключение»](#73-формульное-заключение)
- [Russian inversions of global rules](#russian-inversions-of-global-rules)
- [RU self-audit](#ru-self-audit)

## 44. Russian AI vocabulary and frame phrases

**Words and phrases to watch:** `в современном мире`, `в эпоху цифровизации`, `в условиях стремительных изменений`, `данный` instead of `этот`, `является` where a dash or no copula would do, `осуществлять` instead of a direct verb, `позволяет обеспечить`, `способствует повышению`, `представляет собой`, `играет ключевую роль`, `неотъемлемая часть`, `актуальная задача`, `комплексный подход`, `следует отметить`, `необходимо подчеркнуть`, `важно понимать`, `открывает новые возможности`, `выводит на новый уровень`, `вектор развития`, `точка роста`, `драйвер изменений`, `синергетический эффект`, and bureaucratic noun chains such as `осуществление реализации мероприятий`.

**Problem:** Russian LLM prose mixes translated English AI vocabulary with Soviet administrative language. The result sounds simultaneously like a corporate press release and a ministry circular. A single ordinary word is not evidence; a cluster of frames is.

**Before:**

> В современном мире цифровизации данный инструмент играет ключевую роль в обеспечении повышения эффективности бизнес-процессов, открывая новые возможности для комплексного развития организации.

**After:**

> Инструмент может сделать работу организации эффективнее и помочь ей развиваться.

**Rule:** Delete the frame and keep the claim. Prefer a concrete subject and a direct verb. Replace `данный` with `этот` or omit it; replace `осуществляет обработку` with `обрабатывает`; replace `позволяет обеспечить повышение` with the result the input actually supports. Do not manufacture a concrete result when the input supplies none: hedge it or say it is not documented.

**Morphosyntactic checks and genre gate:** In addition to the word list, count action nominalizations used instead of verbs, genitive chains longer than three nouns, `является` used as a weak copula, and avoidable passive. Flag a cluster at two or more features per 500 words. Treat official, administrative, and legal prose as neutral; in scientific prose require more than three features per 500 words; in blogs, news, and literary prose flag more than one per 500.

**Synthetic teaching pair (do not reuse its facts):**

**Before:**
> Данный метод осуществляет обработку данных в рамках системы оценки эффективности соответствующих показателей.

**After:**
> Этот метод обрабатывает данные в системе, которая оценивает эффективность по соответствующим показателям.

## 45. Russian syntactic calques from English

**Signs to watch:** `Однако,` at the start of a sentence; a comma forced after a short adverbial opener; calqued `Это не про X. Это про Y`; heavy `..., за которым последовало ...`; invented compounds such as `маркетингово-аналитический` or `клиентоориентированно-сервисный`; and rigid subject-verb-object order that flattens natural theme-rheme stress. The sentence can be grammatical yet sound like something nobody would say aloud.

**Problem:** English sentence architecture has been carried into Russian. This structural calque is more informative than any single vocabulary item.

**Before:**

> Благодаря использованию данного подхода, мы, однако, смогли достичь клиентоориентированно-сервисного результата.

**After:**

> Этот подход помог улучшить обслуживание клиентов.

**Rule:**

- Write sentence-initial `Однако` without a following comma when it functions as a conjunction.
- Rewrite `Это не про X, это про Y` as an idiomatic contrast such as `дело не столько в X, сколько в Y`, when that meaning is actually intended.
- Replace `за которым последовало` with `после чего` or a plain verb chain.
- Break invented compound adjectives into ordinary noun phrases.
- Remove commas that exist only because of English structure.
- Vary word order to put known information before new emphasis rather than forcing English SVO order.
- Prefer the construction a person would actually say.

## 46. Russian punctuation tells

**Signs to watch:** an ordinary common noun capitalized after a colon, especially in list items; тире in nearly every sentence; English straight or curly quotation marks instead of Russian `«ёлочки»`; and punctuation so uniformly formal that it conflicts with an informal browser or messenger register.

**Problem:** Russian punctuation differs from English. The capital-after-colon error is especially characteristic of imported English list styling. Unlike English pattern 14, a Russian тире is a normal, often grammatically required mark, so reduce a cluster rather than eliminate the character.

**Before:**

> Преимущества подхода: Высокая скорость, Низкая стоимость, и простота внедрения для любой команды.

**After:**

> У подхода три преимущества: он быстрый, дешёвый и простой во внедрении.

**Rule:**

- Use lowercase after a colon unless a proper noun, direct quotation, or independently capitalized text follows.
- Use `«ёлочки»` for ordinary Russian quotations, nesting `„лапки“` when needed, unless the user's sample or publication style says otherwise.
- Remove the English serial comma before a lone `и` when Russian syntax does not require it.
- Keep тире where Russian grammar or emphasis earns it. Reduce repetitive stylistic dashes, but never apply the English zero-dash scan.
- Match informal typography when a supplied author sample consistently does so; flawless typography is not a goal by itself.

## Additional Russian patterns (70–73)

The pairs below are synthetic teaching pairs. Never reuse their facts in user text; every rewrite must preserve the details and modality of its own `Before` text.

### ##70 Висячий деепричастный оборот

**Признаки:** субъект деепричастия не совпадает с субъектом главного предложения: `Используя этот метод, результаты были улучшены`. Это грамматическая ошибка, а не стилистический выбор, поэтому правило действует во всех жанрах без гейта.

Не путать с корректным оборотом: `Используя этот метод, мы улучшили результаты`.

**До:**
> Используя этот метод, результаты были улучшены на 15%.

**После:**
> При использовании этого метода результаты улучшились на 15%.

### ##71 Дидактические дисклеймеры

**Признаки:** `важно отметить`, `стоит учесть`, `следует помнить`, `значения могут отличаться…`.

**Граница:** отличать эти рамки от эпистемических хеджей `возможно` и `вероятно`. Хеджи и модальность сохранять по правилу 56.

**Порог и гейт:** флаговать не менее двух оборотов на 500 слов в научном, новостном или художественном тексте; учебный и справочный текст считать нейтральным.

**До:**
> Важно отметить, что значения могут отличаться по регионам. Стоит учесть, что результаты зависят от методики.

**После:**
> Значения могут отличаться по регионам, а результаты зависят от методики.

### ##72 Формульные зачины

**Признаки:** `В данной работе…`, `Настоящее исследование посвящено…`, `В данном исследовании рассматривается…` в первых двух предложениях.

**Доказательная база:** AINL-Eval 2025 (arXiv:2508.09622) относит этот зачин к устойчивым признакам сгенерированного русского научного текста, сохраняющимся после явных запретов в промпте.

**Гейт:** стандартную форму аннотации считать нейтральной. Не флаговать зачин, если автор систематически использует его в подлинных образцах голоса.

**До:**
> В данной работе рассматривается проблема классификации текстов.

**После:**
> Предмет работы — проблема классификации текстов.

### ##73 Формульное «Заключение»

**Признаки:** заключение только пересказывает текст с рамками `Таким образом, в данной работе было показано…` или `Подводя итог, можно отметить…`, но не синтезирует следствия.

**Гейт:** флаговать только заключение, состоящее целиком из пересказа. Сам раздел `Заключение` — нормальная часть научной статьи.

**Правка:** заменить рамку на следствие, уже подтверждённое результатами во входном тексте. Если такого следствия нет, закончить конкретным подтверждённым результатом или удалить повтор. Не добавлять проценты, размеры выборок, практические выводы или другие детали, отсутствующие во входе.

## Russian inversions of global rules

Several English rules reverse or soften for Russian. Do not apply them blindly:

- **Pattern 14 (cut all em/en dashes): off.** Тире is core Russian punctuation: zero-copula sentences (`Москва — столица`), ellipsis, apposition, and non-union clauses can require it. Reduce overuse; never target zero.
- **Pattern 13 (passive to active): often inverted.** Russian academic, technical, and business prose naturally uses agentless passive and impersonal forms. Prefer `Можно сделать вывод` over an unnecessary `Мы можем сделать вывод`; add or preserve these forms when the genre calls for them.
- **Pattern 40 (force short sentences): softened.** Russian literary and academic prose tolerates long, multi-clause sentences. Vary length, but do not chop the text into translation-like staccato.
- **Pattern 42 (connectors): language-specific.** Trim clusters of `кроме того`, `таким образом`, `следовательно`, `в связи с этим`, and sentence-opening `однако`, but keep a connector when the logic would otherwise be unclear. Sentence-initial `Однако` normally takes no comma.
- **Pattern 43 (affect): genre-gated.** Do not add first-person feelings to Russian reference, technical, academic, or business prose. Preserve real stance only where the input or voice sample supplies it.
- **Pattern 46 (capitalization after a colon): lowercase by default.** Preserve capitals for proper nouns, quotations, and text that independently requires one.

## RU self-audit

Before returning Russian output:

1. Scan for clusters of the frames in pattern 44 and convert abstract noun chains into direct verbs.
2. Read each sentence aloud for English architecture, especially `Однако,`, `Это не про X`, rigid SVO order, and unnatural compound adjectives.
3. Check lowercase after colons and Russian quotation marks without “correcting” protected quotations or titles.
4. Inspect тире for repetition, not absence. Keep grammatical marks.
5. Preserve long clauses, agentless passive, and impersonal constructions when the genre makes them natural.
6. Compare every claim and detail with the input; never make an abstract claim concrete by inventing a Russian-sounding example.
