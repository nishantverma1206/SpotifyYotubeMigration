from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ["https://www.googleapis.com/auth/youtube"]
CLIENT_SECRET_FILE = r"C:\Users\nishu\Downloads\client_secret_722622143595-fv19ksej3dgmnuhubtkim753sshrvo58.apps.googleusercontent.com.json"

def authenticate_youtube():
    credentials = None
    if os.path.exists('youtube_credentials.pickle'):
        with open('youtube_credentials.pickle', 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            credentials = flow.run_local_server(port=8888)
            with open('youtube_credentials.pickle', 'wb') as token:
                pickle.dump(credentials, token)

    return credentials

if __name__ == "__main__":
    creds = authenticate_youtube()
    print("Access token:", creds.token)
