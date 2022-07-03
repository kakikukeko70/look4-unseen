import random
import re
import math
from pprint import pprint

from django.conf import settings

from googleapiclient.discovery import build

MAX_RESULTS = 50

youtube = build('youtube', 'v3', developerKey=settings.API_KEY)
uploaded_videos = []
random_videos = []

def get_id(url):
    match = re.search('https://www.youtube.com/(.+?)/', url)

    if match:
        found = match.group(1)

    if found == 'user':
        username = url.split("https://www.youtube.com/user/", 1)[1]
        request = youtube.channels().list(
            part='id',
            forUsername=username
        )
        response = request.execute()
        id = response['items'][0]['id']
    
    if found == 'channel':
        id = url.split("https://www.youtube.com/channel/",1)[1]

    if found == 'c':
        c_username = url.split("https://www.youtube.com/c/",1)[1]

        request = youtube.search().list(
            part='snippet',
            q=c_username,
            type='channel',
        )

        response = request.execute()

        id = response['items'][0]['id']['channelId']

    return id

def get_uploads_id(id):
    request = youtube.channels().list(
        part='contentDetails',
        id=id,
    )
    response_for_id = request.execute()
    uploads_id = response_for_id['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    return uploads_id

def get_video_count(id):
    request_for_count = youtube.channels().list(
        part='statistics',
        id=id,
    )
    response_for_count = request_for_count.execute()

    video_count = int(response_for_count['items'][0]['statistics']['videoCount'])

    return video_count

def get_recent_videos(uploads_id):
    request = youtube.playlistItems().list(
        part='snippet',
        playlistId=uploads_id,
        maxResults=MAX_RESULTS,
    )

    response = request.execute()

    for item in response['items']:
        url = 'https://www.youtube.com/watch?v={}&ab_channel={}'.format(
            item['snippet']['resourceId']['videoId'], item['snippet']['channelTitle'].replace(' ', ''))
        video = {
            'title': item['snippet']['title'], 
            'url': url,
            'publishd_at': item['snippet']['publishedAt'], 
            'thumbnails': item['snippet']['thumbnails']['default'] 
        }
        uploaded_videos.append(video)
        
    next_page_token = response['nextPageToken']

    return next_page_token

def get_rest_videos(uploads_id, video_count, next_page_token):
    for i in range(math.ceil((video_count-50)/50)):
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads_id,
            maxResults=MAX_RESULTS,
            pageToken=next_page_token
        )

        response = request.execute()

        for item in response['items']:
            url = 'https://www.youtube.com/watch?v={}&ab_channel={}'.format(
                item['snippet']['resourceId']['videoId'], item['snippet']['channelTitle'].replace(' ', ''))
            video = {
                'title': item['snippet']['title'], 
                'url': url,
                'publishd_at': item['snippet']['publishedAt'], 
                'thumbnails': item['snippet']['thumbnails']['default'] 
            }
            uploaded_videos.append(video)

        try:
            next_page_token = response['nextPageToken']
        except:
            break

def get_random_videos(video_count):
    for i in range(10):
        random_num = random.randrange(0, video_count)
        random_videos.append(uploaded_videos[random_num])

def main(url):
    id = get_id(url=url)
    uploads_id = get_uploads_id(id=id)
    video_count = get_video_count(id=id)
    next_page_token = get_recent_videos(uploads_id=uploads_id)
    get_rest_videos(uploads_id=uploads_id, video_count=video_count, next_page_token=next_page_token)
    get_random_videos(video_count=video_count)
    return random_videos

if __name__ == '__main__':
    main()