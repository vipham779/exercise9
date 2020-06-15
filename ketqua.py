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
def lottery_result(*args):
    resp = requests.get('http://ketqua.net')
    tree = bs4. BeautifulSoup(resp.text, features='html.parser')
    table = tree.find('table', attrs={'id':'result_tab_md'}).find('tbody')
    prizes = []
    for line in table.find_all('tr'):
        prize = line.find_all('td')
        if len(prize) > 1:
            for i in range(len(prize)):
                prizes.append(prize[i].text)
    return prizes


def display_lottery_result(input_data):
    result = gamble(32, 10, 11)
    return result


def verify_slots()


def main():
    
    

if __name__ == '__main__':
    main()