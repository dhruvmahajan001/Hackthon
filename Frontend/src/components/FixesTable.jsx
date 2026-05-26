const FixesTable = ({ data }) => {
  return (
    <div className="bg-white rounded-3xl p-8 shadow-xl border">
      <h2 className="text-xl font-semibold mb-6">
        Fixes Applied
      </h2>

      <table className="w-full text-sm">
        <thead>
          <tr className="border-b">
            <th>File</th>
            <th>Bug Type</th>
            <th>Line Number</th>
            <th>Commit Message</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {data.fixes.map((fix, i) => (
            <tr key={i} className="border-b">
              <td>{fix.file}</td>
              <td>{fix.bugType}</td>
              <td>{fix.line}</td>
              <td>{fix.commit}</td>
              <td>
                {fix.status === "Fixed" ? "✓ Fixed" : "✗ Failed"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FixesTable;