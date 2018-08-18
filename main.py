from authorize import spotify_authorize
import pprint
import pandas as pd
from Youtube2Spotify import Youtube2Spotify

# Authorization
username = '123149945'
yt = Youtube2Spotify()
sp = yt.authorize(username)

yt_playlist_url = "https://www.youtube.com/playlist?list=PLvhwoyf-NI00qk-H_Fk6KjZPNnGSRR2Sm"
sp_playlist_id = '4EfE9bMjuVhWSTcmveqBWC'

track_list = yt.get_yt_playlist(yt_playlist_url)
print(track_list)

#track_list_2 = [x[2] for x in track_list_orig]
#print(track_list_2)

tracks = yt.get_uris(track_list, sp)
sp.user_playlist_add_tracks(username, playlist_id=sp_playlist_id, tracks=tracks)

print("Done!")