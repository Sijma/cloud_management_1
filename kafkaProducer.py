import time
import requests
import json
from kafka import KafkaProducer

import config

NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything?"

producer = KafkaProducer(bootstrap_servers=["localhost:9092"])

while True:
    # Loop through the topics
    for topic in config.keywords:
        # Construct the query string for the News API
        query_string = f"q={topic}&sortBy=popularity&apiKey={config.news_api_key}"

        # Send a GET request to the News API
        response = requests.get(NEWS_API_ENDPOINT + query_string)

        # Check the status code of the response
        if response.status_code == 200:

            # If the request is successful, parse the news articles
            articles = response.json()["articles"]

            # Loop through the articles
            for article in articles:
                # Sleep for 1 second to avoid potentially getting rate limited
                time.sleep(1)

                producer.send(topic, json.dumps(articles).encode("utf-8"))

                # Get the source domain name of the article
                source_domain = article["source"]["name"]

                # Construct the query string for the MediaWiki API
                query_string = f"action=query&format=json&prop=extracts&exintro&explaintext&redirects=1&titles={source_domain}"

                # Send a GET request to the MediaWiki API
                response = requests.get("https://en.wikipedia.org/w/api.php?" + query_string)

                # Check the status code of the response
                if response.status_code == 200:
                    # Get the page ID of the Wikipedia article
                    page_id = list(response.json()["query"]["pages"].keys())[0]

                    # Get the description of the source domain from the JSON response
                    source_description = response.json()["query"]["pages"][page_id]["extract"]

                    # Send the description of the source domain to the "sources domain name" topic in the Kafka cluster
                    producer.send("sources_domain_name", source_description.encode("utf-8"))
                else:
                    # If the request fails, print an error message
                    print(f"Failed to retrieve description for source domain '{source_domain}': {response.text}")
        else:
            # If the request fails, print an error message
            print(f"Failed to retrieve news articles for topic '{topic}': {response.text}")

    # Sleep for 2 hours
    time.sleep(7200)
