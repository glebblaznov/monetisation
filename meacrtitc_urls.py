import time

from bs4 import BeautifulSoup
import logging
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import pandas as pd
from selenium import webdriver

title=[]
appid=[]
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
                    {'title': title, 'appid': appid})
                df.to_csv(r'C:\Users\Admin\Desktop\steamdb1.csv', header=True)
                print('Results saved')
                return simple_get(url)

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        df = pd.DataFrame(
                {'title': title, 'appid': appid})
        df.to_csv(r'C:\Users\Admin\Desktop\steamdb.csv', header=True)
        print('Results saved')
        return simple_get(url)


#raw_html = simple_get("https://steamdb.info/search/?a=app&q=Tom+Clancy%27s+Ghost+Recon%3A+Wildlands")

#raw_html = simple_get("https://microtransaction.zone/Search/Advanced?q=&platforms=94&page=1")

#titles_df = pd.read_csv(r"C:\Users\Admin\Desktop\titles.csv")
#titles1 = titles_df['title'].values.tolist()
# driver = webdriver.Chrome(executable_path='C:/Users/Admin/Desktop/chromedriver_win32/chromedriver.exe')
# driver.get("https://www.igdb.com/games/"+str(titles1[0]))
driver = webdriver.Chrome(executable_path='C:/Users/Admin/Desktop/chromedriver_win32/chromedriver.exe')
names_check=pd.read_excel("C:/Users/Admin/Desktop/ratings_to_find.xls")
title=names_check['Name']
name_web=[]
title_save=[]
links=[]
#print(title)
for i in range(0,100):
    title_save.append(str(title[i]))
    driver.get("https://www.metacritic.com/search/game/"+str(title[i])+"/results?search_type=advanced&plats[3]=1")
    #driver.get("https://www.metacritic.com/search/game/100%%20Orange%20Juice/results?search_type=advanced&plats[3]=1")
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser') # Преобразование HTML кода в объект BeautifulSoup
#print(html)
    if str(soup).find("No search results found")!=-1:
        name_web.append('not_found')
        links.append('not_found')
        print(str(i))
    if str(soup).find("div class=\"error-code\"")!=-1:
        name_web.append('error')
        links.append('error')
        print(str(i))
    if str(soup).find("Bad Request")!=-1:
        name_web.append('error')
        links.append('error')
        print(str(i))
    if str(soup).find("Page Not Found") != -1:
        name_web.append('not_found')
        links.append('not_found')
        print(str(i))
    for li in soup.findAll('li',attrs={'class':"result first_result"}):
        for a in li.findAll('a'):
            link=str(a)
            link=link[link.find("href")+6:link.find("\">")]
            #print(link)
            name=a.text
            name=str(name)
            name=name.replace("\n",'')
            name=name.strip()
            name_web.append(name)
            links.append(link)
print(title)
print(name_web)
print(links)
print(len(title_save))
print(len(name_web))
print(len(links))

df = pd.DataFrame({'title_r': title_save,'title_meta':name_web, 'link': links})
df.to_csv(r'C:\Users\Admin\Desktop\meta_pre_info100.csv', header=True)