import tweepy

# Your Twitter API credentials
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAEH9vgEAAAAAlKXpmpD9QFdO%2BWhhN%2FQjfzZowlQ%3DBpXH6a5m0pmAm3OOrMh7ESWknb0hG5hpsOdjnE5AvOGBQpLmmm'

# Initialize Tweepy with Bearer Token
client = tweepy.Client(bearer_token=bearer_token)

# Define search query
query = '(flood OR earthquake OR disaster) has:images OR has:videos'

# Perform the search request
response = client.search_recent_tweets(query=query, tweet_fields=['attachments', 'text', 'created_at'], media_fields=['url'], expansions='attachments.media_keys', max_results=10)

# Print fetched tweets and associated media URLs
for tweet in response.data:
    print(f"Tweet: {tweet.text}")
    if 'attachments' in tweet:
        for media_key in tweet.attachments['media_keys']:
            media = response.includes['media']
            for item in media:
                if item.media_key == media_key:
                    if item.type == 'photo':
                        print(f"Image URL: {item.url}")
                    elif item.type == 'video':
                        print(f"Video URL: {item.url}")

# Note: Ensure to handle cases where media might not be included or query results might be empty.
