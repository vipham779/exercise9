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
def lottery_result():
    resp = requests.get('http://ketqua.net')
    tree = bs4. BeautifulSoup(resp.text, features='html.parser')
    table = tree.find('table', attrs={'id':'result_tab_md'}).find('tbody')
    prizes = {}
    for row in table.find_all('tr'):
        prize = row.find_all('td')
        if len(prize) > 1:
            for i in prize:
                prizes.update({prize[0].text: [prize[i].text for i in range(1, len(prize))]})
    return prizes


def verify_slots(input_data):
    for key, value in prizes.items():
        for num in value:
            if int(num[-2:]) == input_data:
                result = 'Win'
            else:
                result = 'Lose'
    return result

def main():
    if len(sys.argv) < 2:
        print(lottery_result())
    else:    
    

if __name__ == '__main__':
    main()