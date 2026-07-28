"""
Imperative mood. No yo form. Rules:
  - affirmative tú: same as present indicative él/ella form, except a short
    list of true irregulars (decir, hacer, ir, poner, salir, tener, venir, ser)
  - affirmative vosotros: always regular, stem + ad/ed/id (even for irregular
    verbs), except ir -> id, ser -> sed
  - affirmative usted / ustedes / nosotros: same as present subjunctive
    el / ellos / nosotros form, except ir -> vamos (nosotros affirmative only)
  - negative, all persons: "no" + present subjunctive form
"""

from conj_engine.stems import split_infinitive
from conj_engine.paradigm import present_indicative, present_subjunctive

IMPERATIVE_PERSONS = ["tu", "el", "nosotros", "vosotros", "ellos"]

AFFIRMATIVE_TU_IRREGULAR = {
    "decir": "di",
    "hacer": "haz",
    "ir": "ve",
    "poner": "pon",
    "salir": "sal",
    "tener": "ten",
    "venir": "ven",
    "ser": "sé",
}

VOSOTROS_ENDING = {"ar": "ad", "er": "ed", "ir": "id"}
AFFIRMATIVE_VOSOTROS_IRREGULAR = {"ir": "id", "ser": "sed"}


def affirmative(entry):
    infinitive = entry["infinitive"]
    subjunctive = present_subjunctive(entry)

    tu = AFFIRMATIVE_TU_IRREGULAR.get(infinitive) or present_indicative(entry)["el"]

    if infinitive in AFFIRMATIVE_VOSOTROS_IRREGULAR:
        vosotros = AFFIRMATIVE_VOSOTROS_IRREGULAR[infinitive]
    else:
        stem, ending = split_infinitive(infinitive)
        vosotros = stem + VOSOTROS_ENDING[ending]

    nosotros = "vamos" if infinitive == "ir" else subjunctive["nosotros"]

    return {
        "tu": tu,
        "el": subjunctive["el"],
        "nosotros": nosotros,
        "vosotros": vosotros,
        "ellos": subjunctive["ellos"],
    }


def negative(entry):
    subjunctive = present_subjunctive(entry)
    return {person: f"no {subjunctive[person]}" for person in IMPERATIVE_PERSONS}
