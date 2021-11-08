
import pandas as pd
import os
import re
import datetime
import json
from sklearn.decomposition import PCA
from utils import read_config

"""
< tag >
For tags to
"""
def hot_encoding_from_string(df, col, sep='|'):
    """
    The function to hot_encoding the tag with separator
    """
    ids = df['id']
    split_vals = df[col].apply(lambda row: [r.strip() for r in row.split(sep)])
    
    res = []
    for id, row_values in zip(ids.values, split_vals.values):
        each_data = {value: 1 for value in row_values}
        each_data['id'] = id
        res.append(each_data)
    
    hot_enc = pd.DataFrame(res).fillna(0).astype(int)
    
    df.set_index('id', inplace=True)
    hot_enc.set_index('id', inplace=True)
    joined_df = df.join(hot_enc, how='inner', on=['id'])
    joined_df.reset_index(inplace=True)
    
    return joined_df, hot_enc.columns


"""
<supported languages>
: Functions to clean supported languages texts

- remove_special_char:
- get_unique_value: get
- norm_to_English:
"""

def remove_special_char(row):
    """
    The function to remove special characters in supported language text 
    """
    row = row.replace('\r', ',').replace('\n', ',').replace(',,',',')
    row = re.sub('lt;|rt;|gt;|&amp|strong|/strong|br', '', row)
    row = re.sub('[<>&/*;]', '', row)
    row = re.sub('[[/a-zA-Z]*]', '', row)
    row = re.sub('\([a-zA-Z ]+\)', '', row)
    row = row.replace('languages with full audio support', '')
    return row


def get_unique_value(df):
    """
    Function to check unique language values to create a language map
    """
    result = set()
    for values in df['languages'].values:
        for v in values.split(','):
            if len(v.strip()) > 0:
                result.add(v.strip())
    return result


def norm_to_English(row, language_map):
    """
    Function to normalise 
    """
    result = [k for k, values in language_map.items() for v in values if v in row]
    return ','.join(result)



"""
< pc_minimum >

Extracting CPU clock speed from minimum requirements. 
e.g. \r\n\t\t\t<p><strong>Minimum:</strong> 1.2 GHz Processor (...) → 1.2 
"""

def get_minimum_processor(row):
    
    if row is None or len(row) == 0:
        return 0

    matches = re.findall('[0-9.\+]+[a-z ]*hz', row.lower())
    if len(matches) > 0:
        match = matches[0].replace(' ','').replace('+', '')
        num = re.findall('[0-9.]+', match)[0]
        
        if 'ghz' in match:
            return float(num)
        elif 'mhz' in match:
            return float(num)/10**3
        else:
            return 0



"""
- Release_date
"""
def convert_to_datetime(row):
    """
    Function to clean supported languages texts
    - convert_to_datetime: release date. Some cases it is registered as non-English language, which will be empty.
    """
    try:
        res = datetime.datetime.strptime(row, u'%d %b, %Y')
    except:
        res = ''
    finally:
        return res


def preprocess_release_date(df, col):
    
    df['year'] = pd.DatetimeIndex(df[col]).year.values.astype(int)
    df['year'] = df['year'].apply(lambda x: x if x > 0 else 0)
    df['year'] = df['year'] - df['year'].min()
    
    df['month'] = pd.DatetimeIndex(df[col]).month.values.astype(int)
    df['month'] = df['month'].apply(lambda x: x if x > 0 else 0)

    df['day'] = pd.DatetimeIndex(df[col]).day.values.astype(int)
    df['day'] = df['day'].apply(lambda x: x if x > 0 else 0)
    
    return df



"""
Functions to get dataframes from raw text data.
"""
def get_features_df(fpath):
    """
    Get clean the data and return the data
    """
    language_map, currency_map = read_config('./steam/utils/meta_clean.yaml', ['languages', 'currency'])
    
    with open('./steam/data/features.txt', 'r') as f:
        result = [json.loads(line) for line in f.readlines()]

    df = pd.DataFrame(result)
    cols = ['id', 'metacritic_score', 'required_age', 'dlc_cnt', 'package_cnt', 'achievements']
    
    df['price_norm'] = df['currency'].map(currency_map)*df['price']/100
    
    df['minimum_processor'] = df['pc_minimum'].apply(get_minimum_processor)
    

    df['release_date'] = df['release_date'].apply(convert_to_datetime)
    df = preprocess_release_date(df, 'release_date')
    cols.extend(['year', 'month', 'day'])

    df['language_cleaned'] = df['supported languages'].apply(lambda x: norm_to_English(remove_special_char(x), language_map))
    df, hot_enc_cols = hot_encoding_from_string(df, 'language_cleaned', sep=',')
    cols.extend(hot_enc_cols)

    cols.extend(['price_norm', 'minimum_processor'])
    
    df = df[cols].fillna(0)
    
    return df


def get_tags_df(fpath):
    """
    """
    result = []
    with open(fpath) as f:
        for line in f.readlines():
            _id, _tag = line.replace('\n', '').split(',')
            result.append({"id": int(_id), "tag": _tag})
    df = pd.DataFrame(result).sort_values('id')
    df, _ = hot_encoding_from_string(df, 'tag', sep='|')

    return df


def get_cleaned_df(fpath):
    """
    """
    if not os.path.isfile(fpath):
        data_df = get_features_df('./steam/data/features.txt')
        data_df.set_index('id', inplace=True)
        
        # Read tags data
        tags_df = get_tags_df('./steam/data/tags.txt')
        tags_df.drop(columns=['tag'], inplace=True)
        tags_df.set_index('id', inplace=True)

        merged_df = data_df.join(tags_df, how='inner', on=['id'])
        merged_df.to_csv(fpath)

    return pd.read_csv(fpath)
    
