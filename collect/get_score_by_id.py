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
    return 603110


def get_review_api():
    
    idx = 0
    tor = TorRequest(password='didvk')
    df_ = read_tags()
    last_id = get_last_id()
    ids = df_[df_['id'] > last_id]['id'].values
    print(f"Started scraping from {ids[0]}:{len(ids)} left")

    for app_id in ids:
        
        idx += 1
        
        response = tor.get(f"https://store.steampowered.com/appreviews/{app_id}?json=1")
        json_data = response.json()
        time.sleep(5)
        
        
        if json_data is None:
            print(f"ID {app_id} doesn't have a response data.")
            continue

        if json_data['success'] != 1:
            print(f"ID {app_id} wasn't successful.")
            continue

        response_data = json_data['query_summary']

        data = {
            "id": int(app_id),
            "score": int(response_data['review_score']),
            "score_desc": response_data["review_score_desc"],
            "positive": int(response_data["total_positive"]),
            "negative": int(response_data["total_negative"]),
        }

        with open('./steam/data/scores.txt', 'a') as f:
            f.write(f"{json.dumps(data)}\n")
        time.sleep(3)

        
    if idx % 50 == 0:
        tor.reset_identity()
        idx = 0


get_review_api()