const LogsPanel = ({ data, status }) => {
  if (status !== "PASSED") return null;

  return (
    <div className="bg-sky-50 rounded-3xl p-8 shadow-xl border border-sky-200">
      <h2 className="text-xl font-semibold mb-6 text-sky-700">
        Execution Logs
      </h2>

      <div className="space-y-2 text-sm">
        <p>Cloning repository...</p>
        <p>Running tests...</p>
        <p>Applying fixes...</p>
        <p>Monitoring CI/CD...</p>
        <p>All tests passing ✔</p>
      </div>
    </div>
  );
};

export default LogsPanel;