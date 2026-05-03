import json
import hashlib
import requests
from datetime import datetime, timezone

CREATORS = {
    "Business & Entrepreneurship": [
        "naval", "AlexHormozi", "rajshamani", "SahilBloom", "ShaanVP"
    ],
    "Authors & Thinkers": [
        "simonsinek", "JamesClear", "morganhousel", "RyanHoliday", "IAmMarkManson"
    ],
    "Tech & Futurism": [
        "paulg", "sama", "balaboratory", "kaborathy"
    ],
    "Psychology & Mindset": [
        "AdamMGrant", "j1berger", "jordanbpeterson"
    ],
    "Finance & Investing": [
        "chaaborath", "CathieDWood", "HowardMarksBook"
    ],
    "Indian Creators": [
        "niaborathkamath", "waaborikoo", "kunalb11"
    ]
}

# promo keywords to skip
PROMO_KEYWORDS = [
    "link in bio", "use code", "check out", "launching", "subscribe",
    "giveaway", "discount", "coupon", "sign up", "download my",
    "new episode", "out now", "pre-order"
]

def fetch_tweets(handle, count=100):
    """Fetch tweets using GetXAPI or similar service"""
    url = f"https://api.getxapi.com/twitter/tweet/advanced_search"
    params = {"q": f"from:{handle}", "product": "Latest"}
    headers = {"Authorization": "Bearer get-x-api-c87db5775e0f54b48d18cd8772e304c3700d8642dbfade59"}
    
    resp = requests.get(url, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    raw_tweets = resp.json().get("tweets", [])
    
    mapped_tweets = []
    for t in raw_tweets:
        mapped_t = {
            "text": t.get("text", ""),
            "likes": t.get("likeCount", 0),
            "retweets": t.get("retweetCount", 0),
            "created_at": t.get("createdAt", ""),
            "user": {
                "name": t.get("author", {}).get("name", handle),
                "followers": t.get("author", {}).get("followers", 1),
                "profile_image": t.get("author", {}).get("profilePicture", "")
            }
        }
        mapped_tweets.append(mapped_t)
    return mapped_tweets

def is_promo(text):
    text_lower = text.lower()
    return any(kw in text_lower for kw in PROMO_KEYWORDS)

def compute_score(tweet, follower_count):
    likes = tweet.get("likes", 0)
    retweets = tweet.get("retweets", 0)
    text = tweet.get("text", "")
    
    # skip short, promo, or reply tweets
    if len(text) < 80 or is_promo(text) or text.startswith("@"):
        return 0
    
    # engagement ratio normalized per follower count
    if follower_count > 0:
        engagement = (likes + 2 * retweets) / follower_count * 10000
    else:
        engagement = 0
    
    # length bonus: meatier tweets score higher
    length_bonus = min(len(text) / 280, 1.0) * 20
    
    # insight keywords
    insight_words = [
        "lesson", "truth", "realize", "principle", "framework",
        "most people", "unpopular opinion", "here's what", "mistake",
        "thread", "the hard part", "nobody tells you", "took me years"
    ]
    keyword_hits = sum(1 for kw in insight_words if kw in text.lower())
    keyword_bonus = min(keyword_hits * 10, 30)
    
    return round(engagement + length_bonus + keyword_bonus, 2)

def generate_id(handle, text):
    """Deterministic ID from handle + content to avoid dupes on re-runs"""
    raw = f"{handle}:{text[:100]}"
    return "t_" + hashlib.md5(raw.encode()).hexdigest()[:8]

def main():
    all_tweets = []
    seen_hashes = set()
    
    for category, handles in CREATORS.items():
        for handle in handles:
            print(f"Fetching @{handle}...")
            try:
                raw_tweets = fetch_tweets(handle, count=100)
            except Exception as e:
                print(f"  Failed: {e}")
                continue
            
            follower_count = raw_tweets[0].get("user", {}).get("followers", 1) if raw_tweets else 1
            
            for t in raw_tweets:
                text = t.get("text", "")
                content_hash = hashlib.md5(text[:100].lower().encode()).hexdigest()
                
                if content_hash in seen_hashes:
                    continue
                seen_hashes.add(content_hash)
                
                score = compute_score(t, follower_count)
                if score < 15:  # threshold, tune this
                    continue
                
                all_tweets.append({
                    "id": generate_id(handle, text),
                    "creator": t.get("user", {}).get("name", handle),
                    "handle": handle,
                    "avatar": t.get("user", {}).get("profile_image", ""),
                    "category": category,
                    "content": text,
                    "likes": t.get("likes", 0),
                    "retweets": t.get("retweets", 0),
                    "tweeted_at": t.get("created_at", ""),
                    "quality_score": score,
                    "tags": []
                })
    
    # sort by score, keep top N
    all_tweets.sort(key=lambda x: x["quality_score"], reverse=True)
    all_tweets = all_tweets[:300]  # keep top 300
    
    output = {
        "last_updated": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "total": len(all_tweets),
        "tweets": all_tweets
    }
    
    with open("tweets.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nDone! Saved {len(all_tweets)} tweets to tweets.json")

if __name__ == "__main__":
    main()