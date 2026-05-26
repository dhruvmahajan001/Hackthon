import InputSection from "./InputSection";
import SummaryCards from "./RunSummaryCard";
import AnalyticsSection from "./AnalyticsSection";
import LogsPanel from "./LogsPanel";

const Dashboard = ({ status, setStatus }) => {
  return (
    <div className="space-y-10">
      <InputSection status={status} setStatus={setStatus} />
      <SummaryCards status={status} />
      <AnalyticsSection />
      <LogsPanel status={status} setStatus={setStatus} />
    </div>
  );
};

export default Dashboard;
