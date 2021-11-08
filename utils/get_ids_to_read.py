import pandas as pd

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


def get_last_id_for_score():
    return


def get_last_id_for_data():
    df_ = read_tags()
    last_id = '0'
    ids = df_[df_['id'] > last_id]['id'].values
    return ids


