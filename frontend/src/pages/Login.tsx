import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { login as loginApi } from "../api/auth";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const navigate = useNavigate();

  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    setError("");
    setLoading(true);

    try {
      const response = await loginApi({
        email,
        password,
      });

      login(response.access_token);

      navigate("/dashboard");
    } catch (err) {
      setError("Invalid username or password");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-xl shadow-md w-96"
      >
        <h1 className="text-3xl font-bold text-center mb-8">
          AI DevOps Platform
        </h1>

        <input
          type="email"
          className="border w-full p-3 rounded mb-4"
          placeholder="Email"
          value={email}
          onChange={(e) =>
            setEmail(e.target.value)
          }
        />
        
        <input
          type="password"
          className="border w-full p-3 rounded mb-4"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />

        {error && (
          <div className="text-red-500 mb-4">
            {error}
          </div>
        )}

        <button
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded"
        >
          {loading ? "Signing In..." : "Login"}
        </button>
      </form>
    </div>
  );
}

