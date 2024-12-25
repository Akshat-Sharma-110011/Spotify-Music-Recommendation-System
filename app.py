import streamlit as st
import pandas as pd
import pickle
import os
import random
import time
import requests
from PIL import Image
from io import BytesIO

# Load Data
@st.cache_data
def load_data():
    music_path = 'music.pkl'
    ss_path = 'ss.pkl'
    spotify_csv_path = 'spotify.csv'

    if not os.path.exists(music_path) or not os.path.exists(ss_path) or not os.path.exists(spotify_csv_path):
        st.error("❌ Required files are missing!")
        return None, None

    with open(music_path, 'rb') as f:
        music = pickle.load(f)
    with open(ss_path, 'rb') as f:
        SS = pickle.load(f)

    spotify_df = pd.read_csv(spotify_csv_path)

    music_df = pd.merge(music, spotify_df, on='Track Name', how='left')

    return music_df, SS

# Content-based Recommendation
def recommend_by_content(music_input, pdf, ss):
    recommended_music = []
    music_index = pdf[pdf['Track Name'] == music_input].index[0]
    distances = ss[music_index]
    music_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:51]
    recommended_music = [pdf.iloc[i[0]] for i in music_list]
    return recommended_music

# Popularity-based Selection
def recommend_with_popularity_selection(recommended_music, pdf):
    popularity_weights = [
        (song['Track Name'], song['Popularity']) for _, song in recommended_music.iterrows()
    ]

    total_popularity = sum(popularity for _, popularity in popularity_weights)
    normalized_weights = [(track, popularity / total_popularity) for track, popularity in popularity_weights]

    selected_tracks = []
    while len(selected_tracks) < 6:
        selected_track = random.choices(
            population=[track for track, _ in normalized_weights],
            weights=[popularity for _, popularity in normalized_weights],
            k=1
        )[0]
        if selected_track not in selected_tracks:
            selected_tracks.append(selected_track)

    return selected_tracks

# Mood-based Recommendation
def recommend_by_mood(mood, music_df):
    mood_features = {
        'Happy': {'danceability': 0.8, 'energy': 0.7, 'valence': 0.9},
        'Sad': {'danceability': 0.3, 'energy': 0.2, 'valence': 0.2},
        'Energetic': {'danceability': 0.9, 'energy': 0.9, 'valence': 0.7},
        'Relaxed': {'danceability': 0.5, 'energy': 0.3, 'valence': 0.8},
    }

    features = mood_features[mood]
    filtered_music = music_df[(
            (music_df['Danceability'] >= features['danceability']) &
            (music_df['Energy'] >= features['energy']) &
            (music_df['Valence'] >= features['valence'])
    )]
    return filtered_music

# Playlist Creation (Example: Workout, Study, Chill)
def create_playlist(playlist_type, music_df):
    if playlist_type == 'Workout':
        return recommend_by_mood('Energetic', music_df)
    elif playlist_type == 'Study':
        return recommend_by_mood('Relaxed', music_df)
    elif playlist_type == 'Chill':
        return recommend_by_mood('Relaxed', music_df)
    return pd.DataFrame()

# Convert Track URI to URL
def convert_uri_to_url(uri):
    return uri.replace("spotify:track:", "https://open.spotify.com/track/")

# Retry mechanism to fetch album image
def get_image_with_retry(url, retries=3, delay=2):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return Image.open(BytesIO(response.content))
        except (requests.exceptions.RequestException, IOError) as e:
            attempt += 1
            if attempt < retries:
                time.sleep(delay)
            else:
                return None

# Main Streamlit Application
st.title("Music Recommendation System 🎵")
st.markdown("Discover music based on your preferences! 🎶")
st.markdown('---')

sidebar_image = Image.open('pngegg.png')
sidebar_image = sidebar_image.resize((9000, 8900))  # Resize to fit sidebar space (you can adjust this size)
st.sidebar.image(sidebar_image, use_container_width=True)

# Load data
music_df, SS = load_data()
music_df.drop('Popularity_x', axis=1, inplace=True)
music_df.rename(columns={'Popularity_y': 'Popularity'}, inplace=True)

if music_df is not None and SS is not None:
    # Mood-based Recommendation
    mood = st.sidebar.selectbox("Select Your Mood 🎧", ['Happy 😃', 'Sad 😔', 'Energetic ⚡', 'Relaxed 🧘'])
    if st.sidebar.button("Recommend based on Mood 🎶"):
        recommended_music = recommend_by_mood(mood, music_df)
        st.write(f"### Songs for mood: {mood} 🎵")
        cols = st.columns(2)

        for idx, (_, song) in enumerate(recommended_music.iterrows()):
            col = cols[idx % 2]
            if 'Album Image URL' in song:
                image_url = song['Album Image URL']
                img = get_image_with_retry(image_url)
                if img:
                    img = img.resize((200, 200))
                    col.image(img)
                else:
                    col.error("❌ Failed to load album image.")
            track_url = convert_uri_to_url(song['Track URI'])
            col.markdown(
                f'<div><a href="{track_url}"><b>{song["Track Name"]} 🎶</b></a><br>Artist: {song["Artist Name(s)"]}</div>',
                unsafe_allow_html=True)
            col.markdown(f'<div style="font-size: 12px;">© {song["Artist Name(s)"]} - All Rights Reserved 🎤</div>',
                         unsafe_allow_html=True)

    # Playlist Creation (Example: Workout, Study, Chill)
    playlist = st.sidebar.selectbox("Create Playlist for 🎧", ['Workout 🏋️', 'Study 📚', 'Chill 🧘'])
    if st.sidebar.button("Recommend Playlist 🎵"):
        recommended_music = create_playlist(playlist, music_df)
        st.write(f"### Recommended songs for {playlist} playlist 🎶")
        cols = st.columns(2)

        for idx, (_, song) in enumerate(recommended_music.iterrows()):
            col = cols[idx % 2]
            if 'Album Image URL' in song:
                image_url = song['Album Image URL']
                img = get_image_with_retry(image_url)
                if img:
                    img = img.resize((200, 200))
                    col.image(img)
                else:
                    col.error("❌ Failed to load album image.")
            track_url = convert_uri_to_url(song['Track URI'])
            col.markdown(
                f'<div><a href="{track_url}"><b>{song["Track Name"]} 🎶</b></a><br>Artist: {song["Artist Name(s)"]}</div>',
                unsafe_allow_html=True)
            col.markdown(f'<div style="font-size: 12px;">© {song["Artist Name(s)"]} - All Rights Reserved 🎤</div>',
                         unsafe_allow_html=True)

    # Similarity-based Recommendation (Dropdown Menu for User Input)
    song_list = music_df['Track Name'].unique().tolist()
    selected_song = st.selectbox("Choose a Song 🎵:", song_list)

    recommend_button = st.button("Recommend Based on Song 🎶")

    if recommend_button and selected_song:
        recommended_music = recommend_by_content(selected_song, music_df, SS)
        selected_tracks = recommend_with_popularity_selection(pd.DataFrame(recommended_music), music_df)

        st.write(f"### Recommended songs based on {selected_song} 🎶")

        cols = st.columns(2)

        for idx, track in enumerate(selected_tracks):
            song = music_df[music_df['Track Name'] == track].iloc[0]
            col = cols[idx % 2]
            if 'Album Image URL' in song:
                image_url = song['Album Image URL']
                img = get_image_with_retry(image_url)
                if img:
                    img = img.resize((200, 200))
                    col.image(img)
                else:
                    col.error("❌ Failed to load album image.")
            track_url = convert_uri_to_url(song['Track URI'])
            col.markdown(
                f'<div><a href="{track_url}"><b>{song["Track Name"]} 🎶</b></a><br>Artist: {song["Artist Name(s)"]}</div>',
                unsafe_allow_html=True)
            col.markdown(f'<div style="font-size: 12px;">© {song["Artist Name(s)"]} - All Rights Reserved 🎤</div>',
                         unsafe_allow_html=True)

st.markdown('---')
if st.button('Visit My GitHub 💻'):
    st.markdown('[Go to GitHub](https://github.com/Akshat-Sharma-110011)', unsafe_allow_html=True)

if st.button('Visit My LinkedIn 🌐'):
    st.markdown('[Go to LinkedIn](https://www.linkedin.com/in/akshat-sharma-07350a2b3/)', unsafe_allow_html=True)

st.download_button(
    label="Download Dataset 📥",
    data=music_df.to_csv(index=False),
    file_name="spotify.csv",
    mime="text/csv")
