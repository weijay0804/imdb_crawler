'''

    處理從 imdb 爬取的資料模組

'''


from typing import Dict, List
import json
import requests
import time
import os



def open_file(file_name : str):
    '''打開 json 格式的檔案'''

    try:
        if not os.path.exists(file_name):
            raise Exception('檔案不存在，或檔案名稱錯誤')

        if not file_name.endswith('.json'):
            raise Exception('檔案格式錯誤，必須為 .json')

        with open(file_name, encoding='utf-8') as f:
            datas = json.load(f)

    except Exception as e:
        print(f'錯誤! {e}')
        return None

    return datas


def save_file(file_name : str, datas : Dict) -> json:
    '''儲存檔案，格式為 json'''

    try:
        if os.path.exists(file_name):
            raise Exception('檔案名稱已存在')

        if not file_name.endswith('.json'):
            raise Exception('檔案格式錯誤，必須為 .json')

        with open(file_name, 'w', encoding='utf-8') as f:
            datas = json.dumps(datas, indent=5)
            f.write(datas)

    except Exception as e:
        print(f'錯誤! {e}')
        return ''
    
    print('Done !')
    return None


def from_tmdb_get_movies(imdb_id : str, api_key : str) -> json:
    '''從 Tmdb Api 根據 imdb 電影 id 取得電影資料'''

    imdb_id = imdb_id
    url = f'https://api.themoviedb.org/3/find/{imdb_id}?api_key={api_key}&language=zh-TW&external_source=imdb_id'
    response = requests.get(url)

    if response.status_code != 200:
        return f'連線失敗  status code: {response.status_code}'

    datas = json.loads(response.text)

    return datas

def get_ch_movie_description(movie_datas : List[Dict[str, str]], sleep_time : float = 0.5) -> List[Dict[str, str]]:
    '''用 Tmdb Api 取得中文的電影描述，並更新到原本的電影資料'''
    
    result = []

    for movie in movie_datas:
        imdb_id = movie['movie_id']
        ch_movie_datas = from_tmdb_get_movies(imdb_id)

        if movie['movie_description'] is None or ch_movie_datas['movie_results'][0]['overview'] == '':
            movie['movie_description'] = None
        else:
            movie['movie_description'] = ch_movie_datas['movie_results'][0]['overview']
        
        result.append(movie)

        print(movie)
        print('-------------------\n')

        time.sleep(sleep_time)

def get_ch_movie_type(movie_datas : List[Dict[str, str]]) -> List[Dict[str, str]]:
    '''把電影類別的資料從英文改成中文'''

    type_dict = {
    'Drama': '戲劇', 'Biography': '傳記', 'Western': '西部', 
    'Thriller': '驚悚', 'History': '歷史', 'War': '戰爭', 
    'Film-Noir': '黑色電影', 'Sci-Fi': '科幻', 'Adventure': '冒險', 
    'Fantasy': '科幻', 'Mystery': '神秘', 'Sport': '運動', 'Romance': '浪漫', 
    'Family': '家庭', 'Music': '音樂', 'Crime': '犯罪', 'Action': '動作', 
    'Horror': '恐怖', 'Musical': '舞臺劇', 'Comedy': '喜劇', 'Animation': '動畫'
    }

    result = [] # 儲存結果

    for movie in movie_datas:
        store_types = []  # 暫時存放 type 的地方

        if movie['movie_type'] is None:
            continue

        # 依序取出電影 type
        for movie_type in movie['movie_type']:
            ch_type = type_dict[movie_type]

            store_types.append(ch_type)

        movie['movie_type'] = store_types

        result.append(movie)

    return result

