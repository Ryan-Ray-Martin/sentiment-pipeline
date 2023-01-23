from starlette.requests import Request
from typing import Dict
from transformers import pipeline
from ray import serve

# 1: Wrap the pretrained sentiment analysis model in a Serve deployment.
@serve.deployment(route_prefix="/")
class SentimentAnalysisDeployment:
    def __init__(self):
        self._model = pipeline("sentiment-analysis", model='ProsusAI/finbert', return_all_scores="true")

    def __call__(self, requests: Request) -> Dict:
        return self._model(requests.query_params["text"])[0]


# 2: Deploy the deployment.
sentiment = SentimentAnalysisDeployment.bind()

# to run use: serve run finbert_serve:sentiment
# source: https://docs.ray.io/en/latest/serve/getting_started.html

