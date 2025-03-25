import { Link } from "react-router-dom";

export default function Main() {
  return (
    <main className="flex flex-col items-center justify-center flex-grow p-3">
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
        <Link to="/setting" className="card bg-base-200 shadow-md p-6 hover:shadow-lg hover:scale-105 transition-transform">
          <h2 className="text-xl font-semibold">System Management</h2>
          <p className="text-gray-500">Edit configuration files, start stop restart services, and monitor system status with up down logs for seamless network operations.</p>
        </Link>
      </div>
      
      {/* Cards Section-2 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8 w-full max-w-5xl">
        {/* Report System Card */}
        <Link to="/services" className="card bg-base-200 shadow-md p-6 hover:shadow-lg hover:scale-105 transition-transform">
          <h2 className="text-xl font-semibold">Guidelines from ISO/IEC 27001</h2>
          <p className="text-gray-500">
          <strong>8 Operation</strong><br />
          &nbsp;A.8.15 Logging<br />
          &nbsp;A.8.16 Monitoring activities<br />
          &nbsp;A.8.20 Network Security<br />
          &nbsp;A.8.21 Security of Network Services<br />
          &nbsp; A.8.22 Segregation of Networks<br />
          <strong>9 Performance Evaluation</strong><br />
          &nbsp; A.9.1 Monitoring, Measurement, Analysis and Evaluation<br />
          &nbsp;A.9.2 Internal Audit<br />
          <strong>10 Improvement</strong><br />
          &nbsp; A.10.2 Nonconformity and Corrective Action
          </p>
        </Link>


        {/* Alert System Card */}
        <Link to="/services" className="card bg-base-200 shadow-md p-6 hover:shadow-lg hover:scale-105 transition-transform">
            <h2 className="text-xl font-semibold">Guidelines from TIA-942</h2>
            <p className="text-gray-500">
              <strong>Redundant Cabling</strong><br />
              Monitoring and alerting on network link status and availability<br />
              <strong>Access Control & CCTV</strong><br />
              If the data center includes IP cameras or access control systems,can monitor their status<br />
              <strong>HVAC, Fire Protection, Redundant Power</strong><br />
              monitor UPS, air conditioning, and power systems in the data center
              alerting system to notify administrators about temperature anomalies or power failures
            </p>
          </Link>
      </div>
      {/* Docs*/}
      <div className="mt-5">
        <Link to="/docs">
          <button className="btn btn-primary mt-4">View Docs</button>
        </Link>
      </div>
    </main>
  );
}
