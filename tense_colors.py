"""
Tense display: Spanish label + distinct color per tense.

Colors are chosen so tenses sharing a word (e.g. all "present *") get
very different hues -- no two tenses in the same word-family share a
color family. 256-color codes (color(N)) are used where the basic 16
aren't enough to keep things distinct.
"""

# --- Spanish labels ----------------------------------------------------------

TENSE_LABELS = {
    "present_indicative":          "Presente",
    "present_perfect":             "Pret. perfecto",
    "preterite":                   "Pret. indefinido",
    "imperfect_indicative":        "Pret. imperfecto",
    "pluperfect":                  "Pluscuamperfecto",
    "future":                      "Futuro",
    "future_perfect":               "Futuro perfecto",
    "conditional":                 "Condicional",
    "conditional_perfect":         "Cond. compuesto",
    "present_subjunctive":         "Presente subj.",
    "present_perfect_subjunctive": "Pret. perfecto subj.",
    "imperfect_subjunctive_ra":    "Imperfecto -ra subj.",
    "imperfect_subjunctive_se":    "Imperfecto -se subj.",
    "pluperfect_subjunctive_ra":   "Pluscuam. -ra subj.",
    "pluperfect_subjunctive_se":   "Pluscuam. -se subj.",
    "gerund":                      "Gerundio",
    "imperative_affirmative":      "Imperativo afirm.",
    "imperative_negative":         "Imperativo neg.",
}

# --- Colors ------------------------------------------------------------------
#
# Word-family groups and their hues (all different within each group):
#   present *  → cyan, red, yellow, blue      (4 very different hues)
#   imperfect * → green, pink, purple          (3 very different hues)
#   pluperfect * → orange, teal, dark-red     (3 very different hues)
#   future *   → magenta, light-green          (2 different hues)
#   conditional * → gold, light-blue           (2 different hues)
#   imperative * → light-green-ish, tan         (2 different hues)

TENSE_COLORS = {
    "present_indicative":          "color(51)",    # bright cyan
    "present_perfect":             "color(196)",   # bright red
    "present_subjunctive":         "color(226)",   # bright yellow
    "present_perfect_subjunctive": "color(21)",    # bright blue
    "preterite":                   "color(201)",   # bright magenta
    "imperfect_indicative":        "color(46)",    # bright green
    "pluperfect":                  "color(208)",   # orange
    "future":                      "color(129)",   # purple
    "future_perfect":              "color(72)",    # teal
    "conditional":                 "color(172)",   # dark gold/brown
    "conditional_perfect":         "color(75)",    # light blue
    "imperfect_subjunctive_ra":    "color(162)",   # rose/pink
    "imperfect_subjunctive_se":    "color(99)",    # light purple
    "pluperfect_subjunctive_ra":   "color(30)",    # dark teal
    "pluperfect_subjunctive_se":   "color(124)",   # dark red
    "gerund":                      "color(245)",   # light grey
    "imperative_affirmative":      "color(120)",   # light green
    "imperative_negative":         "color(180)",   # pale tan/khaki
}


def color_for_tense(tense):
    return TENSE_COLORS.get(tense, "white")


def label_for_tense(tense):
    return TENSE_LABELS.get(tense, tense)
