"use client";

import React from "react";

export default function SkeletonCard() {
  return (
    <div className="glass-card p-6 flex flex-col gap-4 animate-pulse">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-[var(--border-glass)]" />
        <div className="flex flex-col gap-2">
          <div className="w-24 h-4 bg-[var(--border-glass)] rounded" />
          <div className="w-16 h-3 bg-[var(--border-glass)] rounded" />
        </div>
      </div>
      <div className="flex flex-col gap-2 mt-2">
        <div className="w-full h-4 bg-[var(--border-glass)] rounded" />
        <div className="w-full h-4 bg-[var(--border-glass)] rounded" />
        <div className="w-3/4 h-4 bg-[var(--border-glass)] rounded" />
      </div>
      <div className="mt-4 flex gap-4">
        <div className="w-12 h-3 bg-[var(--border-glass)] rounded" />
        <div className="w-12 h-3 bg-[var(--border-glass)] rounded" />
      </div>
    </div>
  );
}
