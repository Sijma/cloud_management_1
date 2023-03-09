# News Aggregator and Recommendation System

![image](https://user-images.githubusercontent.com/39009079/224078951-9341cd46-e3f2-4578-8d2d-9594cf2032b7.png)

This project is a News Aggregator and Recommendation System that allows users to get up-to-date news articles from various categories, as well as receive recommendations for articles based on their interests. The system is built using Python and several open-source libraries, such as Flask, Kafka, and PyMongo.

## How it works

The system consists of three main components: the news scraper, the Kafka message broker, and the web application.

The news scraper fetches news articles from various sources using the News API and sends them as Kafka messages to the Kafka message broker. At the same time, it also queries the Wikipedia API to retrieve a short description for each news source and sends that as a separate message to the Kafka message broker.

The Kafka message broker acts as a central hub for all the messages that are sent between the news scraper and the web application. It receives the messages sent by the news scraper and forwards them to the web application.

The web application provides users with a web-based interface where they can view news articles from various categories and receive recommendations for articles based on their interests. The application is built using Flask, a Python web framework, and uses PyMongo to retrieve news articles and recommendations from a MongoDB database. It also uses Kafka-Python to subscribe to the Kafka message broker and receive new articles and recommendations in real-time.

## Project Files
`config.py`: This file contains all the configuration parameters for the project, such as the Kafka bootstrap server and API keys for external APIs.

`database.py`: This file contains the database connection and methods to interact with the MongoDB database.

`app.py`: This file contains the Flask web application and routes for serving news articles and recommendations to users.

`kafkaConsumer.py`: This file contains the Kafka consumer that subscribes to the Kafka message broker and adds new articles to the MongoDB database.

`kafkaProducer.py`: This file contains the Kafka producer that fetches news articles from the News API, sends them to the Kafka message broker, and queries the Wikipedia API to retrieve descriptions for news sources.

`graph.py`: This file contains the code for building a graph of related news articles and recommending articles to users based on their interests.

`stackedBar.py`: This file contains the code for generating a stacked bar plot of the number of articles published per day and per category.

`topics.sh`: This shell script creates the Kafka topics used by the system and starts the Kafka and MongoDB services.

`requirements.txt`: This file contains a list of all the Python libraries required by the project.

## Getting Started
To get started with the News Aggregator and Recommendation System, you will need to have the following installed:

Python 3
Apache Kafka
MongoDB

Then, to install the required Python libraries, run the following command:
```
pip install -r requirements.txt
```

To start the Kafka and MongoDB services and create the necessary Kafka topics, run the following command:
```
./topics.sh
```

First start the Kafka consumer, by running the following command:
```
python kafkaConsumer.py
```

Then start the Kafka producer, by running:
```
python kafkaProducer.py
```

Finally, to start the Flask web application, run the following command:
```
python app.py
```

Once the web application is running, you can access it by navigating to `http://localhost:5000` in your web browser.
