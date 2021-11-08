import requests
import json
import time
from PIL import Image
import pandas as pd
from torrequest import TorRequest


def read_tags():
    result = []
    with open('./steam/data/tags.txt') as f:
        for line in f.readlines():
            _id, _tag = line.replace('\n', '').split(',')
            result.append({
                "id": int(_id),
                "tag": _tag
            })

    df = pd.DataFrame(result).sort_values('id')
    df['tags'] = df['tag'].apply(lambda x: len(x.split('|')))
    df_ = df[df['tags'] > 8]
    return df_


def get_last_id():
    return 1535900


def get_api_data():
    
    idx = 0
    tor = TorRequest(password='didvk')
    df_ = read_tags()
    last_id = get_last_id()
    ids = df_[df_['id'] > last_id]['id'].values
    # print(ids[-1]): 1777670
    print(ids[0])

    for app_id in ids:
        
        idx += 1
        
        response = tor.get(f"https://store.steampowered.com/api/appdetails?appids={app_id}")
        json_data = response.json()
        time.sleep(5)
        
        
        if json_data is None:
            print(f"ID {app_id} doesn't have a response data.")
            continue

        if not json_data[f'{app_id}']['success']:
            print(f"ID {app_id} wasn't successful.")
            continue

        response_data = json_data[f'{app_id}']['data']

        get_data_by_key = lambda key, data: data[key] if (key in data.keys()) else None
        get_cnt = lambda data: 0 if data is None else len(data)

        if get_data_by_key('metacritic', response_data) is None:
            print(f"ID {app_id} doesn't have a metacritic score")
            continue
        
        if (response_data['type'] != 'game') or (response_data['steam_appid'] != app_id):
            print(f"ID {app_id} is not a game or id doesn't match.")
            continue

        data = {
            "id": int(app_id),
            "name": get_data_by_key('name', response_data),
            "metacritic_score": get_data_by_key('score', get_data_by_key('metacritic', response_data)),
            "required_age": get_data_by_key('required_age', response_data),
            "description": get_data_by_key('about_the_game', response_data),
            "supported languages": get_data_by_key('supported_languages', response_data),
            "pc_minimum": get_data_by_key('pc_requirements', response_data) if type(get_data_by_key('pc_requirements', response_data)) == list else get_data_by_key('minimum', get_data_by_key('pc_requirements', response_data)),
            "developers": get_data_by_key('developers', response_data),
            "publishers": get_data_by_key('publishers', response_data),
            "price": 0 if get_data_by_key('price_overview', response_data) is None else get_data_by_key('final', get_data_by_key('price_overview', response_data)),
            "currency": '' if get_data_by_key('price_overview', response_data) is None else get_data_by_key('currency', get_data_by_key('price_overview', response_data)),
            "dlc_cnt": get_cnt(get_data_by_key('dlc', response_data)),
            "package_cnt": get_cnt(get_data_by_key('packages', response_data)),
            "achievements": 0 if get_data_by_key('achievements', response_data) is None else int(get_data_by_key('total', get_data_by_key('achievements', response_data))),
            "release_date": get_data_by_key('date', get_data_by_key('release_date', response_data))
        }

        with open('./steam/data/features.txt', 'a') as f:
            f.write(f"{json.dumps(data)}\n")
        time.sleep(3)

        
        screenshots = get_data_by_key('screenshots', response_data)
        
        if screenshots is not None:
            for idx, screenshot in enumerate(screenshots[:6]):
                fpath = f"./steam/data/imgs/{app_id}_{idx}.jpg"
                img_file = requests.get(screenshots[idx]['path_thumbnail'])
                with open(fpath, 'wb+') as f:
                    f.write(img_file.content)
                time.sleep(3)
                
                img = Image.open(fpath)
                img = img.resize((round(img.size[0]/10), round(img.size[1]/10)), Image.ANTIALIAS)
                img.save(fpath)
        time.sleep(3)
    
    if idx % 50 == 0:
        tor.reset_identity()
        idx = 0


get_api_data()