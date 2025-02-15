import { useState, useEffect } from "react";
import axios from "axios";

export function CustomReport() {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [generatedFiles, setGeneratedFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleGenerateReport = async () => {
    try {
      await axios.post("http://localhost:8000/api/report/generate", {
        start_date: startDate,
        end_date: endDate,
        report_type: "custom",
      });
      alert("Custom Report Generated!");
      fetchGeneratedFiles();
    } catch (error) {
      alert(`Error generating report: ${error.response?.data?.detail || error.message}`);
    }
  };

  const fetchGeneratedFiles = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/files");
      setGeneratedFiles(response.data.filter((file) => file.includes("custom-report")));
    } catch (error) {
      console.error("Error fetching files:", error);
    }
  };

  useEffect(() => {
    fetchGeneratedFiles();
  }, []);

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Custom Reports</h2>
      <div className="flex space-x-4 mb-4">
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
      <button className="btn btn-success mb-6" onClick={handleGenerateReport}>
        Generate Report
      </button>
      <ul className="list-none">
        {generatedFiles.map((file, index) => (
          <li key={index} className="flex justify-between items-center mb-2">
            <span>{file}</span>
            <button className="btn btn-sm" onClick={() => setSelectedFile(file)}>
              View
            </button>
          </li>
        ))}
      </ul>
      {isModalOpen && selectedFile && (
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