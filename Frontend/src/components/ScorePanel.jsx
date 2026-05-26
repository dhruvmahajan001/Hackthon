const ScorePanel = ({ data }) => {
  const base = 100;
  const speedBonus = data.timeTakenSeconds < 300 ? 10 : 0;
  const penalty = data.commitCount > 20
    ? (data.commitCount - 20) * 2
    : 0;

  const finalScore = base + speedBonus - penalty;

  return (
    <div className="bg-emerald-50 rounded-3xl p-8 shadow-xl border border-emerald-200">
      <h2 className="text-xl font-semibold mb-6 text-emerald-700">
        Score Breakdown
      </h2>

      <p>Base Score: 100</p>
      <p>Speed Bonus: +{speedBonus}</p>
      <p>Efficiency Penalty: -{penalty}</p>

      <h3 className="text-3xl font-bold mt-4 text-emerald-700">
        {finalScore} / 120
      </h3>

      <div className="w-full bg-emerald-200 rounded-full h-4 mt-4">
        <div
          className="h-full bg-emerald-500 rounded-full"
          style={{ width: `${(finalScore / 120) * 100}%` }}
        />
      </div>
    </div>
  );
};

export default ScorePanel;