#/bin/bash
set -eu

source venv/bin/activate

echo "Generating J-Wave songlist..."
jwave_songlist=jwave-songlist-`date -v-1d +%Y%m%d`.json
if [ ! -e $jwave_songlist ];then
    python3 jwave-songlist.py > $jwave_songlist
    echo "Done."
else
    echo "Skipped."
fi

echo "Generating YouTube Music songlist..."
ytmusic_songlist=ytmusic-songlist-`date -v-1d +%Y%m%d`.json
if [ ! -e $ytmusic_songlist ];then
    python3 ytmusic-tracks.py headers_auth.json $jwave_songlist > $ytmusic_songlist
    echo "Done."
else
    echo "Skipped."
fi

echo "Updating YouTube Music Playlist..."
playlist_name="J-Wave Songlist"
playlist_description="J-Wave Songlist `date -v-1d +%Y%m%d`"
python3 ytmusic-playlist.py headers_auth.json $ytmusic_songlist "$playlist_name" "$playlist_description" --remove_all_tracks_before_add
echo "Done."
