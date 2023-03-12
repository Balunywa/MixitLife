import base64
import requests
import time
import jwt

class AppleMusicAuth:
    def __init__(self):
        self.base_url = 'https://appleid.apple.com'
        self.client_id = 'your_client_id'
        self.client_secret = 'your_client_secret'

    def get_jwt(self):
        headers = {
            'alg': 'ES256',
            'kid': 'your_kid'
        }
        payload = {
            'iss': self.client_id,
            'iat': time.time(),
            'exp': time.time() + 1800,
            'aud': 'https://appleid.apple.com',
            'sub': self.client_id
        }
        try:
            jwt_token = jwt.encode(payload, self.client_secret, algorithm='ES256', headers=headers)
        except Exception as e:
            print(f'Error generating JWT token: {e}')
            return None
        return jwt_token

    def get_token(self):
        jwt_token = self.get_jwt()
        if jwt_token is None:
            return None
        headers = {
            'Authorization': 'Bearer ' + jwt_token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials',
            'scope': 'music-library'
        }
        response = requests.post(self.base_url + '/auth/oauth2/token', headers=headers, data=data)
        token = response.json()['access_token']
        return token

    def generate_playlist_url(self, playlist_id):
        token = self.get_token()
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
        data = {
            'data': {
                'attributes': {
                    'name': 'My Playlist',
                    'description': 'A great playlist',
                    'public': False
                },
                'relationships': {
                    'tracks': {
                        'data': [
                            {
                                'id': playlist_id,
                                'type': 'songs'
                            }
                        ]
                    }
                },
                'type': 'playlists'
            }
        }
        response = requests.post('https://api.music.apple.com/v1/me/library/playlists', headers=headers, json=data)
        playlist_url = response.json()['data'][0]['attributes']['url']
        return playlist_url


