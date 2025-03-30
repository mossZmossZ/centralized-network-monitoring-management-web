import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { FaBars, FaTimes } from "react-icons/fa";
import { useAuth } from "../../hooks/useAuth";

export default function MobileNavbar() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [location]);

  const handleMobileNavigation = (path) => {
    setIsMobileMenuOpen(false);
    navigate(path);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login"; // 🔁 force refresh logout
  };

  return (
    <div className="md:hidden">
      <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="btn btn-ghost">
        {isMobileMenuOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
      </button>

      {isMobileMenuOpen && (
        <div className="fixed inset-0 z-50 bg-white/50 backdrop-blur-md flex flex-col p-6">
          <ul className="menu menu-vertical text-lg">
            <li>
              <button onClick={() => setIsMobileMenuOpen(false)} className="text-right text-xl">
                &times;
              </button>
            </li>

            {!isAuthenticated ? (
              <li>
                <button onClick={() => handleMobileNavigation("/login")}>Login</button>
              </li>
            ) : (
              <>
                <li><button onClick={() => handleMobileNavigation("/maintenance")}>Maintenance</button></li>
                <li><button onClick={() => handleMobileNavigation("/report")}>Report</button></li>
                <li><button onClick={() => handleMobileNavigation("/alert")}>Alert</button></li>
                <li><button onClick={() => handleMobileNavigation("/services")}>Services</button></li>
                <li><button onClick={() => handleMobileNavigation("/setting")}>Setting</button></li>

                <li className="font-bold">Menu</li>
                <li><button onClick={() => handleMobileNavigation("/user")}>User</button></li>
                {/*<li><button onClick={() => handleMobileNavigation("/docs")}>Docs</button></li>*/}
                <li><button onClick={() => handleMobileNavigation("/about")}>About</button></li>

                <li className="mt-4">
                  <button onClick={handleLogout} className="btn btn-error w-full">
                    Logout
                  </button>
                </li>
              </>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}
