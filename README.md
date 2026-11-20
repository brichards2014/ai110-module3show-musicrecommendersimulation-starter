# 🎵 Music Recommender Simulation

## Project Summary

This project is a small content-based music recommender written in Python. It loads a 20-song catalog from a CSV file, compares each song to a user "taste profile" (favorite genre, favorite mood, and target energy), and returns the top matches with a plain-language reason for each score.

It is a classroom simulation. It shows how data turns into a ranked list of suggestions, and where a simple scoring rule can go wrong.

---

## How The System Works

Real platforms like Spotify and YouTube mix two ideas. Collaborative filtering looks at what other users did (likes, skips, playlists, listening history) and recommends songs that similar users enjoyed. Content-based filtering looks at the song itself (genre, mood, tempo, energy) and recommends songs that resemble what a user already likes. At scale, real systems blend both and add signals like skips and time of day.

This version uses content-based filtering only. It has no other users, so it cannot learn from crowd behavior. It prioritizes genre first, then mood, then how close a song's energy is to the user's target.

**Song features used:** genre, mood, energy (0.0 to 1.0). The CSV also holds tempo_bpm, valence, danceability, and acousticness, but the score does not use them yet.

**UserProfile / preference dictionary:** favorite genre, favorite mood, target energy. The `UserProfile` class also has `likes_acoustic`, which the score does not use yet.

### Algorithm Recipe

Each song gets points from three rules:

- +2.0 if the song's genre matches the user's favorite genre
- +1.0 if the song's mood matches the user's favorite mood
- Up to +1.0 for energy: `1.0 - |song energy - target energy|`

The maximum score is 4.0. `score_song` returns the number and a list of reasons. `recommend_songs` scores every song in the catalog and sorts the results from highest to lowest. Two functions are needed because scoring judges one song, while ranking compares all songs against each other.

### Data flow

```text
User profile  ->  score_song() for every song in the CSV  ->  sort by score  ->  top k
```

### Expected biases

- Genre is worth twice as much as mood, so a song in the right genre can beat a song with the right mood and energy.
- Genre and mood must match exactly. "indie pop" gets no credit for a "pop" fan.
- Energy is the only number used, so songs with similar energy but a very different feel look alike.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app from the project root:

```bash
python -m src.main
```

### Running Tests

```bash
pytest
```

---

## Sample Recommendation Output

Default "pop / happy" profile, top 5:

```text
======================================================================
Default Pop/Happy
Profile: genre=pop, mood=happy, energy=0.8
----------------------------------------------------------------------
1. Sunrise City by Neon Echo  |  score 3.98
   pop / happy / energy 0.82
   Because: genre match (+2.0); mood match (+1.0); energy 0.82 vs target 0.80 (+0.98)
2. Gym Hero by Max Pulse  |  score 2.87
   pop / intense / energy 0.93
   Because: genre match (+2.0); energy 0.93 vs target 0.80 (+0.87)
3. Rooftop Lights by Indigo Parade  |  score 1.96
   indie pop / happy / energy 0.76
   Because: mood match (+1.0); energy 0.76 vs target 0.80 (+0.96)
4. Concrete Crown by Block Theory  |  score 1.00
   hip hop / confident / energy 0.80
   Because: energy 0.80 vs target 0.80 (+1.00)
5. Night Drive Loop by Neon Echo  |  score 0.95
   synthwave / moody / energy 0.75
   Because: energy 0.75 vs target 0.80 (+0.95)
```

The other profiles I tested (High-Energy Pop, Chill Lofi, Deep Intense Rock, and two edge cases) are shown in [model_card.md](model_card.md).

---

## Experiments You Tried

**Weight shift: double energy, halve genre.** Genre went from 2.0 to 1.0 and energy went from 1.0 to 2.0.

For the Default Pop/Happy profile, the top song stayed the same, but the order of the next two songs flipped:

```text
======================================================================
Default Pop/Happy (shifted weights)
Profile: genre=pop, mood=happy, energy=0.8
----------------------------------------------------------------------
1. Sunrise City by Neon Echo  |  score 3.96
   pop / happy / energy 0.82
   Because: genre match (+1.0); mood match (+1.0); energy 0.82 vs target 0.80 (+1.96)
2. Rooftop Lights by Indigo Parade  |  score 2.92
   indie pop / happy / energy 0.76
   Because: mood match (+1.0); energy 0.76 vs target 0.80 (+1.92)
3. Gym Hero by Max Pulse  |  score 2.74
   pop / intense / energy 0.93
   Because: genre match (+1.0); energy 0.93 vs target 0.80 (+1.74)
4. Concrete Crown by Block Theory  |  score 2.00
   hip hop / confident / energy 0.80
   Because: energy 0.80 vs target 0.80 (+2.00)
5. Night Drive Loop by Neon Echo  |  score 1.90
   synthwave / moody / energy 0.75
   Because: energy 0.75 vs target 0.80 (+1.90)
```

Rooftop Lights (indie pop, happy, energy 0.76) moved from 3rd to 2nd. Gym Hero (pop, intense, energy 0.93) dropped from 2nd to 3rd. This makes more sense for a "happy" listener, because Gym Hero is an intense workout track that was only ranked high because it is pop.

For Chill Lofi, the shifted weights moved Sunday Slow Down (indie pop, chill) above Focus Flow (lofi, focused). The results were different rather than clearly better.

---

## Limitations and Risks

- The catalog has only 20 songs, so most genres have one or two entries.
- Genre and mood use exact text matching with no concept of "close" (pop vs indie pop, sad vs melancholy).
- A genre that is not in the catalog (k-pop) can never earn the 2.0 genre points, so those users get lower scores overall.
- The recommender ignores lyrics, language, artist, and listening history.

See `model_card.md` for more detail.

---

## Reflection

Read and complete [Model Card](model_card.md). The personal reflection is in section 9 of the model card.
