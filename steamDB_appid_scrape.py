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
names_check=pd.read_csv("C:/Users/Admin/Desktop/names_check.csv")
title=names_check['Name']
name_web=[]
title_save=[]
#print(title)
for i in range(160,320):
    time.sleep(2)
    title_save.append(str(title[i]))
    driver.get("https://steamdb.info/search/?a=app&q="+str(title[i])+"&type=1&category=0")
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser') # Преобразование HTML кода в объект BeautifulSoup
#print(html)
    if str(html).find("try again in a minute")!=-1:
        print("too many requests at: " +str(i)+" "+str(title[i]))
        time.sleep(75)
        driver.get("https://steamdb.info/search/?a=app&q=" + str(title[i]))
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    if str(html).find("tbody")==-1:
        appid.append('')
        name_web.append('')
    for tbody in soup.findAll('tbody'):
        s=str(tbody)[str(tbody).find("<tr"):str(tbody).find("Game")]
        s=s[s.find("Game")-80:s.find("Game")]
        #print(s)
        id_page=s[s.find("data-appid")+12:s.find("\">")]
        appid.append(id_page)
        name1=str(tbody)[str(tbody).find("Game")+9:str(tbody)[str(tbody).find("Game")+9:str(tbody).find("Game")+100].find("</td>")]
        #print(name1)
        if name1.find("svg")==-1:
            #print(name1)
            name1 = name1[name1.find("d>") + 4:name1.find("</td>")]
        else:
            name1=name1[name1.find("</a>")+4:name1.find("</td>")]
        #print(name1)
        name1=name1.replace("\n","")
        name_web.append(name1)
print(title)
print(appid)
print(name_web)
print(len(appid))
print(len(name_web))
df = pd.DataFrame({'title': title_save,'title_web':name_web, 'appid': appid})
df.to_csv(r'C:\Users\Admin\Desktop\320.csv', header=True)

