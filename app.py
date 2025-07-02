from flask import Flask, redirect, request
import requests
import os
from urllib.parse import urlencode

app = Flask(__name__)

SPOTIFY_CLIENT_ID = os.environ.get("fea87c48e2d24d55b60aa25720815095")
SPOTIFY_CLIENT_SECRET = os.environ.get("72a47e2c234f482c832a95ea34d4f178")
REDIRECT_URI = os.environ.get("REDIRECT_URI")  # This will be your Render URL + /callback

@app.route('/')
def login():
    auth_url = "https://accounts.spotify.com/authorize"
    scope = "user-top-read"
    query = urlencode({
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scope
    })
    return redirect(f"{auth_url}?{query}")

@app.route('/callback')
def callback():
    code = request.args.get("code")
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }

    response = requests.post(token_url, data=payload)
    access_token = response.json().get("access_token")
    return f"Access Token: {access_token}"
