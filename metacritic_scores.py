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
names_check=pd.read_excel("C:/Users/Admin/Desktop/meta_links.xls")
title=names_check['title_r']
name_web=names_check['title_meta']
title_save=[]
title_meta_save=[]
links=names_check['link']
#print(title)
user_ratings=[]
critic_ratings=[]
release_dates=[]
platforms=[]
links_save=[]
too_few_indic=[]
for i in range(250,len(links)):
    title_save.append(str(title[i]))
    title_meta_save.append(str(name_web[i]))
    links_save.append(str(links[i]))
    driver.get("https://www.metacritic.com/"+str(links[i]))
    #driver.get("https://www.metacritic.com/search/game/100%%20Orange%20Juice/results?search_type=advanced&plats[3]=1")
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser') # Преобразование HTML кода в объект BeautifulSoup
#print(html)
    if str(soup).find("No search results found")!=-1:
        user_ratings.append('error')
        critic_ratings.append('error')
        release_dates.append('error')
        platforms.append('error')
        print(str(i))
    if str(soup).find("div class=\"error-code\"")!=-1:
        user_ratings.append('error')
        critic_ratings.append('error')
        release_dates.append('error')
        platforms.append('error')
        print(str(i))
    if str(soup).find("Bad Request")!=-1:
        user_ratings.append('error')
        critic_ratings.append('error')
        release_dates.append('error')
        platforms.append('error')
        print(str(i))
    if str(soup).find("Page Not Found") != -1:
        user_ratings.append('error')
        critic_ratings.append('error')
        release_dates.append('error')
        platforms.append('error')
        print(str(i))
    for div in soup.findAll('div',attrs={'class':"metascore_w user large game positive"}):
        user_rating=div.text
        user_ratings.append(str(user_rating))
    for div in soup.findAll('div',attrs={'class':"metascore_w user large game mixed"}):
        user_rating=div.text
        user_ratings.append(str(user_rating))
    for div in soup.findAll('div',attrs={'class':"metascore_w user large game negative"}):
        user_rating=div.text
        user_ratings.append(str(user_rating))
    for div in soup.findAll('div',attrs={'class':"metascore_w user large game tbd"}):
        user_rating=div.text
        user_ratings.append(str(user_rating))
    if str(soup).find('metascore_w user large game')==-1:
        user_ratings.append('no_rating')
    else:
        user_ratings = user_ratings[0:len(user_ratings) - 1]

    for div in soup.findAll('div',attrs={'class':"metascore_w xlarge game positive"}):
        for span in div.findAll('span',attrs={'itemprop':'ratingValue'}):
            crit_rating=span.text
            critic_ratings.append(str(crit_rating))

    for div in soup.findAll('div',attrs={'class':"metascore_w xlarge game mixed"}):
        for span in div.findAll('span',attrs={'itemprop':'ratingValue'}):
            crit_rating=span.text
            critic_ratings.append(str(crit_rating))

    for div in soup.findAll('div',attrs={'class':"metascore_w xlarge game negative"}):
        for span in div.findAll('span',attrs={'itemprop':'ratingValue'}):
            crit_rating=span.text
            critic_ratings.append(str(crit_rating))
    if str(soup).find('data metascore connect4')!=-1:
        too_few_indic.append(1)
    else:
        too_few_indic.append(0)
    for div in soup.findAll('div',attrs={'class':"data metascore connect4"}):
        crit=str(div)
        if crit.find("grade score_tbd")!=-1:
            temp_rev=[]
            k=0
            if str(soup).find('unscored_reviews') != -1:
                critic_ratings.append('unscored_reviews')
            else:
                for ol in soup.findAll('ol',attrs={'class':'reviews critic_reviews'}):
                    k+=1
                    if k<=1:
                        for div1 in ol.findAll('div',attrs={'class':'review_grade'}):
                            temp_rev.append(int(div1.text))
                    else:
                        pass
                if len(temp_rev)!=0:
                    critic_ratings.append(sum(temp_rev)/len(temp_rev))
                #print(critic_ratings)
                else:
                    critic_ratings.append('no_crit_rev')
                #print("no_crit_rev")
    for li in soup.findAll('li',attrs={'class':'summary_detail release_data'}):
        for span in li.findAll('span',attrs={'class':'data'}):
            release_date=span.text
            release_dates.append(str(release_date))
    if str(soup).find('summary_detail product_platforms')==-1:
        platforms.append('PC_only')
    for li in soup.findAll('li',attrs={'class':'summary_detail product_platforms'}):
        for span in li.findAll('span',attrs={'class':'data'}):
            platform=span.text
            platform=str(platform)
            platform=platform.replace('\\n','')
            platform=platform.strip()
            platforms.append(platform)

    #print(user_ratings)
print(title)
print(name_web)
print(links)
print(len(title_save))
print(len(title_meta_save))
print(len(links_save))
print(len(user_ratings))
print(len(critic_ratings))
print(len(release_dates))
print(len(platforms))
print(user_ratings)
print(critic_ratings)

print(len(too_few_indic))
df = pd.DataFrame({'title_r': title_save,'title_meta':title_meta_save, 'link': links_save,'user_score':user_ratings,'crit_score':critic_ratings,'release_date':release_dates,'platforms':platforms,'crit_revs_low':too_few_indic})
df.to_csv(r'C:\Users\Admin\Desktop\meta_450.csv', header=True)