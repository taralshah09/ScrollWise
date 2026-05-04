"use client";

import React from "react";
import type { Tweet } from "../lib/tweets";

interface TweetCardProps {
  tweet: Tweet;
}

export default function TweetCard({ tweet }: TweetCardProps) {
  const openTweet = () => {
    if (!tweet.tweetId) return;
    const handle = tweet.authorHandle.replace("@", "");
    window.open(`https://x.com/${handle}/status/${tweet.tweetId}`, "_blank");
  };

  return (
    <button
      onClick={openTweet}
      className={`neo-button p-5 md:p-6 gap-3 md:gap-4 h-max mb-6 text-left transition-all hover:scale-[1.01] active:scale-[0.99] ${tweet.isFeatured ? "border-[#d1d1d1] shadow-[4px_4px_0_0_#d1d1d1] md:shadow-[6px_6px_0_0_#d1d1d1]" : ""}`}
    >

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 md:gap-3">
          <img
            src={tweet.authorAvatar}
            alt={tweet.authorName}
            className="w-8 h-8 md:w-10 md:h-10 rounded-full object-cover border border-[var(--border-glass)] bg-zinc-800"
          />
          <div className="flex flex-col text-left">
            <span className="font-bold text-sm md:text-base text-[var(--text-primary)] leading-tight">{tweet.authorName}</span>
            <span className="text-[10px] md:text-xs font-mono text-[var(--text-secondary)]">{tweet.authorHandle}</span>
          </div>
        </div>
      </div>

      <p className={`text-left text-[var(--text-primary)] leading-relaxed whitespace-pre-wrap ${tweet.isFeatured ? "text-lg md:text-2xl font-medium" : "text-sm md:text-base"}`}>
        {tweet.text}
      </p>

      <div className="flex items-center justify-between mt-2 pt-4 border-t border-[var(--border-glass)] text-[10px] md:text-xs font-mono text-[var(--text-secondary)]">
        <div className="flex items-center gap-3 md:gap-4">
          <span className="flex items-center gap-1.5 hover:text-white transition-colors cursor-default">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" className="w-3.5 h-3.5 md:w-4 md:h-4" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            {tweet.likes.toLocaleString()}
          </span>
          <span className="flex items-center gap-1.5 hover:text-white transition-colors cursor-default">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" className="w-3.5 h-3.5 md:w-4 md:h-4" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
            </svg>
            {tweet.retweets.toLocaleString()}
          </span>
        </div>
        {/* <span>{tweet.date}</span> */}
      </div>
    </button>

  );
}
