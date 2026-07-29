"""
Rolling per-tier accuracy tracking, shared by cli.py (to decide when to
unlock the next tier) and session.py (to decide how much to bias a session
toward the tier currently being learned).
"""

LOG_WINDOW = 40
MIN_SAMPLE = 30
ACCURACY_THRESHOLD = 0.85


def record_tier_log(state, tier_ids, was_correct):
    log = state["tier_log"]
    for tier_id in tier_ids:
        entries = log.setdefault(tier_id, [])
        entries.append(was_correct)
        del entries[:-LOG_WINDOW]


def tier_accuracy(state, tier_id):
    entries = state["tier_log"].get(tier_id, [])
    if not entries:
        return 0, 0.0
    return len(entries), sum(entries) / len(entries)


def tier_is_mastered(state, tier_id):
    sample_size, accuracy = tier_accuracy(state, tier_id)
    return sample_size >= MIN_SAMPLE and accuracy >= ACCURACY_THRESHOLD
