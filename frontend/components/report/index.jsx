import { useState } from "react";
import { CustomReport } from "./components/CustomReport";
import { ScheduleReport } from "./components/ScheduleReport";
import { LocalFiles } from "./components/LocalFiles";
import { GenerateReportModal } from "./components/GenerateReportModal"; // Modal Component for Generate Report

export function Report() {
  const [activeSection, setActiveSection] = useState("custom");
  const [isGenerateModalOpen, setGenerateModalOpen] = useState(false); // State for the modal visibility

  return (
    <div className="flex flex-col h-screen">
      {/* Top Navigation Bar */}
      <div className="pt-10">
        <h1></h1>
      </div>
      
      {/* Top Bar with Buttons */}
      <div className="flex justify-between p-1 space-x-4 ml-8 mr-10 border-gray-300">
        {/* Left Section (Custom Report, Schedule, Local) */}
        <div className="flex space-x-4">
          <button
            className={`btn ${activeSection === "custom" ? "btn-primary" : "btn-outline"}`}
            onClick={() => setActiveSection("custom")}
          >
            Custom Report
          </button>
          <button
            className={`btn ${activeSection === "schedule" ? "btn-primary" : "btn-outline"}`}
            onClick={() => setActiveSection("schedule")}
          >
            Schedule
          </button>
          <button
            className={`btn ${activeSection === "local" ? "btn-primary" : "btn-outline"}`}
            onClick={() => setActiveSection("local")}
          >
            Local
          </button>
        </div>

        {/* Right Section (Generate Report button) */}
        <div>
          <button
            className="btn btn-success"
            onClick={() => setGenerateModalOpen(true)} // Open the Generate Report modal
          >
            Generate Report
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex justify-center mt-4 p-2 space-x-4 border-gray-300">
        {activeSection === "custom" && <CustomReport />}
        {activeSection === "schedule" && <ScheduleReport />}
        {activeSection === "local" && <LocalFiles />}
      </div>

      {/* Modal for Generate Report */}
      {isGenerateModalOpen && (
        <GenerateReportModal setIsGenerateModalOpen={setGenerateModalOpen} />
      )}
    </div>
  );
}
