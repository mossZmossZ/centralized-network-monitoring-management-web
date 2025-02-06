import { useEffect, useRef } from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  const featureRef = useRef(null);
  const menuRef = useRef(null);

  // Function to close all dropdowns
  const closeDropdowns = () => {
    if (featureRef.current) featureRef.current.removeAttribute("open");
    if (menuRef.current) menuRef.current.removeAttribute("open");
  };

  // Click outside handler
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        featureRef.current && !featureRef.current.contains(event.target) &&
        menuRef.current && !menuRef.current.contains(event.target)
      ) {
        closeDropdowns();
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div className="navbar bg-base-100">
      <div className="flex-1">
        <Link to="/" className="btn btn-ghost text-xl">Monitoring Management</Link>
      </div>
      <div className="flex-none">
        <ul className="menu menu-horizontal px-1">
          <li><Link to="/report">Report</Link></li>
          <li><Link to="/alert">Alert</Link></li>
          <li><Link to="/systems">System</Link></li>
          <li><Link to="/setting">Setting</Link></li>
          
          {/* Feature Dropdown */}
          <li>
            <details ref={featureRef}>
              <summary>Feature</summary>
              <ul className="bg-base-100 rounded-t-none p-2">
                <li><Link to="/docs" onClick={closeDropdowns}>Password leak</Link></li>
              </ul>
            </details>
          </li>

          {/* Menu Dropdown */}
          <li>
            <details ref={menuRef}>
              <summary>Menu</summary>
              <ul className="bg-base-100 rounded-t-none p-2">
                <li><Link to="/user" onClick={closeDropdowns}>User</Link></li>
                <li><Link to="/docs" onClick={closeDropdowns}>Docs</Link></li>
                <li><Link to="/about" onClick={closeDropdowns}>About</Link></li>
              </ul>
            </details>
          </li>
        </ul>
      </div>
    </div>
  );
}