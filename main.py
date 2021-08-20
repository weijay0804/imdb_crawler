import os
from dotenv import load_dotenv

# ---- 自訂函式 -----
from imdb import get_movies_rank_datas, get_movie_data
from process_imdb import get_ch_movie_type, get_ch_movie_description
from file_function import save_file


load_dotenv()

def main():
    api_key = os.environ.get('TMDB_KEY')
    rank_datas = get_movies_rank_datas('https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm')
    movies_datas = get_movie_data(rank_datas)
    movies_datas = get_ch_movie_type(movies_datas)
    movies_datas = get_ch_movie_description(movies_datas, api_key=api_key, sleep_time=1)
    print('*******************')
    save_file('movies_datas/hot_movie_ch2.json', movies_datas)

if __name__ == '__main__':
    main()

