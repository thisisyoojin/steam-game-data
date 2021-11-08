#%%
import numpy as np
import pandas as pd


class Preprocessor:
    
    def __init__(self):
        self.norm_params = {}
        self.one_hot_params = {}
        self.fe_params = {}
        self.me_params = {}
        self.features = []
        

    def normalise_data(self, X, col):

        params = self.norm_params.get(col)

        if params is None:
            self.norm_params[col] = {
                "mean": np.mean(X[col]),
                "std": np.std(X[col])
            }

        X.loc[:, col] = X[col].apply(lambda x: (x - self.norm_params[col]['mean']) / self.norm_params[col]['std']) 
        


    def frequency_encoding(self, X, col):
        
        params = self.fe_params.get(col)
        
        if params is None:
            self.fe_params[col] = X.groupby(col).size() / len(X)
        
        X.loc[:, f"{col}_freq_enc"] = X[col].map(self.fe_params[col])
        X[f"{col}_freq_enc"].fillna(0, inplace=True)
        self.normalise_data(X, f'{col}_freq_enc')
        self.features.append(f'{col}_freq_enc')

        return X


    def mean_encoding(self, X, y, col):
        
        params = self.me_params.get(col)

        if params is None:
            df = pd.concat([X, y], axis=1)
            self.me_params[col] = df.groupby(col)['Target'].mean()
        
        X.loc[:, f"{col}_mean_enc"] = X[col].map(self.me_params[col])
        X[f'{col}_mean_enc'].fillna(0, inplace=True)
        self.normalise_data(X, f'{col}_mean_enc')
        self.features.append(f'{col}_mean_enc')
        
        return X


    def preprocess(self, X):
        
        self.normalise_data(X, 'required_age')
        self.normalise_data(X, 'dlc_cnt')
        self.normalise_data(X, 'package_cnt')
        self.normalise_data(X, 'year')
        self.normalise_data(X, 'month')
        self.normalise_data(X, 'day')
        self.normalise_data(X, 'price_norm')
        self.normalise_data(X, 'minimum_processor')
        
        # X = self.frequency_encoding(X, 'Developer')
        # X = self.frequency_encoding(X, 'Publisher')
        # X = self.mean_encoding(X, y, 'Developer')
        # X = self.mean_encoding(X, y, 'Publisher')

        return X


    def fit(self, X_train):
        """
        Training dataset
        """
        return self.preprocess(X_train)
        

    def transform(self, X_test):
        """
        validation set, test set
        """
        #self.features = []
        return self.preprocess(X_test)


