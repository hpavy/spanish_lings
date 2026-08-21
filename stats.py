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

console = Console()


def take_snapshot(state):
    """Capture current metrics for trend tracking. Called after each session."""
    srs = state["srs"]
    total_items = len(srs)
    total_seen = sum(v["seen"] for v in srs.values())
    total_correct = sum(v["correct"] for v in srs.values())
    today = datetime.date.today().isoformat()
    due = sum(1 for v in srs.values() if v["due"] <= today)
    mastered = sum(1 for v in srs.values() if v["box"] >= 4)
    accuracy = total_correct / total_seen if total_seen else 0.0
    return {
        "date": today,
        "mastered": mastered,
        "seen": total_items,
        "accuracy": round(accuracy, 4),
        "due": due,
    }


def _delta(current, old, suffix="%", invert=False):
    """Format a delta with arrow. invert=True means decrease is good (due)."""
    if old is None:
        return ""
    diff = current - old
    if diff == 0:
        return "(→)"
    arrow = "↑" if diff > 0 else "↓"
    good = (diff > 0) != invert
    color = "green" if good else "red"
    if suffix == "%":
        return f"([{color}]{arrow} {abs(diff):.1f}{suffix}[/{color}])"
    return f"([{color}]{arrow} {abs(diff)}{suffix}[/{color}])"


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

    # --- weekly delta --------------------------------------------------------
    history = state.get("history", [])
    week_ago = None
    if history:
        cutoff = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
        for entry in reversed(history):
            if entry["date"] <= cutoff:
                week_ago = entry
                break
        if week_ago is None:
            week_ago = history[0]

    if week_ago:
        d_acc = _delta(overall_acc * 100, week_ago["accuracy"] * 100)
        d_mastered = _delta(mastered, week_ago["mastered"], suffix="")
        d_seen = _delta(total_items, week_ago["seen"], suffix="")
        d_due = _delta(due, week_ago["due"], suffix="", invert=True)

        console.print("[bold]this week[/bold]")
        console.print(
            f"  [dim]mastered[/dim]  {mastered} {d_mastered}    "
            f"[dim]accuracy[/dim]  {overall_acc * 100:.1f}% {d_acc}    "
            f"[dim]seen[/dim]  {total_items} {d_seen}    "
            f"[dim]due[/dim]  {due} {d_due}"
        )
        console.print()

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
        is_mastered = tier_is_mastered(state, tier["id"])
        bar_len = 20
        pct = min(acc / ACCURACY_THRESHOLD, 1.0) if n else 0.0
        filled = int(bar_len * pct)
        bar = "█" * filled + "░" * (bar_len - filled)
        status = "✓" if is_mastered else " "
        console.print(
            f"  {status} [dim]{tier['id']:35s}[/dim] {bar} "
            f"{acc * 100:.0f}% ({n})"
        )
    console.print()
