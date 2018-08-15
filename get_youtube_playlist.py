from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

data_path = '/Users/mvaughan/Documents/Code/youtube2spotify/playlists/'
#url = "https://www.youtube.com/playlist?list=PLeblcLK1Ghf4mVQ2OzRjI72ffMshnBtK4"

def getPlaylistLinks(url):
    sourceCode = requests.get(url).text
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
        df.to_csv(data_path + 'playlist.csv', index=False)

    return track_list


