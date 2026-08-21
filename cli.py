import glob

from rich.console import Console
from rich.panel import Panel

from curriculum import TIERS, tier_index
from conj_engine.exercise import item_id, prompt
from progress_store import load, save
from session import pick_session, all_items_for_tiers
from srs import record_answer, due_items, new_items
from checker import check
from tier_progress import record_tier_log, tier_accuracy, tier_is_mastered, MIN_SAMPLE, ACCURACY_THRESHOLD
from tense_colors import color_for_tense, label_for_tense
from stats import print_dashboard, take_snapshot

console = Console()


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
    if tier_is_mastered(state, tier["id"]):
        state["unlocked_tiers"].append(TIERS[idx + 1]["id"])
        return True
    return False


def book_chapter_for_tier(tier_id):
    prefix = tier_id.split("_")[0]
    matches = glob.glob(f"book/{prefix}_*.md")
    return matches[0] if matches else None


def print_progress(state):
    console.print()
    current = state["unlocked_tiers"][-1]
    for tier in TIERS:
        if tier["id"] not in state["unlocked_tiers"]:
            break
        sample_size, accuracy = tier_accuracy(state, tier["id"])
        if tier["id"] == current:
            bar_len = 20
            pct = min(accuracy / ACCURACY_THRESHOLD, 1.0) if sample_size else 0.0
            filled = int(bar_len * pct)
            bar = "█" * filled + "░" * (bar_len - filled)
            console.print(
                f"[dim]{tier['id']:32s}[/dim] {bar} "
                f"{accuracy * 100:.0f}% accuracy over last {sample_size} answers "
                f"(need {ACCURACY_THRESHOLD * 100:.0f}% over {MIN_SAMPLE}+)"
            )
        else:
            console.print(f"[dim]{tier['id']:32s}[/dim] cleared")
    console.print()

    chapter = book_chapter_for_tier(current)
    if chapter:
        console.print(f"[dim]rule reference: {chapter}[/dim]\n")


def run_session(state, session_size=15):
    unlocked = state["unlocked_tiers"]
    items = pick_session(state, unlocked, session_size=session_size)
    if not items:
        console.print("[yellow]Nothing to drill right now — all caught up.[/yellow]")
        return

    correct_count = 0
    for item in items:
        answer = item["answer"]
        tense = item["tense"]
        color = color_for_tense(tense)
        label = label_for_tense(tense)
        console.print(Panel(prompt(item), title=f"[{color}]{label}[/{color}]", expand=False))
        user_input = console.input("> ")

        result = check(user_input, answer)
        iid = item_id(item)

        was_correct = result == "correct"
        if result == "correct":
            console.print("[green]correct[/green]\n")
            correct_count += 1
        elif result == "accent_only":
            console.print(f"[yellow]almost — check accents. correct: {answer}[/yellow]\n")
        else:
            console.print(f"[red]wrong — correct: {answer}[/red]\n")

        record_answer(state["srs"], iid, was_correct=was_correct)
        record_tier_log(state, item["tiers"], was_correct)

    console.print(f"session done: {correct_count}/{len(items)} correct")

    if maybe_unlock_next_tier(state):
        newly_unlocked = TIERS[tier_index(state["unlocked_tiers"][-1])]
        console.print(f"[bold green]tier unlocked: {newly_unlocked['label']}[/bold green]")


def main():
    state = load()
    if not state["unlocked_tiers"]:
        state["unlocked_tiers"] = [TIERS[0]["id"]]

    print_dashboard(state)
    run_session(state)
    state.setdefault("history", []).append(take_snapshot(state))
    # keep only last 90 snapshots (~3 months of daily practice)
    del state["history"][:-90]
    save(state)


if __name__ == "__main__":
    main()
