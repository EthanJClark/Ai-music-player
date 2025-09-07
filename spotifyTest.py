import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os, random
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="user-library-read user-read-playback-state, user-modify-playback-state",
    ))

def toggle_playback(sp):
    playback = sp.current_playback()
    if playback and playback['is_playing']:
        sp.pause_playback()
    else:
        sp.start_playback()

def get_random_saved_track(sp):
    results = sp.current_user_saved_tracks()
    track = results['items'][random.randint(0, len(results['items']) - 1)]['track']
    return [track['uri'],track['name'], track['artists']]

def get_saved_tracks(sp):
    results = sp.current_user_saved_tracks()
    tracks = {}
    for item in results['items']:
        track = item['track']
        tracks[track['name'].lower()] = {
            'uri': track['uri'],
            'artist': track['artists'][0]['name']
        }

    return tracks

def play_track(sp, track_uri):
    if "track" in track_uri:
        sp.start_playback(uris=[track_uri]) 
    else:
        sp.start_playback(context_uri=track_uri)

def search_saved_tracks(sp, query):
    all_tracks = get_saved_tracks(sp)
    matching_tracks = all_tracks.get(query.lower(), None)
    return matching_tracks

def change_volume(sp, volume_change_by):
    target_volume = sp.current_playback()['device']['volume_percent'] + volume_change_by
    target_volume = max(0, min(100, target_volume))  # Ensure volume is between 0 and 100

    
    sp.volume(
        target_volume
    )

def search_for_song(sp, query):
    search = sp.search(q=query, type='track,album,playlist', limit=3)
    # return results["playlists"]["items"]
    
    results = {
        "songs":{},
        "albums":{},
        "playlists":{}
    }

    for item in search['tracks']['items']:
        if item is None:
            continue
        results["songs"][item['name']] = {
            "uri": item['uri'],
            "artist": item['artists'][0]['name']
        }
    for item in search['albums']['items']:
        if item is None:
            continue
        results["albums"][item['name']] = {
            "uri": item['uri'],
            "artist": item['artists'][0]['name']
        }
    for item in search['playlists']['items']:
        if item is None:
            continue
        results["playlists"][item['name']] = {
            "uri": item['uri'],
            "owner": item['owner']['display_name']
        }
    return results




if __name__ == "__main__":
    # x = sp.current_user_playlists()
    # x = x['items'][0]['uri']
    # playlist_uri = "spotify:playlist:YOUR_PLAYLIST_ID"
    # play_playlist(sp, x)

    print(search_for_song(sp, "halloween playlist"))

    # sp.start_playback(context_uri="spotify:playlist:0oGK7xmyKLusOZ3j2x83IY")
    play_track(sp, "spotify:playlist:0oGK7xmyKLusOZ3j2x83IY")

    # while True:
    #     command = input("Enter 'p' to toggle play/pause, 'q' to quit: ")
    #     if command == 'p':
    #         toggle_playback(sp)
    #     elif command == 'q':
    #         break