from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import json
import pickle
import os
import time

# Initialize the YouTube API
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def youtube_authenticate():
    credentials = None
    if os.path.exists('youtube_credentials.pickle'):
        with open('youtube_credentials.pickle', 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        raise RuntimeError("Failed to authenticate. Run the authentication script again.")
    return build("youtube", "v3", credentials=credentials)

def create_youtube_playlist(youtube, playlist_name, description="Created via Spotify Migration"):
    try:
        request = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": playlist_name,
                    "description": description
                },
                "status": {
                    "privacyStatus": "private"  # Change to "public" or "unlisted" if needed
                }
            }
        )
        response = request.execute()
        return response["id"]  # Return the playlist ID
    except HttpError as e:
        print(f"An error occurred: {e}")
        return None

def search_and_add_track(youtube, playlist_id, track_name, artist_name):
    try:
        # Search for the track on YouTube
        search_response = youtube.search().list(
            part="snippet",
            q=f"{track_name} {artist_name}",
            type="video",
            maxResults=1
        ).execute()

        if search_response["items"]:
            video_id = search_response["items"][0]["id"]["videoId"]
            
            # Add the track to the playlist
            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            ).execute()
            print(f"Added track: {track_name} by {artist_name}")
        else:
            print(f"No results found for: {track_name} by {artist_name}")
    except HttpError as e:
        print(f"An error occurred: {e}")

def main():
    # Authenticate YouTube API
    youtube = youtube_authenticate()
    
    # Load Spotify data (replace 'spotify_data.json' with your actual file)
    with open("SpotifyData.json", "r") as file:
        playlists = json.load(file)
    
    for playlist in playlists:
        print(f"Creating playlist: {playlist['name']}")
        playlist_id = create_youtube_playlist(youtube, playlist["name"])
        
        if playlist_id:
            print(f"Playlist created with ID: {playlist_id}")
            for track in playlist["tracks"]:
                search_and_add_track(youtube, playlist_id, track["track_name"], track["artist_name"])
                time.sleep(1)  # Pause to avoid hitting API limits
        else:
            print(f"Failed to create playlist: {playlist['name']}")

if __name__ == "__main__":
    main()
