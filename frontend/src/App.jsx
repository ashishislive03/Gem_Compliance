import React, { useState } from "react";
import Home from "./pages/Home";
import ComplianceDashboard from "./pages/Dashboard";
 
export default function App() {
  const [page, setPage] = useState("home"); // "home" | "dashboard"
 
  if (page === "dashboard") {
    return <ComplianceDashboard onBack={() => setPage("home")} />;
  }
  return <Home onLaunch={() => setPage("dashboard")} />;
}
 
