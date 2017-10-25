# youtubedl import and init
from __future__ import unicode_literals
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass
    
    def warning(self, msg):
        pass
    
    def error(self, msg):
        print(msg)
    

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting...')
    
# spotify api imports
import sys
import spotipy
import spotipy.util as util
    
# youtube search imports
import urllib.request
import urllib.parse
import re

# youtube download
from subprocess import call

# import id3 tag editor
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import mutagen.id3

# import os functions to test if folder are created
import os
import time


def get_latest_saved_songs():
    scope = 'user-library-read'

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0]))
        sys.exit()

    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_tracks()
        lst = []
        for item in results['items']:
            track = item['track']
            lst.append((track['name'], track['artists'][0]['name'], track['album']['name']))
        return lst
    else:
        print("Can't get token for", username)


# Source 
def get_yt_link( name ):
    query_string = urllib.parse.urlencode({"search_query" : name})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    return "http://www.youtube.com/watch?v=" + search_results[0]


def dl_from_yt(url, path, codec):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': codec,
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return

i = 1
for (song_title, artist, album_name) in get_latest_saved_songs():
    print("(" + str(i) + "/20) " + song_title)
    i += 1

    # Create folder structure
    folder_path = os.path.expanduser('~/Music/' + artist + '/' + album_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Download the song
    codec = 'mp3'
    ytdl_path = folder_path + '/' + song_title
    full_path = ytdl_path + '.' + codec
    if not os.path.exists(full_path):
        dl_from_yt(get_yt_link(song_title + ' ' + artist), ytdl_path + '.%(ext)s', codec)

        # Add ID3 tags to it
        # Wait for the conversion to finish
        while not os.path.exists(full_path):
            time.sleep(1)

        music_file = MP3(full_path, ID3=EasyID3)
    
        music_file["artist"] = artist
        music_file["album"] = album_name
        music_file["title"] = song_title
        music_file.save()
    else:
        print(song_title + ' already downloaded !')
