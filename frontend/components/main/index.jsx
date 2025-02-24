import { Link } from "react-router-dom";

export default function Main() {
  return (
    <main className="flex flex-col items-center justify-center flex-grow p-6">
      {/* Hero Section */}
      <div className="text-center">
        <h1 className="text-4xl font-bold">Welcome to Centralize Network Monitoring</h1>
        <p className="mt-2 text-lg text-gray-600">
          We provide Monitoring Infrastructure related with ISO 27001, TIA-942 standard.
        </p>
        <Link to="/login">
          <button className="btn btn-primary mt-4">Get Started</button>
        </Link>
      </div>

      {/* Cards Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8 w-full max-w-4xl">
        {/* Report System Card */}
        <Link to="/report" className="card bg-base-200 shadow-md p-6 hover:shadow-lg hover:scale-105 transition-transform">
          <h2 className="text-xl font-semibold">Report System</h2>
          <p className="text-gray-500">Generate scheduled reports and customize time range reports. Reports comply with ISO 27001 and TIA-942 standards for security and infrastructure.</p>
        </Link>

        {/* Alert System Card */}
        <Link to="/alert" className="card bg-base-200 shadow-md p-6 hover:shadow-lg hover:scale-105 transition-transform">
          <h2 className="text-xl font-semibold">Alert System</h2>
          <p className="text-gray-500">Manage alerts efficiently with a dashboard for viewing previous alerts. Create and send alert messages for quick incident response.</p>
        </Link>

        {/* System Management Card */}
        <Link to="/systems" className="card bg-base-200 shadow-md p-6 hover:shadow-lg hover:scale-105 transition-transform">
          <h2 className="text-xl font-semibold">System Management</h2>
          <p className="text-gray-500">Edit configuration files, start stop restart services, and monitor system status with up down logs for seamless network operations.</p>
        </Link>
      </div>
      <div className="mt-5">
        <Link to="/docs">
          <button className="btn btn-primary mt-4">View Docs</button>
        </Link>
      </div>
    </main>
  );
}
