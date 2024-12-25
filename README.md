# Spotify-Music-Recommendation-System
Welcome to the Music Recommendation System! This web application uses data-driven methods to recommend music based on your preferences. You can discover new tracks through mood-based recommendations, playlist generation (such as workout or study playlists), or similarity-based suggestions from a selected song. It's powered by Streamlit, machine learning models, and Spotify data!

Features
1. Mood-Based Recommendations
Select your mood (Happy, Sad, Energetic, Relaxed) and get music recommendations that match your current emotional state.

2. Playlist Creation
Create playlists tailored for different activities, including:

Workout 🏋️: Energetic music to keep you going.
Study 📚: Relaxing tracks for concentration.
Chill 🧘: Soothing music for unwinding.
3. Similarity-Based Recommendations
Input a song you love and receive personalized music suggestions based on similar tracks.

4. Album Artwork & Track Links
View album artwork for each track and easily visit the Spotify page for each song.

Requirements
To run this application locally, you need to have the following Python libraries installed:

Streamlit
pandas
requests
Pillow
pickle
os
random
You can install them using pip:

bash
Copy code
pip install streamlit pandas requests Pillow
File Structure
music.pkl: Contains the music data.
ss.pkl: Contains the precomputed similarity matrix.
spotify.csv: A CSV file with additional Spotify data for the tracks.
pngegg.png: Image for the sidebar.
How to Run the Application
Clone the repository to your local machine:
bash
Copy code
git clone https://github.com/yourusername/music-recommendation.git
Install the required dependencies:
bash
Copy code
pip install -r requirements.txt
Run the Streamlit app:
bash
Copy code
streamlit run app.py
The application will open in your web browser.

How to Use the Application
Mood-Based Recommendation: Select a mood from the sidebar and click "Recommend based on Mood" to get songs that match your mood.
Playlist Creation: Select a playlist type (Workout, Study, Chill) and click "Recommend Playlist" to generate a playlist.
Song Similarity: Select a song from the dropdown menu and click "Recommend Based on Song" to receive song suggestions based on the similarity of the selected track.
Contributing
Feel free to fork this repository, make improvements, or submit issues and pull requests.

Fork the repository
Create a new branch for your changes (git checkout -b feature-xyz)
Commit your changes (git commit -am 'Add feature xyz')
Push to the branch (git push origin feature-xyz)
Create a new Pull Request
License
This project is open-source and available under the MIT License. See the LICENSE file for more details.

Contact
If you have any questions or suggestions, feel free to reach out to me through my profiles:

GitHub
LinkedIn
This README provides an overview of your music recommendation system and guides users through setting up and using the application. Make sure to adjust any links or filenames according to your repo structure.
