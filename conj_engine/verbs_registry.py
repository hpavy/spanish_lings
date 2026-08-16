"""
Registry of verbs with their conjugation classification. Each entry:
  infinitive: str
  strong_change: one of e_ie/o_ue/e_i/u_ue or None (present tense boot change)
  weak_change: one of e_i/o_u or None (-ir verbs only, hits preterite/subj/gerund)
  ortho: one of c_qu/g_gu/z_c/cer_zc/guir_g/ger_j/uir_y or None
  tags: curriculum grouping hints (frequency/topic), used by curriculum.py
"""

VERBS = [
    # regular -ar/-er/-ir, high frequency
    {"infinitive": "hablar", "tags": ["a2", "regular_ar"]},
    {"infinitive": "trabajar", "tags": ["a2", "regular_ar"]},
    {"infinitive": "estudiar", "tags": ["a2", "regular_ar"]},
    {"infinitive": "comer", "tags": ["a2", "regular_er"]},
    {"infinitive": "beber", "tags": ["a2", "regular_er"]},
    {"infinitive": "vivir", "tags": ["a2", "regular_ir"]},
    {"infinitive": "escribir", "tags": ["a2", "regular_ir"]},

    # e_ie stem change
    {"infinitive": "querer", "strong_change": "e_ie", "tags": ["b1", "stem_change"]},
    {"infinitive": "pensar", "strong_change": "e_ie", "tags": ["b1", "stem_change"]},
    {"infinitive": "entender", "strong_change": "e_ie", "tags": ["b1", "stem_change"]},
    {"infinitive": "sentir", "strong_change": "e_ie", "weak_change": "e_i", "tags": ["b1", "stem_change"]},
    {"infinitive": "preferir", "strong_change": "e_ie", "weak_change": "e_i", "tags": ["b1", "stem_change"]},

    # o_ue stem change
    {"infinitive": "poder", "strong_change": "o_ue", "tags": ["b1", "stem_change"]},
    {"infinitive": "dormir", "strong_change": "o_ue", "weak_change": "o_u", "tags": ["b1", "stem_change"]},
    {"infinitive": "morir", "strong_change": "o_ue", "weak_change": "o_u", "tags": ["b1", "stem_change"]},
    {"infinitive": "volver", "strong_change": "o_ue", "tags": ["b1", "stem_change"]},
    {"infinitive": "contar", "strong_change": "o_ue", "tags": ["b1", "stem_change"]},

    # e_i stem change (-ir only)
    {"infinitive": "pedir", "strong_change": "e_i", "weak_change": "e_i", "tags": ["b1", "stem_change"]},
    {"infinitive": "servir", "strong_change": "e_i", "weak_change": "e_i", "tags": ["b1", "stem_change"]},
    {"infinitive": "repetir", "strong_change": "e_i", "weak_change": "e_i", "tags": ["b1", "stem_change"]},

    # u_ue
    {"infinitive": "jugar", "strong_change": "u_ue", "ortho": "g_gu", "tags": ["b1", "stem_change"]},

    # orthographic: car/gar/zar
    {"infinitive": "buscar", "ortho": "c_qu", "tags": ["b1", "ortho"]},
    {"infinitive": "sacar", "ortho": "c_qu", "tags": ["b1", "ortho"]},
    {"infinitive": "llegar", "ortho": "g_gu", "tags": ["b1", "ortho"]},
    {"infinitive": "pagar", "ortho": "g_gu", "tags": ["b1", "ortho"]},
    {"infinitive": "empezar", "strong_change": "e_ie", "ortho": "z_c", "tags": ["b1", "ortho", "stem_change"]},
    {"infinitive": "comenzar", "strong_change": "e_ie", "ortho": "z_c", "tags": ["b1", "ortho", "stem_change"]},
    {"infinitive": "cruzar", "ortho": "z_c", "tags": ["b1", "ortho"]},

    # orthographic: cer/cir -> zc
    {"infinitive": "conocer", "ortho": "cer_zc", "tags": ["b1", "ortho"]},
    {"infinitive": "parecer", "ortho": "cer_zc", "tags": ["b1", "ortho"]},

    # orthographic: guir -> g
    {"infinitive": "seguir", "strong_change": "e_i", "weak_change": "e_i", "ortho": "guir_g", "tags": ["b2", "ortho", "stem_change"]},

    # orthographic: ger/gir -> j
    {"infinitive": "coger", "ortho": "ger_j", "tags": ["b1", "ortho"]},
    {"infinitive": "elegir", "strong_change": "e_i", "weak_change": "e_i", "ortho": "ger_j", "tags": ["b2", "ortho", "stem_change"]},
    {"infinitive": "dirigir", "ortho": "ger_j", "tags": ["b1", "ortho"]},

    # orthographic: uir -> y
    {"infinitive": "construir", "ortho": "uir_y", "tags": ["b1", "ortho"]},
    {"infinitive": "huir", "ortho": "uir_y", "tags": ["b1", "ortho"]},
    {"infinitive": "destruir", "ortho": "uir_y", "tags": ["b1", "ortho"]},

    # true irregulars
    {"infinitive": "ser", "tags": ["a1", "irregular"]},
    {"infinitive": "estar", "tags": ["a1", "irregular"]},
    {"infinitive": "ir", "tags": ["a1", "irregular"]},
    {"infinitive": "haber", "tags": ["a2", "irregular"]},
    {"infinitive": "dar", "tags": ["a2", "irregular"]},
    {"infinitive": "ver", "tags": ["a2", "irregular"]},
    {"infinitive": "tener", "tags": ["a2", "irregular"]},
    {"infinitive": "hacer", "tags": ["a2", "irregular"]},
    {"infinitive": "saber", "tags": ["a2", "irregular"]},
    {"infinitive": "poner", "tags": ["a2", "irregular"]},
    {"infinitive": "venir", "tags": ["a2", "irregular"]},
    {"infinitive": "decir", "tags": ["a2", "irregular"]},
    {"infinitive": "traer", "tags": ["b1", "irregular"]},
    {"infinitive": "caer", "tags": ["b1", "irregular"]},
    {"infinitive": "oir", "tags": ["b1", "irregular"]},
    {"infinitive": "salir", "tags": ["a2", "irregular"]},
    {"infinitive": "valer", "tags": ["b2", "irregular"]},
    {"infinitive": "caber", "tags": ["b2", "irregular"]},
    {"infinitive": "andar", "tags": ["b1", "irregular"]},

    # reflexive
    {"infinitive": "levantarse", "reflexive": True, "tags": ["b1", "reflexive"]},
    {"infinitive": "sentirse", "reflexive": True, "strong_change": "e_ie", "weak_change": "e_i", "tags": ["b1", "reflexive", "stem_change"]},
    {"infinitive": "vestirse", "reflexive": True, "strong_change": "e_i", "weak_change": "e_i", "tags": ["b1", "reflexive", "stem_change"]},
    {"infinitive": "irse", "reflexive": True, "tags": ["b1", "reflexive", "irregular"]},
    {"infinitive": "atreverse", "reflexive": True, "tags": ["b2", "reflexive"]},
    {"infinitive": "quejarse", "reflexive": True, "tags": ["b1", "reflexive"]},
    {"infinitive": "despertarse", "reflexive": True, "strong_change": "e_ie", "tags": ["b1", "reflexive", "stem_change"]},

    # irregular past participle only
    {"infinitive": "romper", "tags": ["b1", "irregular_participle"]},
    {"infinitive": "abrir", "tags": ["b1", "irregular_participle"]},
    {"infinitive": "cubrir", "tags": ["b2", "irregular_participle"]},
    {"infinitive": "resolver", "strong_change": "o_ue", "tags": ["b2", "irregular_participle", "stem_change"]},
    {"infinitive": "devolver", "strong_change": "o_ue", "tags": ["b2", "irregular_participle", "stem_change"]},
]

BY_INFINITIVE = {v["infinitive"]: v for v in VERBS}
