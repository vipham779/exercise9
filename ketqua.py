'''
This is the script that checks whether a person wins at gambling.
He wins if the slots he takes a gamble on are exactly the last 2 digits
of any prize of the lottery result released on the day he gambles.
Otherwise, he loses.
'''
import bs4
import requests
import sys


def lottery_result():
    resp = requests.get('http://ketqua.net')
    tree = bs4. BeautifulSoup(resp.text, features='html.parser')
    rs = tree.find_all('td', attrs={'id': ['rs_0_0', 'rs_1_0', 'rs_2_0',
                                           'rs_3_0', 'rs_3_1', 'rs_3_2',
                                           'rs_3_3', 'rs_3_4', 'rs_3_5',
                                           'rs_4_0', 'rs_4_1', 'rs_4_2',
                                           'rs_4_3', 'rs_5_0', 'rs_5_1',
                                           'rs_5_1', 'rs_5_2', 'rs_5_3',
                                           'rs_5_4', 'rs_5_5', 'rs_6_0',
                                           'rs_6_1', 'rs_6_2', 'rs_7_0',
                                           'rs_7_1', 'rs_7_2', 'rs_7_3']})
    prizes = [{'Special prize': [int(rs[0].text)]},
              {'1st prize': [int(rs[1].text)]},
              {'2nd prize': [int(rs[2].text)]},
              {'3rd prize': [int(rs[i].text) for i in range(3, 9)]},
              {'4th prize': [int(rs[i].text) for i in range(9, 13)]},
              {'5th prize': [int(rs[i].text) for i in range(13, 19)]},
              {'6th prize': [int(rs[i].text) for i in range(19, 22)]},
              {'7th prize': [int(rs[i].text) for i in range(22, 26)]}]
    return prizes


def verify_slots(input_data):
    prizes = lottery_result()
    values = []
    temp = []
    result = []
    for prize in prizes:
        for _, i in prize.items():
            values.extend(i)
    for i in input_data:
        for num in values:
            if int(str(num)[-2:]) == int(i):
                temp = 'Win'
            else:
                temp = 'Lose'
        if temp == "Win":
            result.append(result)
        else:
            result.append(result)
    return result


def main():
    if len(sys.argv) < 2:
        print(lottery_result())
        print('To know if you are luckly enough,\
               please input an INTEGER with the format:\
               python(3) ketqua.py [Integer1] [Integer2]...')
        sys.exit()
    else:
        input_data = sys.argv[1:]
        print(verify_slots(input_data))


if __name__ == '__main__':
    main()
