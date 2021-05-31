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
names_check=pd.read_excel("C:/Users/Admin/Desktop/for_igdb.xls")
title=names_check['Name']
name_web=names_check['Name_igdb']
title_save=[]
links=[]
#print(title)
user_scores_igdb=[]
crit_scores_igdb=[]
genres=[]
playmodes=[]
igdb_save=[]
series=[]
platforms=[]
release_dates=[]
for i in range(0,len(name_web)):
    title_save.append(str(title[i]))
    igdb_save.append(str(name_web[i]))
    driver.get("https://www.igdb.com/games/"+str(name_web[i]))
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

    for div in soup.findAll('div',attrs={'class':'gamepage-gauge'}):
        k=0
        for svg in div.findAll('svg'):
            k += 1
            sss=svg.text
            print(sss)
            if k==1:
                user_scores_igdb.append(str(sss))
            else:
                crit_scores_igdb.append(str(sss))

    for div in soup.findAll('div',attrs={'class':'optimisly-game-extrainfo1'}):
        genre_temp=[]
        playmodes_temp=[]
        for a in div.findAll('a',attrs={'itemprop':'genre'}):
            q=a.text
            genre_temp.append(str(q))
        for a1 in div.findAll('a',attrs={'itemprop':'playMode'}):
            qq=a1.text
            playmodes_temp.append(str(qq))
        if len(genre_temp)==0:
            genres.append('')
        else:
            qqq='|'.join(genre_temp)
            genres.append(qqq)
        if len(playmodes_temp)==0:
            playmodes.append('')
        else:
            qqq='|'.join(playmodes_temp)
            playmodes.append(qqq)
    for div in soup.findAll('div',attrs={'class':'optimisly-game-extrainfo2'}):
        if str(div).find('Series')!=-1:
            series_name=str(div)
            series_name=series_name[series_name.find('Series'):len(series_name)]
            series_name=series_name[series_name.find('rel=')+10:series_name.find('</a>')]
            series.append(series_name)
        else:
            series.append('no_series')
    for div in soup.findAll('div',attrs={'class':'optimisly-game-maininfo'}):
        platform_temp=[]
        rel_dates_temp=[]
        for div1 in div.findAll('div',attrs={'class':'hide'}):
            for h3 in div1.findAll('h3'):
                platform1=h3.text
                platform_temp.append(str(platform1))
            for time in div1.findAll('time'):
                rel_date=time.text
                rel_dates_temp.append(str(rel_date))
        if len(platform_temp)!=0:
            plat_string='|'.join(platform_temp)
            platforms.append(plat_string)
        else:
            platforms.append('no_platforms')
        if len(rel_dates_temp)!=0:
            rel_dates_string='|'.join(rel_dates_temp)
            release_dates.append(rel_dates_string)
        else:
            release_dates.append('no_dates')
    if str(soup).find('We couldn\'t find')!=-1:
        user_scores_igdb.append('try_again')
        crit_scores_igdb.append('try_again')
        genres.append('try_again')
        playmodes.append('try_again')
        series.append('try_again')
        platforms.append('try_again')
        release_dates.append('try_again')

print(title_save)
print(igdb_save)

print(len(title_save))
print(len(igdb_save))
print(len(genres))
print(len(playmodes))
print(len(series))
print(len(platforms))
print(len(release_dates))
print(len(user_scores_igdb))
print(len(crit_scores_igdb))
df = pd.DataFrame({'title_r': title_save,'title_igdb':igdb_save, 'user_score_igdb':user_scores_igdb,'crit_score_igdb':crit_scores_igdb,'genre': genres,'playmodes':playmodes,'series':series,'platform':platforms,'release_dates':release_dates})
df.to_csv(r'C:\Users\Admin\Desktop\igdb_infototal.csv', header=True)