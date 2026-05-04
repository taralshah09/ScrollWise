import HeroSection from "@/components/HeroSection";
import TweetWall from "@/components/TweetWall";

export default function Home() {
  return (

    <main className="flex w-full min-h-screen items-start justify-center">
      <div className="relative w-full max-w-7xl min-h-screen overflow-x-hidden">
        <div className="relative z-10 py-8 px-4 md:py-12 md:px-8 lg:px-16 mx-auto">
          <HeroSection />
          <TweetWall />
        </div>
      </div>
    </main>
  );
}
