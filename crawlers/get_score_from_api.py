import json
import time
from torrequest import TorRequest
from utils import get_last_id_for_data

def get_last_id():
    return 603110


def get_score_from_api():
    
    idx = 0
    tor = TorRequest(password='didvk')
    
    ids = get_last_id_for_data()
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
