const Timeline = ({ data }) => {
  return (
    <div className="bg-violet-50 rounded-3xl p-8 shadow-xl border border-violet-200">
      <h2 className="text-xl font-semibold mb-6 text-violet-700">
        CI/CD Timeline ({data.iterations.length}/5)
      </h2>

      {data.iterations.map((run, i) => (
        <div key={i} className="flex justify-between mb-3">
          <span>Iteration {i + 1}</span>
          <span>{run.status}</span>
          <span>{run.timestamp}</span>
        </div>
      ))}
    </div>
  );
};

export default Timeline;