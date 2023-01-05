import time
import requests
import json
from kafka import KafkaProducer

import config

producer = KafkaProducer(bootstrap_servers=["localhost:9092"])

NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything?"
WIKI_API_ENDPOINT = "https://en.wikipedia.org/w/api.php"

news_payload = {"sortBy": "popularity", "apiKey": config.news_api_key, "q": ""}
wiki_payload = {"action": "query", "format": "json", "prop": "extracts", "explaintext": "1", "redirects": "1", "titles": ""}

while True:
    # Loop through the topics
    for topic in config.keywords:
        # Add topic as param to payload
        news_payload['q'] = topic

        # Send a GET request to the News API
        response = requests.get(NEWS_API_ENDPOINT, params=news_payload)

        # Check the status code of the response
        if response.status_code == 200:

            # If the request is successful, parse the news articles
            articles = response.json()["articles"]

            # Loop through the articles
            for article in articles:
                # Sleep for 1 second to avoid potentially getting rate limited
                time.sleep(1)

                # Send the article to the corresponding topic in the kafka cluster
                producer.send(topic, json.dumps(article).encode("utf-8"))

                # Get the source domain name of the article
                source_domain = article["source"]["name"]

                # Add the source domain as the title to search in wiki params
                wiki_payload["titles"] = source_domain

                response = requests.get(WIKI_API_ENDPOINT, params=wiki_payload)

                if response.status_code == 200:
                    # Get the page ID of the Wikipedia article
                    page_id = list(response.json()["query"]["pages"].keys())[0]

                    # Get the description of the source domain from the JSON response using the page ID
                    source_description = response.json()["query"]["pages"][page_id]["extract"]

                    description_dict = {"domain_name": source_domain, "description": source_description}

                    # Send the description of the source domain to the "sources_domain_name" topic in the Kafka cluster
                    producer.send("sources_domain_name", json.dumps(description_dict).encode("utf-8"))

    # Sleep for 2 hours
    time.sleep(7200)
