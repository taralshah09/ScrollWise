"use client";

import React from "react";

export default function HeroSection() {
  return (
    <div className="flex flex-col items-center justify-center text-center py-20 px-4 animate-fade-in">
      <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-4 text-white drop-shadow-lg font-sans">
        ScrollWise
      </h1>
      <p className="text-lg md:text-xl text-[var(--text-secondary)] font-medium max-w-lg mx-auto">
        "The internet's best thinkers. Curated daily."
      </p>
    </div>
  );
}
