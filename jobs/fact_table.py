import sys
import pandas as pd
import requests
import json
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

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


sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.commit()

logger = glueContext.get_logger()

args = getResolvedOptions(sys.argv, ['JOB_NAME',
                                     'url',
                                     'targetBucket',
                                     'registrationkey'])




current = parse_data('https://download.bls.gov/pub/time.series/oe/oe.data.0.Current')
current = current.rename(columns={'series_id                     ':'series_id', '       value': 'value'})
current['value'] = pd.to_numeric(current['value'], errors='coerce')

series = parse_data('https://download.bls.gov/pub/time.series/oe/oe.series')
series = series.rename(columns={'series_id                     ':'series_id'})

fact = series.merge(current, on='series_id', how='left')


fact.to_parquet(f"{args['targetBucket']}/fact.parquet", index=False)