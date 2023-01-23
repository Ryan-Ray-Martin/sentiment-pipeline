import pandas as pd
import requests
import time
import dateutil
import datetime
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from typing import List
from data_pipeline import *
from tqdm import tqdm

def send_request(date):
    '''Sends a request to the NYT Archive API for given date.'''
    base_url = 'https://api.nytimes.com/svc/archive/v1/'
    url = base_url + '/' + date[0] + '/' + date[1] + '.json?api-key=' + os.environ["NYTIMES_API"]
    response = requests.get(url).json()
    time.sleep(6)
    return response

def is_valid(article, date):
    '''An article is only worth checking if it is in range, and has a headline.'''
    is_in_range = date > start and date < end
    has_headline = type(article['headline']) == dict and 'main' in article['headline'].keys()
    return is_in_range and has_headline

def parse_response(response):
    '''Parses and returns response as pandas data frame.'''
    data = {'headline': [], 'date': []}
    articles = response['response']['docs'] 
    for article in articles: # For each article, make sure it falls within our date range
        date = dateutil.parser.parse(article['pub_date']).date()
        # Nov. 12 change from "Business Day" to just "Business"
        if is_valid(article, date) and 'Business' in article['section_name']:
            data['date'].append(date)
            data['headline'].append(article['headline']['main']) 
    return pd.DataFrame(data)

if __name__ == '__main__':
    dp = DataPipeline()
    end = datetime.date.today()
    start = datetime.date(2022, 10, 1)
    months_in_range = [x.split(' ') for x in pd.date_range(start, end, freq='MS').strftime("%Y %-m").tolist()]
    month_object = tqdm(months_in_range)
    for date in month_object:
        month_object.set_description(f"Month in progress: {date}")
        response = send_request(date)
        data = parse_response(response)
        df = dp.transform(data)
        #df.to_csv('nytimes_sentiment/{}_{}'.format(date[0], date[1]))
        dp.load(df)