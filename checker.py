import unicodedata


def _strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def check(user_input, expected):
    """Returns ('correct', 'accent_only', or 'wrong'). accent_only means
    right word but missing/wrong accents -- flagged, not silently accepted,
    since accents matter for C1 writing."""
    user = user_input.strip().lower()
    exp = expected.strip().lower()
    if user == exp:
        return "correct"
    if _strip_accents(user) == _strip_accents(exp):
        return "accent_only"
    return "wrong"
