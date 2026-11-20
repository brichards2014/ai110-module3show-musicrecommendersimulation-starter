"""
Command line runner for the Music Recommender Simulation.

Run from the project root with: python -m src.main
"""

from src.recommender import DEFAULT_WEIGHTS, load_songs, recommend_songs

PROFILES = {
    "Default Pop/Happy": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "High-Energy Pop": {"genre": "pop", "mood": "intense", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92},
}

# Edge cases meant to trick the scoring logic.
ADVERSARIAL_PROFILES = {
    "Conflicting: high energy but sad": {"genre": "folk", "mood": "sad", "energy": 0.9},
    "Genre not in catalog": {"genre": "k-pop", "mood": "happy", "energy": 0.8},
}

# Experiment: double energy, halve genre.
SHIFTED_WEIGHTS = {"genre": 1.0, "mood": 1.0, "energy": 2.0}


def show(title: str, prefs: dict, songs: list, weights=None, k: int = 5) -> None:
    """Print the top k recommendations for one profile."""
    print("=" * 70)
    print(f"{title}")
    print(f"Profile: genre={prefs['genre']}, mood={prefs['mood']}, energy={prefs['energy']}")
    print("-" * 70)
    for rank, (song, score, explanation) in enumerate(
        recommend_songs(prefs, songs, k=k, weights=weights), start=1
    ):
        print(f"{rank}. {song['title']} by {song['artist']}  |  score {score:.2f}")
        print(f"   {song['genre']} / {song['mood']} / energy {song['energy']:.2f}")
        print(f"   Because: {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    print(f"Weights: {DEFAULT_WEIGHTS}\n")
    for title, prefs in {**PROFILES, **ADVERSARIAL_PROFILES}.items():
        show(title, prefs, songs)

    print("#" * 70)
    print(f"EXPERIMENT: weight shift {SHIFTED_WEIGHTS}")
    print("#" * 70 + "\n")
    for title in ("Default Pop/Happy", "Chill Lofi"):
        show(f"{title} (shifted weights)", PROFILES[title], songs, weights=SHIFTED_WEIGHTS)


if __name__ == "__main__":
    main()
