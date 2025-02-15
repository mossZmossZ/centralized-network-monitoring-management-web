import { useState, useEffect, useCallback } from "react";
import axios from "axios";

export function ScheduleReport() {
  const [reportType, setReportType] = useState("week");
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Use useCallback to memoize the fetchFiles function
  const fetchFiles = useCallback(async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/files");
      setFiles(
        response.data.filter((file) =>
          file.startsWith(reportType === "week" ? "week" : "month")
        )
      );
    } catch (error) {
      console.error("Error fetching files:", error);
    }
  }, [reportType]); // Dependency array includes reportType

  useEffect(() => {
    fetchFiles();
  }, [fetchFiles]); // Dependency array includes fetchFiles

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Scheduled Reports</h2>
      <div className="flex space-x-4 mb-4">
        <button
          className={`btn ${reportType === "week" ? "btn-primary" : "btn-outline"}`}
          onClick={() => setReportType("week")}
        >
          Weekly
        </button>
        <button
          className={`btn ${reportType === "month" ? "btn-primary" : "btn-outline"}`}
          onClick={() => setReportType("month")}
        >
          Monthly
        </button>
      </div>
      <ul>
        {files.map((file, index) => (
          <li key={index} className="flex justify-between items-center">
            <span>{file}</span>
            <button className="btn btn-sm" onClick={() => setSelectedFile(file)}>
              View
            </button>
          </li>
        ))}
      </ul>
      {isModalOpen && (
        <div className="modal modal-open">
          <div className="modal-box">
            <h3 className="font-bold">Viewing: {selectedFile}</h3>
            <iframe
              src={`http://localhost:8000/api/files/view/${selectedFile}`}
              className="w-full h-96"
            ></iframe>
            <div className="modal-action">
              <button className="btn" onClick={() => setIsModalOpen(false)}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}