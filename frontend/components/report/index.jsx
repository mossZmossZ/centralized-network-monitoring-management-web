import { useState } from "react";
import { CustomReport } from "./components/CustomReport";
import { ScheduleReport } from "./components/ScheduleReport";
import { LocalFiles } from "./components/LocalFiles";

export function Report() {
  const [activeSection, setActiveSection] = useState("custom");

  return (
    <div className="flex flex-col h-screen ">
      {/* Top Navigation Bar */}
      <div className="pt-10">
        <h1></h1>
      </div>
      <div className="flex justify-left  p-1 space-x-4  ml-8 border-gray-300">
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
          Schedule
        </button>
        <button
          className={`btn ${
            activeSection === "local" ? "btn-primary" : "btn-outline"
          }`}
          onClick={() => setActiveSection("local")}
        >
          Local
        </button>
      </div>

      {/* Main Content Area */}
      <div className="flex justify-center mt-4 p-2 space-x-4 border-gray-300">
        {activeSection === "custom" && <CustomReport />}
        {activeSection === "schedule" && <ScheduleReport />}
        {activeSection === "local" && <LocalFiles />}
      </div>
    </div>
  );
}