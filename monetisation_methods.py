from bs4 import BeautifulSoup
import logging
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import pandas as pd
from selenium import webdriver


def is_good_response(resp):  # Функция возвращает True, если ответ HTML; в другом случае False
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):  # Лог ошибок
    print(e)


def simple_get(url):  # Функция для извлечения HTML кода, заданной web-страницы
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                df = pd.DataFrame(
                    {'title': title, 'monetisation': money})
                df.to_csv(r'C:\Users\Admin\Desktop\info4.csv', header=True)
                print('Results saved')
                return simple_get(url)

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        df = pd.DataFrame(
                {'title': title, 'monetisation': money})
        df.to_csv(r'C:\Users\Admin\Desktop\info14.csv', header=True)
        print('Results saved')
        return simple_get(url)


# raw_html = simple_get("https://www.metacritic.com/browse/games/score/metascore/all/all/filtered")
title=[]
money=[]
#raw_html = simple_get("https://microtransaction.zone/Search/Advanced?q=&platforms=94&page=1")
#print(raw_html)
#titles_df = pd.read_csv(r"C:\Users\Admin\Desktop\titles.csv")
#titles1 = titles_df['title'].values.tolist()
# driver = webdriver.Chrome(executable_path='C:/Users/Admin/Desktop/chromedriver_win32/chromedriver.exe')
# driver.get("https://www.igdb.com/games/"+str(titles1[0]))
driver = webdriver.Chrome(executable_path='C:/Users/Admin/Desktop/chromedriver_win32/chromedriver.exe')

for i in range (1,97):

    driver.get("https://microtransaction.zone/Search/Advanced?q=&platforms=94&page="+str(i))
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser') # Преобразование HTML кода в объект BeautifulSoup
    dates = ''
    devel = ''
    publ = ''
    sup_dev = ''
    for a in soup.findAll('a', attrs={'class': 'list-game-name indigo'}):
        name = a.text
        title.append(name)
        #print(name)

    for div in soup.findAll('div', attrs={'class': 'flag-row flex-md-row justify-content-around'}):  # Извелечение наименований продуктов; в данном случае,
        # они заключены в метки div, у которых class=name
        #print(str(div)+"\n")
        #print(str(div)[602:615])
        q=[i for i in range(len(str(div))) if str(div).startswith("class=\"flag-img\"",i)]
        items = []
        for j in q:
            #print(j)

            s=str(div)[int(j):len(str(div))]
            itm=s[s.find("Images/"):s.find(".svg")]
            itm=itm[7:len(itm)]
            items.append(itm)
        money.append(items)

    if i==96:
        print(title)
        print(money)
        df = pd.DataFrame({'title': title, 'monetisation': money})
        df.to_csv(r'C:\Users\Admin\Desktop\infofinal.csv', header=True)