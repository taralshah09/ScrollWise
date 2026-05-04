"use client";

import React from "react";
import type { Tweet } from "../lib/tweets";

interface FeaturedTweetProps {
  tweet: Tweet;
}

export default function FeaturedTweet({ tweet }: FeaturedTweetProps) {
  return (
    <div className="hover-3d w-full mb-12 group/main">
      <figure className="max-w-full rounded-2xl overflow-hidden shadow-2xl">
        <div className="neo-button p-5 md:p-8 gap-4 md:gap-6 h-max border-[#d1d1d1] shadow-[4px_4px_0_0_#d1d1d1] md:shadow-[6px_6px_0_0_#d1d1d1] bg-[#0a0a0a] relative overflow-hidden">
          {/* Background Glow Effect */}
          <div className="absolute top-0 right-0 w-64 h-64 bg-[var(--accent)] opacity-10 blur-[100px] pointer-events-none group-hover/main:opacity-20 transition-opacity duration-500" />

          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 relative z-10">
            <div className="flex items-center gap-3 md:gap-4">
              <img
                src={tweet.authorAvatar}
                alt={tweet.authorName}
                className="w-10 h-10 md:w-12 md:h-12 rounded-full object-cover border-2 border-[var(--accent)] bg-zinc-800"
              />
              <div className="flex flex-col">
                <span className="font-bold text-lg md:text-xl text-white leading-tight">{tweet.authorName}</span>
                <span className="text-xs md:text-sm font-mono text-[var(--accent)]">{tweet.authorHandle}</span>
              </div>
            </div>
            <div className="flex flex-row sm:flex-col items-center sm:items-end gap-2 w-full sm:w-auto">
              <span className="text-[9px] md:text-[10px] uppercase font-bold tracking-widest px-2 md:px-3 py-1 rounded bg-[var(--accent)]/10 text-[var(--accent)] border border-[var(--accent)]/20">
                Featured Insight
              </span>
            </div>
          </div>

          <p className="text-base md:text-xl font-medium text-white leading-relaxed whitespace-pre-wrap relative z-10 mt-2">
            {tweet.text}
          </p>

          <div className="flex items-center justify-between mt-2 md:mt-4 pt-4 md:pt-6 border-t border-[var(--border-glass)] text-xs md:text-sm font-mono text-[var(--text-secondary)] relative z-10">
            <div className="flex items-center gap-4 md:gap-6">
              <span className="flex items-center gap-2 hover:text-white transition-colors cursor-default">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" className="w-4 h-4 md:w-5 md:h-5" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
                {tweet.likes.toLocaleString()}
              </span>
              <span className="flex items-center gap-2 hover:text-white transition-colors cursor-default">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" className="w-4 h-4 md:w-5 md:h-5" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                </svg>
                {tweet.retweets.toLocaleString()}
              </span>
            </div>
            {/* <span className="text-[10px] md:text-xs">{tweet.date}</span> */}
          </div>
        </div>
      </figure>

      {/* 3x3 Hover Grid */}
      <div className="hover-grid absolute inset-0 z-50 grid grid-cols-3 grid-rows-3 pointer-events-none">
        {[...Array(9)].map((_, i) => (
          <div key={i} className="pointer-events-auto" />
        ))}
      </div>
    </div>
  );
}

