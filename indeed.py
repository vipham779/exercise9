"""
Command line: python3 indeed.py [POSITION][MULTIPLE OF 10]
This script returns a csv file containing job posts from Indeed.

The white space among words in [POSITION] is replaced with '+'
The input integer is 10 units fewer than the number of posts returned

If you want to return 10 posts of position 'Data Analyst', run
'python(3) jobcrawler3.py data+analyst 0'
The same pattern is applied to 20 posts, 30 posts, etc..

Be noted that you are only allowed to input an integer that is a
multiple of 10
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys

# from crontab import CronTab


def location(soup):
    locations = [
        span.text for span in soup.find_all("span", attrs={"class": "location"})
    ]
    return locations


def title(soup):
    titles = [
        a["title"] for a in soup.find_all("a", attrs={"data-tn-element": "jobTitle"})
    ]
    return titles


def company(soup):
    companies = [
        span.text.strip() for span in soup.find_all("span", attrs={"class": "company"})
    ]
    return companies


def date(soup):
    dates = [span.text for span in soup.find_all("span", attrs={"class": "date"})]
    temp = []
    for date in dates:
        idx = date.rfind("n")
        if date[: idx - 1].endswith("+"):
            temp.append("{}+ days ago".format(date[: idx - 2]))
        elif 'Hôm' in date:
            temp.append('01 day ago')
        else:
            temp.append("{} days ago".format(date[: idx - 1].zfill(2)))
    return temp


def request(position, number_results):
    columns = ["location", "title", "company", "date"]
    df = pd.DataFrame(columns=columns)
    job_location = []
    job_title = []
    job_company = []
    job_date = []
    for start in range(0, int(number_results), 10):
        url = "https://vn.indeed.com/jobs"
        params = {"q": position.lower(), "l": "vietnam", "start": start}
        resp = requests.get(url, params=params)
        time.sleep(1)
        soup = BeautifulSoup(resp.text, features="html.parser")
        job_location.extend(location(soup))
        job_title.extend(title(soup))
        job_company.extend(company(soup))
        job_date.extend(date(soup))
    df["location"] = job_location
    df["title"] = job_title
    df["company"] = job_company
    df["date"] = job_date
    result = df.sort_values("date").reset_index()
    del result["index"]
    return result


def main():
    if len(sys.argv) < 2:
        print(
            "Please input a mulitple of 10 with the format: "
            "python(3) indeed.py [POSITION][MULTIPLE OF 10]"
        )
        sys.exit()
    else:
        position = sys.argv[1]
        number_results = sys.argv[-1]
        df = request(position, number_results)
        df.to_csv("indeed.csv", encoding="utf8")


if __name__ == "__main__":
    main()
