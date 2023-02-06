import argparse
import os

import pandas as pd
import requests
import time
import dateutil
import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from data_pipeline import *
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Example of custom type usage')
parser.add_argument('-start', '--start-datetime',
                        dest='start_datetime',
                        type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d').date(),
                        default=None,
                        required=True,
                        help='start datetime in format "YYYY-MM-DD"')
parser.add_argument('-stop', '--end-datetime',
                        dest='stop_datetime',
                        type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d').date(),
                        default=datetime.date.today(),
                        required=False,
                        help='stop datetime in format "YYYY-MM-DD"')

class NYTimesDataModel: 
    """A data model to retrieve data from nytimes archive and label with sentiment scores"""

    def __init__(self, start, stop) -> pd.DataFrame:
        self.dp = DataPipeline()
        self.start = start
        self.stop = stop
    
    def send_request(self, date):
        '''Sends a request to the NYT Archive API for given date.'''
        base_url = 'https://api.nytimes.com/svc/archive/v1/'
        url = base_url + '/' + date[0] + '/' + date[1] + '.json?api-key=' + os.environ["NYTIMES_API"]
        response = requests.get(url).json()
        time.sleep(6)
        return response

    def is_valid(self, article, date):
        '''An article is only worth checking if it is in range, and has a headline.'''
        is_in_range = date > self.start and date < self.stop
        has_headline = type(article['headline']) == dict and 'main' in article['headline'].keys()
        return is_in_range and has_headline

    def parse_response(self, response):
        '''Parses and returns response as pandas data frame.'''
        data = {'headline': [], 'date': []}
        articles = response['response']['docs'] 
        for article in articles: # For each article, make sure it falls within our date range
            date = dateutil.parser.parse(article['pub_date']).date()
            # Nov. 12 change from "Business Day" to just "Business"
            if self.is_valid(article, date) and 'Business' in article['section_name']:
                data['date'].append(date)
                data['headline'].append(article['headline']['main']) 
        return pd.DataFrame(data)

    def extract(self) -> pd.DataFrame:
        months_in_range = [x.split(' ') for x in pd.date_range(self.start, self.stop, freq='MS').strftime("%Y %-m").tolist()]
        month_object = tqdm(months_in_range)
        for date in month_object:
            month_object.set_description(f"Month in progress: {date}")
            response = self.send_request(date)
            data = self.parse_response(response)
            df = self.dp.transform(data)
            self.dp.load(df)


if __name__ == '__main__':
    args = parser.parse_args()
    start_date = args.start_datetime
    stop_date = args.stop_datetime
    NYTimesDataModel(start=start_date, stop=stop_date).extract()

    