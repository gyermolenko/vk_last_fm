# -*- coding: utf-8 -*-

import requests
import json
import os
import datetime


# APP_ID = '4945278'    # (client_id)
# To refresh expired token you need to:
#   1. put the following link into browser:
#   http://api.vkontakte.ru/oauth/authorize?client_id=4945278&scope=audio&redirect_uri=&display=page&v=5.35&response_type=token
#   2. extract "access_token=" value from address bar of received response. E.g.:
#   https://oauth.vk.com/blank.html#access_token=b970209a2b65a90c39b58f6c3e1cec344236d239c97e593cca2f02e546919990543a721832bc41b3f6a46&expires_in=86400&user_id=5110875
#   3. update ACCESS_TOKEN variable below:

ACCESS_TOKEN = 'b970209a2b65a90c39b58f6c3e1cec344236d239c97e593cca2f02e546919990543a721832bc41b3f6a46'  # Generated at (2015-08-03 13:59). Works for 24 hours ("expires_in=86400").

track_name_01 = 'Hatebreed - I will be heard'  # this part will be modified to get list from txt or something
# track_name_02 = 'Drowning Pool - Bodies'
track_name_02 = u'mujuice - приключения'  # Test for cyrillic
# track_name_01 = 'aarstarts'  # Test for no results
# track_name_01 = 'random choice'  # Test for mismatch

# list_of_tracks = [track_name_01]
list_of_tracks = [track_name_01, track_name_02]  # Test for more than one

VK_METHOD_NAME = 'audio.search'
RESULTS_QTY = '1'
VK_API_VERSION = '5.35'  # 2015-08-02

foldername = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
os.mkdir(foldername)


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


def download_song(download_url, track_title):
    filename = track_title + '.mp3'
    with open(os.path.join(foldername, filename), 'w+') as f:
        f.write(requests.get(download_url).content)


def main():
    for track_title in list_of_tracks:
        parsed_json = get_vk_response(track_title)

        # Case of error in response ( error codes explained: http://vk.com/dev/errors )
        if 'error' in parsed_json:
            print 'Error.', parsed_json['error']['error_msg']  # ex. 'User authorization failed: access_token has expired.'
            # TODO: add call to renew token
            continue

        # Case of 0 results found
        if parsed_json['response']['count'] == 0:
            print 'Track "{}" was not found.'.format(track_title)
            continue

        # Case of title mismatch situation
        artist = parsed_json['response']['items'][0]['artist']
        title = parsed_json['response']['items'][0]['title']
        song_title_from_response = ' - '.join((artist, title))
        if song_title_from_response.lower() != track_title.lower():
            print 'Track "{}", was not found. Closest match: "{}"'.format(track_title, song_title_from_response)
            continue

        # Case when everything is OK
        full_link = parsed_json['response']['items'][0]['url']
        download_url = full_link.split('?')[0]  # ex. u'http://cs7-5v4.vk-cdn.net/p1/f2063e505df7b0.mp3'
        download_song(download_url, track_title)

main()


# TODO
# v - if response contains error - return its text
# v - analyse possible track title mismatch situation
# v - "track not found" situation handling
# v - put tracks into separate folder. Name it with current timestamp
# v - try with 2-3 tracks finally
# x - renew access_token automatically - impossible wo 3rd party tools
# v - probably solved issue with cyrillic titles


# - combine with track list from last.fm part

# GUI ?
