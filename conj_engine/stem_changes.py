"""
Stem-changing ("boot") verbs. The change applies to the stressed syllable,
which in present tense/subjunctive means every person except nosotros/vosotros.

For -ir verbs, there's a secondary weak change (e->i or o->u) that also hits
preterite (3rd persons), imperfect subjunctive, gerund, and nosotros/vosotros
of present subjunctive. e.g. pedir: pidió, pidiera, pidiendo; dormir: durmió.
"""

from conj_engine.stems import PERSONS
from conj_engine.regular_simple import (
    PRESENT_ENDINGS,
    PRETERITE_ENDINGS,
    PRESENT_SUBJUNCTIVE_ENDINGS,
    IMPERFECT_SUBJUNCTIVE_RA_ENDINGS,
    IMPERFECT_SUBJUNCTIVE_SE_ENDINGS,
)

BOOT_PERSONS = {"yo", "tu", "el", "ellos"}

STRONG_CHANGES = {"e_ie", "o_ue", "e_i", "u_ue"}
WEAK_CHANGES = {"e_i", "o_u"}

VOWEL_REPLACEMENT = {
    "e_ie": ("e", "ie"),
    "o_ue": ("o", "ue"),
    "e_i": ("e", "i"),
    "u_ue": ("u", "ue"),
    "o_u": ("o", "u"),
}

VOWELS = "aeiou"


def _replace_last_vowel(stem, target, replacement):
    for i in range(len(stem) - 1, -1, -1):
        if stem[i] == target:
            return stem[:i] + replacement + stem[i + 1 :]
    raise ValueError(f"no '{target}' vowel found in stem '{stem}'")


def _changed_stem(stem, change):
    target, replacement = VOWEL_REPLACEMENT[change]
    return _replace_last_vowel(stem, target, replacement)


def _weak_stem(stem, weak_change):
    target, replacement = VOWEL_REPLACEMENT[weak_change]
    return _replace_last_vowel(stem, target, replacement)


def present_indicative(stem, ending, strong_change):
    changed = _changed_stem(stem, strong_change)
    endings = PRESENT_ENDINGS[ending]
    return {
        person: (changed if person in BOOT_PERSONS else stem) + e
        for person, e in zip(PERSONS, endings)
    }


def present_subjunctive(stem, ending, strong_change, weak_change=None):
    endings = PRESENT_SUBJUNCTIVE_ENDINGS[ending]
    changed = _changed_stem(stem, strong_change)
    weak = _weak_stem(stem, weak_change) if weak_change else stem
    result = {}
    for person, e in zip(PERSONS, endings):
        if person in BOOT_PERSONS:
            result[person] = changed + e
        elif weak_change:
            result[person] = weak + e
        else:
            result[person] = stem + e
    return result


def preterite(stem, ending, weak_change=None):
    """Only -ir verbs with a weak change deviate, on 3rd persons (el, ellos)."""
    endings = PRETERITE_ENDINGS[ending]
    if not weak_change:
        return {p: stem + e for p, e in zip(PERSONS, endings)}
    weak = _weak_stem(stem, weak_change)
    result = {}
    for person, e in zip(PERSONS, endings):
        result[person] = (weak if person in ("el", "ellos") else stem) + e
    return result


def imperfect_subjunctive(stem, ending, weak_change, variant="ra"):
    endings = (
        IMPERFECT_SUBJUNCTIVE_RA_ENDINGS[ending]
        if variant == "ra"
        else IMPERFECT_SUBJUNCTIVE_SE_ENDINGS[ending]
    )
    weak = _weak_stem(stem, weak_change)
    return {person: weak + e for person, e in zip(PERSONS, endings)}


def gerund(stem, ending, weak_change=None):
    base = _weak_stem(stem, weak_change) if weak_change else stem
    suffix = "ando" if ending == "ar" else "iendo"
    return base + suffix
