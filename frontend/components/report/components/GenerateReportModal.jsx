import { useState } from "react";
import axios from "axios";
import Swal from "sweetalert2";

export function GenerateReportModal({ setIsGenerateModalOpen }) {
  const [reportType, setReportType] = useState("Daily-Report");
  const [date, setDate] = useState("");  // New state for the date input

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
        // Show loading spinner using SweetAlert2
        Swal.fire({
          title: 'Generating report...',
          text: 'Please wait while we generate your report.',
          icon: 'info',
          allowOutsideClick: false,  // Disable closing the modal until report is done
          didOpen: () => {
            Swal.showLoading();  // Show loading spinner
          },
        });

        // Determine the correct API endpoint based on the selected report type
        let apiUrl = "";
        if (reportType === "Daily-Report") {
          apiUrl = "http://localhost:8000/custom-daily-report";
        } else if (reportType === "Weekly-Report") {
          apiUrl = "http://localhost:8000/custom-weekly-report";
        } else if (reportType === "Monthly-Report") {
          apiUrl = "http://localhost:8000/custom-monthly-report";
        }

        // Send Axios request to generate the report
        const response = await axios.post(apiUrl, {
          date: date,  // Send the date entered in the input field
        });

        // Close the loading spinner and show success message
        Swal.close();  // Close the loading spinner
        Swal.fire("Success!", `${response.data.message}`, "success");

        // Close the modal
        setIsGenerateModalOpen(false);
      } catch (error) {
        // Close the loading spinner and show error message
        Swal.close();  // Close the loading spinner
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

        {/* Input field for the date */}
        <input
          type="date"
          className="input input-bordered w-full mb-4"
          value={date}
          onChange={(e) => setDate(e.target.value)}  // Update the date state
        />

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
