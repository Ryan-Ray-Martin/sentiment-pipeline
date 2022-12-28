import requests
from starlette.requests import Request
from typing import Dict

from transformers import pipeline

import ray
from ray import serve

# initialize ray cluster with ray start --head, then run python 
# use ray stop to stop all ray processes
ray.init(address="ray://raycluster-autoscaler-head-svc:10001", namespace="serve")
serve.start(detached=True)
# 1: Wrap the pretrained sentiment analysis model in a Serve deployment.
@serve.deployment(route_prefix="/finbert")
class SentimentAnalysisDeployment:
    def __init__(self):
        self._model = pipeline("sentiment-analysis", model='ProsusAI/finbert', return_all_scores="true")

    def __call__(self, request: Request) -> Dict:
        return self._model(request.query_params["text"])[0]


# 2: Deploy the deployment.
#ray.init(address='auto')
SentimentAnalysisDeployment.deploy()

# 3: Query the deployment and print the result.
print(
    requests.get(
        "http://raycluster-autoscaler-head-svc:8000/finbert", params={"text": "Stocks rallied and the British pound gained."}
    ).json()
)
# when return all scores is true: [{'label': 'positive', 'score': 0.898361325263977}, 
# {'label': 'negative', 'score': 0.034473564475774765}, {'label': 'neutral', 'score': 0.06716513633728027}]
# when return all scores is deleted : {'label': 'positive', 'score': 0.898361325263977}