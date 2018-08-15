import spotipy
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pprint
import sys
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import client_id, client_secret

cid = client_id # Client ID; copy this from your app 
secret = client_secret # Client Secret; copy this from your app
username = '123149945' # Your Spotify username

def spotify_authorize():
    #for avaliable scopes see https://developer.spotify.com/web-api/using-scopes/
    scope = 'user-library-read playlist-modify-public playlist-read-private'
    redirect_uri='https://google.com/' # Paste your Redirect URI here
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    token = util.prompt_for_user_token(username, scope, cid, secret, redirect_uri)

    if token:
        sp = spotipy.Spotify(auth=token)
        return sp
    else:
        print("Can't get token for", username)




