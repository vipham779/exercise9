'''
Crawl video information from Youtube
Command line: python3 youtube.py [key word] [order by which criteria] [number of results]
- Key word: the white space (if any) between words need replacing with '+'
- Criteria: view or date
- Number of results: a positive integer
'''


import requests
import time
import sys
from bs4 import BeautifulSoup
from apiclient.discovery import build
import pandas as pd
import datetime


api_key = 'AIzaSyCjpgF23NQ_H3PrEptKmpqbo5ujBjXlg8A'
def request(keyword, n):
    youtube = build('youtube', 'v3', developerKey=api_key)
    req = youtube.search().list(
        q='{}'.format(keyword), part='snippet', maxResults='{}'.format(n), type='video'
    )
    resp = req.execute()
    return resp


def title(keyword,n):
    resp = request(keyword,n)
    result = [item['snippet']['title'] for item in resp['items']]
    return result


def link(keyword,n):
    resp = request(keyword,n)
    result = ['https://www.youtube.com/watch?v={}'.format(item['id']['videoId']) for item in resp['items']]
    return result


def statistics(keyword,n):
    resp = request(keyword,n)
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
        # view = f"{num:,}"
        result.append(num)
    return result


def date(keyword,n):
    resp = request(keyword,n)
    result = []
    for item in resp['items']:
        string_temp = item['snippet']['publishedAt'][:10]
        published_date = datetime.datetime.strptime(string_temp, '%Y-%m-%d').strftime('%Y-%b-%d')
        result.append(published_date)
    return result


def channel(keyword,n):
    resp = request(keyword,n)
    result = [item['snippet']['channelTitle'] for item in resp['items']]
    return result


def table(keyword,criteria, n):
    columns = ['title', 'link', 'view', 'date', 'channel']
    df = pd.DataFrame(columns=columns)
    df['title'] = title(keyword,n)
    df['link'] = link(keyword,n)
    df['view'] = statistics(keyword, n)
    df['date'] = date(keyword,n)
    df['channel'] = channel(keyword,n)
    if criteria == 'view':
        kf = df.sort_values('view', ascending=False)
        kf['view'] = [f'{num:,}' for num in kf['view']]
    elif criteria == 'date':
        kf = df.sort_values('date', ascending=False)
        kf['view'] = [f'{num:,}' for num in kf['view']]
    return kf

def main():
    if len(sys.argv) < 2:
        print('Please input with the format: python3 youtube.py [keyword] [criteria] [number of results]')
        sys.exit(1)
    keyword = sys.argv[1]
    criteria = sys.argv[2]
    n = sys.argv[-1]
    if criteria not in ['view', 'date']:
        print('Criteria is either view or date. Please input again: python3 youtube.py [keyword] [criteria] [number of results]')
    if int(n) <= 0 or not n.isdigit():
        print('Number is a positive integer')
    kf = table(keyword, criteria, n).reset_index()
    del kf['index']
    kf.to_csv('youtube.csv', encoding='utf8')


if __name__ == '__main__':
    main()
        


