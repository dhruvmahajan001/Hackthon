const RunSummaryCard = ({ data }) => {
  return (
    <div className="bg-indigo-50 rounded-3xl p-8 shadow-xl border border-indigo-200">
      <h2 className="text-xl font-semibold mb-6 text-indigo-700">
        Run Summary
      </h2>

      <div className="grid grid-cols-2 gap-6 text-sm">
        <p><b>Repository:</b> {data.repoUrl}</p>
        <p><b>Team:</b> {data.teamName}</p>
        <p><b>Leader:</b> {data.leaderName}</p>
        <p><b>Branch:</b> {data.branch}</p>
        <p><b>Total Failures:</b> {data.totalFailures}</p>
        <p><b>Total Fixes:</b> {data.totalFixes}</p>
        <p><b>Time Taken:</b> {data.timeTakenSeconds}s</p>
        <p><b>Status:</b> {data.status}</p>
      </div>
    </div>
  );
};

export default RunSummaryCard;