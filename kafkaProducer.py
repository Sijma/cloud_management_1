import time
import requests
import json
from kafka import KafkaProducer

import config

TIME_TO_WAIT = 7200  # The specified amount of time to wait for new topic requests. Current is 2 hours.

producer = KafkaProducer(bootstrap_servers=[config.bootstrap_server])

NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything?"
WIKI_API_ENDPOINT = "https://en.wikipedia.org/w/api.php"

news_payload = {"sortBy": "popularity", "apiKey": config.news_api_key, "q": ""}
wiki_payload = {"action": "query", "format": "json", "prop": "extracts", "explaintext": "1", "redirects": "1", "titles": ""}

print("connected")

while True:
    seen_domains = []

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
                # For demonstration purposes
                time.sleep(1)

                # Send the article to the corresponding topic in the kafka cluster
                producer.send(topic, json.dumps(article).encode("utf-8"))
                print("Sent: ", article["title"])

                # Get the source domain name of the article
                source_domain = article["source"]["name"]

                if source_domain not in seen_domains:
                    # Sleep for 1 second to avoid potentially getting rate limited
                    # Creates a bit of a time offset between keyword queries, so articles from last keywords might be more recent
                    time.sleep(1)

                    seen_domains.append(source_domain)

                    print(f"{source_domain} is new.")

                    # Add the source domain as the title to search in wiki params
                    wiki_payload["titles"] = source_domain

                    response = requests.get(WIKI_API_ENDPOINT, params=wiki_payload)

                    if response.status_code == 200:
                        # Get the page ID of the Wikipedia article
                        page_id = list(response.json()["query"]["pages"].keys())[0]

                        # Get the description of the source domain from the JSON response using the page ID
                        source_description = response.json()["query"]["pages"][page_id].get("extract")
                        if source_description is not None:
                            description_dict = {"domain_name": source_domain, "description": source_description}

                            # Send the description of the source domain to the "sources_domain_name" topic in the Kafka cluster
                            producer.send("sources_domain_name", json.dumps(description_dict).encode("utf-8"))

    # Sleep for specified amount
    time.sleep(TIME_TO_WAIT)
