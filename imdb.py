'''

    從 imdb 爬取電影資料

'''


from bs4 import BeautifulSoup
from typing import List, Dict
from time import time
import json
import datetime
import requests



def from_url_get_datas(url : str) -> BeautifulSoup:
    '''根據 url 獲得 html 資料'''

    response = requests.get(url)

    if response.status_code != 200:
        print(f'連線失敗 status code: {response.status_code}')

        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup
        
def get_movies_rank_datas(url : str, limlit : int = None) -> List[Dict[str , str]]:
    '''取得imdb電影排名的資料'''
    movies_list = []

    soup = from_url_get_datas(url)
    contents = soup.find_all('td', class_ = 'titleColumn', limit=limlit)

    for content in contents:
        content_post = content.find_previous_sibling('td', class_ = 'posterColumn')

        meta_dict = {
            'movie_id' : content.find('a').get('href').split('/')[2],
            'title' : content.find('a').string
        }

        movies_list.append(meta_dict)

    return movies_list


def get_movie_data(movies_list : List[Dict[str, str]]) -> List[Dict[str, str]]:
    '''由特定的電影連結爬取電影的詳細資料'''
    result = []

    for datas in movies_list:

        url = f"https://www.imdb.com/title/{datas['movie_id']}"

        soup = from_url_get_datas(url)

        image = soup.find('div', class_ = 'ipc-media__img').find('img').get('src')

        movie_rate = soup.find('span',class_='iTLWoV') # 電影評分
            
        # 檢查有沒有電影評分，沒有就為 None
        if movie_rate is None:
            movie_rate = None
        else:
            movie_rate = movie_rate.string


        tables = soup.find('div', class_ = 'hWHMKr') # 包含電影年分 分級 時間的資料

        OG_title = tables.find('div', class_ = 'OriginalTitle__OriginalTitleText-jz9bzr-0 llYePj') # 原始電影名稱

        # 查看有沒有電影原始名稱，沒有就為 None
        if OG_title is None:
            OG_title = None
        else:
            OG_title = OG_title.string.split(':')[1].lstrip()


        movie_year_grade_datas = tables.find_all('a', class_ = 'rgaOW') # 找到電影年分 分級
        movie_year_and_grad_and_time = [i.string for i in movie_year_grade_datas] # 使用 list 儲存

        # 找電影時間，如果沒有就為 None 並加到電影年分 list
        try:
            movie_time = tables.find_all('li', class_ = 'ipc-inline-list__item')[2].string
        except:
            movie_time = None
        finally:
            movie_year_and_grad_and_time.append(movie_time)

        #   判斷電影頁面有沒有影片
        if soup.find('div', class_ = 'Hero__MediaContainer__Video-kvkd64-3 FKYGY') is not None:

            movie_datas = soup.find('div', class_ = 'Hero__MetaContainer__Video-kvkd64-4 kNqsIK') # 電影的種類、導演、演員等資料
        else:
            movie_datas = soup.find('div', class_ = 'Hero__MetaContainer__NoVideo-kvkd64-8 TqBgz' )# 電影的種類、導演、演員等資料


        movie_type = movie_datas.find_all('a', class_ = 'GenresAndPlot__GenreChip-cum89p-3 fzmeux ipc-chip ipc-chip--on-baseAlt') # 電影類別
        movie_type = [i.string for i in movie_type]

        movie_description = movie_datas.find('span', class_ = 'gCtawA').string # 電影描述

        movie_persons = movie_datas.find_all('li', class_ = 'ipc-metadata-list__item') # 電影導演、編劇、演員

        director = movie_persons[0].find_all('a', class_ = 'ipc-metadata-list-item__list-content-item--link') # 導演
        director = [i.string for i in director]

        writers = movie_persons[1].find_all('a', class_ = 'ipc-metadata-list-item__list-content-item--link') # 編劇
        writers = [i.string for i in writers]

        start = movie_persons[2].find_all('a', class_ = 'ipc-metadata-list-item__list-content-item--link') # 演員
        start = [i.string for i in start]

        movie_datas_dict = {
            'movie_id' : datas['movie_id'],
            'movie_title' :datas['title'],
            'movies_OG_title' : OG_title,
            'movie_rate' : movie_rate,
            'movie_year_grade_time' : movie_year_and_grad_and_time,
            'movie_type' : movie_type,
            'movie_description' : movie_description,
            'director' : director,
            'writers' : writers,
            'start' : start,
            'movie_img' : image,
            'time' : str(datetime.date.today().isoformat())
        }
        
        print(movie_datas_dict)
        result.append(movie_datas_dict)
        print('--------------------\n')
        
    return result