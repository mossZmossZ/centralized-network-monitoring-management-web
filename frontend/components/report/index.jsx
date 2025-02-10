import { useState, useEffect } from "react";
import axios from "axios";

export function Report() {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [reportType, setReportType] = useState("week"); // week or month
  const [generatedFiles, setGeneratedFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState("");

  const handleGenerateReport = async () => {
    try {
      await axios.post("http://localhost:8000/api/report/generate", {
        start_date: startDate,  // ✅ Match FastAPI field name
        end_date: endDate,      // ✅ Match FastAPI field name
        report_type: reportType // ✅ Match FastAPI field name
      });

      alert("Report generated successfully!");
      fetchGeneratedFiles();
    } catch (error) {
      alert(`Failed to generate report: ${error.response?.data?.detail || error.message}`);
    }
  };

  const fetchGeneratedFiles = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/files");
      setGeneratedFiles(response.data);
    } catch (error) {
      console.error("Failed to fetch files:", error);
    }
  };

  const handleViewFile = (file) => {
    setSelectedFile(file);
  };

  const handleDownloadFile = async (file) => {
    try {
      const response = await axios.get(`http://localhost:8000/api/files/download/${file}`, {
        responseType: "blob", // ✅ Important for handling binary data
      });

      const blob = new Blob([response.data], { type: "application/pdf" });
      const link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      link.download = file;
      link.click();
    } catch{
      alert("Failed to download file.");
    }
  };

  useEffect(() => {
    fetchGeneratedFiles();
  }, []); // ✅ Fetch files on component mount

  return (
    <div className="flex flex-col items-center justify-center h-full p-6">
      <h1 className="text-3xl font-bold mb-4">Report</h1>

      {/* Date Range Selection */}
      <div className="flex space-x-4 mb-6">
        <input
          type="date"
          className="input input-bordered"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
        <input
          type="date"
          className="input input-bordered"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />
      </div>

      {/* Report Type Selection */}
      <div className="flex space-x-4 mb-6">
        <button
          className={`btn ${reportType === "week" ? "btn-primary" : "btn-outline"}`}
          onClick={() => setReportType("week")}
        >
          Weekly Report
        </button>
        <button
          className={`btn ${reportType === "month" ? "btn-primary" : "btn-outline"}`}
          onClick={() => setReportType("month")}
        >
          Monthly Report
        </button>
      </div>

      {/* Generate Report */}
      <button className="btn btn-success mb-6" onClick={handleGenerateReport}>
        Generate Report
      </button>

      {/* Tabs */}
      <div className="tabs mb-6">
        <a className="tab tab-active">Schedule</a>
        <a className="tab">History</a>
      </div>

      {/* File List */}
      <ul className="w-full max-w-lg space-y-4">
        {generatedFiles.map((file, index) => (
          <li key={index} className="flex justify-between items-center">
            <span className="truncate">{file}</span>
            <div className="flex space-x-2">
              <button
                className="btn btn-sm btn-outline"
                onClick={() => handleViewFile(file)}
              >
                View
              </button>
              <button
                className="btn btn-sm btn-primary"
                onClick={() => handleDownloadFile(file)}
              >
                Download
              </button>
            </div>
          </li>
        ))}
      </ul>

      {/* PDF Viewer */}
      {selectedFile && (
        <div className="mt-6">
          <iframe
            src={`http://localhost:8000/api/files/view/${selectedFile}`}
            className="w-full h-96 border rounded"
          ></iframe>
        </div>
      )}
    </div>
  );
}