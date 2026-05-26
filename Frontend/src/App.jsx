import { useState, useEffect } from "react";
import Header from "./components/Header";
import InputSection from "./components/InputSection";
import RunSummaryCard from "./components/RunSummaryCard";
import ScorePanel from "./components/ScorePanel";
import FixesTable from "./components/FixesTable";
import Timeline from "./components/Timeline";
import LogsPanel from "./components/LogsPanel";
import Auth from "./components/Auth";

function App() {
  const [status, setStatus] = useState("IDLE");
  const [runResult, setRunResult] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("auth");
    if (saved === "true") setIsAuthenticated(true);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("auth");
    setIsAuthenticated(false);
  };

  const startMockRun = (repoUrl, teamName, leaderName) => {
    setStatus("RUNNING");

    const branch =
      `${teamName.toUpperCase().replace(/\s/g, "_")}_` +
      `${leaderName.toUpperCase().replace(/\s/g, "_")}_AI_Fix`;

    setTimeout(() => {
      const mockResult = {
        repoUrl,
        teamName,
        leaderName,
        branch,
        totalFailures: 3,
        totalFixes: 3,
        commitCount: 22,
        timeTakenSeconds: 240,
        status: "PASSED",
        iterations: [
          { status: "FAILED", timestamp: "19:10:12" },
          { status: "FAILED", timestamp: "19:12:45" },
          { status: "PASSED", timestamp: "19:14:02" }
        ],
        fixes: [
          {
            file: "src/utils.py",
            bugType: "LINTING",
            line: 15,
            commit: "[AI-AGENT] Remove unused import",
            status: "Fixed"
          }
        ]
      };

      setRunResult(mockResult);
      setStatus("PASSED");
    }, 2500);
  };

  if (!isAuthenticated) {
    return <Auth setIsAuthenticated={setIsAuthenticated} />;
  }

  return (
    <div className="min-h-screen">
      <Header status={status} onLogout={handleLogout} />

      <div className="max-w-7xl mx-auto px-8 py-10 space-y-8">
        <InputSection status={status} startRun={startMockRun} />

        {runResult && (
          <>
            <RunSummaryCard data={runResult} />
            <ScorePanel data={runResult} />
            <FixesTable data={runResult} />
            <Timeline data={runResult} />
            <LogsPanel data={runResult} status={status} />
          </>
        )}
      </div>
    </div>
  );
}

export default App;