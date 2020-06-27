




import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


url = 'https://vn.indeed.com/jobs?q=data+analyst&l=vietnam'
resp = requests.get(url)
soup = BeautifulSoup(resp.text)


def job_title(soup):
    job_titles = []
    for div in soup.find_all('div', attrs={'class': 'row'}):
        for a in div.find_all('a', attrs={'data-tn-element': 'jobTitle'}):
            job_titles.append(a['title'])
    return job_titles

def company(soup):
    companies = []
    for div in soup.find_all('div', attrs={'class': 'row'}):
        company = div.find_all('span', attrs={'class': 'company'})
        for name in company:
            companies.append(name.text.strip())
    return companies

def location(soup):
    locations = []
    for div in soup.find_all('div', attrs={'class': 'row'}):
        location = div.find_all('span', attrs={'class': 'location'})
        for address in location:
            locations.append(address.text.strip())
    return locations

def summary(soup):
    scopes = soup.find_all('div', attrs={'class': 'summary'})
    summaries = [scope.text.strip().split('\n') for scope in scopes]
    return summaries

columns = ['location', 'job_title', 'company', 'summary']
df = pd.DataFrame(columns=columns)
df['location'] = location(soup)
df['job_title'] = job_title(soup)
df['company'] = company(soup)
df['summary'] = summary(soup)
df.to_csv('jobcrawler3.csv', encoding='utf8')