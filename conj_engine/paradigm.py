"""
Orchestrator: given a verb registry entry, produce conjugated forms for any
tense/mood. Priority order per tense:
  1. Fully irregular hardcoded form (irregular_verbs.IRREGULAR)
  2. Rule-based: stem change + orthographic adjustment (possibly combined)
  3. Regular conjugation
"""

from conj_engine.stems import split_infinitive, PERSONS
from conj_engine import regular_simple as rs
from conj_engine import stem_changes as sc
from conj_engine import orthographic as ortho_mod
from conj_engine.irregular_verbs import IRREGULAR
from conj_engine.irregular_participles import IRREGULAR_PARTICIPLES

CONSONANT_ORTHO = {"c_qu", "g_gu", "z_c", "cer_zc", "guir_g", "ger_j"}


def _irregular_form(infinitive, tense):
    return IRREGULAR.get(infinitive, {}).get(tense)


def _combined_present_indicative(stem, ending, strong_change, ortho):
    endings = rs.PRESENT_ENDINGS[ending]
    result = {}
    for person, e in zip(PERSONS, endings):
        s = sc._changed_stem(stem, strong_change) if person in sc.BOOT_PERSONS else stem
        s = _apply_consonant_ortho(s, ortho, e)
        result[person] = s + e
    return result


def _combined_present_subjunctive(stem, ending, strong_change, weak_change, ortho):
    endings = rs.PRESENT_SUBJUNCTIVE_ENDINGS[ending]
    result = {}
    for person, e in zip(PERSONS, endings):
        if person in sc.BOOT_PERSONS:
            s = sc._changed_stem(stem, strong_change)
        elif weak_change:
            s = sc._weak_stem(stem, weak_change)
        else:
            s = stem
        s = _apply_consonant_ortho(s, ortho, e)
        result[person] = s + e
    return result


def _apply_consonant_ortho(stem, ortho, ending_str):
    if ortho in ("c_qu", "g_gu", "z_c"):
        return ortho_mod._car_gar_zar(stem, ortho, ending_str)
    if ortho == "cer_zc":
        return ortho_mod._cer_cir_zc(stem, ending_str)
    if ortho == "guir_g":
        return ortho_mod._guir_gu_g(stem, ending_str)
    if ortho == "ger_j":
        return ortho_mod._ger_gir_g_j(stem, ending_str)
    return stem


def present_indicative(entry):
    infinitive = entry["infinitive"]
    irregular = _irregular_form(infinitive, "present_indicative")
    if irregular:
        return irregular

    stem, ending = split_infinitive(infinitive)
    strong_change = entry.get("strong_change")
    ortho = entry.get("ortho")

    if ortho == "uir_y":
        return ortho_mod.present_indicative(stem, ending, ortho)
    if strong_change and ortho in CONSONANT_ORTHO:
        return _combined_present_indicative(stem, ending, strong_change, ortho)
    if strong_change:
        return sc.present_indicative(stem, ending, strong_change)
    if ortho in CONSONANT_ORTHO:
        return ortho_mod.present_indicative(stem, ending, ortho)
    return rs.present_indicative(stem, ending)


def present_subjunctive(entry):
    infinitive = entry["infinitive"]
    irregular = _irregular_form(infinitive, "present_subjunctive")
    if irregular:
        return irregular

    stem, ending = split_infinitive(infinitive)
    strong_change = entry.get("strong_change")
    weak_change = entry.get("weak_change")
    ortho = entry.get("ortho")

    if ortho == "uir_y":
        return ortho_mod.present_subjunctive(stem, ending, ortho)
    if strong_change and ortho in CONSONANT_ORTHO:
        return _combined_present_subjunctive(stem, ending, strong_change, weak_change, ortho)
    if strong_change:
        return sc.present_subjunctive(stem, ending, strong_change, weak_change)
    if ortho in CONSONANT_ORTHO:
        return ortho_mod.present_subjunctive(stem, ending, ortho)
    return rs.present_subjunctive(stem, ending)


def preterite(entry):
    infinitive = entry["infinitive"]
    irregular = _irregular_form(infinitive, "preterite")
    if irregular:
        return irregular

    stem, ending = split_infinitive(infinitive)
    weak_change = entry.get("weak_change")
    ortho = entry.get("ortho")

    if ortho == "uir_y":
        return ortho_mod.preterite(stem, ending, ortho)
    if ortho in ("c_qu", "g_gu", "z_c"):
        return ortho_mod.preterite(stem, ending, ortho)
    if weak_change:
        return sc.preterite(stem, ending, weak_change)
    return rs.preterite(stem, ending)


def imperfect_indicative(entry):
    infinitive = entry["infinitive"]
    irregular = _irregular_form(infinitive, "imperfect_indicative")
    if irregular:
        return irregular
    stem, ending = split_infinitive(infinitive)
    return rs.imperfect_indicative(stem, ending)


def future(entry):
    infinitive = entry["infinitive"]
    irregular = _irregular_form(infinitive, "future")
    if irregular:
        return irregular
    stem = IRREGULAR.get(infinitive, {}).get("future_stem", infinitive)
    return rs.future(stem)


def conditional(entry):
    infinitive = entry["infinitive"]
    irregular = _irregular_form(infinitive, "conditional")
    if irregular:
        return irregular
    stem = IRREGULAR.get(infinitive, {}).get("future_stem", infinitive)
    return rs.conditional(stem)


def imperfect_subjunctive(entry, variant="ra"):
    infinitive = entry["infinitive"]
    tense = f"imperfect_subjunctive_{variant}"
    irregular = _irregular_form(infinitive, tense)
    if irregular:
        return irregular

    stem, ending = split_infinitive(infinitive)
    weak_change = entry.get("weak_change")
    ortho = entry.get("ortho")

    if ortho == "uir_y":
        return ortho_mod.imperfect_subjunctive(stem, ending, ortho, variant)
    if weak_change:
        return sc.imperfect_subjunctive(stem, ending, weak_change, variant)
    if variant == "ra":
        return rs.imperfect_subjunctive_ra(stem, ending)
    return rs.imperfect_subjunctive_se(stem, ending)


def gerund(entry):
    infinitive = entry["infinitive"]
    irregular = IRREGULAR.get(infinitive, {}).get("gerund")
    if irregular:
        return irregular

    stem, ending = split_infinitive(infinitive)
    ortho = entry.get("ortho")
    weak_change = entry.get("weak_change")

    if ortho == "uir_y":
        return ortho_mod.gerund(stem, ortho)
    if weak_change:
        return sc.gerund(stem, ending, weak_change)
    return stem + ("ando" if ending == "ar" else "iendo")


def past_participle(entry):
    infinitive = entry["infinitive"]
    irregular = IRREGULAR.get(infinitive, {}).get("past_participle")
    if irregular:
        return irregular
    if infinitive in IRREGULAR_PARTICIPLES:
        return IRREGULAR_PARTICIPLES[infinitive]

    stem, ending = split_infinitive(infinitive)
    if ending == "ar":
        return stem + "ado"
    if stem[-1] in "aeo":
        return stem + "ído"
    return stem + "ido"


TENSE_FUNCS = {
    "present_indicative": present_indicative,
    "preterite": preterite,
    "imperfect_indicative": imperfect_indicative,
    "future": future,
    "conditional": conditional,
    "present_subjunctive": present_subjunctive,
}

COMPOUND_TENSES = {
    "present_perfect",
    "pluperfect",
    "future_perfect",
    "conditional_perfect",
    "present_perfect_subjunctive",
    "pluperfect_subjunctive_ra",
    "pluperfect_subjunctive_se",
}


def _simple_or_compound(entry, tense):
    if tense == "imperfect_subjunctive_ra":
        return imperfect_subjunctive(entry, "ra")
    if tense == "imperfect_subjunctive_se":
        return imperfect_subjunctive(entry, "se")
    if tense == "gerund":
        return gerund(entry)
    if tense in COMPOUND_TENSES:
        from conj_engine.compound import compound

        return compound(entry, tense)
    return TENSE_FUNCS[tense](entry)


def conjugate(entry, tense):
    if not entry.get("reflexive"):
        if tense == "imperative_affirmative":
            from conj_engine.imperative import affirmative

            return affirmative(entry)
        if tense == "imperative_negative":
            from conj_engine.imperative import negative

            return negative(entry)
        return _simple_or_compound(entry, tense)

    from conj_engine.imperative import affirmative, negative, IMPERATIVE_PERSONS
    from conj_engine.reflexive import (
        strip_se,
        preposed,
        preposed_negative_imperative,
        attached_imperative,
        attached_gerund,
        attached_infinitive,
    )

    base = dict(entry)
    base["infinitive"] = strip_se(entry["infinitive"])

    if tense == "infinitive":
        return entry["infinitive"]
    if tense == "gerund":
        return attached_gerund(gerund(base))
    if tense == "imperative_affirmative":
        return attached_imperative(affirmative(base), base["infinitive"])
    if tense == "imperative_negative":
        subj = present_subjunctive(base)
        return preposed_negative_imperative(subj, IMPERATIVE_PERSONS)

    return preposed(_simple_or_compound(base, tense))
