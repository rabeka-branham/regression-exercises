import os
from env import get_db_url
import pandas as pd
from sklearn.model_selection import train_test_split

def check_file_exists(filename, query, url):
    if os.path.exists(filename):
        # print('File exists - reading CSV file')
        df = pd.read_csv(filename, index_col=0)
    else:
        # print('File does not exist - creating CSV file')
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
    from properties_2017 as p
    join propertylandusetype as l
        on p.propertylandusetypeid = l.propertylandusetypeid
    where propertylandusedesc in ('Single Family Residential')
    """

    df = check_file_exists(filename,query,url)
    
    return df

def prep_zillow(df):
    df = df.dropna()
    df = df.rename(columns={'bedroomcnt': 'bed_count', 
                   'bathroomcnt' : 'bath_count',
                   'calculatedfinishedsquarefeet' : 'sq_ft',
                   'taxvaluedollarcnt': 'property_value',
                   'yearbuilt': 'year_built',
                   'taxamount': 'tax_amount'})
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
    df = acquire_zillow()
    df = prep_zillow(df)
    train, validate, test = split_data(df)
    
    return train, validate, test
    