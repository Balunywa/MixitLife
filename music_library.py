import requests
class AppleMusicLibrary:
    def __init__(self, auth):
        self.base_url = 'https://api.music.apple.com/v1/me'
        self.auth = auth

    def get_playlists(self):
        token = self.auth.get_token()
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
        response = requests.get(self.base_url + '/library/playlists', headers=headers)
        playlists = response.json()['data']
        return playlists

    def get_playlist_name(self, playlist_id):
        token = self.auth.get_token()
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
        response = requests.get(self.base_url + '/library/playlists/' + playlist_id, headers=headers)
        playlist_name = response.json()['data'][0]['attributes']['name']
        return playlist_name
