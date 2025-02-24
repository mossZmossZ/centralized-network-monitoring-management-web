import { useEffect, useRef, useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { FaBars, FaTimes } from "react-icons/fa";

export default function Navbar() {
  const featureRef = useRef(null);
  const menuRef = useRef(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  // Close mobile menu when route changes
  useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [location]);

  // Function to close all dropdowns
  const closeDropdowns = () => {
    if (featureRef.current) featureRef.current.removeAttribute("open");
    if (menuRef.current) menuRef.current.removeAttribute("open");
    setIsMobileMenuOpen(false);
  };

  // Function to handle navigation for mobile view
  const handleMobileNavigation = (path) => {
    navigate(path);
    setTimeout(() => {
      setIsMobileMenuOpen(false);
    }, 150); // delay of 150ms to allow navigation to occur
  };
  

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
    <nav className="navbar bg-base-100 shadow-none border-none px-4">
      <div className="flex-1">
        <Link to="/" className="btn btn-ghost text-xl">
          Monitoring Management
        </Link>
      </div>

      {/* Mobile Menu Icon */}
      <div className="md:hidden">
        <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="btn btn-ghost">
          {isMobileMenuOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
        </button>
      </div>

      {/* Desktop Version - Keep This Exactly as It Is */}
      <div className="hidden md:flex md:items-center">
        <ul className="menu menu-horizontal px-1">
          <li><Link to="/maintenance">Maintenance</Link></li>
          <li><Link to="/report">Report</Link></li>
          <li><Link to="/alert">Alert</Link></li>
          <li><Link to="/systems">System</Link></li>
          <li><Link to="/setting">Setting</Link></li>

          {/* Feature Dropdown */}
          <li>
            <details ref={featureRef}>
              <summary>Feature</summary>
              <ul className="absolute z-50 bg-white/50 backdrop-blur-md border border-gray-300 rounded-lg p-2">
                <li><Link to="/docs" onClick={closeDropdowns}>Password leak</Link></li>
              </ul>
            </details>
          </li>

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

      {/* Mobile Fullscreen Menu (Separate Dropdown Items) */}
      {isMobileMenuOpen && (
        <div className="fixed inset-0 z-50 bg-white/50 backdrop-blur-md flex flex-col md:hidden p-6">
          <ul className="menu menu-vertical text-lg">
            <li>
              <button onClick={() => setIsMobileMenuOpen(false)} className="text-right text-xl">
                &times;
              </button>
            </li>
            <li>
              <button onClick={() => handleMobileNavigation("/maintenance")}>
                Maintenance
              </button>
            </li>
            <li>
              <button onClick={() => handleMobileNavigation("/report")}>
                Report
              </button>
            </li>
            <li>
              <button onClick={() => handleMobileNavigation("/alert")}>
                Alert
              </button>
            </li>
            <li>
              <button onClick={() => handleMobileNavigation("/systems")}>
                System
              </button>
            </li>
            <li>
              <button onClick={() => handleMobileNavigation("/setting")}>
                Setting
              </button>
            </li>
            {/* Feature Section */}
            <li className="font-bold">Feature</li>
            <li>
              <button onClick={() => handleMobileNavigation("/docs")}>
                Password leak
              </button>
            </li>
            {/* Menu Section */}
            <li className="font-bold">Menu</li>
            <li>
              <button onClick={() => handleMobileNavigation("/user")}>
                User
              </button>
            </li>
            <li>
              <button onClick={() => handleMobileNavigation("/docs")}>
                Docs
              </button>
            </li>
            <li>
              <button onClick={() => handleMobileNavigation("/about")}>
                About
              </button>
            </li>
          </ul>
        </div>
      )}


    </nav>
  );
}
