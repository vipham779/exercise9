'''
This script returns a csv file containing job details relating to
'Data Analyst' from Indeed. 

If you want to return 10 posts, please
input with the format: python(3) jobcrawler3.py 10. The same pattern 
applies for 20, 30, etc.

Be noted that you are only allowed to input an integer that is a 
multiple of 10
'''


import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys


def location(soup):
    locations = []
    for div in soup.find_all('div', attrs={'class': 'row'}):
        location = div.find_all('span', attrs={'class': 'location'})
        for address in location:
            locations.append(address.text.strip())
    return locations


def title(soup):
    titles = []
    for div in soup.find_all('div', attrs={'class': 'row'}):
        for a in div.find_all('a', attrs={'data-tn-element': 'jobTitle'}):
            titles.append(a['title'])
    return titles


def company(soup):
    companies = []
    for div in soup.find_all('div', attrs={'class': 'row'}):
        company = div.find_all('span', attrs={'class': 'company'})
        for name in company:
            companies.append(name.text.strip())
    return companies


def summary(soup):
    scopes = soup.find_all('div', attrs={'class': 'summary'})
    summaries = [scope.text.strip() for scope in scopes]
    return summaries


def request(number_results):
    columns = ['location', 'job_title', 'company', 'summary']
    df = pd.DataFrame(columns=columns)
    job_location = []
    job_title = []
    job_company = []
    job_summary = []
    for start in range(0, int(number_results), 10):
        url = 'https://vn.indeed.com/jobs?q=data+analyst&l=vietnam'\
              '&start={}'.format(start)
        resp = requests.get(url)
        time.sleep(1)
        soup = BeautifulSoup(resp.text, features='html.parser')
        job_location.extend(location(soup))
        job_title.extend(title(soup))
        job_company.extend(company(soup))
        job_summary.extend(summary(soup))
    df['location'] = job_location
    df['job_title'] = job_title
    df['company'] = job_company
    df['summary'] = job_summary
    return df


def main():
    if len(sys.argv) < 2:
        print('Please input a mulitple of 10 with the format: '
              'python(3) jobcrawler3.py [MULTIPLE OF 10]')
        sys.exit()
    else:
        number_results = sys.argv[1]
        df = request(number_results)
        df.to_csv('jobcrawler3.csv', encoding='utf8')


if __name__ == '__main__':
    main()
