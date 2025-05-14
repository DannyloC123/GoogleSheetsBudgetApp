#pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
#pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib


import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

