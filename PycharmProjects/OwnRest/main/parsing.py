import requests
from bs4 import BeautifulSoup

data_list = []


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1'
    }
    response = requests.get(url, headers=headers)
    return response.text


def parsing_istore(html):
    soup = BeautifulSoup(html, 'lxml')
    apple = soup.find('div', class_="sh_newsgl sh_newsgl2").find_all('div', class_="news_vip3")
    for apples in apple:
        try:
            title = apples.find('a').text.strip()
        except:
            title = ''

        try:
            link = 'https://m.footballhd.ru/'+apples.find('a').get('href')
        except Exception as e:
            print(e)

        # try:
        #     price = apples.find('p', class_="card-price-usd my-1").text.strip()
        # except:
        #     price = ''

        data = {'title': title, 'link': link}
        # print(data)
        data_list.append(data)


    return data_list


def parsing():
    url = 'https://m.footballhd.ru/'
    # data_list.clear()
    return parsing_istore(get_html(url))

parsing()