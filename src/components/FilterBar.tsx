"use client";

import React from "react";

interface FilterBarProps {
  activeWriter: string;
  onSelectWriter: (writer: string) => void;
  writers: string[];
}

export default function FilterBar({ activeWriter, onSelectWriter, writers }: FilterBarProps) {
  return (
    <div className="w-full mb-8 md:mb-12">
      <div className="flex overflow-x-auto sm:flex-wrap gap-2 md:gap-3 justify-start sm:justify-center pb-4 sm:pb-0 hide-scrollbar px-2 sm:px-0">
        {writers.map((writer) => {
          const isActive = writer === activeWriter;
          return (
            <button
              key={writer}
              onClick={() => onSelectWriter(writer)}
              className={`px-4 py-2 rounded-xl whitespace-nowrap text-xs md:text-sm font-semibold transition-all duration-300 border shrink-0 ${
                isActive
                  ? "bg-[var(--accent)] text-white border-[var(--accent)] shadow-[0_8px_20px_rgba(79,142,247,0.3)] scale-105"
                  : "bg-[var(--bg-glass)] text-[var(--text-secondary)] border-[var(--border-glass)] hover:border-[var(--accent)] hover:text-white hover:bg-[rgba(255,255,255,0.08)]"
              } backdrop-blur-xl`}
            >
              {writer}
            </button>
          );
        })}
      </div>
    </div>
  );
}
