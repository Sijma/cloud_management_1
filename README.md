# Brief Setup that is expected by the python processes.

### Install Kafka, mongoDB and start them.

### Install the packages required in requirements.txt by running `pip install -r requirements.txt`.

### Run the topics.sh script.
Before running it, make sure to edit the `KAFKA_BIN_PATH` variable to your own, and change the topics and/or boostrap_server address if necessary.

### Edit config.py, such as the news_api_key, server addresses, topics, etc.

### Run kafkaConsumer.py, kafkaProducer.py and app.py in that order.
You can look into app.py for the available url paths. Flask should be running at http://127.0.0.1:5000 by default
