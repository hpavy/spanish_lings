"""
Builds the pool of drillable items for a set of unlocked tiers, and picks
what to show in a given session: due-for-review items first, then new items
to fill up to the session size.
"""

import random

from curriculum import TIERS, verbs_for_tier
from conj_engine.verbs_registry import VERBS
from conj_engine.exercise import build_items, item_id
from srs import due_items, new_items


def all_items_for_tiers(unlocked_tier_ids):
    items_by_id = {}
    for tier in TIERS:
        if tier["id"] not in unlocked_tier_ids:
            continue
        verbs = verbs_for_tier(tier, VERBS)
        for verb in verbs:
            for tense in tier["tenses"]:
                for item in build_items(verb, tense):
                    items_by_id[item_id(item)] = item
    return items_by_id


def pick_session(state, unlocked_tier_ids, session_size=15, new_ratio=0.3):
    items_by_id = all_items_for_tiers(unlocked_tier_ids)
    all_ids = list(items_by_id.keys())

    due = due_items(state, all_ids)
    fresh = new_items(state, all_ids)

    due_seen = [i for i in due if i not in fresh]
    random.shuffle(due_seen)
    random.shuffle(fresh)

    new_budget = max(1, int(session_size * new_ratio)) if fresh else 0
    picked = due_seen[: session_size - new_budget] + fresh[:new_budget]

    if len(picked) < session_size:
        overflow_pool = [i for i in due_seen + fresh if i not in picked]
        picked += overflow_pool[: session_size - len(picked)]

    random.shuffle(picked)
    return [items_by_id[i] for i in picked]
