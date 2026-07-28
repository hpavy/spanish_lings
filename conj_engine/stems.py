PERSONS = ["yo", "tu", "el", "nosotros", "vosotros", "ellos"]


def split_infinitive(infinitive):
    """('hablar') -> ('habl', 'ar')"""
    ending = infinitive[-2:]
    if ending not in ("ar", "er", "ir"):
        raise ValueError(f"not a valid infinitive: {infinitive}")
    return infinitive[:-2], ending
