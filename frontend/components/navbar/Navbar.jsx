import { useCallback } from "react";
import { Link } from "react-router-dom";
import DesktopNavbar from "./DesktopNavbar";
import MobileNavbar from "./MobileNavbar";

export default function Navbar() {
  // ✅ Wrap closeDropdowns in useCallback to prevent re-creation on every render
  const closeDropdowns = useCallback(() => {
    document.querySelectorAll("details[open]").forEach((el) => {
      el.removeAttribute("open");
    });
  }, []);

  return (
    <nav className="navbar bg-base-100 shadow-none border-none px-4">
      <div className="flex-1">
        <Link to="/" className="btn btn-ghost text-xl">
          Monitoring Management
        </Link>
      </div>

      {/* Mobile Navbar */}
      <MobileNavbar />

      {/* Desktop Navbar */}
      <DesktopNavbar closeDropdowns={closeDropdowns} />
    </nav>
  );
}