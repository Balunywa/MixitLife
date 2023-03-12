from flask import Flask, render_template, request
from music_auth import AppleMusicAuth
from music_library import AppleMusicLibrary

app = Flask(__name__)
music_auth = AppleMusicAuth()
music_library = AppleMusicLibrary(music_auth)

@app.route('/')
def index():
    playlists = music_library.get_playlists()
    return render_template('index.html', playlists=playlists)

@app.route('/playlist', methods=['POST'])
def playlist():
    playlist_id = request.form['playlist']
    playlist_name = music_library.get_playlist_name(playlist_id)
    return render_template('playlist.html', playlist_name=playlist_name, playlist_id=playlist_id)

@app.route('/share', methods=['POST'])
def share():
    playlist_id = request.form['playlist_id']
    dj = request.form['dj']
    station = request.form['station']
    playlist_url = music_auth.generate_playlist_url(playlist_id)
    return render_template('share.html', playlist_url=playlist_url, dj=dj, station=station)

if __name__ == '__main__':
    app.run(debug=True)


