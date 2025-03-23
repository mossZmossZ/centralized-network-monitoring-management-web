import { useState, useEffect } from "react";
import axios from "axios";
import Swal from "sweetalert2";

export function CustomReport() {
  const [reportType, setReportType] = useState("Daily-Report");
  const [generatedFiles, setGeneratedFiles] = useState([]);

  // Fetch generated files from the server
  const fetchGeneratedFiles = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/files");
      setGeneratedFiles(
        response.data.filter((file) =>
          file.includes(reportType.toLowerCase().replace("-", ""))
        )
      );
    } catch (error) {
      console.error("Error fetching files:", error);
    }
  };

  useEffect(() => {
    fetchGeneratedFiles();
  }, [reportType]);

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Custom Reports</h2>

      {/* Table to show the generated reports */}
      <table className="table table-zebra w-full">
        <thead>
          <tr>
            <th>File Name</th>
            <th>Generated Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {generatedFiles.length > 0 ? (
            generatedFiles.map((file, index) => (
              <tr key={index}>
                <td>{file}</td>
                <td>{new Date().toLocaleDateString()}</td>
                <td>
                  <button className="btn btn-sm">View</button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="3" className="text-center">
                No reports found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
