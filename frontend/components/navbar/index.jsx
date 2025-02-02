import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <div className="navbar bg-base-100">
      <div className="flex-1">
        <Link to="/" className="btn btn-ghost text-xl">Monitoring Management</Link>
      </div>
      <div className="flex-none">
        <ul className="menu menu-horizontal px-1">
          <li><Link to="/report">Report</Link></li>
          <li><Link to="/alert">Alert</Link></li>
          <li><Link to="/systems">Systems</Link></li>
          <li><Link to="/setting">Setting</Link></li>
          <li>
            <details>
              <summary>Feature</summary>
              <ul className="bg-base-100 rounded-t-none p-2">
                <li><Link to="/docs">Password leak</Link></li>
              </ul>
            </details>
          </li>
          <li>
            <details>
              <summary>Menu</summary>
              <ul className="bg-base-100 rounded-t-none p-2">
                <li><Link to="/user">User</Link></li>
                <li><Link to="/docs">Docs</Link></li>
                <li><Link to="/about">About</Link></li>
              </ul>
            </details>
          </li>
        </ul>
      </div>
    </div>
  );
}
