"""
Compound tenses: a conjugated form of haber + the verb's past participle.
The participle doesn't inflect for person/number in these constructions.
"""

from conj_engine.stems import PERSONS
from conj_engine.paradigm import conjugate, past_participle
from conj_engine.verbs_registry import BY_INFINITIVE

HABER = BY_INFINITIVE.get("haber") or {"infinitive": "haber"}

HABER_TENSE_FOR = {
    "present_perfect": "present_indicative",
    "pluperfect": "imperfect_indicative",
    "future_perfect": "future",
    "conditional_perfect": "conditional",
    "present_perfect_subjunctive": "present_subjunctive",
    "pluperfect_subjunctive_ra": "imperfect_subjunctive_ra",
    "pluperfect_subjunctive_se": "imperfect_subjunctive_se",
}


def compound(entry, tense):
    haber_tense = HABER_TENSE_FOR[tense]
    haber_forms = conjugate(HABER, haber_tense)
    participle = past_participle(entry)
    return {person: f"{haber_forms[person]} {participle}" for person in PERSONS}
