# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Intended Use

VibeMatch suggests songs from a small catalog based on a user's favorite genre, favorite mood, and target energy level. It assumes the user can describe their taste with those three values.

It is built for classroom exploration. It is not meant for real users or a real music service.

**Not intended for:** a production app, any decision about artists or pay, or any user whose taste is not captured by one genre, one mood, and one energy level.

---

## 3. How the Model Works

Every song gets a score for the user. The score has three parts:

- 2.0 points if the song's genre is the user's favorite genre.
- 1.0 point if the song's mood is the user's favorite mood.
- Up to 1.0 point for energy. A song that matches the user's target energy exactly gets the full point. The further away it is, the fewer points it gets.

The top possible score is 4.0. The system scores all songs, sorts them from highest to lowest, and shows the top five. Each result also lists the reasons for its score, such as "genre match (+2.0)".

Changes from the starter: the starter code had empty functions. I filled in loading, scoring, ranking, and explanations, and added optional weights so I could test a weight shift.

---

## 4. Data

The catalog has 20 songs. The starter file had 10, and I added 10 more to cover genres and moods that were missing (hip hop, country, EDM, R&B, metal, classical, folk, reggae, punk, and a second indie pop track).

Each song has genre, mood, energy, tempo, valence, danceability, and acousticness. The score only uses genre, mood, and energy.

Limits: most genres have only one or two songs. The data is invented, so it does not reflect real listening. It also leaves out language, lyrics, era, and artist popularity.

---

## 5. Strengths

- It works well for users whose taste fits one clear genre and mood. Chill Lofi and Deep Intense Rock both put the obvious song first (Library Rain and Storm Runner).
- The reasons list makes each result easy to check. You can see exactly why a song ranked where it did.
- Energy closeness works as intended. In the edge-case tests, songs with no genre or mood match are ranked by how close their energy is to the target (0.99 for Storm Runner, 0.94 for Neon Pulse).

---

## 6. Limitations and Bias

The system gives a lot of weight to genre and mood, which are all-or-nothing matches. In the "high energy but sad" test, the top result was Porch Light, a quiet folk song with energy 0.30, even though the user asked for energy 0.9. It won because genre (+2.0) and mood (+1.0) added up to 3.0 before energy was even considered. The energy mismatch cost it only 0.6 points. A listener who wants loud, sad music gets a soft ballad first.

A second weakness is that genre must match exactly. A k-pop fan gets no genre points from any song, so the best possible score is 2.0, and the results are just "happy, medium-energy" songs. Pop fans also see "indie pop" songs treated as a different genre. That is why Gym Hero, a pop workout track, keeps showing up for people who only want happy pop: it matches the genre, which is worth more than the mood it misses.

---

## 7. Evaluation

I tested four normal profiles and two edge cases, and read the top 5 for each.

**Normal profiles:** Default Pop/Happy, High-Energy Pop, Chill Lofi, Deep Intense Rock.
**Edge cases:** "Conflicting: high energy but sad" and "Genre not in catalog" (k-pop).

I looked for whether the top result matched my intuition, and whether the same song kept showing up.

**What surprised me:** Gym Hero came second for the Default Pop/Happy profile even though it is an intense workout song. It appeared because it is pop and its energy (0.93) is close to the 0.80 target.

**Experiment:** I doubled the energy weight and halved the genre weight. See the README for the output. Rooftop Lights (happy) moved above Gym Hero (intense) for the pop/happy profile, which feels more accurate.

### Profile comparisons

- **Default Pop/Happy vs High-Energy Pop:** Both put a pop song first, but the mood changes which one. Pop/Happy picks Sunrise City (happy), and High-Energy Pop picks Gym Hero (intense) and ranks Sunrise City second. That makes sense, because the mood setting is the only thing separating them.
- **High-Energy Pop vs Chill Lofi:** The results share no songs. High-Energy Pop pulls punk and EDM tracks at energy 0.9+, while Chill Lofi pulls quiet tracks around 0.3 to 0.4. This is the clearest sign that the energy rule works.
- **Chill Lofi vs Deep Intense Rock:** These are opposite profiles with no overlap. Lofi results fill all five slots with songs under energy 0.45. Rock gets one real rock song, then fills the rest with whatever has high energy (pop, punk, EDM, metal), because the catalog has only one rock song.
- **Deep Intense Rock vs High-Energy Pop:** Both rank Storm Runner and Gym Hero near the top, but in a different order. Rock puts Storm Runner first (genre match), and Pop puts Gym Hero first (genre match). Both profiles want high energy, so the lower slots look similar (Basement Static, Neon Pulse).
- **Conflicting (high energy, sad) vs Deep Intense Rock:** After the first slot, the conflicting profile's results look like Deep Intense Rock's list, because only energy is left to score. That shows the system falls back on energy alone when genre and mood do not match.
- **Genre not in catalog vs Default Pop/Happy:** Same mood and energy, but without a genre match the top score drops from 3.98 to 1.98. The recommendations still look reasonable, which hides the fact that the system has no pop-like songs to offer.

### Output for each profile

```text
======================================================================
High-Energy Pop
Profile: genre=pop, mood=intense, energy=0.9
----------------------------------------------------------------------
1. Gym Hero by Max Pulse  |  score 3.97
   pop / intense / energy 0.93
   Because: genre match (+2.0); mood match (+1.0); energy 0.93 vs target 0.90 (+0.97)
2. Sunrise City by Neon Echo  |  score 2.92
   pop / happy / energy 0.82
   Because: genre match (+2.0); energy 0.82 vs target 0.90 (+0.92)
3. Storm Runner by Voltline  |  score 1.99
   rock / intense / energy 0.91
   Because: mood match (+1.0); energy 0.91 vs target 0.90 (+0.99)
4. Basement Static by The Fuses  |  score 0.97
   punk / angry / energy 0.93
   Because: energy 0.93 vs target 0.90 (+0.97)
5. Neon Pulse by Circuit Bloom  |  score 0.94
   edm / euphoric / energy 0.96
   Because: energy 0.96 vs target 0.90 (+0.94)
```

```text
======================================================================
Chill Lofi
Profile: genre=lofi, mood=chill, energy=0.35
----------------------------------------------------------------------
1. Library Rain by Paper Lanterns  |  score 4.00
   lofi / chill / energy 0.35
   Because: genre match (+2.0); mood match (+1.0); energy 0.35 vs target 0.35 (+1.00)
2. Midnight Coding by LoRoom  |  score 3.93
   lofi / chill / energy 0.42
   Because: genre match (+2.0); mood match (+1.0); energy 0.42 vs target 0.35 (+0.93)
3. Focus Flow by LoRoom  |  score 2.95
   lofi / focused / energy 0.40
   Because: genre match (+2.0); energy 0.40 vs target 0.35 (+0.95)
4. Sunday Slow Down by Indigo Parade  |  score 1.97
   indie pop / chill / energy 0.38
   Because: mood match (+1.0); energy 0.38 vs target 0.35 (+0.97)
5. Spacewalk Thoughts by Orbit Bloom  |  score 1.93
   ambient / chill / energy 0.28
   Because: mood match (+1.0); energy 0.28 vs target 0.35 (+0.93)
```

```text
======================================================================
Deep Intense Rock
Profile: genre=rock, mood=intense, energy=0.92
----------------------------------------------------------------------
1. Storm Runner by Voltline  |  score 3.99
   rock / intense / energy 0.91
   Because: genre match (+2.0); mood match (+1.0); energy 0.91 vs target 0.92 (+0.99)
2. Gym Hero by Max Pulse  |  score 1.99
   pop / intense / energy 0.93
   Because: mood match (+1.0); energy 0.93 vs target 0.92 (+0.99)
3. Basement Static by The Fuses  |  score 0.99
   punk / angry / energy 0.93
   Because: energy 0.93 vs target 0.92 (+0.99)
4. Neon Pulse by Circuit Bloom  |  score 0.96
   edm / euphoric / energy 0.96
   Because: energy 0.96 vs target 0.92 (+0.96)
5. Broken Static by Hollow Saints  |  score 0.95
   metal / angry / energy 0.97
   Because: energy 0.97 vs target 0.92 (+0.95)
```

```text
======================================================================
Conflicting: high energy but sad
Profile: genre=folk, mood=sad, energy=0.9
----------------------------------------------------------------------
1. Porch Light by Willow Creek  |  score 3.40
   folk / sad / energy 0.30
   Because: genre match (+2.0); mood match (+1.0); energy 0.30 vs target 0.90 (+0.40)
2. Storm Runner by Voltline  |  score 0.99
   rock / intense / energy 0.91
   Because: energy 0.91 vs target 0.90 (+0.99)
3. Gym Hero by Max Pulse  |  score 0.97
   pop / intense / energy 0.93
   Because: energy 0.93 vs target 0.90 (+0.97)
4. Basement Static by The Fuses  |  score 0.97
   punk / angry / energy 0.93
   Because: energy 0.93 vs target 0.90 (+0.97)
5. Neon Pulse by Circuit Bloom  |  score 0.94
   edm / euphoric / energy 0.96
   Because: energy 0.96 vs target 0.90 (+0.94)
```

```text
======================================================================
Genre not in catalog
Profile: genre=k-pop, mood=happy, energy=0.8
----------------------------------------------------------------------
1. Sunrise City by Neon Echo  |  score 1.98
   pop / happy / energy 0.82
   Because: mood match (+1.0); energy 0.82 vs target 0.80 (+0.98)
2. Rooftop Lights by Indigo Parade  |  score 1.96
   indie pop / happy / energy 0.76
   Because: mood match (+1.0); energy 0.76 vs target 0.80 (+0.96)
3. Concrete Crown by Block Theory  |  score 1.00
   hip hop / confident / energy 0.80
   Because: energy 0.80 vs target 0.80 (+1.00)
4. Night Drive Loop by Neon Echo  |  score 0.95
   synthwave / moody / energy 0.75
   Because: energy 0.75 vs target 0.80 (+0.95)
5. Storm Runner by Voltline  |  score 0.89
   rock / intense / energy 0.91
   Because: energy 0.91 vs target 0.80 (+0.89)
```

---

## 8. Future Work

- Use more features. Valence, danceability, and acousticness are already in the data. The `likes_acoustic` preference is stored but never used.
- Give partial credit for related genres and moods, so "indie pop" earns some points for a pop fan and "melancholy" earns some for "sad".
- Add a diversity rule so the top 5 do not repeat the same artist or genre.
- Cap how much genre and mood can contribute, so a large energy mismatch can pull a song down further.

---

## 9. Personal Reflection

> **Draft: rewrite this in your own words before submitting.** The rubric asks for specific, honest details about your own process. Keep what matches your experience and replace the rest.

**Biggest learning moment:** Seeing the "high energy but sad" test return a quiet folk song first. The scoring looked fair on paper, but the weights let two exact matches outweigh a large energy gap. I would not have caught that without testing a conflicting profile.

**How AI helped, and what I double-checked:** I used Claude to write the recommender code, expand the song list, and draft the documentation. I checked the results by running every profile and reading the top 5 against my own sense of the music. I also checked the score math by hand for a couple of songs, such as Sunrise City at 3.98 (2.0 + 1.0 + 0.98).

**What surprised me:** A rule with three ingredients already feels like a real recommendation. The "Because" lines make the results feel intentional, even though the system is just adding numbers.

**What I would try next:** Add the unused features (valence, danceability, acousticness), add partial credit for related genres, and test with a bigger catalog.
