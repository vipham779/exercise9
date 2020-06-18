'''
'''
import itertools
import requests
import sys


def top_answers(n):
    path = 'http://api.stackexchange.com/2.2/questions?pagesize={}&order=desc&sort=votes&tagged=label&site=stackoverflow&filter=!-Kh(SzYi6xv1bR9.UW3FnYazg)LA73IP9'.format(n)
    resp = requests.get(path)
    data = resp.json().get('items')
    temp = []
    for elem in data:
        link_title1= dict(itertools.islice(elem.items(), 3, 5))
        link_title2 = dict(sorted(link_title1.items(), key=lambda x:x[0], reverse=True))
        for key, value in link_title2.items():
            temp.append('{}: {}\n'.format(key, value))
    result = '\n'.join(temp)
    return result
    


def main():
    if len(sys.argv) != 3:
        print('Please input with the format: python(3) so.py [Integer] label')
        sys.exit()
    n = sys.argv[1]
    if not n.isdigit() or int(n) == 0:
        print('Please input an INTEGER LARGER THAN 0')
        sys.exit()
    print(top_answers(n))


if __name__ == '__main__':
    main()