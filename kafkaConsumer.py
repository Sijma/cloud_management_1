from kafka import KafkaConsumer

# Specify the list of topics to subscribe to
topics=["current", "breaking", "world", "political", "business", "sports", "entertainment", "technology", "sources_domain_name"]

# Set up the Kafka consumer
consumer = KafkaConsumer(
    # Set the Kafka bootstrap server
    bootstrap_servers=["localhost:9092"],
    # Set the consumer group
    group_id="news",
    # Use the latest offsets
    auto_offset_reset="latest",
    # Enable automatic commit of offsets
    enable_auto_commit=True,
)

consumer.subscribe(topics=topics)

# Loop forever
while True:
    # Poll the Kafka consumer for new messages
    for message in consumer:
        # Print the topic and message
        print(f"Topic: {message.topic}, Message: {message.value}")