import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export function User() {
  const [username, setUsername] = useState("");
  const navigate = useNavigate();
  
  const fetchUser = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const res = await axios.get("http://localhost:8000/api/auth/me", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUsername(res.data.username);
    } catch {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  useEffect(() => {
    fetchUser();
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-6">
      <div className="bg-white shadow-lg rounded-2xl p-8 max-w-sm w-full text-center">
        <img
          src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSzw-X03a5FfJMYtU9p2gQd2HNhK93FfFmFdw&s"
          alt="User Avatar"
          className="mx-auto rounded-full mb-4"
        />
        <h2 className="text-xl font-bold mb-2">Welcome</h2>
        <p className="text-gray-700 mb-6">User: {username || "..."}</p>
        <button onClick={handleLogout} className="btn btn-error w-full">
          Logout
        </button>
      </div>
    </div>
  );
}
