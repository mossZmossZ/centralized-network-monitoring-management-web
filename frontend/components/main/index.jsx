import { Link } from "react-router-dom";

export default function Main() {
    return (
      <main className="flex flex-col items-center justify-center flex-grow p-6">
        {/* Hero Section */}
        <div className="text-center">
          <h1 className="text-4xl font-bold">Welcome to Centralize Network Monitoring</h1>
          <p className="mt-2 text-lg text-gray-600">
            We provide Monitoring Infrastructure related with ISO 27001 , TIA-942 standard.
          </p>
          <button className="btn btn-primary mt-4">
            <Link to="/login">Get Started</Link>
            </button>
        </div>
  
        {/* Cards Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8 w-full max-w-4xl">
          <div className="card bg-base-200 shadow-md p-6">
            <h2 className="text-xl font-semibold">Report system</h2>
            <p className="text-gray-500">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
          </div>
          <div className="card bg-base-200 shadow-md p-6">
            <h2 className="text-xl font-semibold">Alert system</h2>
            <p className="text-gray-500">Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
          </div>
          <div className="card bg-base-200 shadow-md p-6">
            <h2 className="text-xl font-semibold">password leak check</h2>
            <p className="text-gray-500">Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.</p>
          </div>
        </div>

        <button className="btn btn-primary mt-4">
            <Link to="/docs">Docs</Link>
            </button>
      </main>
    );
  }
  