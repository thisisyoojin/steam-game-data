import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datasets.preprocess import get_cleaned_df, Preprocessor

def feature_select_with_elimination(X_train, y_train, estimator, max_num):
    
    selector = RFE(estimator, n_features_to_select=max_num, step=1)
    selector = selector.fit(X_train, y_train)
    sort_orders = sorted(zip(X_train.columns, selector.ranking_), key=lambda x: x[1], reverse=False)[:max_num]

    return [s[0] for s in sort_orders]


def create_data():
    
    df = get_cleaned_df('./steam/data/cleaned_df.csv')
    y = df['metacritic_score']
    df.drop(columns=['id', 'metacritic_score'], inplace=True)
    
    X_train, X_test, y_train, y_test = train_test_split(df, y, train_size=0.9, random_state=31)
    
    #pc = Preprocessor()
    #X_transformed = pc.fit(X_train)
    #possible_features = feature_select_with_elimination(X_transformed, y_train, RandomForestRegressor(), 50)

    train_data = pd.concat([X_train, y_train], axis=1)
    test_data = pd.concat([X_test, y_test], axis=1)
    train_data.to_csv('./steam/data/train_data.csv', index=False)
    test_data.to_csv('./steam/data/test_data.csv', index=False)
    
    return
