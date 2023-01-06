import requests

print(
    requests.get(
        "http://rayservice-sample-serve-svc:8000/", params={"text": "Stocks rallied and the British pound gained."}
    ).json()
)