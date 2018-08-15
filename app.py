from authorize import spotify_authorize
import pprint
import pandas as pd
from get_youtube_playlist import getPlaylistLinks

# Authorization
sp = spotify_authorize()
username = '123149945'
playlist_url = "https://www.youtube.com/playlist?list=PLt_JjdAPV6eDcfHrbu0Kc4p8Vul4xmEnf"
playlist_id = '63IU61sIKDQZVXkBUaP13h'

track_list_orig = getPlaylistLinks(playlist_url)
print(track_list_orig)

track_list_2 =[x[2] for x in track_list_orig]
print(track_list_2)

def get_uris(track_list):
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

tracks = get_uris(track_list_2)
sp.user_playlist_add_tracks(username, playlist_id=playlist_id, tracks=tracks)

print("Done!")