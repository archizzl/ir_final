from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

with open('shows.json', encoding='utf-8') as f:
    shows = json.load(f)

SPOTIFY_CLIENT_ID = "db78fdfd9ace49e9ba4489bcf2ad036f"  
SPOTIFY_CLIENT_SECRET = "e43d7f7f96de47d285e0745e9f810864"  

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

import random
def get_song_features(songs):
    moods = [
        "Happy & Energetic",
        "Happy & Calm",
        "Energetic & Serious",
        "Calm & Serious"
    ]
    return random.choice(moods)

def get_song_features(songs):
    if not all(isinstance(song, dict) and 'artist' in song and 'song' in song for song in songs):
        raise ValueError("Each song must be a dictionary with 'artist' and 'song' keys.")

    features = []
    for song in songs:
        query = f"{song['song']} {song['artist']}"
        try:
            results = sp.search(q=query, type='track', limit=1)
            time.sleep(0.2)  # Avoid rate limiting
            if results['tracks']['items']:
                track_id = results['tracks']['items'][0]['id']
                audio_features = sp.audio_features([track_id])[0]
                if audio_features:
                    features.append(audio_features)
                else:
                    print(f"No audio features found for {query}. Skipping.")
        except Exception as e:
            print(f"Error fetching features for {query}: {str(e)}")
            continue

    if not features:
        return "Unknown"

    avg_valence = np.mean([f['valence'] for f in features])
    avg_energy = np.mean([f['energy'] for f in features])

    if avg_valence > 0.6 and avg_energy > 0.6:
        return "Happy & Energetic"
    elif avg_valence > 0.6:
        return "Happy & Calm"
    elif avg_energy > 0.6:
        return "Energetic & Serious"
    else:
        return "Calm & Serious"

corpus = [
    f"{show['title']} {show['bio']} {show['dj']} {show['genre']} {show['episode']} {show['description']}"
    for show in shows
]

song_corpus = [
    " ".join([f"{song['artist']} {song['song']}" for song in show.get('songs', [])])
    for show in shows
]

combined_corpus = [
    f"{corpus[i]} {song_corpus[i]}" for i in range(len(shows))
]

vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(combined_corpus)

def search_shows(query, tfidf_matrix, shows, vectorizer, output_file="show_search_results.txt"):
    query_vec = vectorizer.transform([query])

    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

    ranked_indices = np.argsort(-scores)
    ranked_shows = [
        (scores[i], shows[i]['title'], shows[i]['dj'], shows[i]['genre'], shows[i]['bio'], shows[i].get('songs', []))
        for i in ranked_indices if scores[i] > 0
    ]

    with open(output_file, "w", encoding="utf-8") as f:
        for rank, (score, title, dj, genre, bio, songs) in enumerate(ranked_shows, 1):
            sanitized_title = title.encode("ascii", errors="ignore").decode("ascii") if title else "None"
            sanitized_dj = dj.encode("ascii", errors="ignore").decode("ascii") if dj else "None"
            sanitized_genre = genre.encode("ascii", errors="ignore").decode("ascii") if genre else "None"
            sanitized_bio = bio.encode("ascii", errors="ignore").decode("ascii") if bio else "None"

            mood = get_song_features(songs)
            f.write(f"Rank {rank} (Score: {score:.4f}):\n")
            f.write(f"Title: {sanitized_title}\n")
            f.write(f"DJ: {sanitized_dj}\n")
            f.write(f"Genre: {sanitized_genre}\n")
            f.write(f"Bio: {sanitized_bio}\n")
            f.write(f"Mood: {mood}\n")

            if songs:
                f.write("Songs:\n")
                for song in songs:
                    artist = song.get('artist', '').encode("ascii", errors="ignore").decode("ascii")
                    song_title = song.get('song', '').encode("ascii", errors="ignore").decode("ascii")
                    f.write(f"  - {artist}: {song_title}\n")
            f.write("\n")
    
    print(f"Search results saved to {output_file}")

# Input query and search
query = input("Enter search query: ")
search_shows(query, tfidf_matrix, shows, vectorizer)
