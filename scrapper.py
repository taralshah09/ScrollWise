import json
import hashlib
import requests
import time
from datetime import datetime, timezone
from difflib import SequenceMatcher

# ─────────────────────────────────────────────
#  CREATOR REGISTRY  (21 → 55 handles)
# ─────────────────────────────────────────────
CREATORS = {
    "Business & Entrepreneurship": [
        "naval",          # Naval Ravikant — wealth & philosophy
        "AlexHormozi",    # $100M Offers
        "rajshamani",     # Indian entrepreneur & storyteller
        "SahilBloom",     # curiosity-driven business frameworks
        "ShaanVP",        # My First Million host
        "garyvee",        # hustle culture, DTC
        "jasonfried",     # Basecamp / REWORK author
        "dhh",            # Rails creator, anti-hustle
        "paulg",          # YC essays (also in Tech)
        "hnshah",         # Product Hunt founder
        "patrick_oshag",  # Invest Like the Best
        "lennysan",       # Lenny's Newsletter - PM & growth
    ],

    "Authors & Thinkers": [
        "simonsinek",     # Start With Why
        "JamesClear",     # Atomic Habits
        "morganhousel",   # Psychology of Money
        "RyanHoliday",    # Stoicism / Daily Stoic
        "IAmMarkManson",  # Subtle Art of Not Giving a F*ck
        "naval",          # cross-listed intentionally
        "BreneBrown",     # Daring Greatly
        "SethGodin",      # Marketing & creativity
        "timferriss",     # 4-Hour Work Week
        "AnnieDuke",      # Thinking in Bets — decision making
        "michaelleibowitz", # deep thinking threads
        "shane_parrish",  # Farnam Street / mental models
    ],

    "Tech & Futurism": [
        "sama",           # Sam Altman — OpenAI
        "balajis",        # Network State / crypto futurism
        "karpathy",       # AI/ML educator (ex-Tesla, OpenAI)
        "elonmusk",       # Tesla / SpaceX / X
        "BenedictEvans",  # tech strategy analyst
        "stratechery",    # Ben Thompson — tech business
        "NatFriedman",    # ex-GitHub CEO
        "danielgross",    # AI investor
        "emollick",       # AI & future of work (Wharton)
        "goodside",       # prompt engineering deep dives
        "fchollet",       # Keras / deep learning researcher
        "ylecun",         # Meta Chief AI Scientist
    ],

    "Psychology & Mindset": [
        "AdamMGrant",     # Organizational psychologist
        "j1berger",       # Jonah Berger — Contagious
        "jordanbpeterson", # Maps of Meaning
        "hubermanlab",    # Neuroscience / performance
        "drjoeDispenza",  # Mindset & neuroplasticity
        "ChrisVoss",      # Never Split the Difference
        "VictoriaArlen",  # resilience & mindset
        "melrobbins",     # The 5 Second Rule
    ],

    "Finance & Investing": [
        "chamath",        # Social Capital
        "CathieDWood",    # ARK Invest
        "HowardMarksBook", # Oaktree memos
        "BillAckman",     # Pershing Square
        "naval",          # wealth creation principles
        "10kdiver",       # financial independence math threads
        "modestproposal1", # macro & rates
        "ByrneHobart",    # The Diff newsletter
    ],

    "Health & Performance": [
        "PeterAttiaMD",   # Outlive — longevity medicine
        "hubermanlab",    # Huberman Lab
        "richroll",       # ultra-endurance & plant-based
        "davidgoggins",   # mental toughness
        "DrRhondaPatrick", # micronutrients & longevity
    ],

    "Creativity & Design": [
        "austinkleon",    # Steal Like an Artist
        "pvh",            # Paul Haddad — design thinking
        "joulee",         # Julie Zhuo — design leadership
        "figma",          # design culture
        "robinsloan",     # media inventor / writer
    ],

    "Indian Creators": [
        "Nithin0dha",     # Zerodha founder
        "warikoo",        # career & life advice
        "kunalb11",       # Kunal Shah — CRED founder
        "ankurwarikoo",   # same as warikoo (alt handle)
        "suhailkakar",    # indie hacker / dev
        "nireyal",        # Hooked author (Indian-American)
        "aarthimurali",   # startup & product
    ],

    "Journalism & Media": [
        "ezraklein",      # policy & ideas
        "karaswisher",    # big tech accountability
        "BenThompson",    # Stratechery
        "gruber",         # Daring Fireball — Apple
        "BrookingsInst",  # policy think tank
    ],
}

# ─────────────────────────────────────────────
#  PER-CREATOR MINIMUM TWEET LENGTH
#  (short-form thinkers get a lower floor)
# ─────────────────────────────────────────────
MIN_LENGTH_OVERRIDES = {
    "naval":        30,   # "Seek wealth, not money or status."
    "SethGodin":    40,
    "JamesClear":   50,
    "simonsinek":   50,
    "morganhousel": 50,
    "paulg":        50,
    "RyanHoliday":  50,
    "davidgoggins": 40,
}
DEFAULT_MIN_LENGTH = 70

# ─────────────────────────────────────────────
#  PROMO / NOISE KEYWORDS
# ─────────────────────────────────────────────
PROMO_KEYWORDS = [
    "link in bio", "use code", "check out", "launching", "subscribe",
    "giveaway", "discount", "coupon", "sign up", "download my",
    "new episode", "out now", "pre-order", "my course", "join my",
    "affiliate", "sponsored", "paid partnership", "ad:", "[ad]",
    "free trial", "click here", "swipe up",
]

# ─────────────────────────────────────────────
#  INSIGHT KEYWORDS (scoring)
# ─────────────────────────────────────────────
INSIGHT_KEYWORDS = [
    "lesson", "truth", "realize", "principle", "framework",
    "most people", "unpopular opinion", "here's what", "mistake",
    "thread", "the hard part", "nobody tells you", "took me years",
    "wisdom", "advice", "success", "failure", "habits", "discipline",
    "mental model", "first principles", "counterintuitive", "paradox",
    "underrated", "overrated", "the real reason", "what i learned",
    "uncomfortable truth", "hard truth", "ironically", "in reality",
    "the key is", "simple truth", "stop doing", "start doing",
]

API_HEADERS = {
    "Authorization": "Bearer get-x-api-31e906ef64bf72511f8eec8c6a712bcb721475cee74cfae3"
}


# ─────────────────────────────────────────────
#  FETCH: deep timeline pagination
# ─────────────────────────────────────────────
def fetch_tweets_timeline(handle: str, max_pages: int = 20) -> list[dict]:
    """
    Pull from user timeline — excludes replies & retweets.
    20 pages × ~20 tweets ≈ 400 original tweets per creator.
    """
    url = "https://api.getxapi.com/twitter/user/tweets"
    all_tweets = []
    cursor = None

    for page in range(max_pages):
        params = {
            "username": handle,
            "count": 20,
            "exclude": "replies,retweets",
        }
        if cursor:
            params["cursor"] = cursor

        try:
            resp = requests.get(url, params=params, headers=API_HEADERS, timeout=15)
            resp.raise_for_status()
            data = resp.json()

            tweets = data.get("tweets", [])
            all_tweets.extend(tweets)

            cursor = data.get("cursor")
            if not cursor or len(tweets) < 5:
                break

            time.sleep(0.4)   # rate-limit courtesy pause

        except Exception as e:
            print(f"    [timeline] page {page+1} error for @{handle}: {e}")
            break

    return all_tweets


# ─────────────────────────────────────────────
#  FETCH: top search results (supplement)
# ─────────────────────────────────────────────
def fetch_tweets_search(handle: str, max_pages: int = 5) -> list[dict]:
    """
    Advanced search for high-engagement tweets.
    Complements timeline by surfacing viral older content.
    """
    url = "https://api.getxapi.com/twitter/tweet/advanced_search"
    # Low min_faves so scoring handles filtering — not the query
    query = f"from:{handle} min_faves:200 -filter:replies lang:en"
    all_tweets = []
    cursor = None

    for page in range(max_pages):
        params = {"q": query, "product": "Top", "count": 20}
        if cursor:
            params["cursor"] = cursor

        try:
            resp = requests.get(url, params=params, headers=API_HEADERS, timeout=15)
            resp.raise_for_status()
            data = resp.json()

            tweets = data.get("tweets", [])
            all_tweets.extend(tweets)

            cursor = data.get("cursor")
            if not cursor or len(tweets) < 5:
                break

            time.sleep(0.4)

        except Exception as e:
            print(f"    [search] page {page+1} error for @{handle}: {e}")
            break

    return all_tweets


# ─────────────────────────────────────────────
#  FETCH: stitch threads
# ─────────────────────────────────────────────
def fetch_thread(tweet_id: str) -> str | None:
    """
    If a tweet is the first post of a thread, fetch and
    concatenate the rest. Returns stitched text or None.
    """
    url = "https://api.getxapi.com/twitter/tweet/thread"
    try:
        resp = requests.get(
            url, params={"tweetId": tweet_id}, headers=API_HEADERS, timeout=15
        )
        resp.raise_for_status()
        data = resp.json()
        thread_tweets = data.get("tweets", [])
        if len(thread_tweets) > 1:
            return "\n\n".join(t.get("text", "") for t in thread_tweets)
    except Exception:
        pass
    return None


# ─────────────────────────────────────────────
#  NORMALISE raw API tweet → internal dict
# ─────────────────────────────────────────────
def normalise(raw: dict, handle: str) -> dict:
    author = raw.get("author") or raw.get("user") or {}
    return {
        "text":          raw.get("text", ""),
        "likes":         raw.get("likeCount", raw.get("likes", 0)),
        "retweets":      raw.get("retweetCount", raw.get("retweets", 0)),
        "created_at":    raw.get("createdAt", raw.get("created_at", "")),
        "tweet_id":      raw.get("id", raw.get("tweetId", "")),
        "user": {
            "name":          author.get("name", handle),
            "followers":     author.get("followers", author.get("followersCount", 1)),
            "profile_image": author.get("profilePicture", author.get("profile_image", "")),
        },
    }


# ─────────────────────────────────────────────
#  FILTERS
# ─────────────────────────────────────────────
def is_promo(text: str) -> bool:
    tl = text.lower()
    return any(kw in tl for kw in PROMO_KEYWORDS)


def is_reply(text: str) -> bool:
    return text.strip().startswith("@")


def is_too_short(text: str, handle: str) -> bool:
    min_len = MIN_LENGTH_OVERRIDES.get(handle, DEFAULT_MIN_LENGTH)
    return len(text.strip()) < min_len


# ─────────────────────────────────────────────
#  SCORING
# ─────────────────────────────────────────────
def compute_score(tweet: dict, follower_count: int, handle: str) -> float:
    text  = tweet.get("text", "")
    likes = tweet.get("likes", 0)
    rts   = tweet.get("retweets", 0)

    if is_too_short(text, handle) or is_promo(text) or is_reply(text):
        return 0.0

    abs_engagement = likes + 2 * rts

    # Banger bonus — absolute virality
    if abs_engagement > 50_000:
        banger_bonus = 100
    elif abs_engagement > 10_000:
        banger_bonus = 60
    elif abs_engagement > 2_000:
        banger_bonus = 30
    else:
        banger_bonus = 0

    # Relative engagement ratio
    engagement_ratio = (abs_engagement / max(follower_count, 1)) * 10_000

    # Length bonus — longer = more substance (capped at 1 full tweet)
    length_bonus = min(len(text) / 280, 1.0) * 15

    # Thread bonus
    is_thread = any(marker in text for marker in ["1/", "1)", "🧵", "thread"])
    thread_bonus = 20 if is_thread else 0

    # Insight keyword bonus
    tl = text.lower()
    kw_hits = sum(1 for kw in INSIGHT_KEYWORDS if kw in tl)
    keyword_bonus = min(kw_hits * 8, 48)

    return round(
        engagement_ratio + banger_bonus + length_bonus + thread_bonus + keyword_bonus,
        2,
    )


# ─────────────────────────────────────────────
#  DEDUPLICATION (semantic similarity)
# ─────────────────────────────────────────────
def is_near_duplicate(new_text: str, existing_texts: list[str], threshold: float = 0.75) -> bool:
    snippet = new_text[:120].lower()
    for existing in existing_texts:
        ratio = SequenceMatcher(None, snippet, existing[:120].lower()).ratio()
        if ratio > threshold:
            return True
    return False


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def generate_id(handle: str, text: str) -> str:
    raw = f"{handle}:{text[:100]}"
    return "t_" + hashlib.md5(raw.encode()).hexdigest()[:8]


def deduplicate_handles(creators: dict) -> dict:
    """Remove duplicate handles that appear in multiple categories."""
    seen = set()
    deduped = {}
    for cat, handles in creators.items():
        unique = []
        for h in handles:
            if h not in seen:
                seen.add(h)
                unique.append(h)
        deduped[cat] = unique
    return deduped


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    creators = deduplicate_handles(CREATORS)

    all_tweets: list[dict] = []
    content_hashes: set[str] = set()
    existing_texts: list[str] = []

    total_handles = sum(len(v) for v in creators.values())
    processed = 0

    for category, handles in creators.items():
        for handle in handles:
            processed += 1
            print(f"[{processed}/{total_handles}] @{handle}  ({category})")

            # ── 1. Pull from timeline (primary — most raw volume)
            raw_timeline = []
            try:
                raw_timeline = fetch_tweets_timeline(handle, max_pages=20)
                print(f"    timeline → {len(raw_timeline)} raw")
            except Exception as e:
                print(f"    timeline failed: {e}")

            # ── 2. Pull top search results (supplementary)
            raw_search = []
            try:
                raw_search = fetch_tweets_search(handle, max_pages=5)
                print(f"    search   → {len(raw_search)} raw")
            except Exception as e:
                print(f"    search failed: {e}")

            raw_all = raw_timeline + raw_search
            if not raw_all:
                print("    ⚠ no tweets fetched, skipping")
                continue

            # follower count from first tweet
            follower_count = (
                normalise(raw_all[0], handle)["user"]["followers"] or 1
            )

            added = 0
            for raw in raw_all:
                t = normalise(raw, handle)
                text = t["text"]

                # ── exact-content dedup
                content_hash = hashlib.md5(text[:100].lower().encode()).hexdigest()
                if content_hash in content_hashes:
                    continue
                content_hashes.add(content_hash)

                # ── score filter
                score = compute_score(t, follower_count, handle)
                if score < 15:
                    continue

                # ── semantic dedup (skip if very similar to what we already have)
                if is_near_duplicate(text, existing_texts):
                    continue

                # ── thread expansion
                tweet_id = t.get("tweet_id", "")
                is_thread_tweet = any(m in text for m in ["1/", "1)", "🧵", "thread"])
                if tweet_id and is_thread_tweet:
                    stitched = fetch_thread(tweet_id)
                    if stitched:
                        text = stitched
                        t["text"] = stitched

                existing_texts.append(text)
                all_tweets.append({
                    "id":            generate_id(handle, text),
                    "creator":       t["user"]["name"],
                    "handle":        handle,
                    "avatar":        t["user"]["profile_image"],
                    "category":      category,
                    "content":       text,
                    "likes":         t["likes"],
                    "retweets":      t["retweets"],
                    "tweeted_at":    t["created_at"],
                    "quality_score": score,
                    "is_thread":     is_thread_tweet,
                    "tags":          [],
                })
                added += 1

            print(f"    ✓ kept {added} tweets  (running total: {len(all_tweets)})")

    # ── sort by quality, keep top 1 500
    all_tweets.sort(key=lambda x: x["quality_score"], reverse=True)
    all_tweets = all_tweets[:1500]

    output = {
        "last_updated": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "total":        len(all_tweets),
        "tweets":       all_tweets,
    }

    with open("tweets.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅  Done! Saved {len(all_tweets)} tweets to tweets.json")


if __name__ == "__main__":
    main()