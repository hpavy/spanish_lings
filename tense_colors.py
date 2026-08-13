"""
Color per tense, grouped by time-family so recognition is fast during a
drill: same hue for a mood/time family (e.g. green = present), brighter
shade of that hue for its compound tense (e.g. bright_green = present
perfect). Imperative and gerund are their own families outside this.
"""

TENSE_COLORS = {
    "present_indicative": "bold green",
    "present_perfect": "bright_green",
    "preterite": "red",
    "imperfect_indicative": "yellow",
    "pluperfect": "bright_yellow",
    "future": "blue",
    "future_perfect": "bright_blue",
    "conditional": "magenta",
    "conditional_perfect": "bright_magenta",
    "present_subjunctive": "cyan",
    "present_perfect_subjunctive": "bright_cyan",
    "imperfect_subjunctive_ra": "white",
    "imperfect_subjunctive_se": "white",
    "pluperfect_subjunctive_ra": "bright_white",
    "pluperfect_subjunctive_se": "bright_white",
    "gerund": "grey70",
    "imperative_affirmative": "orange1",
    "imperative_negative": "orange1",
}


def color_for_tense(tense):
    return TENSE_COLORS.get(tense, "white")
