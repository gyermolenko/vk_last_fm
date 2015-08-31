# -*- coding: utf-8 -*-

import requests
import json
import os
import datetime
import last_fm as fm


# APP_ID = '4945278'    # (client_id)
# To refresh expired token you need to:
#   1. put the following link into browser:
#   http://api.vkontakte.ru/oauth/authorize?client_id=4945278&scope=audio&redirect_uri=&display=page&v=5.35&response_type=token
#   2. extract "access_token=" value from address bar of received response. E.g.:
#   https://oauth.vk.com/blank.html#access_token=b970209a2b65a90c39b58f6c3e1cec344236d239c97e593cca2f02e546919990543a721832bc41b3f6a46&expires_in=86400&user_id=5110875
#   3. update ACCESS_TOKEN variable below:

ACCESS_TOKEN = '434d67b3fb5186bab7e0fc85b47da37d81144d44fa253f3243433b2360d388bbef33ed473f78441099aab'  # Generated at (2015-08-31 21-15). Works for 24 hours ("expires_in=86400").

VK_METHOD_NAME = 'audio.search'
RESULTS_QTY = '1'
VK_API_VERSION = '5.35'  # 2015-08-02

foldername = ''


def get_vk_response(song_title):
    # e.g.: https://api.vk.com/method/audio.search?v=5.33&q=hatebreed%20-%20i%20will%20be%20heard&count=1&access_token=b970209a2b65a90c39b58f6c3e1cec344236d239c97e593cca2f02e546919990543a721832bc41b3f6a46
    request_url = 'https://api.vk.com/method/' + VK_METHOD_NAME + '?' + \
                    '&'.join(('v=' + VK_API_VERSION,
                              'q=' + song_title,
                              'count=' + RESULTS_QTY,
                              'access_token=' + ACCESS_TOKEN))
    response = requests.get(request_url)
    parsed_json = json.loads(response.text)
    return parsed_json


def download_song(download_url, song_title):
    # global foldername
    filename = song_title + '.mp3'
    with open(os.path.join(foldername, filename), 'w+') as f:
        f.write(requests.get(download_url).content)


def process_json(parsed_json, song_title):
    # Case of error in response. Err codes explained: http://vk.com/dev/errors
    if 'error' in parsed_json:
        # ex. 'User authorization failed: access_token has expired.'
        print 'Error.', parsed_json['error']['error_msg']
        return

    # Case of 0 results found
    if parsed_json['response']['count'] == 0:
        print 'Track "{}" was not found.'.format(song_title)
        return

    # Case of title mismatch situation
    artist = parsed_json['response']['items'][0]['artist']
    title = parsed_json['response']['items'][0]['title']
    song_title_from_response = ' - '.join((artist, title))
    if song_title_from_response.lower() != song_title.lower():
        print 'Track "{}", was not found. Closest match: "{}"'.format(song_title.encode('utf-8'), song_title_from_response.encode('utf-8'))
        return

    # Case when everything is OK
    full_link = parsed_json['response']['items'][0]['url']
    download_url = full_link.split('?')[0]  # ex. u'http://cs7-5v4.vk-cdn.net/p1/f2063e505df7b0.mp3'
    download_song(download_url, song_title)
    print 'Track "{}" processed.'.format(song_title.encode('utf-8'))


def main():
    global foldername

    last_fm_friends = fm.get_friends_list(fm.BASE_USERNAME)
    friend = last_fm_friends[0]

    foldername = friend + '__' + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    os.mkdir(foldername)

    his_loved_tracks = fm.get_loved_tracks(friend)
    for track in his_loved_tracks[:35]:
        if fm.get_artist_play_count_by_user(track[0], fm.BASE_USERNAME) < 4:
            song_title = ' - '.join(track)
            parsed_json = get_vk_response(song_title)
            process_json(parsed_json, song_title)


main()


# TODO
# v - last.fm part of application now works
# v - combined with last.fm part.
# v - folder is named with friend's name

# issues with some (not all) cylillyc. E.g. "Die Ärzte - Schrei nach Liebe"
# GUI ?
