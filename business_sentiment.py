import feedparser
from datetime import datetime
import pandas as pd
from time import mktime
from data_pipeline import *

def extract() -> dict:
    data = {'headline': [], 'summary': [], 'date': []}
    NewsFeed = feedparser.parse("https://rss.nytimes.com/services/xml/rss/nyt/Business.xml")
    entry = NewsFeed.entries
    for article in entry: # For each article, make sure it falls within our date range
        dt = datetime.fromtimestamp(mktime(article.published_parsed))
        data['date'].append(dt)
        data['headline'].append(article.title)
        #data['summary'].append(article.summary) 
    return pd.DataFrame(data)
    

if __name__ == "__main__":
    dp = DataPipeline()
    order_data = extract()
    etl = dp.transform(order_data)
    print(etl)
    dp.load(etl)