"""
Dopamine Menu Generator — Web Interface (Flask)
Run: python app.py
Visit: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
from engine import UserInput, generate_menu
from activities import MOODS, ENERGY_LEVELS, CATEGORIES

app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        "index.html",
        moods=MOODS,
        energy_levels=ENERGY_LEVELS,
        categories=CATEGORIES,
    )


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json or {}
    try:
        user = UserInput(
            mood=data.get("mood", ""),
            available_time=int(data.get("available_time", 30)),
            energy=data.get("energy", "medium"),
            preferred_categories=data.get("preferred_categories", []),
        )
        results = generate_menu(user, top_n=5)
        return jsonify({
            "success": True,
            "results": [
                {
                    "rank": i + 1,
                    "name": r.activity["name"],
                    "emoji": r.activity["emoji"],
                    "category": r.activity["category"],
                    "min_time": r.activity["min_time"],
                    "score": r.score,
                    "mechanism": r.activity["mechanism"],
                    "research_note": r.activity["research_note"],
                    "tip": r.activity["tip"],
                    "reasons": r.reasons,
                }
                for i, r in enumerate(results)
            ],
        })
    except (ValueError, KeyError) as e:
        return jsonify({"success": False, "error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
