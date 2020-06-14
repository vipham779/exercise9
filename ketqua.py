'''
This is the script that checks whether a person wins at gambling. 
He wins if the slots he takes a gamble on are exactly the last 2 digits
of any prize of the lottery result released on the day he gambles. 
Otherwise, he loses.
'''
import bs4
import requests
import sys


# return 
def gamble(*args):
    resp = requests.get('http://ketqua.net')
    tree = bs4. BeautifulSoup(resp.text, features='html.parser')
    rs = tree.find_all('td', attrs={'id': ['rs_0_0', 'rs_1_0', 'rs_2_0',
                                           'rs_3_0', 'rs_3_1', 'rs_3_2',
                                           'rs_3_3', 'rs_3_4', 'rs_3_5',
                                           'rs_4_0', 'rs_4_1', 'rs_4_2',
                                           'rs_4_3', 'rs_5_0', 'rs_5_1',
                                           'rs_5_2', 'rs_5_3', 'rs_5_4',
                                           'rs_5_5', 'rs_6_0', 'rs_6_1',
                                           'rs_6_2', 'rs_7_0', 'rs_7_1',
                                           'rs_7_2', 'rs_7_3']})
    temp = [int(rs[i].text[-2:]) for i in range(26)]
    result = [(num, 'You win') if num in temp else (num, 'You lose') 
              for num in args]
    if not args:
        result = [{'Special prize': rs[0].text}, {'1st prize': rs[1].text},
                  {'2nd prize': rs[2].text},
                  {'3rd prize': [rs[i].text for i in range(3,9)]}, 
                  {'4th prize': [rs[i].text for i in range(9, 13)]}, 
                  {'5th prize': [rs[i].text for i in range(13, 19)]},
                  {'6th prize': [rs[i].text for i in range(19, 22)]}, 
                  {'7th prize': [rs[i].text for i in range(22,26)]}
                 ]
    return result


def solve():
    result = gamble(32, 10, 11)
    return result


def main():
    args = sys.argv[0]
    print(len(sys.argv))
    print(solve())
    

if __name__ == '__main__':
    main()