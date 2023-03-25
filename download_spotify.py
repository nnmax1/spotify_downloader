import urllib.request
from os import path

import mutagen
import yt_dlp as youtube_dl
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


from spotify import  fetch_track


def downloadTrack(spotify_creds, url, directory):
    C_ID= spotify_creds['C_ID']
    C_SECRET = spotify_creds['C_SECRET']
    sp_client = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=C_ID,client_secret=C_SECRET))
    song= fetch_track(sp_client, url)
    format_string = 'bestaudio/best'
 
    query = f"{song.get('artist')} - {song.get('name')}".replace(":", "").replace("\"", "")
    #print(query)
    download_archive = './'+directory+ '/downloaded_songs.txt'
    file_name = str(song.get('name')+' - '+song.get('artist'))
    #file_name= str(song.get('spotify_id'))
    file_path = './'+directory+'/'+str(file_name)
    sponsorblock_remove_list = []
    outtmpl = f"{file_path}.%(ext)s"
    ydl_opts = {
        'format': format_string,
        'download_archive': download_archive,
        'outtmpl': outtmpl,
        'default_search': 'ytsearch',
        'noplaylist': True,
        'no_color': False,
        'postprocessors': [
            {'key': 'SponsorBlock',
            'categories': sponsorblock_remove_list,
            },
            {
            'key': 'ModifyChapters',
            'remove_sponsor_segments': ['music_offtopic'],
            'force_keyframes': True,
        }],
        'postprocessor_args': ['-metadata', 'title=' + song.get('name'),
        '-metadata', 'artist=' + song.get('artist'),
        '-metadata', 'album=' + song.get('album')]
        }
    # need ffmpeg
    mp3_postprocess_opts = {
        'key': 'FFmpegExtractAudio',
       'preferredcodec': 'mp3',
        'preferredquality': '192',
      }
    ydl_opts['postprocessors'].append(mp3_postprocess_opts.copy())

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([query])
        except Exception as e:
            #print(e)
            print('Failed to download: {}, please ensure YouTubeDL is up-to-date. '.format(query))
            return {'error':'unable to download'}
    mp3filename = f"{file_path}.mp3"
    mp3file_path = path.join(mp3filename)
    if not path.exists(mp3file_path):
        try:
            song_file = MP3(mp3file_path, ID3=EasyID3)
        except mutagen.MutagenError as e:
            #print(e)
            #print('Failed to download: {}, please ensure YouTubeDL is up-to-date. '.format(query))
            return {'error':'unable to download'}
        song_file['date'] = song.get('year')
    
        song_file['genre'] = song.get('genre')
        song_file.save()
        song_file = MP3(mp3filename, ID3=ID3)
        cover = song.get('cover')
        if cover is not None:
            if cover.lower().startswith('http'):
                req = urllib.request.Request(cover)
            else:
                raise ValueError from None
            with urllib.request.urlopen(req) as resp:  # nosec
                song_file.tags['APIC'] = APIC(
                    encoding=3,
                    mime='image/jpeg',
                    type=3, desc=u'Cover',
                    data=resp.read()
                )
        song_file.save()
        return {'error':'Successfully downloaded'}
    #else:
        #print('File {} already exists, we do not overwrite it '.format(mp3filename))
        #return {'error':'file already exists'}
   


