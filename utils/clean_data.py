
import pandas as pd
import os
import re
import datetime
import json
from utils import read_config

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
    Function to translate localised languages to English.
    e.g. converting 한국어 to Korean.
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



"""
Functions to get dataframes from raw text data.
"""
def clean_df(fpath):
    """
    Get clean the data and return the data
    """
    language_map, currency_map = read_config('./steam/utils/meta_clean.yaml', ['languages', 'currency'])
    
    with open('./steam/data/features.txt', 'r') as f:
        result = [json.loads(line) for line in f.readlines()]

    df = pd.DataFrame(result)
    
    df['price_norm'] = df['currency'].map(currency_map)*df['price']/100
    df['minimum_processor'] = df['pc_minimum'].apply(get_minimum_processor)
    df['release_date'] = df['release_date'].apply(convert_to_datetime)
    df['language_cleaned'] = df['supported languages'].apply(lambda x: norm_to_English(remove_special_char(x), language_map))
    
    return df