#!/bin/bash

# Set the path to the bin where kafka-topics.sh is
KAFKA_BIN_PATH="/home/sijma/Kafka/kafka_2.13-3.3.1/bin/"

KAFKA_PATH="/home/sijma/Kafka/kafka_2.13-3.3.1/"

$KAFKA_BIN_PATH"zookeeper-server-start.sh" $KAFKA_PATH"config/zookeeper.properties" &
sleep 2
$KAFKA_BIN_PATH"kafka-server-start.sh" $KAFKA_PATH"config/server.properties" &
sleep 5

# Set the bootstrap server and topic names
BOOTSTRAP_SERVER="localhost:9092"
TOPICS=("current" "breaking" "world" "political" "business" "sports" "entertainment" "technology" "sources_domain_name")

# Loop through the topics
for topic in ${TOPICS[@]}; do
  # Check if the topic already exists
  TOPIC_EXISTS=`$KAFKA_BIN_PATH"kafka-topics.sh" --list --bootstrap-server $BOOTSTRAP_SERVER | grep $topic`
  if [ -z "$TOPIC_EXISTS" ]; then
    # If the topic does not exist, create it
    $KAFKA_BIN_PATH"kafka-topics.sh" --create --bootstrap-server $BOOTSTRAP_SERVER --replication-factor 1 --partitions 1 --topic $topic
  else
    # If the topic already exists, skip it
    echo "Topic '$topic' already exists, skipping..."
  fi
done

service mongod start

#TODO: Could also start the 3 python processes here in order
