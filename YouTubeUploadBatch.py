import json
import time
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle
import os

# Function to authenticate with YouTube
def youtube_authenticate():
    credentials = None
    if os.path.exists('youtube_credentials.pickle'):
        with open('youtube_credentials.pickle', 'rb') as token:
            credentials = pickle.load(token)
    if not credentials or not credentials.valid:
        raise RuntimeError("Failed to authenticate. Run the authentication script again.")
    return build("youtube", "v3", credentials=credentials)

# Function to create a playlist
def create_playlist(youtube, title, description=""):
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["Spotify", "YouTube", "Music"],
            "defaultLanguage": "en"
        },
        "status": {
            "privacyStatus": "private"
        }
    }
    response = youtube.playlists().insert(part="snippet,status", body=request_body).execute()
    return response["id"]

# Function to search for a track on YouTube
def search_track(youtube, query):
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=1
    )
    response = request.execute()
    items = response.get("items", [])
    if not items:
        return None
    return items[0]["id"]["videoId"]

# Function to add a track to a playlist
def add_to_playlist(youtube, playlist_id, video_id):
    request_body = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
            }
        }
    }
    youtube.playlistItems().insert(part="snippet", body=request_body).execute()

# Main function to process tracks in batches
def main():
    # Authenticate YouTube
    youtube = youtube_authenticate()

    # Load trimmed Spotify data
    with open("SpotifyData.json", "r") as f:
        spotify_data = json.load(f)

    # Process each playlist
    for playlist in spotify_data:
        playlist_name = playlist["name"]
        tracks = playlist["tracks"]

        # Create a YouTube playlist
        print(f"Creating playlist: {playlist_name}")
        youtube_playlist_id = create_playlist(youtube, playlist_name)
        print(f"Playlist created with ID: {youtube_playlist_id}")

        # Migrate tracks in batches
        for i in range(0, len(tracks), 50):  # Process 50 tracks per batch
            batch = tracks[i:i + 50]
            for track in batch:
                query = f"{track['track_name']} {track['artist_name']}"
                print(f"Searching for track: {query}")
                try:
                    video_id = search_track(youtube, query)
                    if video_id:
                        add_to_playlist(youtube, youtube_playlist_id, video_id)
                        print(f"Added track: {track['track_name']} by {track['artist_name']}")
                    else:
                        print(f"Track not found: {track['track_name']} by {track['artist_name']}")
                except Exception as e:
                    print(f"An error occurred: {e}")
            print("Batch processed. Pausing to avoid hitting quota...")
            time.sleep(30)  # Pause for 30 seconds after each batch

if __name__ == "__main__":
    main()
