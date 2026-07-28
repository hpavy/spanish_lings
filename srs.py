"""
Leitner-box spaced repetition. Each item lives in a box 1-5. Correct answer
promotes it (longer interval before it's due again); wrong answer demotes it
to box 1 (due immediately / very soon). Box -> interval in days below.

State is a flat dict keyed by item_id (see conj_engine.exercise.item_id):
  {"box": int, "due": "YYYY-MM-DD", "seen": int, "correct": int}
"""

import datetime

BOX_INTERVALS_DAYS = {1: 0, 2: 1, 3: 3, 4: 7, 5: 16}
MAX_BOX = 5


def _today():
    return datetime.date.today().isoformat()


def new_item_state():
    return {"box": 1, "due": _today(), "seen": 0, "correct": 0}


def record_answer(state, item_id, was_correct):
    entry = state.get(item_id, new_item_state())
    entry["seen"] += 1
    if was_correct:
        entry["correct"] += 1
        entry["box"] = min(entry["box"] + 1, MAX_BOX)
    else:
        entry["box"] = 1

    interval = BOX_INTERVALS_DAYS[entry["box"]]
    due_date = datetime.date.today() + datetime.timedelta(days=interval)
    entry["due"] = due_date.isoformat()

    state[item_id] = entry
    return entry


def is_due(state, item_id):
    entry = state.get(item_id)
    if entry is None:
        return True
    return entry["due"] <= _today()


def due_items(state, all_item_ids):
    return [iid for iid in all_item_ids if is_due(state, iid)]


def new_items(state, all_item_ids):
    """Items never seen before -- distinct from due-for-review items."""
    return [iid for iid in all_item_ids if iid not in state]
