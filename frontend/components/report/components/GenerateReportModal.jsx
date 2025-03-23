import { useState } from "react";
import axios from "axios";
import Swal from "sweetalert2";

export function GenerateReportModal({ setIsGenerateModalOpen }) {
  const [reportType, setReportType] = useState("Daily-Report");

  // Handle the report generation
  const handleGenerateReport = async () => {
    // Show SweetAlert2 confirmation dialog
    const result = await Swal.fire({
      title: "Are you sure?",
      text: `You are about to generate a ${reportType}. Proceed?`,
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Yes, generate it!",
      cancelButtonText: "Cancel",
    });

    if (result.isConfirmed) {
      try {
        // Send Axios request to generate the report
        await axios.post("http://localhost:8000/api/report/generate", {
          report_type: reportType,
        });

        // Show success message
        Swal.fire("Success!", `${reportType} generated successfully!`, "success");

        // Close the modal
        setIsGenerateModalOpen(false);
      } catch (error) {
        Swal.fire("Error!", `Error generating the report: ${error.message}`, "error");
      }
    }
  };

  return (
    <div className="fixed inset-0 flex justify-center items-center bg-gray-700 bg-opacity-50">
      <div className="bg-white p-6 rounded-lg shadow-lg w-80">
        <h3 className="font-bold text-xl mb-4">Generate Report</h3>
        
        {/* Dropdown to select report type */}
        <select
          className="select select-bordered w-full mb-4"
          value={reportType}
          onChange={(e) => setReportType(e.target.value)}
        >
          <option value="Daily-Report">Daily Report</option>
          <option value="Weekly-Report">Weekly Report</option>
          <option value="Monthly-Report">Monthly Report</option>
        </select>

        <div className="flex justify-end space-x-4">
          {/* Close Button */}
          <button
            className="btn btn-secondary"
            onClick={() => setIsGenerateModalOpen(false)} // Close the modal
          >
            Close
          </button>

          {/* Generate Report Button */}
          <button
            className="btn btn-success"
            onClick={handleGenerateReport} // Generate the report
          >
            Generate Report
          </button>
        </div>
      </div>
    </div>
  );
}
