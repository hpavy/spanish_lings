"""
Ordered tiers from A2 -> C1. Each tier is a (verb_tags, tenses) pair: any verb
carrying one of the listed tags, drilled in the listed tenses, becomes part
of that tier's exercise pool. Tiers are cumulative for the SRS: once a tier
is unlocked, its items stay in the pool forever (see srs.py).
"""

TIERS = [
    {
        "id": "01_present_regular",
        "label": "Present indicative — regular verbs",
        "verb_tags": ["regular_ar", "regular_er", "regular_ir"],
        "tenses": ["present_indicative"],
    },
    {
        "id": "02_present_stem_change",
        "label": "Present indicative — stem-changing verbs",
        "verb_tags": ["stem_change"],
        "tenses": ["present_indicative"],
    },
    {
        "id": "03_present_ortho",
        "label": "Present indicative — spelling-change verbs",
        "verb_tags": ["ortho"],
        "tenses": ["present_indicative"],
    },
    {
        "id": "04_present_irregular",
        "label": "Present indicative — irregular verbs",
        "verb_tags": ["irregular"],
        "tenses": ["present_indicative"],
    },
    {
        "id": "05_preterite_regular",
        "label": "Preterite — regular verbs",
        "verb_tags": ["regular_ar", "regular_er", "regular_ir"],
        "tenses": ["preterite"],
    },
    {
        "id": "06_preterite_ortho_stem",
        "label": "Preterite — spelling-change & stem-changing verbs",
        "verb_tags": ["ortho", "stem_change"],
        "tenses": ["preterite"],
    },
    {
        "id": "07_preterite_irregular",
        "label": "Preterite — irregular verbs",
        "verb_tags": ["irregular"],
        "tenses": ["preterite"],
    },
    {
        "id": "08_imperfect",
        "label": "Imperfect indicative (all verb types)",
        "verb_tags": ["regular_ar", "regular_er", "regular_ir", "stem_change", "ortho", "irregular"],
        "tenses": ["imperfect_indicative"],
    },
    {
        "id": "09_future_conditional",
        "label": "Future & conditional",
        "verb_tags": ["regular_ar", "regular_er", "regular_ir", "stem_change", "ortho", "irregular"],
        "tenses": ["future", "conditional"],
    },
    {
        "id": "10_gerund_participle",
        "label": "Gerund & past participle",
        "verb_tags": ["regular_ar", "regular_er", "regular_ir", "stem_change", "ortho", "irregular", "irregular_participle"],
        "tenses": ["gerund"],
    },
    {
        "id": "11_present_perfect",
        "label": "Present perfect",
        "verb_tags": ["regular_ar", "regular_er", "regular_ir", "stem_change", "ortho", "irregular", "irregular_participle"],
        "tenses": ["present_perfect"],
    },
    {
        "id": "12_pluperfect_future_perfect",
        "label": "Pluperfect, future perfect, conditional perfect",
        "verb_tags": ["regular_ar", "regular_er", "regular_ir", "irregular"],
        "tenses": ["pluperfect", "future_perfect", "conditional_perfect"],
    },
    {
        "id": "13_present_subjunctive",
        "label": "Present subjunctive (all verb types)",
        "verb_tags": ["regular_ar", "regular_er", "regular_ir", "stem_change", "ortho", "irregular"],
        "tenses": ["present_subjunctive"],
    },
    {
        "id": "14_imperfect_subjunctive",
        "label": "Imperfect subjunctive (-ra / -se)",
        "verb_tags": ["regular_ar", "regular_er", "regular_ir", "stem_change", "ortho", "irregular"],
        "tenses": ["imperfect_subjunctive_ra", "imperfect_subjunctive_se"],
    },
    {
        "id": "15_perfect_subjunctive",
        "label": "Present & pluperfect subjunctive",
        "verb_tags": ["regular_ar", "regular_er", "regular_ir", "irregular"],
        "tenses": ["present_perfect_subjunctive", "pluperfect_subjunctive_ra", "pluperfect_subjunctive_se"],
    },
    {
        "id": "16_imperative",
        "label": "Imperative — affirmative & negative",
        "verb_tags": ["regular_ar", "regular_er", "regular_ir", "stem_change", "irregular"],
        "tenses": ["imperative_affirmative", "imperative_negative"],
    },
    {
        "id": "17_reflexive",
        "label": "Reflexive verbs — full paradigm",
        "verb_tags": ["reflexive"],
        "tenses": [
            "present_indicative", "preterite", "present_subjunctive",
            "imperative_affirmative", "imperative_negative", "gerund",
        ],
    },
]


def verbs_for_tier(tier, all_verbs):
    tags = set(tier["verb_tags"])
    return [v for v in all_verbs if tags & set(v.get("tags", []))]


def tier_by_id(tier_id):
    for tier in TIERS:
        if tier["id"] == tier_id:
            return tier
    raise KeyError(f"no tier with id {tier_id}")


def tier_index(tier_id):
    for i, tier in enumerate(TIERS):
        if tier["id"] == tier_id:
            return i
    raise KeyError(f"no tier with id {tier_id}")
