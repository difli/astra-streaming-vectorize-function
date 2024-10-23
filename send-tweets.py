import pulsar
from pulsar.schema import Record, String, Integer, JsonSchema
import json

# Replace with your Pulsar service URL and token
PULSAR_SERVICE_URL = 'pulsar+ssl://<astra-streaming-service-url>'
TOPIC = "persistent://streaming-demo/default/tweets-topic"
AUTH_TOKEN = "<your-auth-token>"

# Define the JSON schema as a class
class TweetData(Record):
    lang = String()
    id = String()
    tweet = String()
    createdAt = String()
    sentiment = Integer()

# Create a Pulsar client
client = pulsar.Client(PULSAR_SERVICE_URL, authentication=pulsar.AuthenticationToken(AUTH_TOKEN))

# Create a producer with the specified JSON schema
producer = client.create_producer(
    TOPIC,
    schema=JsonSchema(TweetData)  # Use the new JSON schema class here
)

# Open and read the JSON file containing multiple tweet objects
with open('data.json', 'r') as file:
    tweet_data_list = json.load(file)  # Load the JSON data as a list

# Iterate over each tweet object in the JSON array
for tweet_data in tweet_data_list:
    try:
        # Create a message that adheres to the schema
        message = TweetData(
            lang=tweet_data.get("lang", ""),
            id=tweet_data.get("id", ""),
            tweet=tweet_data.get("tweet", ""),
            createdAt=tweet_data.get("createdAt", ""),
            sentiment=tweet_data.get("sentiment", 0)
        )

        # Produce the JSON message directly
        producer.send(message)
        print(f"Message sent successfully for tweet ID: {tweet_data['id']}")

    except Exception as e:
        print(f"Failed to send message for tweet ID: {tweet_data.get('id')} due to error: {e}")

# Close the producer and client
producer.close()
client.close()

print("All JSON messages produced successfully.")
