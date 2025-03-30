import { useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { useAuth } from "../../hooks/useAuth";

export default function DesktopNavbar({ closeDropdowns }) {
  const featureRef = useRef(null);
  const menuRef = useRef(null);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        featureRef.current &&
        !featureRef.current.contains(event.target) &&
        menuRef.current &&
        !menuRef.current.contains(event.target)
      ) {
        closeDropdowns();
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [closeDropdowns]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login"; // 🔁 force refresh to clear state
  };

  return (
    <div className="hidden md:flex md:items-center">
      <ul className="menu menu-horizontal px-1">
        {!isAuthenticated ? (
          <li><Link to="/login">Login</Link></li>
        ) : (
          <>
            <li><Link to="/maintenance">Maintenance</Link></li>
            <li><Link to="/report">Report</Link></li>
            <li><Link to="/alert">Alert</Link></li>
            <li><Link to="/services">Services</Link></li>
            <li><Link to="/setting">Setting</Link></li>

            <li>
              <details ref={menuRef}>
                <summary>Menu</summary>
                <ul className="absolute z-50 bg-white/50 backdrop-blur-md border border-gray-300 rounded-lg p-2">
                  <li><Link to="/user" onClick={closeDropdowns}>User</Link></li>
                  {/*<li><Link to="/docs" onClick={closeDropdowns}>Docs</Link></li>}*/}
                  <li><Link to="/about" onClick={closeDropdowns}>About</Link></li>
                  <li>
                    <button onClick={handleLogout} className="text-left w-full text-red-500 hover:underline">
                      Logout
                    </button>
                  </li>
                </ul>
              </details>
            </li>
          </>
        )}
      </ul>
    </div>
  );
}

DesktopNavbar.propTypes = {
  closeDropdowns: PropTypes.func.isRequired,
};
