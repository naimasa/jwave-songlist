
import argparse
import json

from ytmusicapi import YTMusic

PLAYLIST_NAME = "J-Wave Songlist"


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("headers_auth_file", help="path to headers auth json")
    parser.add_argument("tracks_file", help="tracks json to be added to playlist")
    parser.add_argument("playlist_name", help="playlist name to operate")
    parser.add_argument("playlist_description", help="playlist description")
    parser.add_argument("--remove_all_tracks_before_add", action='store_true', help="remove all tracks from playlist before adding new songs")

    return parser.parse_args()


def find_playlist_by_name(ytmusic, name):

    playlists = ytmusic.get_library_playlists()
    for playlist in playlists:
        if playlist["title"] == name:
            return playlist["playlistId"]
    
    return None

if __name__ == "__main__":
    args = parse_args()

    ytmusic = YTMusic(args.headers_auth_file)

    with open(args.tracks_file) as f:
        tracks = json.load(f)

    video_ids_to_add = [track["videoId"] for track in tracks]
    #print(video_ids_to_add)
    
    playlist_id = find_playlist_by_name(ytmusic, args.playlist_name)
    
    if playlist_id:
        if args.remove_all_tracks_before_add:
            playlist = ytmusic.get_playlist(playlist_id, limit=9999)
            if playlist["tracks"]:
                ytmusic.remove_playlist_items(playlist_id, playlist["tracks"])

        ret = ytmusic.add_playlist_items(playlist_id, video_ids_to_add, duplicates=True)
        #print(ret)
        ytmusic.edit_playlist(playlist_id, description=args.playlist_description)
    else:
        ytmusic.create_playlist(args.playlist_name, args.playlist_description, video_ids=video_ids_to_add)
    