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
                    {'Name': title_save,'Name_game_stats':name_web_save, 'revenue_est': revenues,'publishers':publishers,'developers':developers})
                df.to_csv(r'C:\Users\Admin\Desktop\game_stats350.csv', header=True)
                print('Results saved')
                return simple_get(url)

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        df = pd.DataFrame(
                {'Name': title_save,'Name_game_stats':name_web_save, 'revenue_est': revenues,'publishers':publishers,'developers':developers})
        df.to_csv(r'C:\Users\Admin\Desktop\game_stats350.csv', header=True)
        print('Results saved')
        return simple_get(url)




#raw_html = simple_get("https://microtransaction.zone/Search/Advanced?q=&platforms=94&page=1")

#titles_df = pd.read_csv(r"C:\Users\Admin\Desktop\titles.csv")
#titles1 = titles_df['title'].values.tolist()
# driver = webdriver.Chrome(executable_path='C:/Users/Admin/Desktop/chromedriver_win32/chromedriver.exe')
# driver.get("https://www.igdb.com/games/"+str(titles1[0]))
driver = webdriver.Chrome(executable_path='C:/Users/Admin/Desktop/chromedriver_win32/chromedriver.exe')
names_check=pd.read_excel("C:/Users/Admin/Desktop/to_find_revenue.xls")
title=names_check['Name']
name_web=names_check['Name_game_stats']
title_save=[]
name_web_save=[]
revenues=[]
publishers=[]
developers=[]
#print(title)
for i in range(350,len(name_web)):

    #raw_html = simple_get("https://games-stats.com/steam/game/" + str(name_web[i]))
    driver.get("https://games-stats.com/steam/game/"+str(name_web[i]))
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser') # Преобразование HTML кода в объект BeautifulSoup
#print(html)
    title_save.append(str(title[i]))
    name_web_save.append(str(name_web[i]))
    if str(html).find("Page Not Found")!=-1:
        print("Incorrect name " +str(i)+" "+str(title[i]))
        revenues.append('try_again')
        publishers.append('try_again')
        developers.append('try_again')

    for div in soup.findAll('div',attrs={'class':'col-lg-5'}):
        s=str(div)
        s=s[s.find('Revenue Estimate'):len(s)]
        s=s[s.find(':')+4:s.find('</p>')]
        print(s)


        if s.find('million')!=-1:
            s=s[0:s.find('million')]
            s=s.strip()
            s = float(s)
            s=s*1000000


        revenues.append(s)
        a=str(div)
        a=a[a.find('Publisher'):len(a)]
        a=a[a.find('text-info')+11:a.find('</a>')]
        a=a[a.find('>')+1:len(a)]
        print(a)
        publishers.append(a)
        s=str(div)
        s=s[s.find('Developer'):len(s)]
        s=s[s.find('class=\"text-info\"')+17:s.find('</a>')]
        s=s[s.find('>')+1:len(s)]
        print(s)
        developers.append(s)
        #print(name1)
print(title_save)
print(name_web_save)
print(len(title_save))
print(len(name_web_save))
print(len(revenues))
print(len(publishers))
print(len(developers))
df = pd.DataFrame({'Name': title_save,'Name_game_stats':name_web_save, 'revenue_est': revenues,'publishers':publishers,'developers':developers})
df.to_csv(r'C:\Users\Admin\Desktop\game_stats_end.csv', header=True)