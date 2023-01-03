import feedparser
from datetime import datetime
import pandas as pd
from time import mktime
import requests
import sqlalchemy
import os

from google.cloud.sql.connector import Connector, IPTypes
import pg8000



# connect_with_connector initializes a connection pool for a
# Cloud SQL instance of Postgres using the Cloud SQL Python Connector.
def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"] #e.g. 'project:region:instance'
    db_user = os.environ["DB_USER"]   #e.g. 'my-db-user'
    db_pass = os.environ["DB_PASS"]  #e.g. 'my-db-password'
    db_name = os.environ["DB_NAME"]  # e.g. 'my-database'

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    # initialize Cloud SQL Python Connector object
    connector = Connector()

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        )
        return conn

    # The Cloud SQL Python Connector can be used with SQLAlchemy
    # using the 'creator' argument to 'create_engine'
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        # ...
    )
    return pool

def query(payload):
    return requests.get("http://raycluster-autoscaler-head-svc:8000/serve/finbert", params={"text": str(payload)}).json()

def extract() -> dict:
    data = {'headline': [], 'summary': [], 'date': []}
    NewsFeed = feedparser.parse("https://rss.nytimes.com/services/xml/rss/nyt/Business.xml")
    entry = NewsFeed.entries
    for article in entry: # For each article, make sure it falls within our date range
        dt = datetime.fromtimestamp(mktime(article.published_parsed))
        data['date'].append(dt)
        data['headline'].append(article.title)
        data['summary'].append(article.summary) 
    return pd.DataFrame(data)


def transform(df: dict) -> dict:
    sentiments = ["positive", "negative", "neutral"]
    df.dropna(subset=['headline'], inplace=True)
    for i, sentiment_str in enumerate(sentiments):
        df['headline_sentiment_{}'.format(sentiment_str)] = df.apply(lambda row : query(row['headline'])[i]['score'], axis=1)
    return df


def load(df: dict)-> sqlalchemy.engine.base.Engine:
    pool = connect_with_connector()
    df.to_sql('nytimes', con=pool, if_exists='append', index=False)
    

if __name__ == "__main__":
    order_data = extract()
    etl = transform(order_data)
    load(etl)