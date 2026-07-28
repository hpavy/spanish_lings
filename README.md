# spanish_conj

Rustlings-style drill tool for Spanish conjugation, A2 → C1. Instant feedback,
progressive tiers, spaced repetition so old material keeps resurfacing
instead of a one-shot linear walk.

## Run

```
python3 cli.py
```

Each run is one 15-item session. Progress (per-item spaced-repetition state,
unlocked tiers) is saved to `progress.json` after every session — safe to
stop anytime.

Answer prompts in lowercase, accents matter (typing without accents is
flagged as "almost" rather than wrong or silently accepted).

Each session prints the path to the grammar chapter for your current tier
(`book/`). Read it before drilling — the whole rule book is in Spanish and
self-contained, no need to look anything up elsewhere.

## How it works

- `conj_engine/` — the conjugation engine. Rule-based (stems, stem changes,
  orthographic adjustments) layered with hardcoded tables for true
  irregulars (ser, ir, tener, decir, ...). Single entrypoint:
  `conj_engine.paradigm.conjugate(verb_entry, tense)`.
- `curriculum.py` — 17 ordered tiers, each a set of verb tags × tenses
  (e.g. "present indicative, regular verbs" → "imperfect subjunctive,
  all verbs" → "reflexive full paradigm").
- `srs.py` — Leitner-box spaced repetition (5 boxes, wrong answer resets
  to box 1, correct answer promotes and pushes the next review further out).
- `session.py` — builds a session by mixing due-for-review items with a
  slice of brand-new items from the currently unlocked tiers.
- `cli.py` — the loop: shows a prompt, checks the answer, updates SRS state,
  prints a progress bar per tier, unlocks the next tier once ≥80% of the
  current tier's items reach box ≥3.

## Tests

```
python3 -m conj_engine.test_paradigm
```

Assertion-based checks for the engine (regular, stem-change, orthographic,
irregular, combined cases). All verbs in `conj_engine/verbs_registry.py` are
also smoke-tested against every tense with zero expected exceptions.

## Grammar book

`book/` holds one markdown chapter per tier (17 chapters + index), written
in Spanish, covering every rule the curriculum drills — regular endings,
stem/orthographic changes, all irregular paradigms, compound tenses,
imperative, reflexives. All example tables are generated straight from the
engine (`book/generate_tables.py`) so they can't drift from what the app
actually quizzes.

Start at `book/00_indice.md`.

## Adding verbs

Add an entry to `conj_engine/verbs_registry.py`:

```python
{"infinitive": "pensar", "strong_change": "e_ie", "tags": ["b1", "stem_change"]}
```

Tags determine which curriculum tier(s) pick up the verb — see
`curriculum.py` for the tag → tier mapping. True irregulars need a paradigm
entry in `conj_engine/irregular_verbs.py` instead (or in addition, for
irregular past participles: `conj_engine/irregular_participles.py`).
