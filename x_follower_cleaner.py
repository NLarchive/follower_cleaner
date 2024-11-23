# X (Twitter) Bot Follower Cleaner
# Make sure to install the required library:
# !pip install tweepy

import tweepy
import time

# Authentication credentials

# Consumer Keys
X_API_key = ''
X_API_key_secret = ''
consumer_key = X_API_key
consumer_secret = X_API_key_secret

#Authentication Tokens
Bearer_Token = ''
access_token = ""
access_token_secret = ""

# Authenticate with X API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True)

def is_bot(user):
    """
    Check if a user is likely a bot based on the follower-to-following ratio.
    Returns True if the user follows more than 10 times the number of their followers.
    """
    if user.followers_count == 0:
        return True
    return (user.friends_count / user.followers_count) > 10

def clean_bots():
    """
    Clean bot followers from the authenticated user's account.
    """
    print("Starting bot cleaning process...")
    me = api.verify_credentials()
    follower_count = me.followers_count
    processed = 0
    removed = 0

    for follower in tweepy.Cursor(api.get_followers).items():
        processed += 1
        if is_bot(follower):
            try:
                api.destroy_friendship(follower.id)
                print(f"Removed bot: @{follower.screen_name}")
                removed += 1
            except tweepy.TweepError as e:
                print(f"Error removing @{follower.screen_name}: {e}")

        if processed % 100 == 0:
            print(f"Processed {processed}/{follower_count} followers. Removed {removed} bots.")

        # Add a small delay to avoid hitting rate limits
        time.sleep(1)

    print(f"Finished processing. Total followers processed: {processed}")
    print(f"Total bots removed: {removed}")

if __name__ == "__main__":
    clean_bots()
