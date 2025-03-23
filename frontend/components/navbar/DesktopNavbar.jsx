import { useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";

export default function DesktopNavbar({ closeDropdowns }) {
  const featureRef = useRef(null);
  const menuRef = useRef(null);

  // ✅ Close dropdowns when clicking outside
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
  }, [closeDropdowns]); // ✅ Now included in dependencies

  return (
    <div className="hidden md:flex md:items-center">
      <ul className="menu menu-horizontal px-1">
        <li><Link to="/maintenance">Maintenance</Link></li>
        <li><Link to="/report">Report</Link></li>
        <li><Link to="/alert">Alert</Link></li>
        <li><Link to="/services">Services</Link></li>
        <li><Link to="/setting">Setting</Link></li>
        {/* Menu Dropdown */}
        <li>
          <details ref={menuRef}>
            <summary>Menu</summary>
            <ul className="absolute z-50 bg-white/50 backdrop-blur-md border border-gray-300 rounded-lg p-2">
              <li><Link to="/user" onClick={closeDropdowns}>User</Link></li>
              <li><Link to="/docs" onClick={closeDropdowns}>Docs</Link></li>
              <li><Link to="/about" onClick={closeDropdowns}>About</Link></li>
            </ul>
          </details>
        </li>
      </ul>
    </div>
  );
}

// ✅ Add PropTypes for ESLint validation
DesktopNavbar.propTypes = {
  closeDropdowns: PropTypes.func.isRequired,
};