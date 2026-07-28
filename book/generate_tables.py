"""
Generates markdown conjugation tables straight from conj_engine, so the
book's example tables can never drift from what the app actually quizzes.
Run standalone to print a table for manual copy-paste into a chapter, or
import table_md() from a chapter-writing script.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conj_engine.verbs_registry import BY_INFINITIVE
from conj_engine.paradigm import conjugate

PERSON_LABELS = ["yo", "tú", "él/ella/usted", "nosotros", "vosotros", "ellos/ellas/ustedes"]
PERSON_KEYS = ["yo", "tu", "el", "nosotros", "vosotros", "ellos"]

IMPERATIVE_PERSON_LABELS = ["tú", "usted", "nosotros", "vosotros", "ustedes"]
IMPERATIVE_PERSON_KEYS = ["tu", "el", "nosotros", "vosotros", "ellos"]


def table_md(verb, tense, header=None):
    entry = BY_INFINITIVE[verb]
    forms = conjugate(entry, tense)

    if tense in ("imperative_affirmative", "imperative_negative"):
        labels, keys = IMPERATIVE_PERSON_LABELS, IMPERATIVE_PERSON_KEYS
    else:
        labels, keys = PERSON_LABELS, PERSON_KEYS

    title = header or f"**{verb}**"
    lines = [f"{title}", "", "| persona | forma |", "|---|---|"]
    for label, key in zip(labels, keys):
        lines.append(f"| {label} | {forms[key]} |")
    return "\n".join(lines)


def multi_table_md(verbs, tense, headers=None):
    blocks = []
    for i, verb in enumerate(verbs):
        header = headers[i] if headers else None
        blocks.append(table_md(verb, tense, header))
    return "\n\n".join(blocks)


if __name__ == "__main__":
    verb, tense = sys.argv[1], sys.argv[2]
    print(table_md(verb, tense))
