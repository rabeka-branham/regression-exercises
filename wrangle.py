import os
from env import get_db_url
import pandas as pd
from sklearn.model_selection import train_test_split

def check_file_exists(filename, query, url):
    if os.path.exists(filename):
        df = pd.read_csv(filename, index_col=0)
        
    else:
        df = pd.read_sql(query,url)
        df.to_csv(filename)
        
    return df

def acquire_zillow():
    filename = 'zillow.csv'
    url = get_db_url('zillow')
    query = """
           select bedroomcnt, 
                bathroomcnt,
                calculatedfinishedsquarefeet,
                taxvaluedollarcnt,
                yearbuilt,
                taxamount, 
                fips 
            from properties_2017
            where propertylandusetypeid = 261
            """

    df = check_file_exists(filename,query,url)
    return df

def prep_zillow(df):
    df = df.dropna()
    df = df.rename(columns={'bedroomcnt': 'bed_count', 
                           'bathroomcnt' : 'bath_count',
                           'calculatedfinishedsquarefeet' : 'area',
                           'taxvaluedollarcnt': 'property_value',
                           'yearbuilt': 'year_built',
                           'taxamount': 'tax_amount',
                           'fips': 'county'})
    
    make_int = []
    for col in df.columns:
        has_non_zero_decimal = df[col].apply(lambda x: x % 1 != 0)
        if has_non_zero_decimal.sum() == 0:
            make_int.append(col)
        else:
            continue
        
    for col in make_int:
        df[col] = df[col].astype(int)
        
    df.county = df.county.map({6037:'Los Angeles',6059:'Orange',6111:'Ventura'})
    
    df = df.reset_index().drop(columns='index')
    
    return df

def split_data(dataframe):
    train, validate_test = train_test_split(dataframe, 
                                            train_size=.6, 
                                            random_state=913
                                           )
    validate, test = train_test_split(validate_test,
                                      test_size=0.50, 
                                      random_state=913
                                     )
    return train, validate, test

def wrangle_zillow():
    train, validate, test = split_data(prep_zillow(acquire_zillow()))
    
    return train, validate, test
    