import json

HIGH_SCORE_FILE = "assets/high_scores.json"

def load_high_scores():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_high_score(game, score):
    high_scores = load_high_scores()
    if game not in high_scores or score > high_scores[game]:
        high_scores[game] = score
        with open(HIGH_SCORE_FILE, "w") as f:
            json.dump(high_scores, f)
