import requests

print(
    requests.get(
        "http://localhost:8000/", params={"text": "Stocks rallied and the British pound gained."}
    ).json()
)

# when return all scores is true: [{'label': 'positive', 'score': 0.898361325263977}, 
# {'label': 'negative', 'score': 0.034473564475774765}, {'label': 'neutral', 'score': 0.06716513633728027}]
# when return all scores is deleted : {'label': 'positive', 'score': 0.898361325263977}