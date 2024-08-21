import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"  # Replace with your client secret file

# This OAuth 2.0 access scope allows for full read/write access to the authenticated user's account.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

def upload_video(youtube, video_file_path, title, description, tags):
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '22'  # Category for "People & Blogs"
        },
        'status': {
            'privacyStatus': 'public',  # or "private", "unlisted"
        }
    }

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
    )

    response = insert_request.execute()
    print(f"Video uploaded. Video ID: {response['id']}")

if __name__ == '__main__':
    youtube = get_authenticated_service()
    
    # Define your video file path and details
    video_file_path = 'video.mp4'
    title = 'Your Video Title'
    description = 'Your video description'
    tags = ['tag1', 'tag2', 'tag3']

    # Upload video
    upload_video(youtube, video_file_path, title, description, tags)
