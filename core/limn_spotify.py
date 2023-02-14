import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="16b3fc31b76a48e6a169df7206ceccad"),
                                                client_secret="96b200204f794de48df1ba62c4c99be9",
                                                redirect_uri="http://localhost:1234",
                                                scope="user-library-read")

taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'

results = sp.artist_albums(taylor_uri, album_type='album')
albums = results['items']
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])