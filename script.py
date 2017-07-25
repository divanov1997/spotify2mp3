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
            lst.append((track['name'], track['artists'][0]['name']))
        return lst
    else:
        print("Can't get token for", username)


# Source 
def get_yt_link( name ):
    query_string = urllib.parse.urlencode({"search_query" : name})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    return "http://www.youtube.com/watch?v=" + search_results[0]


def dl_from_yt(url, song_title, artist):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '~/Music/spotify2mp3/' + artist + ' - '+ song_title + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return


for (song_title, artist) in get_latest_saved_songs():
    print(song_title)
    dl_from_yt(get_yt_link(song_title + ' ' + artist), song_title, artist)
