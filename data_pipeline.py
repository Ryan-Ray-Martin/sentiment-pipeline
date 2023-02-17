import requests
import sqlalchemy
from cloud_sql_tcp import connect_tcp_socket
from tqdm.auto import tqdm
import pandas as pd

class DataPipeline:
    def __init__(self) -> None:
        self.get_data = """SELECT * FROM nytimes"""
        self.get_avg = """SELECT date, AVG(headline_sentiment_positive) as positive
                          FROM nytimes
                          GROUP BY date
                          ORDER BY date ASC"""

    def query(self, payload):
        # "http://rayservice-sample-serve-svc:8000/"
        return requests.get("http://localhost:8000/", params={"text": str(payload)}).json()

    def transform(self, df: dict) -> dict:
        sentiments = ["positive", "negative", "neutral"]
        df.dropna(subset=['headline'], inplace=True)
        for i, sentiment_str in enumerate(sentiments):
            tqdm.pandas(desc=sentiment_str)
            df[
                'headline_sentiment_{}'.format(sentiment_str)
                ] = df.progress_apply(
                lambda row : self.query
                (
                    row['headline'])[i]['score'],
                     axis=1
                     )
        return df

    def load(self, df: dict)-> sqlalchemy.engine.base.Engine:
        pool = connect_tcp_socket()
        df.to_sql('nytimes', con=pool, if_exists='append', index=False)

    def select(self)-> sqlalchemy.engine.base.Engine:
        pool = connect_tcp_socket()
        return pd.read_sql(self.get_avg, con=pool)