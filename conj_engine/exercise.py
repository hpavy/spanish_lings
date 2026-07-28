"""
Turns a (verb, tense) pair into individual drillable items: one per person,
since that's the unit the SRS tracks and the CLI quizzes on.
"""

from conj_engine.paradigm import conjugate
from conj_engine.imperative import IMPERATIVE_PERSONS
from conj_engine.stems import PERSONS

PERSON_LABELS = {
    "yo": "yo",
    "tu": "tú",
    "el": "él / ella / usted",
    "nosotros": "nosotros",
    "vosotros": "vosotros",
    "ellos": "ellos / ellas / ustedes",
}

NO_PERSON_TENSES = {"gerund", "infinitive"}


def persons_for_tense(tense):
    if tense in ("imperative_affirmative", "imperative_negative"):
        return IMPERATIVE_PERSONS
    return PERSONS


def build_items(verb_entry, tense):
    """Returns a list of dicts: {verb, tense, person, answer}."""
    infinitive = verb_entry["infinitive"]

    if tense in NO_PERSON_TENSES:
        answer = conjugate(verb_entry, tense)
        return [{"verb": infinitive, "tense": tense, "person": None, "answer": answer}]

    forms = conjugate(verb_entry, tense)
    persons = persons_for_tense(tense)
    return [
        {"verb": infinitive, "tense": tense, "person": p, "answer": forms[p]}
        for p in persons
    ]


def item_id(item):
    return f"{item['verb']}|{item['tense']}|{item['person']}"


def prompt(item):
    label = PERSON_LABELS.get(item["person"])
    if label is None:
        return item["verb"]
    return f"{item['verb']} ({label})"
