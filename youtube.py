'''
crawl video info from youtube
'''


import requests
import time
import sys
from bs4 import BeautifulSoup
from apiclient.discovery import build
import pandas as pd
import datetime


api_key = key
def request(keyword):
    youtube = build('youtube', 'v3', developerKey=api_key)
    req = youtube.search().list(
        q='{}'.format(keyword), part='snippet', maxResults=5, type='video'
    )
    resp = req.execute()
    return resp


def title(keyword):
    resp = request(keyword)
    result = [item['snippet']['title'] for item in resp['items']]
    return result


def link(keyword):
    resp = request(keyword)
    result = ['https://www.youtube.com/watch?v={}'.format(item['id']['videoId']) for item in resp['items']]
    return result


def statistics(keyword):
    resp = request(keyword)
    video_ids = [item['id']['videoId'] for item in resp['items']]
    url = 'https://www.googleapis.com/youtube/v3/videos'
    result = []
    for video_id in video_ids:
        params = {
            'key': api_key,
            'part': 'statistics',
            'id':'{}'.format(video_id)
        }
        resp = requests.get(url, params=params).json()
        time.sleep(1)
        num = int(resp['items'][0]['statistics']['viewCount'])
        view = f"{num:,}"
        result.append(view)
    return result


def date(keyword):
    resp = request(keyword)
    result = []
    for item in resp['items']:
        string_temp = item['snippet']['publishedAt'][:10]
        published_date = datetime.datetime.strptime(string_temp, '%Y-%m-%d').strftime('%Y-%b-%d')
        result.append(published_date)
    return result


def channel(keyword):
    resp = request(keyword)
    result = [item['snippet']['channelTitle'] for item in resp['items']]
    return result


def table(keyword, criteria):
    columns = ['title', 'link', 'view', 'date', 'channel']
    df = pd.DataFrame(columns=columns)
    df['title'] = title(keyword)
    df['link'] = link(keyword)
    df['view'] = statistics(keyword)
    df['date'] = date(keyword)
    df['channel'] = channel(keyword)
    if criteria == 'view':
        kf = df.sort_values('view', ascending=False)
        kf['view'] = ['f{i:,}' for num in kf['view']]
    elif criteria == 'date':
        kf = df.sort_values('date', ascending=False)
        kf['view'] = ['f{i:,}' for num in kf['view']]
    return kf

def main():
    if len(sys.argv) < 2:
        print('Please input with the format: python3 youtube.py [keyword] [order by]')
        sys.exit(1)
    else:
        keyword = sys.argv[1]
        criteria = sys.argv[-1]
        table(keyword, criteria)


if __name__ == '__main__':
    main()
        


