'''

    處理文件儲存 開啟等函式庫

'''

import os
import json
from typing import Dict

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