"""
Color per tense. Each tense gets its own distinct hue so recognition is
instant during a drill -- no two tenses share a color family. Compound
tenses use a related-but-distinct shade (e.g. present_indicative =
bright_cyan, present_perfect = cyan).
"""

TENSE_COLORS = {
    "present_indicative":          "bright_cyan",
    "present_perfect":             "cyan",
    "preterite":                   "red",
    "imperfect_indicative":        "yellow",
    "pluperfect":                  "bright_yellow",
    "future":                      "blue",
    "future_perfect":              "bright_blue",
    "conditional":                 "magenta",
    "conditional_perfect":         "bright_magenta",
    "present_subjunctive":         "green",
    "present_perfect_subjunctive": "bright_green",
    "imperfect_subjunctive_ra":    "orange1",
    "imperfect_subjunctive_se":    "deep_pink1",
    "pluperfect_subjunctive_ra":   "hot_pink",
    "pluperfect_subjunctive_se":   "medium_purple1",
    "gerund":                      "grey70",
    "imperative_affirmative":      "chartreuse1",
    "imperative_negative":         "chartreuse3",
}


def color_for_tense(tense):
    return TENSE_COLORS.get(tense, "white")
