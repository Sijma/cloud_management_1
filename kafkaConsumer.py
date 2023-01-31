import config
from kafka import KafkaConsumer
import database
import json

# Adding keywords + sources_domain_name as topics to subscribe to
topics = config.keywords.copy()
topics.append("sources_domain_name")

# Set up the Kafka consumer
consumer = KafkaConsumer(
    bootstrap_servers=[config.bootstrap_server],
    group_id="news",
    auto_offset_reset="latest",
    enable_auto_commit=True,
)

consumer.subscribe(topics=topics)

print("Connected")

# Loop forever
while True:
    # Poll the Kafka consumer for new messages
    for message in consumer:
        if message.topic != "sources_domain_name":
            print("Received: ", json.loads(message.value)["title"])  # For demonstration purposes
        database.add_to_database(message.topic, message.value)
