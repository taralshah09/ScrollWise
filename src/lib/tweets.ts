import tweetsData from "../../public/tweets.json";

export interface Tweet {
  id: string;
  text: string;
  authorName: string;
  authorHandle: string;
  authorAvatar: string;
  date: string;
  likes: number;
  retweets: number;
  category: string;
  tweetId: string;
  isFeatured?: boolean;
}

const ALL_TWEETS_BASE: Tweet[] = tweetsData.tweets.map(t => ({
  id: t.id,
  text: t.content,
  authorName: t.creator,
  authorHandle: t.handle.startsWith('@') ? t.handle : `@${t.handle}`,
  authorAvatar: t.avatar,
  date: t.tweeted_at,
  likes: t.likes,
  retweets: t.retweets,
  category: t.category,
  tweetId: (t as any).tweet_id || t.id,
}));

function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

const ALL_TWEETS = ALL_TWEETS_BASE;


export async function fetchTweets(writer: string = "All", page: number = 1): Promise<Tweet[]> {
  // Simulating an API call
  return new Promise((resolve) => {
    setTimeout(() => {
      let filtered = ALL_TWEETS;
      if (writer !== "All") {
        filtered = ALL_TWEETS.filter(t => t.authorName === writer);
      }

      const ITEMS_PER_PAGE = 10;
      const start = (page - 1) * ITEMS_PER_PAGE;
      const end = page * ITEMS_PER_PAGE;

      resolve(filtered.slice(start, end));
    }, 500);
  });
}


export function getAllWriters(): string[] {
  const writers = new Set(ALL_TWEETS.map(t => t.authorName));
  return ["All", ...Array.from(writers).sort()];
}
