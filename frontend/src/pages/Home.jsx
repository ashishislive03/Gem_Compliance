import React from "react";
import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import CapabilitiesSection from "../components/CapabilitiesSection";
import HowItWorksSection from "../components/HowItWorksSection";
import ImpactSection from "../components/ImpactSection";
import Footer from "../components/Footer";

export default function Home({ onLaunch }) {
  return (
    <div className="min-h-screen bg-[#F7F6F1]">
      <Navbar onLaunch={onLaunch} />
      <Hero onLaunch={onLaunch} />
      <CapabilitiesSection />
      <HowItWorksSection />
      <ImpactSection onLaunch={onLaunch} />
      <Footer />
    </div>
  );
}