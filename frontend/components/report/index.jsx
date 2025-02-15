import { useState } from "react";
import { CustomReport } from "./components/CustomReport";
import { ScheduleReport } from "./components/ScheduleReport";
import { LocalFiles } from "./components/LocalFiles";

export function Report() {
  const [activeSection, setActiveSection] = useState("custom");

  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Top Navigation Bar */}
      <div className="pt-10">
        <h1></h1>
      </div>
      <div className="flex justify-center mt-4 p-2 space-x-4  border-gray-300">
        <button
          className={`btn ${
            activeSection === "custom" ? "btn-primary" : "btn-outline"
          }`}
          onClick={() => setActiveSection("custom")}
        >
          Custom Report
        </button>
        <button
          className={`btn ${
            activeSection === "schedule" ? "btn-primary" : "btn-outline"
          }`}
          onClick={() => setActiveSection("schedule")}
        >
          Schedule Report
        </button>
        <button
          className={`btn ${
            activeSection === "local" ? "btn-primary" : "btn-outline"
          }`}
          onClick={() => setActiveSection("local")}
        >
          Local Files
        </button>
      </div>

      {/* Main Content Area */}
      <div className="flex-grow flex flex-col items-start justify-start p-6">
        {activeSection === "custom" && <CustomReport />}
        {activeSection === "schedule" && <ScheduleReport />}
        {activeSection === "local" && <LocalFiles />}
      </div>
    </div>
  );
}