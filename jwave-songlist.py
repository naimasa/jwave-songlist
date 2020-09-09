
import json
import urllib.request

from bs4 import BeautifulSoup

def get_song_list():
    JWAVE_SONGLIST_URL="https://www.j-wave.co.jp/songlist/pc_y.html"

    with urllib.request.urlopen(JWAVE_SONGLIST_URL) as response:
        soup = BeautifulSoup(response, features="html.parser")
    
    titles = [e.get_text() for e in soup.select("#block_playlist > div > div.list_songs > div > div.song_wrap > div > div.col_l > div.song_info > h4")]
    artists = [e.get_text() for e in soup.select("#block_playlist > div > div.list_songs > div > div.song_wrap > div > div.col_l > div.song_info > p.txt_artist > span")]
    times = [str.strip(e['data-oadate']) for e in soup.select("#block_playlist > div > div.list_songs > div > div.song_wrap > div > div.col_l > div.song_info > p.time > span")]

    return zip(artists, titles, times)

if __name__ == "__main__":
    song_dict = [{"artist":artist,"title":title,"time":time} for artist,title,time in get_song_list()]
    print(json.dumps(song_dict))
    