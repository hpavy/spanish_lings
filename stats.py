"""
Session dashboard: a compact stats summary shown before each session.
Gives a quick "where am I" snapshot so you know what to focus on.
"""

import datetime
from collections import Counter

from rich.console import Console
from rich.table import Table

from curriculum import TIERS
from tier_progress import tier_accuracy, tier_is_mastered, ACCURACY_THRESHOLD
from conj_engine.exercise import PERSON_LABELS
from tense_colors import label_for_tense

console = Console()


def _format_item(iid):
    """Parse 'parecer|present_subjunctive|tu' -> 'parecer (Presente subj., tú)'"""
    parts = iid.split("|")
    verb = parts[0]
    tense = parts[1] if len(parts) > 1 else ""
    person = parts[2] if len(parts) > 2 else None
    tense_label = label_for_tense(tense)
    person_label = PERSON_LABELS.get(person)
    if person_label:
        return f"{verb} ({tense_label}, {person_label})"
    return f"{verb} ({tense_label})"


def print_dashboard(state):
    srs = state["srs"]
    total_items = len(srs)
    if total_items == 0:
        console.print("[dim]no items yet[/dim]\n")
        return

    total_seen = sum(v["seen"] for v in srs.values())
    total_correct = sum(v["correct"] for v in srs.values())
    overall_acc = total_correct / total_seen if total_seen else 0

    today = datetime.date.today().isoformat()
    due = sum(1 for v in srs.values() if v["due"] <= today)

    mastered = sum(1 for v in srs.values() if v["box"] >= 4)
    mastered_pct = mastered / total_items * 100

    boxes = Counter(v["box"] for v in srs.values())

    # --- summary table -------------------------------------------------------
    summary = Table(show_header=False, box=None, padding=(0, 2))
    summary.add_column(style="bold")
    summary.add_column()
    summary.add_column(style="bold")
    summary.add_column()
    summary.add_column(style="bold")
    summary.add_column()
    summary.add_row(
        "accuracy", f"{overall_acc * 100:.1f}%",
        "mastered", f"{mastered}/{total_items} ({mastered_pct:.0f}%)",
        "due", f"{due} ({due / total_items * 100:.0f}%)",
    )
    console.print(summary)
    console.print()

    # --- box distribution ----------------------------------------------------
    max_box_count = max(boxes.values()) if boxes else 1
    box_parts = []
    for b in range(1, 8):
        count = boxes.get(b, 0)
        bar_len = max(1, int(count / max_box_count * 20))
        box_parts.append(f"[dim]box {b}[/dim] {'█' * bar_len} {count}")
    console.print("  ".join(box_parts))
    console.print()

    # --- all tiers ----------------------------------------------------------
    console.print("[bold]tiers[/bold]")
    for tier in TIERS:
        if tier["id"] not in state["unlocked_tiers"]:
            break
        n, acc = tier_accuracy(state, tier["id"])
        mastered = tier_is_mastered(state, tier["id"])
        bar_len = 20
        pct = min(acc / ACCURACY_THRESHOLD, 1.0) if n else 0.0
        filled = int(bar_len * pct)
        bar = "█" * filled + "░" * (bar_len - filled)
        status = "✓" if mastered else " "
        console.print(
            f"  {status} [dim]{tier['id']:35s}[/dim] {bar} "
            f"{acc * 100:.0f}% ({n})"
        )
    console.print()

    # --- weakest items -------------------------------------------------------
    weak = []
    for iid, v in srs.items():
        if v["seen"] >= 3:
            acc = v["correct"] / v["seen"]
            if acc < 0.80:
                weak.append((iid, acc, v["seen"], v["correct"]))
    weak.sort(key=lambda x: x[1])


