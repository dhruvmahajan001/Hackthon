import { useState } from "react";

const Auth = ({ setIsAuthenticated }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleAuth = () => {
    if (!email || !password) return;

    localStorage.setItem("auth", "true");
    setIsAuthenticated(true);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-100 via-white to-sky-100">
      <div className="bg-white rounded-3xl shadow-2xl p-10 w-96 border border-gray-200">
        <h2 className="text-2xl font-bold mb-6 text-center text-indigo-600">
          {isLogin ? "Login" : "Sign Up"}
        </h2>

        <div className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            className="w-full border rounded-xl px-4 py-3"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full border rounded-xl px-4 py-3"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button
            onClick={handleAuth}
            className="w-full bg-indigo-600 text-white py-3 rounded-xl font-medium"
          >
            {isLogin ? "Login" : "Create Account"}
          </button>

          <p
            className="text-sm text-center text-indigo-600 cursor-pointer"
            onClick={() => setIsLogin(!isLogin)}
          >
            {isLogin
              ? "Don't have an account? Sign up"
              : "Already have an account? Login"}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Auth;