"""
Spelling-only changes that preserve pronunciation when a stem meets an ending
starting with e/i vs a/o/u. These are not "irregular" in any meaningful sense,
just Spanish orthography rules applied consistently. Verb is tagged with an
`ortho` code and the paradigm layer calls the matching function per-ending.
"""

from conj_engine.stems import PERSONS
from conj_engine.regular_simple import (
    PRESENT_ENDINGS,
    PRETERITE_ENDINGS,
    PRESENT_SUBJUNCTIVE_ENDINGS,
)

FRONT_VOWEL_ENDING = {"e", "i"}


def _first_letter(ending_str):
    return ending_str[0]


def _car_gar_zar(stem, ortho, ending_str):
    """buscar -> busque/busqué ; llegar -> llegue/llegué ; empezar -> empiece/empecé
    Applies before e (subjunctive, some preterite yo)."""
    if _first_letter(ending_str) not in ("e", "é"):
        return stem
    return {
        "c_qu": stem[:-1] + "qu",
        "g_gu": stem[:-1] + "gu",
        "z_c": stem[:-1] + "c",
    }[ortho]


def _cer_cir_zc(stem, ending_str):
    """conocer -> conozco (yo present, before o), conozca (subjunctive, before a)."""
    if _first_letter(ending_str) not in ("o", "a", "á"):
        return stem
    return stem[:-1] + "zc"


def _guir_gu_g(stem, ending_str):
    """seguir -> sigo (present/subjunctive, before o/a: drop u)."""
    if _first_letter(ending_str) in ("o", "a", "á"):
        return stem[:-1]
    return stem


def _ger_gir_g_j(stem, ending_str):
    """coger -> cojo (present / subjunctive, before o/a)."""
    if _first_letter(ending_str) in ("o", "a", "á"):
        return stem[:-1] + "j"
    return stem


def _uir_present_indicative(stem, ending, endings_table):
    """construir -> construyo, construyes, construye, construimos, construis, construyen.
    y appears in boot persons only (like a stem change), because the ending's
    vowel-initial start would otherwise create an i-i hiatus with the stem's final i."""
    from conj_engine.stem_changes import BOOT_PERSONS

    endings = endings_table[ending]
    return {
        person: (stem + "y" if person in BOOT_PERSONS else stem) + e
        for person, e in zip(PERSONS, endings)
    }


def _uir_present_subjunctive(stem, ending, endings_table):
    """construya, construyas, ... y in every person: subjunctive endings for -ir
    verbs (a/as/a/amos/ais/an) all start with a vowel."""
    endings = endings_table[ending]
    return {person: stem + "y" + e for person, e in zip(PERSONS, endings)}


def _uir_preterite(stem, ending, endings_table):
    """construi, construiste, construyo, construimos, construisteis, construyeron.
    Only el/ellos: the -io/-ieron endings contract with stem's i into y."""
    endings = endings_table[ending]
    result = {}
    for person, e in zip(PERSONS, endings):
        if person in ("el", "ellos"):
            result[person] = stem + "y" + e[1:]
        else:
            result[person] = stem + e
    return result


def _uir_gerund(stem):
    return stem + "yendo"


ORTHO_APPLIERS = {
    "c_qu": _car_gar_zar,
    "g_gu": _car_gar_zar,
    "z_c": _car_gar_zar,
    "cer_zc": _cer_cir_zc,
    "guir_g": _guir_gu_g,
    "ger_j": _ger_gir_g_j,
}


def _apply_with_ortho(stem, ending, ortho, endings_table):
    endings = endings_table[ending]
    result = {}
    for person, e in zip(PERSONS, endings):
        if ortho in ("c_qu", "g_gu", "z_c"):
            adjusted_stem = _car_gar_zar(stem, ortho, e)
        else:
            adjusted_stem = ORTHO_APPLIERS[ortho](stem, e)
        result[person] = adjusted_stem + e
    return result


def present_indicative(stem, ending, ortho):
    if ortho == "uir_y":
        return _uir_present_indicative(stem, ending, PRESENT_ENDINGS)
    return _apply_with_ortho(stem, ending, ortho, PRESENT_ENDINGS)


def present_subjunctive(stem, ending, ortho):
    if ortho == "uir_y":
        return _uir_present_subjunctive(stem, ending, PRESENT_SUBJUNCTIVE_ENDINGS)
    return _apply_with_ortho(stem, ending, ortho, PRESENT_SUBJUNCTIVE_ENDINGS)


def preterite(stem, ending, ortho):
    if ortho == "uir_y":
        return _uir_preterite(stem, ending, PRETERITE_ENDINGS)
    return _apply_with_ortho(stem, ending, ortho, PRETERITE_ENDINGS)


def gerund(stem, ortho):
    if ortho == "uir_y":
        return _uir_gerund(stem)
    raise ValueError(f"gerund override not needed for ortho={ortho}")


def imperfect_subjunctive(stem, ending, ortho, variant="ra"):
    from conj_engine.regular_simple import (
        IMPERFECT_SUBJUNCTIVE_RA_ENDINGS,
        IMPERFECT_SUBJUNCTIVE_SE_ENDINGS,
    )

    if ortho != "uir_y":
        raise ValueError(f"imperfect subjunctive override not needed for ortho={ortho}")
    endings = (
        IMPERFECT_SUBJUNCTIVE_RA_ENDINGS[ending]
        if variant == "ra"
        else IMPERFECT_SUBJUNCTIVE_SE_ENDINGS[ending]
    )
    return {person: stem + "y" + e[1:] for person, e in zip(PERSONS, endings)}
