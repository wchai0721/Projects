"""
Recommendation engine for the Dopamine Menu Generator.
Scores and ranks activities based on mood, energy, and time constraints.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from activities import ACTIVITIES, MOODS, ENERGY_LEVELS


ENERGY_RANK = {"low": 1, "medium": 2, "high": 3}


@dataclass
class UserInput:
    mood: str
    available_time: int          # minutes
    energy: str                  # "low" | "medium" | "high"
    preferred_categories: list[str] = field(default_factory=list)

    def validate(self) -> list[str]:
        errors = []
        if self.mood not in MOODS:
            errors.append(f"Mood '{self.mood}' not recognized. Choose from: {', '.join(MOODS)}")
        if self.available_time < 2:
            errors.append("Available time must be at least 2 minutes.")
        if self.energy not in ENERGY_LEVELS:
            errors.append(f"Energy '{self.energy}' not recognized. Choose from: {', '.join(ENERGY_LEVELS)}")
        return errors


@dataclass
class ScoredActivity:
    activity: dict
    score: float
    reasons: list[str]


def score_activity(activity: dict, user: UserInput) -> Optional[ScoredActivity]:
    """
    Score an activity for a given user input.
    Returns None if the activity is fundamentally incompatible.
    """
    score = activity["benefit_score"]  # base score (0–10)
    reasons = []

    # Hard filter: time
    if activity["min_time"] > user.available_time:
        return None

    # Hard filter: energy — can't do high-energy activities on low energy
    activity_energy = ENERGY_RANK[activity["energy"]]
    user_energy = ENERGY_RANK[user.energy]
    if activity_energy > user_energy + 1:
        return None

    # Mood match bonus
    if user.mood in activity["moods"]:
        score += 2.0
        reasons.append(f"Directly targets {user.mood} mood")

    # Energy alignment bonus/penalty
    energy_diff = abs(activity_energy - user_energy)
    if energy_diff == 0:
        score += 1.0
        reasons.append("Perfect energy match")
    elif energy_diff == 1:
        score += 0.3
    else:
        score -= 0.5

    # Category preference bonus
    if user.preferred_categories and activity["category"] in user.preferred_categories:
        score += 1.0
        reasons.append(f"Matches your preferred category: {activity['category']}")

    # Time fit bonus — activities that use available time well (not over, not under 25%)
    time_ratio = activity["min_time"] / user.available_time
    if 0.5 <= time_ratio <= 1.0:
        score += 0.5
        reasons.append("Good use of your available time")
    elif time_ratio < 0.25:
        score -= 0.2  # slight penalty for very short activities when lots of time

    if not reasons:
        reasons.append("Evidence-backed general benefit")

    return ScoredActivity(activity=activity, score=round(score, 2), reasons=reasons)


def generate_menu(user: UserInput, top_n: int = 5) -> list[ScoredActivity]:
    """
    Generate a ranked list of recommended activities for the user.
    """
    errors = user.validate()
    if errors:
        raise ValueError("\n".join(errors))

    scored = []
    for activity in ACTIVITIES:
        result = score_activity(activity, user)
        if result is not None:
            scored.append(result)

    # Sort by score descending, then by benefit_score as tiebreaker
    scored.sort(key=lambda x: (x.score, x.activity["benefit_score"]), reverse=True)

    return scored[:top_n]


def format_menu_text(results: list[ScoredActivity], user: UserInput) -> str:
    """
    Render the menu as a clean terminal-friendly text block.
    """
    lines = []
    lines.append("\n" + "═" * 58)
    lines.append("  🧠  YOUR DOPAMINE MENU")
    lines.append("═" * 58)
    lines.append(f"  Mood: {user.mood.capitalize()}  |  Time: {user.available_time} min  |  Energy: {user.energy.capitalize()}")
    lines.append("─" * 58)

    for i, result in enumerate(results, 1):
        a = result.activity
        lines.append(f"\n  #{i}  {a['emoji']}  {a['name']}")
        lines.append(f"       Category: {a['category']}  |  Min time: {a['min_time']} min  |  Score: {result.score:.1f}/12")
        lines.append(f"       Why it works: {a['mechanism']}")
        lines.append(f"       💡 Tip: {a['tip']}")
        lines.append(f"       📖 {a['research_note']}")
        if result.reasons:
            lines.append(f"       ✓ Matched because: {'; '.join(result.reasons)}")
        lines.append("  " + "─" * 54)

    lines.append("\n  Built with positive psychology research.")
    lines.append("  github.com/your-username/dopamine-menu\n")
    return "\n".join(lines)
