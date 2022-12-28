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
SentimentAnalysisDeployment.deploy()
