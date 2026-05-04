#!/usr/bin/env python3
"""
Dopamine Menu Generator — Command Line Interface
Run: python cli.py
"""

import sys
from engine import UserInput, generate_menu, format_menu_text
from activities import MOODS, ENERGY_LEVELS, CATEGORIES


def prompt_choice(label: str, options: list[str]) -> str:
    print(f"\n  {label}")
    for i, opt in enumerate(options, 1):
        print(f"    [{i}] {opt}")
    while True:
        raw = input("  → Enter number or name: ").strip().lower()
        # Try by number
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx]
        # Try by name
        matches = [o for o in options if o.lower().startswith(raw)]
        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            print(f"  Ambiguous — did you mean: {', '.join(matches)}?")
        else:
            print(f"  Not recognized. Options: {', '.join(options)}")


def prompt_int(label: str, min_val: int = 2, max_val: int = 480) -> int:
    while True:
        raw = input(f"\n  {label}: ").strip()
        if raw.isdigit():
            val = int(raw)
            if min_val <= val <= max_val:
                return val
            print(f"  Please enter a number between {min_val} and {max_val}.")
        else:
            print("  Please enter a whole number.")


def prompt_categories() -> list[str]:
    print(f"\n  Any preferred activity types? (optional — press Enter to skip)")
    print(f"  Options: {', '.join(CATEGORIES)}")
    raw = input("  → ").strip()
    if not raw:
        return []
    selected = []
    for part in raw.replace(",", " ").split():
        matches = [c for c in CATEGORIES if c.lower().startswith(part.lower())]
        if matches:
            selected.append(matches[0])
    return selected


def run_cli():
    print("\n" + "═" * 58)
    print("  🧠  DOPAMINE MENU GENERATOR")
    print("  Evidence-backed restoration, personalized for right now.")
    print("═" * 58)

    mood = prompt_choice("How are you feeling?", MOODS)
    time_available = prompt_int("How many minutes do you have? (2–480)", min_val=2, max_val=480)
    energy = prompt_choice("What's your energy level?", ENERGY_LEVELS)
    preferred_cats = prompt_categories()

    user = UserInput(
        mood=mood,
        available_time=time_available,
        energy=energy,
        preferred_categories=preferred_cats,
    )

    try:
        results = generate_menu(user, top_n=5)
    except ValueError as e:
        print(f"\n  Error: {e}")
        sys.exit(1)

    if not results:
        print("\n  No activities matched your current filters. Try more time or higher energy.")
        sys.exit(0)

    print(format_menu_text(results, user))

    # Offer to save
    save = input("  Save this menu to a file? (y/N): ").strip().lower()
    if save == "y":
        filename = f"dopamine_menu_{mood}_{time_available}min.txt"
        with open(filename, "w") as f:
            f.write(format_menu_text(results, user))
        print(f"  Saved to {filename}\n")


if __name__ == "__main__":
    run_cli()
