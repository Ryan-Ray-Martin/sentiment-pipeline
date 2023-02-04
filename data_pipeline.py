import requests
import sqlalchemy
from cloud_sql_tcp import connect_tcp_socket
from tqdm.auto import tqdm

class DataPipeline:
    def __init__(self) -> None:
        pass

    def query(self, payload):
        return requests.get("http://rayservice-sample-serve-svc:8000/", params={"text": str(payload)}).json()

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