import { motion } from "framer-motion";
import { useState } from "react";
import axios from "axios";


export function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  

  // ✅ Use VITE_API_URL from .env file
  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

  const handleLogin = async (e) => {
    e.preventDefault(); // ✅ Prevent default form reload

    try {
      // Use VITE_API_URL dynamically
      const res = await axios.post(
        `${API_URL}/auth/token`, // Dynamically use API URL
        new URLSearchParams({
          username,
          password,
        }),
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      localStorage.setItem("token", res.data.access_token);
      window.location.href = "/services";
    } catch (err) {
      setError("Invalid credentials");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-[#faf7f5] via-[#f1f2f4] to-[#e8eaed] p-4">
      <motion.div
        className="bg-white shadow-2xl rounded-2xl p-8 w-full max-w-md"
        initial={{ opacity: 0, y: 80 }}
        animate={{ opacity: 1, y: -100 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
      >
        <h2 className="text-2xl font-semibold text-center text-gray-800 mb-6">
          Welcome to Centralized Network Monitoring
        </h2>

        {error && <p className="text-red-500 text-sm text-center mb-4">{error}</p>}

        {/* ✅ Wrap in form to capture Enter key */}
        <form onSubmit={handleLogin}>
          <div className="form-control w-full mb-4">
            <label className="label">
              <span className="label-text">Username</span>
            </label>
            <input
              type="text"
              placeholder="Enter your username"
              className="input input-bordered w-full"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="form-control w-full mb-6">
            <label className="label">
              <span className="label-text">Password</span>
            </label>
            <input
              type="password"
              placeholder="Enter your password"
              className="input input-bordered w-full"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="btn btn-primary w-full">
            Login
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-gray-500">
          Don’t have an account?{" "}
          <a href="#" className="text-purple-600 hover:underline">
            Tell Admin
          </a>
        </p>
      </motion.div>
    </div>
  );
}
