const Header = ({ status, onLogout }) => {
  return (
    <div className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-8 py-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-indigo-600">
          Autonomous CI/CD Healing Agent
        </h1>

        <div className="flex items-center gap-4">
          <span className={`px-4 py-2 rounded-full text-sm font-semibold
            ${status === "PASSED" ? "bg-green-200 text-green-700" :
              status === "RUNNING" ? "bg-yellow-200 text-yellow-700" :
              "bg-gray-200 text-gray-600"}`}>
            {status}
          </span>

          <button
            onClick={onLogout}
            className="bg-red-100 text-red-600 px-4 py-2 rounded-xl text-sm"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
};

export default Header;