"use client";

import React, { useState, useEffect, useRef, useCallback } from "react";
import TweetCard from "./TweetCard";
import FeaturedTweet from "./FeaturedTweet";
import SkeletonCard from "./SkeletonCard";
import { fetchTweets, getAllWriters, type Tweet } from "../lib/tweets";

export default function TweetWall() {
  const [activeWriter, setActiveWriter] = useState("All");
  const [tweets, setTweets] = useState<Tweet[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [writers, setWriters] = useState<string[]>([]);
  const [isShuffling, setIsShuffling] = useState(false);
  const observerTarget = useRef<HTMLDivElement>(null);

  // Load writers once
  useEffect(() => {
    setWriters(getAllWriters());
  }, []);

  const loadTweets = useCallback(async (writer: string, pageNum: number, isNewWriter: boolean = false) => {
    setLoading(true);
    if (isNewWriter) {
      setTweets([]);
      setPage(1);
    }

    try {
      const newTweets = await fetchTweets(writer, pageNum);
      setTweets(prev => {
        if (isNewWriter) return newTweets;

        // simple deduplication
        const existingIds = new Set(prev.map(t => t.id));
        const uniqueNew = newTweets.filter(t => !existingIds.has(t.id));
        return [...prev, ...uniqueNew];
      });
    } catch (error) {
      console.error("Failed to fetch tweets:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  const shuffleTweets = useCallback(() => {
    setIsShuffling(true);

    // Artificial delay for the "wow" factor/animation
    setTimeout(() => {
      setTweets(prev => {
        const shuffled = [...prev];
        for (let i = shuffled.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
      });
      setIsShuffling(false);
    }, 600);
  }, []);


  // Initial load or writer change
  useEffect(() => {
    loadTweets(activeWriter, 1, true);
  }, [activeWriter, loadTweets]);

  // Infinite scroll intersection observer
  useEffect(() => {
    const observer = new IntersectionObserver(
      entries => {
        if (entries[0].isIntersecting && !loading && tweets.length > 0) {
          const nextPage = page + 1;
          setPage(nextPage);
          loadTweets(activeWriter, nextPage);
        }
      },
      { threshold: 0.1, rootMargin: "200px" }
    );

    if (observerTarget.current) {
      observer.observe(observerTarget.current);
    }

    return () => observer.disconnect();
  }, [loading, page, activeWriter, loadTweets, tweets.length]);

  return (
    <div className="w-full flex flex-col items-center">

      {/* Featured Big Card - Only show the very first tweet of the entire list */}
      {tweets.length > 0 && (
        <FeaturedTweet tweet={tweets[0]} />
      )}

      {tweets.length === 0 && !loading && (
        <div className="text-center py-20 text-[var(--text-secondary)]">
          No tweets found for this person.
        </div>
      )}


      {/* Masonry CSS implementation using columns - updated for responsiveness */}
      <div className="w-full columns-1 sm:columns-2 gap-4 md:gap-6 lg:gap-8 space-y-4 md:space-y-6 lg:space-y-8">
        {tweets.slice(1).map(tweet => (
          <div key={tweet.id} className="break-inside-avoid mb-4 md:mb-6 lg:mb-8">
            <TweetCard tweet={tweet} />
          </div>
        ))}
      </div>

      {(loading) && (
        <div className="w-full columns-1 sm:columns-2 gap-4 md:gap-6 lg:gap-8 mt-6">
          <div className="break-inside-avoid mb-4 md:mb-6 lg:mb-8"><SkeletonCard /></div>
          <div className="break-inside-avoid hidden sm:block mb-4 md:mb-6 lg:mb-8"><SkeletonCard /></div>
        </div>
      )}


      <div ref={observerTarget} className="h-20 w-full mt-4" />

      {/* Floating Jumble Button */}
      <button
        onClick={shuffleTweets}
        disabled={isShuffling || tweets.length === 0}
        className={`fixed bottom-8 right-8 z-[100] w-14 h-14 rounded-full flex items-center justify-center transition-all duration-500 shadow-2xl group ${isShuffling ? "scale-90 opacity-80" : "hover:scale-110 active:scale-95"
          }`}
        style={{
          background: "rgba(255, 255, 255, 0.05)",
          backdropFilter: "blur(16px)",
          border: "1px solid rgba(255, 255, 255, 0.1)",
          boxShadow: "0 0 30px rgba(79, 142, 247, 0.2), inset 0 0 10px rgba(255, 255, 255, 0.05)"
        }}
        title="Jumble Tweets"
      >
        {/* Glow Effect */}
        <div className="absolute inset-0 rounded-full bg-[var(--accent)] opacity-20 blur-xl group-hover:opacity-40 transition-opacity" />

        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.5"
          className={`w-6 h-6 text-white relative z-10 transition-transform duration-700 ${isShuffling ? "rotate-[360deg]" : "group-hover:rotate-12"}`}
        >
          <path d="M16 3h5v5" />
          <path d="M4 20L21 3" />
          <path d="M21 16v5h-5" />
          <path d="M15 15l6 6" />
          <path d="M4 4l5 5" />
        </svg>
      </button>
    </div>
  );
}
