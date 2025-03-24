import { useState } from "react";
import axios from "axios";
import Swal from "sweetalert2";

export function GenerateReportModal({ setIsGenerateModalOpen }) {
  const [reportType, setReportType] = useState("Daily-Report");

  // Handle the report generation
  const handleGenerateReport = async (e) => {
    // Prevent any default action, in case it's coming from a form submit
    e.preventDefault();
  
    // Get today's date adjusted to GMT+7 (Thailand Time Zone)
    const today = new Date();
    const options = { timeZone: "Asia/Bangkok", year: "numeric", month: "2-digit", day: "2-digit" };
    const todayDate = today.toLocaleDateString("en-GB", options).split("/").reverse().join("-");  // Format as YYYY-MM-DD
  
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
          date: todayDate,  // Send today's date as the date (in GMT+7 timezone)
        });
  
        // Close the loading spinner and show success message
        Swal.close();  // Close the loading spinner
        const successResult = await Swal.fire("Success!", `${response.data.message}`, "success");
  
        if (successResult.isConfirmed) {
          // Refresh the page only after the user clicks "OK"
          window.location.reload();  // Refresh the page
        }

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
