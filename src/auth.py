import os
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_service():
    creds=None
    token_path="credentials/token.json"
    creds_path="credentials/credentials.json"

    # if token is exist then use it directly without creating it

    if os.path.exists(token_path):
        creds=Credentials.from_authorized_user_file(token_path,SCOPES)

    # if token not exist or expired:

    if not creds or not creds.valid:
        # if creds are expired but refresh token is available the refresh silently
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # run whole OAuth flow to get creds
            flow=InstalledAppFlow.from_client_secrets_file(creds_path,SCOPES)
            creds=flow.run_local_server(port=0)
        # save the token to reuse
        with open(token_path,"w") as token:
            token.write(creds.to_json())
    # create Gmail API client

    from googleapiclient.discovery import build
    service=build("gmail","v1",credentials=creds)
    return service