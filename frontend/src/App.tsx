import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import RiskOutput from "./components/RiskOutput";
import EmergencyInfo from "./components/EmergencyInfo";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

function Home() {
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-8 text-white">
      {/* Top nav with emergency link */}
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-3xl font-bold text-white">🌪️ TropoScan</h1>
        <Link
          to="/emergency"
          className="text-sm text-blue-400 hover:underline hover:text-blue-300 transition duration-200"
        >
          🛟 Emergency Info
        </Link>
      </div>

      <UploadForm setResult={setResult} />
      {result && <RiskOutput result={result} />}
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/emergency" element={<EmergencyInfo />} />
      </Routes>
    </Router>
  );
}

export default App;
