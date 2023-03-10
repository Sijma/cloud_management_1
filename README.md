# News Aggregator and Article Recommendation System

![image](https://user-images.githubusercontent.com/39009079/224078951-9341cd46-e3f2-4578-8d2d-9594cf2032b7.png)

## Overview

This is a microservices-based application which allows for scalability, flexibility, and modularity. It collects news articles from the News API, information regarding their sources, then stores them in a MongoDB database, and provides recommendations to users based on subscribed topics and related articles. The system consists of three microservices that work together to provide the full functionality of the system: the Kafka Producer, the Kafka Consumer, the Flask API and a Data Access Layer (DAL) that provides the 3 services with easy access to a common, local database.

## Architecture

### Kafka producer
The Kafka Producer is responsible for fetching news articles from the News API and sending them to the Kafka cluster. It is designed to run continuously and fetch new articles every two hours. It implements a loop that sends requests to the News API for each of the keywords in the configuration file. For each keyword, it sends the articles to the corresponding topic in the Kafka cluster and queries the Wikipedia API for a description of the source domain. The Kafka Producer then sleeps for two hours before repeating the loop.

### Kafka consumer
The Kafka consumer is simply responsible for receiving the articles from the Kafka cluster, processing the articles, and storing them in the MongoDB database.

### Flask web application
The Flask API provides a RESTful interface to users, allowing them to query the database for articles based on keywords they are subscribed to and recommendations based on related articles and authors. It also provides operations for registering to the system and subscribing to certain news keyword/topics.

### Data Access Layer
`database.py` serves as a DOL module for handling all database interactions and CRUD operations using MongoDB. A DOL approach was chosen to help enforce consistency and standardization in database operations across the multiple microservices. It also makes maintaining and expanding the system less error-prone regarding implementation, by providing a higher-level interface that is easier to use correctly, simplifying and abstracting the details and syntax needed to interact with it.

The database schema used in this project is very simple, as each collection in the database corresponds to a single keyword. This design allows for easy scalability, as new keywords can be added simply by creating a new collection. The simplicity of the schema also allows for fast retrieval of articles using PyMongo's find() function.
