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
from tier_progress import tier_is_mastered


def all_items_for_tiers(unlocked_tier_ids):
    """Each item also carries a 'tiers' list: every unlocked tier whose
    (verb_tags, tenses) claims it. An item can belong to more than one tier
    if tag/tense ranges overlap; this is used to attribute correct/wrong
    answers to the right tier's rolling accuracy log."""
    items_by_id = {}
    for tier in TIERS:
        if tier["id"] not in unlocked_tier_ids:
            continue
        verbs = verbs_for_tier(tier, VERBS)
        for verb in verbs:
            for tense in tier["tenses"]:
                for item in build_items(verb, tense):
                    iid = item_id(item)
                    if iid in items_by_id:
                        items_by_id[iid]["tiers"].append(tier["id"])
                    else:
                        item["tiers"] = [tier["id"]]
                        items_by_id[iid] = item
    return items_by_id


def _split_due_new(state, ids):
    due = due_items(state, ids)
    fresh = new_items(state, ids)
    due_seen = [i for i in due if i not in fresh]
    random.shuffle(due_seen)
    random.shuffle(fresh)
    return due_seen, fresh


def _fill_bucket(due_seen, fresh, budget, new_ratio):
    if budget <= 0:
        return []
    new_budget = max(1, int(budget * new_ratio)) if fresh else 0
    picked = due_seen[: budget - new_budget] + fresh[:new_budget]
    if len(picked) < budget:
        overflow = [i for i in due_seen + fresh if i not in picked]
        picked += overflow[: budget - len(picked)]
    return picked


def pick_session(state, unlocked_tier_ids, session_size=15, new_ratio=0.3, current_tier_ratio=0.6):
    """Reserves current_tier_ratio of the session for the most recently
    unlocked tier, as long as it hasn't been mastered yet -- otherwise its
    (usually small) pool gets drowned out by older, larger tiers that keep
    resurfacing via SRS review. Once the current tier is mastered (i.e. the
    whole curriculum is cleared, or between unlocks), sessions fall back to
    an even mix across all unlocked tiers so no single tier hogs review
    forever."""
    items_by_id = all_items_for_tiers(unlocked_tier_ids)
    current_tier_id = unlocked_tier_ids[-1]
    still_learning_current = not tier_is_mastered(state, current_tier_id)

    current_ids = [i for i, item in items_by_id.items() if current_tier_id in item["tiers"]]
    other_ids = [i for i, item in items_by_id.items() if current_tier_id not in item["tiers"]]

    if other_ids and still_learning_current:
        current_budget = int(session_size * current_tier_ratio)
        review_ids = other_ids
    else:
        # current tier already mastered (or nothing else to review): treat
        # everything as one even pool instead of reserving a fixed share.
        current_budget = 0
        review_ids = current_ids + other_ids
    review_budget = session_size - current_budget

    current_due, current_fresh = _split_due_new(state["srs"], current_ids)
    picked_current = _fill_bucket(current_due, current_fresh, current_budget, new_ratio)

    review_due, review_fresh = _split_due_new(state["srs"], review_ids)
    picked_review = _fill_bucket(review_due, review_fresh, review_budget, new_ratio)

    picked = picked_current + picked_review
    if len(picked) < session_size:
        leftover = [i for i in current_ids + other_ids if i not in picked]
        random.shuffle(leftover)
        picked += leftover[: session_size - len(picked)]

    random.shuffle(picked)
    return [items_by_id[i] for i in picked]
