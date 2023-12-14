import pandas as pd
import sklearn.preprocessing

def preprocess_and_scale_zillow(train,validate,test):
    encoded_dfs = []
    for df in [train,validate,test]:
        df_encoded_cols = pd.get_dummies(df.county).astype(int)
        df = pd.concat([df,df_encoded_cols],axis=1).drop(columns='county')
        encoded_dfs.append(df)    

    X_dfs = []
    for df in encoded_dfs:
        X_dfs.append(df.drop(columns='property_value'))
    
    scaled_dfs = []
    scaler = sklearn.preprocessing.MinMaxScaler()
    scaler = scaler.fit(X_dfs[0])
    for df in X_dfs:
        df = scaler.transform(df)
        scaled_dfs.append(df)
    
    for df in [train,validate,test]:
        scaled_dfs.append(df.property_value)
    
    dfs = []
    for df in scaled_dfs:
        dfs.append(pd.DataFrame(df))
        
    print(F'X_train: \t{dfs[0].shape}')
    print(F'y_train: \t{dfs[3].shape}')
    print()
    print(F'X_validate: \t{dfs[1].shape}')
    print(F'y_validate: \t{dfs[4].shape}')
    print()
    print(F'X_test: \t{dfs[2].shape}')
    print(F'y_test: \t{dfs[5].shape}')
          
    return dfs