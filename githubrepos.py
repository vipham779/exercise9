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
    temp = [i['name'] for i in data]
    result = '\n'.join(temp)
    return result


def main():
    if len(sys.argv) < 2:
        print('Please input with the format: python(3) githubrepos.py username')
        sys.exit()
    username = sys.argv[1]
    print(repos(username))


if __name__ == '__main__':
    main()
