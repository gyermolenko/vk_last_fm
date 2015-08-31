import requests
import json


BASE_USERNAME = 'peck_wtf'
API_KEY = '9224ad2d6e20ec8a7b8ee84e38c3bf2b'
BASE = 'http://ws.audioscrobbler.com/'
API_VERSION = '2.0'
REQUEST_FORMAT = 'json'


def make_url(method, user, limit=0, artist=''):
    url = BASE + API_VERSION + '/?' + '&'.join((
        'method=' + method,
        'user=' + user,
        'api_key=' + API_KEY,
        'format=' + REQUEST_FORMAT,
        ))

    if limit:
        url += '&' + 'limit=' + limit
    if artist:
        url += '&' + 'artist=' + artist

    return url


def get_friends_list(username):
    user = username
    method = 'user.getfriends'
    limit = '100'
    friends_list = []

    url = make_url(method, user, limit)
    response = requests.get(url)
    response_json = json.loads(response.text)

    for el in response_json['friends']['user']:
        friends_list.append(el['name'])

    return friends_list


def get_loved_tracks(username):
    user = username
    method = 'user.getlovedtracks'
    limit = '1000'  # 1-1000
    loved_tracks = []

    url = make_url(method, user, limit)
    response = requests.get(url)
    response_json = json.loads(response.text)

    for rec in response_json['lovedtracks']['track']:
        artist = rec['artist']['name']
        track = rec['name']
        loved_tracks.append((artist, track))

    return loved_tracks


def get_artist_play_count_by_user(artist, user):
    method = 'user.getartisttracks'

    url = make_url(method, user, artist=artist)
    response = requests.get(url)
    response_json = json.loads(response.text)

    return len(response_json['artisttracks']['track'])
