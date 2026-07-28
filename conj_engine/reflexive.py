"""
Reflexive pronoun attachment. The verb conjugates exactly like its
non-reflexive form (levantarse conjugates like levantar); only the pronoun
placement differs:
  - conjugated indicative/subjunctive, negative imperative: pronoun BEFORE
    the verb (me levanto, no te levantes)
  - infinitive, gerund, affirmative imperative: pronoun ATTACHED after
    the verb (levantarse, levantándome, levántate)
"""

REFLEXIVE_PRONOUNS = {
    "yo": "me",
    "tu": "te",
    "el": "se",
    "nosotros": "nos",
    "vosotros": "os",
    "ellos": "se",
}

# vosotros affirmative imperative drops the final -d before attaching "os"
# (levantad + os -> levantaos), except irse -> idos
VOSOTROS_D_DROP = {"ir": "idos"}

VOWELS = "aeiou"
STRONG_VOWELS = "aeo"
ACCENT_MAP = {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú"}


def _vowel_groups(word):
    groups = []
    i = 0
    while i < len(word):
        if word[i] in VOWELS:
            start = i
            while i < len(word) and word[i] in VOWELS:
                i += 1
            groups.append((start, i))
        else:
            i += 1
    return groups


def _stress_index_in_group(word, start, end):
    for i in range(start, end):
        if word[i] in STRONG_VOWELS:
            return i
    return end - 1


def _attach_with_accent(base_form, pronoun):
    """Attaching a pronoun adds a syllable, which shifts where the stress
    would 'naturally' fall if unmarked. Spanish keeps the original stress
    by writing an accent on it once it's no longer the second-to-last
    syllable: habla -> háblate, hable -> háblese. Monosyllabic bases
    (pon, ven, di) never need one."""
    groups = _vowel_groups(base_form)
    if len(groups) <= 1:
        return base_form + pronoun
    start, end = groups[-2]
    idx = _stress_index_in_group(base_form, start, end)
    accented = base_form[:idx] + ACCENT_MAP[base_form[idx]] + base_form[idx + 1 :]
    return accented + pronoun


def strip_se(infinitive):
    if not infinitive.endswith("se"):
        raise ValueError(f"not a reflexive infinitive: {infinitive}")
    return infinitive[:-2]


def preposed(conjugated_forms):
    """conjugated_forms: dict person -> verb form (already conjugated on the
    base, non-reflexive verb). Returns pronoun + form."""
    return {
        person: f"{REFLEXIVE_PRONOUNS[person]} {form}"
        for person, form in conjugated_forms.items()
    }


def preposed_negative_imperative(subjunctive_forms, persons):
    """no te levantes, no se levante, ... 'no' comes first, then pronoun,
    then verb -- distinct from preposed() ordering used elsewhere."""
    return {
        person: f"no {REFLEXIVE_PRONOUNS[person]} {subjunctive_forms[person]}"
        for person in persons
    }


def attached_infinitive(base_infinitive):
    return base_infinitive + "se"


def attached_gerund(gerund_form):
    return _attach_with_accent(gerund_form, "se")


UNACCENTED_TO_ACCENTED = {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú"}


def _nosotros_monos(form):
    """Dropping final -s before attaching -nos shifts the stressed syllable
    relative to the word's end, so Spanish orthography requires marking it:
    levantemos -> levantémonos, vamos -> vámonos."""
    stressed_vowel = form[-4]
    accented = UNACCENTED_TO_ACCENTED[stressed_vowel]
    return form[:-4] + accented + form[-3:-1] + "nos"


def _vosotros_os(imperative_form):
    stem = imperative_form[:-1]  # drop final "d"
    if stem[-1] == "i":
        return stem[:-1] + "íos"
    return stem + "os"


def attached_imperative(imperative_forms, base_infinitive):
    result = {}
    for person, form in imperative_forms.items():
        pronoun = REFLEXIVE_PRONOUNS[person]
        if person == "vosotros":
            result[person] = VOSOTROS_D_DROP.get(base_infinitive) or _vosotros_os(form)
        elif person == "nosotros":
            result[person] = _nosotros_monos(form)
        else:
            result[person] = _attach_with_accent(form, pronoun)
    return result
