# Spotify to YouTube Music Migrator
Effortlessly migrate your Spotify playlists to YouTube Music! This script automates the process of transferring your favorite tracks by leveraging the Spotify Web API and YouTube Data API.

## Features
- Transfer tracks from a Spotify playlist or library to YouTube Music.
- Automatically searches for the closest match on YouTube Music.
- Logs successes and tracks that couldn't be found for further review.
- Designed with error handling for smooth operation.

## Prerequisites
1. Python Requirements
   - Python 3.8 or higher
   - Install dependencies using pip
2. APIs and Keys
   - Spotify Web API: Follow Spotify's Developer Guide to create an app and obtain: client_id and client_secret
   - YouTube Data API: Follow YouTube's API Guide to enable the API and get an API key.

## Setup and Usage
1. Clone repository
2. Create a virtual environment
3. Prepare your Spotify data using Spotify_Auth.py
   - Use the Spotify Exporter or a script to retrieve this data in a .json file
4. Run the scripts in the given order
   1. YTAuth.py
   2. YoutubeUpload.py
5. Daily Quota Management
   The YouTube Data API enforces a daily quota. If your migration stops due to quota limits:
   - Wait for 24 hours when the limit resets
   - Restart the script to continue the migration

If the track count is high on Spotify, consider migration in batches: Run script: YouTubeUploadBatch.py

## Known Limitations
- Quota Limit: The YouTube Data API limits daily requests; large migrations may take several days.
- Track Mismatches: Some tracks may not have an exact match on YouTube Music.

## Acknowledgements
- Spotify Web API
- YouTube Data API
- Open-source libraries that power this project.
