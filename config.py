# TODO: Maybe separate api key to its own file or env variable?
news_api_key = "YOUR KEY HERE"

bootstrap_server = "localhost:9092"
mongo_server = "mongodb://localhost:27017/"
database_name = "cm_db"

keywords = ["current", "breaking", "world", "political", "business", "sports", "entertainment", "technology"]
collections = keywords.copy()
collections.extend(["sources_domain_name", "users"])
