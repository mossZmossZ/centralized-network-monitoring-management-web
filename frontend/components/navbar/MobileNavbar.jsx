import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { FaBars, FaTimes } from "react-icons/fa";

export default function MobileNavbar() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  // Close mobile menu when route changes
  useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [location]);

  // Handle navigation
  const handleMobileNavigation = (path) => {
    setIsMobileMenuOpen(false);
    navigate(path);
  };

  return (
    <div className="md:hidden">
      {/* Mobile Menu Icon */}
      <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="btn btn-ghost">
        {isMobileMenuOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
      </button>

      {/* Mobile Fullscreen Menu */}
      {isMobileMenuOpen && (
        <div className="fixed inset-0 z-50 bg-white/50 backdrop-blur-md flex flex-col p-6">
          <ul className="menu menu-vertical text-lg">
            <li>
              <button onClick={() => setIsMobileMenuOpen(false)} className="text-right text-xl">
                &times;
              </button>
            </li>
            <li><button onClick={() => handleMobileNavigation("/maintenance")}>Maintenance</button></li>
            <li><button onClick={() => handleMobileNavigation("/report")}>Report</button></li>
            <li><button onClick={() => handleMobileNavigation("/alert")}>Alert</button></li>
            <li><button onClick={() => handleMobileNavigation("/services")}>Services</button></li>
            <li><button onClick={() => handleMobileNavigation("/setting")}>Setting</button></li>
            
            
            {/* Menu Section */}
            <li className="font-bold">Menu</li>
            <li><button onClick={() => handleMobileNavigation("/user")}>User</button></li>
            <li><button onClick={() => handleMobileNavigation("/docs")}>Docs</button></li>
            <li><button onClick={() => handleMobileNavigation("/about")}>About</button></li>
          </ul>
        </div>
      )}
    </div>
  );
}