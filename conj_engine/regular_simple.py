from conj_engine.stems import PERSONS

PRESENT_ENDINGS = {
    "ar": ["o", "as", "a", "amos", "áis", "an"],
    "er": ["o", "es", "e", "emos", "éis", "en"],
    "ir": ["o", "es", "e", "imos", "ís", "en"],
}

PRETERITE_ENDINGS = {
    "ar": ["é", "aste", "ó", "amos", "asteis", "aron"],
    "er": ["í", "iste", "ió", "imos", "isteis", "ieron"],
    "ir": ["í", "iste", "ió", "imos", "isteis", "ieron"],
}

IMPERFECT_ENDINGS = {
    "ar": ["aba", "abas", "aba", "ábamos", "abais", "aban"],
    "er": ["ía", "ías", "ía", "íamos", "íais", "ían"],
    "ir": ["ía", "ías", "ía", "íamos", "íais", "ían"],
}

FUTURE_ENDINGS = ["é", "ás", "á", "emos", "éis", "án"]
CONDITIONAL_ENDINGS = ["ía", "ías", "ía", "íamos", "íais", "ían"]

PRESENT_SUBJUNCTIVE_ENDINGS = {
    "ar": ["e", "es", "e", "emos", "éis", "en"],
    "er": ["a", "as", "a", "amos", "áis", "an"],
    "ir": ["a", "as", "a", "amos", "áis", "an"],
}

IMPERFECT_SUBJUNCTIVE_RA_ENDINGS = {
    "ar": ["ara", "aras", "ara", "áramos", "arais", "aran"],
    "er": ["iera", "ieras", "iera", "iéramos", "ierais", "ieran"],
    "ir": ["iera", "ieras", "iera", "iéramos", "ierais", "ieran"],
}

IMPERFECT_SUBJUNCTIVE_SE_ENDINGS = {
    "ar": ["ase", "ases", "ase", "ásemos", "aseis", "asen"],
    "er": ["iese", "ieses", "iese", "iésemos", "ieseis", "iesen"],
    "ir": ["iese", "ieses", "iese", "iésemos", "ieseis", "iesen"],
}


def _apply(stem, endings):
    return {person: stem + ending for person, ending in zip(PERSONS, endings)}


def present_indicative(stem, ending):
    return _apply(stem, PRESENT_ENDINGS[ending])


def preterite(stem, ending):
    return _apply(stem, PRETERITE_ENDINGS[ending])


def imperfect_indicative(stem, ending):
    return _apply(stem, IMPERFECT_ENDINGS[ending])


def future(infinitive):
    return _apply(infinitive, FUTURE_ENDINGS)


def conditional(infinitive):
    return _apply(infinitive, CONDITIONAL_ENDINGS)


def present_subjunctive(stem, ending):
    return _apply(stem, PRESENT_SUBJUNCTIVE_ENDINGS[ending])


def imperfect_subjunctive_ra(stem, ending):
    return _apply(stem, IMPERFECT_SUBJUNCTIVE_RA_ENDINGS[ending])


def imperfect_subjunctive_se(stem, ending):
    return _apply(stem, IMPERFECT_SUBJUNCTIVE_SE_ENDINGS[ending])
