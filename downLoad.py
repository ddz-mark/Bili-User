import requests
from bs4 import BeautifulSoup

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}


def load():
    names = []
    texts = []
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml', from_encoding='UTF-8')
        # first item
        names.append(soup.find('div', class_='col1').div.h2.string)
        texts.append(soup.find('div', class_='content').get_text())
        for link in soup.find_all('div', class_='article block untagged mb15 typs_hot'):
            names.append(link.find('div', class_='author clearfix').h2.string)
            texts.append(link.find('div', class_='content').get_text())
        i = 0
        for name in names:
            print(name, texts[i])
            i += 1
    except requests.HTTPError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)


if __name__ == '__main__':
    load()
