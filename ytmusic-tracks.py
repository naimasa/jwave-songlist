
import argparse
import json

from ytmusicapi import YTMusic


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("headers_auth_file", help="path to headers auth json")
    parser.add_argument("songlist", help="songlist json to be converted to Youtube Music tracks")

    return parser.parse_args()

def get_video_ids_from_song_list(ytmusic, songlist):

    tracks = []
    for track in songlist:
        artist = track["artist"]
        title = track["title"]

        query = f'"{artist}" "{title}"'
        songs = ytmusic.search(query, filter="songs")
        
        if songs:
            tracks.append(songs[0])
    
    return tracks

if __name__ == "__main__":
    args = parse_args()

    ytmusic = YTMusic(args.headers_auth_file)

    with open(args.songlist) as f:
        songlist = json.load(f)
        #print(songlist)

        tracks = get_video_ids_from_song_list(ytmusic, songlist)
        print(json.dumps(tracks))
    