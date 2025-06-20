import os
import requests
from dotenv import load_dotenv
from twitter_plugin_gamesdk.twitter_plugin import TwitterPlugin

def safe_get_data(response, key="data"):
    """Safely get data from API response, handling both dict and object formats"""
    if hasattr(response, key):
        return getattr(response, key)
    elif isinstance(response, dict) and key in response:
        return response[key]
    else:
        return response

def run_twitter_actions():
    load_dotenv()
    token = os.getenv("GAME_TWITTER_ACCESS_TOKEN")
    print("Token:", token)
    if not token:
        raise RuntimeError("Please set GAME_TWITTER_ACCESS_TOKEN in your .env")

    options = {
        "credentials": {
            "game_twitter_access_token": token
        }
    }

    twitter_plugin = TwitterPlugin(options)
    client = twitter_plugin.twitter_client

    try:
        # 1. Who am I?
        me = client.get_me()
        me_data = safe_get_data(me, "data")
        user_id = me_data["id"]
        print(f"🙋 Logged in as: @{me_data['username']} ({me_data['name']})")

        # 2. Post a tweet
        tweet = client.create_tweet(text="Hello Web3 🧵 #GameByVirtuals - Testing GAME SDK!")
        tweet_data = safe_get_data(tweet, "data")
        tweet_id = tweet_data["id"]
        print(f"✅ Tweet posted: https://x.com/i/web/status/{tweet_id}")

        # 3. Like it (with better error handling)
        try:
            like_response = client.like(tweet_id=tweet_id)
            print("❤️ Tweet liked!")
        except Exception as e:
            print(f"⚠️ Like failed: {e}")

        # 4. Reply to it
        try:
            reply = client.create_tweet(
                text="Replying to my own tweet 😎",
                in_reply_to_tweet_id=tweet_id
            )
            reply_data = safe_get_data(reply, "data")
            print(f"💬 Replied: https://x.com/i/web/status/{reply_data['id']}")
        except Exception as e:
            print(f"⚠️ Reply failed: {e}")

        # 5. Quote it
        try:
            quote = client.create_tweet(
                text="Excited to be testing the new Game Twitter Plugin!",
                quote_tweet_id=tweet_id
            )
            quote_data = safe_get_data(quote, "data")
            print(f"🔁 Quoted: https://x.com/i/web/status/{quote_data['id']}")
        except Exception as e:
            print(f"⚠️ Quote failed: {e}")

        # 6. Search tweets
        try:
            search = client.search_recent_tweets(query="#GameByVirtuals", max_results=10)
            hits = search.get("data", []) if isinstance(search, dict) else []
            print(f"🔍 Found {len(hits)} tweets for #GameByVirtuals:")
            for i, t in enumerate(hits[:3], 1):  # Show only first 3
                print(f"  {i}. https://x.com/i/web/status/{t['id']}")
        except Exception as e:
            print(f"⚠️ Search failed: {e}")

        # 7. Mentions timeline
        try:
            mentions = client.get_users_mentions(id=user_id, max_results=5)
            mdata = mentions.get("data", []) if isinstance(mentions, dict) else []
            print(f"🔔 You have {len(mdata)} recent mentions:")
            for i, t in enumerate(mdata, 1):
                print(f"  {i}. https://x.com/i/web/status/{t['id']}")
        except Exception as e:
            print(f"⚠️ Mentions failed: {e}")

        # 8. Get my public metrics
        try:
            metrics = client.get_me(user_fields=["public_metrics"])
            metrics_data = safe_get_data(metrics, "data")
            print("📊 My metrics:", metrics_data["public_metrics"])
        except Exception as e:
            print(f"⚠️ Metrics failed: {e}")

        # 9. Read-only lookup of another user
        try:
            other = client.get_user(username="GAME_Virtuals")
            other_data = safe_get_data(other, "data")
            print("🔎 Lookup @GAME_Virtuals:", other_data)
        except Exception as e:
            print(f"⚠️ User lookup failed: {e}")

        print("\n✅ Twitter test completed successfully!")

    except Exception as e:
        print("❌ Error during Twitter actions:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_twitter_actions() 