import pandas as pd
import os
from sklearn.model_selection import train_test_split
from preprocess import create_data, Preprocessor


def prepare_dataset(kind='cv'):
    """
    Get dataset
    """
    train_fpath = './steam/data/train_data.csv'
    test_fpath = './steam/data/train_data.csv'

    if not os.path.isfile(train_fpath):
        create_data()

    train_data = pd.read_csv(train_fpath)
    test_data = pd.read_csv(test_fpath)
    pc = Preprocessor()
    
    X_train, y_train = train_data.drop(columns=['metacritic_score']), train_data['metacritic_score']
    X_test, y_test = test_data.drop(columns=['metacritic_score']), test_data['metacritic_score']

    if kind == 'cv':
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, random_state=33, train_size=0.9)
        X_train = pc.fit(X_train)
        X_val = pc.transform(X_val)
        return X_train, X_val, y_train, y_val

    else:
        X_train = pc.fit(X_train)
        X_test = pc.transform(X_test)
        return X_train, X_test, y_train, y_test

