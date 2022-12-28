from starlette.requests import Request
from typing import Dict

from transformers import pipeline

import ray
from ray import serve

ray.init(address="ray://raycluster-autoscaler-head-svc:10001", namespace="serve")
serve.start(detached=True, http_options={"host": "0.0.0.0"})

@serve.deployment(route_prefix="/finbert")
class SentimentAnalysisDeployment:
    def __init__(self):
        self._model = pipeline("sentiment-analysis", model='ProsusAI/finbert', return_all_scores="true")

    def __call__(self, request: Request) -> Dict:
        return self._model(request.query_params["text"])[0]


SentimentAnalysisDeployment.deploy()
