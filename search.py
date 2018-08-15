import spotipy
import sys
import pprint

def search(search_str):

    sp = spotipy.Spotify()
    result = sp.search(search_str)
    
    pprint.pprint(result)
    return result

if __name__ == "__main__":
    
    search('Frits Wentink')