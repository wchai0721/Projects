# 🧠 Dopamine Menu Generator

> *Evidence-backed restorative activities, personalized for how you actually feel right now.*

A Python tool that takes your current mood, available time, and energy level — then generates a ranked "menu" of restorative activities grounded in positive psychology research (Seligman, Csikszentmihalyi, Fredrickson, Pennebaker, and others).

**Two ways to use it:** a clean terminal CLI, or a local web app with a thoughtful UI.

---

## Why this exists

Most productivity apps assume you want to optimize. This one assumes you're human. The activity recommendations are scored by psychological mechanism — not by what's easiest or most popular — and each one includes the research behind it and a concrete, specific tip for actually doing it.

---

## Features

- **25+ evidence-backed activities** across 7 categories: Movement, Creative, Social, Rest, Learning, Meaning, Sensory
- **Scoring engine** that weights mood match, energy alignment, time fit, and base benefit score
- **Research citations** for every activity (real papers, not vibes)
- **Concrete tips** — not "go for a walk" but *"leave your phone in your pocket for the first 10 minutes"*
- **CLI** for terminal lovers
- **Web UI** (Flask) for everyone else
- **Save to file** option from the CLI

---

## Quickstart

```bash
git clone https://github.com/your-username/dopamine-menu.git
cd dopamine-menu
pip install -r requirements.txt
```

### Terminal (CLI)
```bash
python cli.py
```

### Web app
```bash
python app.py
# then open http://localhost:5000
```

---

## Project structure

```
dopamine-menu/
├── activities.py      # Activity database with research notes
├── engine.py          # Scoring and recommendation logic
├── cli.py             # Terminal interface
├── app.py             # Flask web app
├── templates/
│   └── index.html     # Web UI
├── requirements.txt
└── README.md
```

---

## Activity categories

| Category  | Examples |
|-----------|----------|
| Movement  | Nature walk, dancing alone, cold shower, yoga |
| Creative  | Freewriting, drawing, cooking something new |
| Social    | Phone call (not text), writing a letter, shared meal |
| Rest      | Box breathing, nap, doing absolutely nothing |
| Learning  | Read fiction, deep-dive one random topic |
| Meaning   | Hyper-specific gratitude, helping someone, watching the sky |
| Sensory   | Full album listen, mindful eating, intentional scent |

---

## Scoring methodology

Each activity starts with a base benefit score (0–10) drawn from the psychological literature. The engine then adjusts that score based on:

- **Mood match** (+2.0 if the activity directly targets your mood state)
- **Energy alignment** (+1.0 perfect match, penalties for mismatches)
- **Time fit** (+0.5 if the activity makes good use of available time)
- **Category preference** (+1.0 if it matches your optional preference)

Activities that require more energy than you have, or more time than you've got, are filtered out entirely.

---

## Extending the activity database

Activities live in `activities.py` as plain Python dicts. Adding one looks like this:

```python
{
    "id": "unique_id",
    "name": "Your activity name",
    "emoji": "🌱",
    "category": "Rest",          # one of the 7 categories
    "min_time": 15,              # minimum minutes needed
    "energy": "low",             # "low" | "medium" | "high"
    "moods": ["anxious", "sad"], # subset of MOODS list
    "benefit_score": 8.0,        # 0–10, your evidence-based estimate
    "mechanism": "Why it works (psychological mechanism)",
    "research_note": "One-sentence citation.",
    "tip": "Specific, concrete action tip.",
}
```

---

## Research foundations

- Bratman et al. (2015) — Nature and rumination
- Pennebaker & Beall (1986) — Expressive writing
- Sandstrom & Boothby (2021) — Phone calls vs. texts
- Balban et al. (2023) — Cyclic sighing and anxiety
- Dunn et al. (2008) — Prosocial spending
- Gruber et al. (2014) — Curiosity and dopamine
- Conner et al. (2016) — Everyday creativity and flourishing
- Emmons & McCullough (2003) — Gratitude specificity
- Stellar et al. (2018) — Awe and self-transcendence
- Blumenthal et al. (1999) — Exercise and depression
- Lovato & Lack (2010) — Nap duration and alertness
- And more, cited per activity in `activities.py`

---

## License

MIT — use freely, fork generously.

---

*Built because "just go for a walk" is incomplete advice.*
