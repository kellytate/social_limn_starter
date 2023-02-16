# import spotipy
# from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

# # This is just an example to test spotify connectivity

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(cc
#                                                 scope="user-library-read"))


# taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'

# results = sp.artist_albums(taylor_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = sp.next(results)
#     albums.extend(results['items'])

# for album in albums:
#     print(album['name'])


# def search_spotify(query):
#     client_credentials_manager = SpotifyClientCredentials()
#     sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#     results = sp.search(q=query, limit=20)
#     for i,t in enumerate(results['tracks']['items']):
#         print(' ', i, t)
