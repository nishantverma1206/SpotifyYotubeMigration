import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
from flask import Flask, request, redirect, session, url_for
import json

app = Flask(__name__)

app.secret_key = 'Franko@123'

SPOTIPY_CLIENT_ID = 'a3ff15bca47e4b1597a1000440cxx777'
SPOTIPY_CLIENT_SECRET = '721d8e1b6edf4944a23f6426e2d31221'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

scope = "user-library-read playlist-read-private"

sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope)
#token_info = sp_oauth.get_access_token(as_dict=False)
#spotify = spotipy.Spotify(auth=token_info)

@app.route('/')
def index():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    if token_info:
        # Save the token to session
        session['token_info'] = token_info
        return redirect(url_for('get_playlists'))
    return 'Error during Spotify authentication', 400

@app.route('/get_playlists')
def get_playlists():
    token_info = session.get('token_info')
    if not token_info:
        return redirect('/')
    
    # Initialize Spotify client with the token
    sp = spotipy.Spotify(auth=token_info['access_token'])

    # Fetch playlists with pagination
    playlists = []
    limit = 50  # Max limit per request is 50
    offset = 0

    while True:
        current_batch = sp.current_user_playlists(limit=limit, offset=offset)
        playlists.extend(current_batch['items'])

        if len(current_batch['items']) < limit:
            # No more playlists to fetch
            break

        offset += limit  # Move to the next batch

    # Store playlist information
    playlist_info = []

    # Iterate through playlists and extract their names and tracks
    for playlist in playlists:
        playlist_data = {
            'name': playlist['name'],
            'total_tracks': playlist['tracks']['total'],
            'tracks': []
        }

        # Fetch all tracks from each playlist
        tracks = sp.playlist_tracks(playlist['id'])
        for item in tracks['items']:
            track = item['track']
            playlist_data['tracks'].append({
                'track_name': track['name'],
                'artist_name': track['artists'][0]['name']
            })

        playlist_info.append(playlist_data)

    # Return playlist information as JSON (for now, you can format it as you like)
    return json.dumps(playlist_info, indent=4)

if __name__ == "__main__":
    app.run(port=8888, debug=True)
