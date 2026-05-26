import { useState } from "react";

const InputSection = ({ status, startRun }) => {
  const [repoUrl, setRepoUrl] = useState("");
  const [teamName, setTeamName] = useState("");
  const [leaderName, setLeaderName] = useState("");

  return (
    <div className="bg-blue-50 rounded-3xl p-8 shadow-xl border border-blue-200">
      <h2 className="text-xl font-semibold mb-6 text-blue-700">
        Run Agent
      </h2>

      <div className="space-y-4">
        <input
          type="text"
          placeholder="GitHub Repository URL"
          className="w-full border rounded-xl px-4 py-3"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
        />

        <input
          type="text"
          placeholder="Team Name"
          className="w-full border rounded-xl px-4 py-3"
          value={teamName}
          onChange={(e) => setTeamName(e.target.value)}
        />

        <input
          type="text"
          placeholder="Team Leader Name"
          className="w-full border rounded-xl px-4 py-3"
          value={leaderName}
          onChange={(e) => setLeaderName(e.target.value)}
        />

        <button
          onClick={() => startRun(repoUrl, teamName, leaderName)}
          disabled={status === "RUNNING"}
          className="w-full bg-blue-600 text-white py-3 rounded-xl font-medium"
        >
          {status === "RUNNING" ? "Running Agent..." : "Analyze Repository"}
        </button>
      </div>
    </div>
  );
};

export default InputSection;