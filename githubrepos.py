'''
This is the script that returns a list of repositories of a username
on GitHub
The format of command line: python(3) githubrepos.py username
'''

import sys
import requests


# convert the link to a json file
# return a list of repositories in that username
def repos(username):
    path = 'https://api.github.com/users/{}/repos'.format(username)
    r = requests.get(path)
    data = r.json()
    result = [i['name'] for i in data]
    return result


def solve(username):
    result = repos(username)
    return result


def main():
    username = sys.argv[1]
    result = solve(username)
    print(result)


if __name__ == '__main__':
    main()
