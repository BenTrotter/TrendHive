
import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


CLIENT_SECRETS_FILE = "client_secret.json"  # Replace with your client secret file
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
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

    insert_request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
    )

    response = insert_request.execute()
    print(f"Video uploaded. Video ID: {response['id']}\n")


def upload_to_youtube(title, description, tags):
    print("\nUploading video to YouTube...\n")
    youtube = get_authenticated_service()
    
    video_file_path = 'video.mp4'
    title = title
    description = description
    tags = tags

    upload_video(youtube, video_file_path, title, description, tags)