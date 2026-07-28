from rich.console import Console
from rich.panel import Panel

from curriculum import TIERS, tier_index, verbs_for_tier
from conj_engine.verbs_registry import VERBS
from conj_engine.exercise import build_items, item_id, prompt, PERSON_LABELS
from progress_store import load, save
from session import pick_session, all_items_for_tiers
from srs import record_answer, due_items, new_items
from checker import check

console = Console()


def tier_completion(state, tier):
    verbs = verbs_for_tier(tier, VERBS)
    total = 0
    mastered = 0
    for verb in verbs:
        for tense in tier["tenses"]:
            for item in build_items(verb, tense):
                total += 1
                entry = state["srs"].get(item_id(item))
                if entry and entry["box"] >= 3:
                    mastered += 1
    return mastered, total


def maybe_unlock_next_tier(state):
    unlocked = state["unlocked_tiers"]
    if not unlocked:
        state["unlocked_tiers"] = [TIERS[0]["id"]]
        return True

    last_unlocked = unlocked[-1]
    idx = tier_index(last_unlocked)
    if idx + 1 >= len(TIERS):
        return False

    tier = TIERS[idx]
    mastered, total = tier_completion(state, tier)
    if total > 0 and mastered / total >= 0.8:
        state["unlocked_tiers"].append(TIERS[idx + 1]["id"])
        return True
    return False


def print_progress(state):
    console.print()
    for tier in TIERS:
        if tier["id"] not in state["unlocked_tiers"]:
            break
        mastered, total = tier_completion(state, tier)
        bar_len = 20
        filled = int(bar_len * mastered / total) if total else 0
        bar = "█" * filled + "░" * (bar_len - filled)
        console.print(f"[dim]{tier['id']:32s}[/dim] {bar} {mastered}/{total}")
    console.print()


def run_session(state, session_size=15):
    unlocked = state["unlocked_tiers"]
    items = pick_session(state, unlocked, session_size=session_size)
    if not items:
        console.print("[yellow]Nothing to drill right now — all caught up.[/yellow]")
        return

    correct_count = 0
    for item in items:
        answer = item["answer"]
        console.print(Panel(prompt(item), title=item["tense"], expand=False))
        user_input = console.input("> ")

        result = check(user_input, answer)
        iid = item_id(item)

        if result == "correct":
            console.print("[green]correct[/green]\n")
            record_answer(state["srs"], iid, was_correct=True)
            correct_count += 1
        elif result == "accent_only":
            console.print(f"[yellow]almost — check accents. correct: {answer}[/yellow]\n")
            record_answer(state["srs"], iid, was_correct=False)
        else:
            console.print(f"[red]wrong — correct: {answer}[/red]\n")
            record_answer(state["srs"], iid, was_correct=False)

    console.print(f"session done: {correct_count}/{len(items)} correct")

    if maybe_unlock_next_tier(state):
        newly_unlocked = TIERS[tier_index(state["unlocked_tiers"][-1])]
        console.print(f"[bold green]tier unlocked: {newly_unlocked['label']}[/bold green]")


def main():
    state = load()
    if not state["unlocked_tiers"]:
        state["unlocked_tiers"] = [TIERS[0]["id"]]

    print_progress(state)
    run_session(state)
    save(state)


if __name__ == "__main__":
    main()
