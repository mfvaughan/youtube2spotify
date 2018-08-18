import spotipy
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pprint
import sys
import re
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from credentials import client_id, client_secret


class Youtube2Spotify(object):
    
    def __init__(self):
        self.cid = client_id # Client ID; copy this from your app 
        self.secret = client_secret # Client Secret; copy this from your app
        #self.username = spotify_user # Your Spotify username
        
    
    def authorize(self, username):
        #for avaliable scopes see https://developer.spotify.com/web-api/using-scopes/
        scope = 'user-library-read playlist-modify-public playlist-read-private'
        redirect_uri='https://google.com/' # Paste your Redirect URI here
        client_credentials_manager = SpotifyClientCredentials(client_id=self.cid, client_secret=self.secret) 
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
        token = util.prompt_for_user_token(username, scope, self.cid, self.secret, redirect_uri)
        
        if token:
            sp = spotipy.Spotify(auth=token)
            return sp
        else:
            print("Can't get token for", username)


    def get_yt_playlist(self, url, data_path=None):
        
        sourceCode = requests.get(url).text
        playlist_id = str(url).split("=")[-1]
        soup = BeautifulSoup(sourceCode, 'html.parser')
        domain = 'https://www.youtube.com'
    
        track_list = []
        for link in soup.find_all("a", {"dir": "ltr"}):
            href = link.get('href')
            if href.startswith('/watch?'):
                #print(link.string.strip())
                #print(domain + href + '\n')

                full_trackname = link.string.strip()
                artist = link.string.strip().split('-')[0].strip()
                
                try:
                    track = link.string.strip().split('-')[1].strip()
                except IndexError:
                    track = ""
                
                track_filtered = re.sub("[\(\[].*?[\)\]]", "", track)

                track_list.append((artist, track_filtered, full_trackname))
    
            df = pd.DataFrame(data = track_list, columns = ('artist', 'track', 'full_trackname'))
            
            if data_path:
                df.to_csv(data_path + '{}_playlist.csv'.format(playlist_id), index=False)


            full_track_list = [x[2] for x in track_list]

        return full_track_list


    def get_uris(self, track_list, sp):
        uri_list = []
        for i, track in enumerate(track_list):
            search_result = sp.search(track)
            search_result = search_result['tracks']
            #print(search_result)
            
            if(search_result['total'] > 0):
                uri_list.append(search_result['items'][0]['uri'])
                
                # If you want to loop through all search results for a particular string query....
                # for j, val in enumerate(sp.search(track[2])['tracks']['items']):
                #   print(sp.search(track[2])['tracks']['items'][j]['name'])    
        
        return uri_list
        

    def create_playlist(self, title, tracks, sp):
        """Creates a new playlist from all tracks that met conditions"""
        playlist = self.sp.user_playlist_create(self.id, title, False)
        for track in tracks:
            self.sp.user_playlist_add_tracks(self.id, playlist['id'], [track])
        print "Playlist Created"