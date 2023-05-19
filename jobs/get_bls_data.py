import sys
import pandas as pd
import requests
from awsglue.utils import getResolvedOptions

def get_data(url : str) -> list:
    
    headers = {"User-Agent":"Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)

    data = response.text.split('\n')
    
    return data


def parse_data(url : str, csv : bool = False, columns_headers : bool = True, columns : list =[], contains_comma : bool = False ) -> pd.DataFrame:

    data = get_data(url)
    
    if columns_headers:
        columns = data[0]
        data = data[1:]
        if csv:
            if contains_comma:
                columns = columns.split('",')
                columns = [i.replace('\r','').replace('"','') for i in columns]
            else:
                columns = columns.split(',')
                columns = [i.replace('\r','').replace('"','') for i in columns]
        else:
            columns = columns.split('\t')
            columns = [i.replace('\r','') for i in columns]
    
    
    if csv:
        if contains_comma:
            data = [i.replace('\r','').replace('",','|').replace('"', '').split('|') for i in data]
        else:
            data = [i.replace('\r','').replace('"','').split(',') for i in data]
    else:
        
        data = [i.replace('\r','').split('\t') for i in data]
    
    df = pd.DataFrame(data)
    df = df.replace('', None)
    df = df.dropna(how='all', axis=1)
    df.columns = columns
    df = df.dropna(how='all', axis=0)
    
    return df



args = getResolvedOptions(sys.argv, ['JOB_NAME',
                                     'url',
                                     'targetBucket'])


df = parse_data(args['url'])

df.to_parquet(args['targetBucket'])