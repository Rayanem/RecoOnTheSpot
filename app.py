from flask import Flask, redirect, request, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from collections import Counter

# Configuration
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = "user-top-read"

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Spotipy OAuth Setup
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)

@app.route('/')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('get_top_artists'))

@app.route('/top-artists')
def get_top_artists():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_tracks = sp.current_user_top_tracks(limit=1, offset=0, time_range='long_term')

    if top_tracks:
        response = "Top 10 artistes les plus écoutés :<br>"
        for item in top_tracks['items']:
            response += f"{sp.audio_features(tracks=item['id'])}<br>"
        return response
    else:
        return "Aucun artiste trouvé."

if __name__ == '__main__':
    app.run(debug=True)
