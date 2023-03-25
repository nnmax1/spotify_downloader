
import sys

# remove unwanted characters from string
def sanitize(name, replace_with=''):
    clean_up_list = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|", "\0", "$"]
    for x in clean_up_list:
        name = name.replace(x, replace_with)
    return 

# fetches tracks from the provided url
def fetch_track(sp,  url):
    songs_list = []
    offset = 0

    items = sp.track(track_id=url)
    track_name = items.get('name')
    album_info = items.get('album')
    track_artist = ", ".join([artist['name'] for artist in items['artists']])
    if album_info:
        track_album = album_info.get('name')
        track_year = album_info.get('release_date')[:4] if album_info.get('release_date') else ''
        album_total = album_info.get('total_tracks')
    track_num = items['track_number']
    spotify_id = items['id']
    if len(items['album']['images']) > 0:
        cover = items['album']['images'][0]['url']
    else:
        cover = None
    if len(sp.artist(artist_id=items['artists'][0]['uri'])['genres']) > 0:
        genre = sp.artist(artist_id=items['artists'][0]['uri'])['genres'][0]
    else:
        genre = ""
    song = {"name": track_name, "artist": track_artist, "album": track_album, "year": track_year,
            "num_tracks": album_total, "num": track_num, "playlist_num": offset + 1,
            "cover": cover, "genre": genre, "spotify_id": spotify_id}

    return song 

# parse spotify url 
def parse_spotify_url(url):
    if url.startswith("spotify:"):
        #print("invalid url.")
        sys.exit(1)
    parsed_url = url.replace("https://open.spotify.com/", "")
    item_type = parsed_url.split("/")[0]
    item_id = parsed_url.split("/")[1]
    return item_type, item_id


# get item name by type (playlist, album or track)
def get_item_name(sp, item_type, item_id):
    if item_type == 'playlist':
        name = sp.playlist(playlist_id=item_id, fields='name').get('name')
    elif item_type == 'album':
        name = sp.album(album_id=item_id).get('name')
    elif item_type == 'track':
        name = sp.track(track_id=item_id).get('name')
    return sanitize(name)

# check if url is valid
def validate_spotify_url(url):
    item_type, item_id = parse_spotify_url(url)
    #print(f"Got item type {item_type} and item_id {item_id}")
    if item_type not in ['album', 'track', 'playlist']:
        #print("Only albums/tracks/playlists are supported")
        return False
    if item_id is None:
        #print("Couldn't get a valid id")
        return False
    return True


