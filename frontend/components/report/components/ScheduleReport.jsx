import { useState, useEffect } from "react";
import axios from "axios";
import Swal from 'sweetalert2'; // SweetAlert2 import
import { Worker, Viewer } from "@react-pdf-viewer/core";
import { defaultLayoutPlugin } from "@react-pdf-viewer/default-layout";
import { toolbarPlugin } from "@react-pdf-viewer/toolbar";
import '@react-pdf-viewer/core/lib/styles/index.css';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';
import '@react-pdf-viewer/toolbar/lib/styles/index.css';

export function ScheduleReport() {
  const [reportType, setReportType] = useState("Daily-Report");
  const [generatedFiles, setGeneratedFiles] = useState({
    daily: [],
    weekly: [],
    monthly: [],
  });
  const [pdfUrl, setPdfUrl] = useState(""); // URL of the PDF to preview
  const [fileName, setFileName] = useState(""); // Track the file name being previewed
  const [isModalOpen, setIsModalOpen] = useState(false); // State to track if the modal is open
  const [searchQuery, setSearchQuery] = useState(""); // State for search query

  // Setup plugins
  const defaultLayoutPluginInstance = defaultLayoutPlugin();
  const toolbarPluginInstance = toolbarPlugin();

  // Fetch generated files from the server
  const fetchGeneratedFiles = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/schedule/files");
      setGeneratedFiles(response.data);
    } catch (error) {
      console.error("Error fetching files:", error);
    }
  };

  useEffect(() => {
    fetchGeneratedFiles();
  }, []);

  // Filter files based on the selected report type and search query
  const filteredFiles = generatedFiles[reportType.toLowerCase().split('-')[0]]
    .filter((file) => file.toLowerCase().includes(searchQuery.toLowerCase()));

  // Function to preview the file (PDF) in a modal
  const handlePreview = (fileType, fileName) => {
    const fileUrl = `http://localhost:8000/api/schedule/files/${fileType}/${fileName}/preview`;
    setPdfUrl(fileUrl); // Set PDF URL to the state
    setFileName(fileName); // Set the file name for display
    setIsModalOpen(true); // Open the modal
  };

  // Function to download the file
  const handleDownload = (fileType, fileName) => {
    const fileUrl = `http://localhost:8000/api/schedule/files/${fileType}/${fileName}/download`;
    const link = document.createElement("a");
    link.href = fileUrl;
    link.download = fileName; // The file name to use for the downloaded file
    link.click(); // Trigger the download
  };

  // Function to delete the file with SweetAlert confirmation
  const handleDelete = (fileType, fileName) => {
    Swal.fire({
      title: 'Are you sure?',
      text: `You are about to delete ${fileName} permanently!`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Yes, delete it!',
      cancelButtonText: 'No, cancel!',
      input: 'text',  // Adding an input field to type "delete"
      inputPlaceholder: 'Type "delete" to confirm',
      preConfirm: (inputValue) => {
        // Check if the input value matches "delete"
        if (inputValue.toLowerCase() !== 'delete') {
          Swal.showValidationMessage('You need to type "delete" to confirm');
          return false;
        }
        return true; // Proceed if input is correct
      }
    }).then(async (result) => {
      if (result.isConfirmed) {
        try {
          const response = await axios.delete(
            `http://localhost:8000/api/schedule/files/${fileType}/${fileName}`
          );
          Swal.fire('Deleted!', response.data.message, 'success');
          fetchGeneratedFiles(); // Refresh the list of files after deletion
        } catch (error) {
          Swal.fire('Error!', 'There was an error deleting the file.', 'error');
        }
      }
    });
  };

  // Function to close the modal
  const closeModal = () => {
    setIsModalOpen(false); // Close the modal
    setPdfUrl(""); // Reset the PDF URL
  };

  return (
    <div className="container mx-auto p-6 flex flex-col min-h-screen">
      <h2 className="text-2xl font-bold mb-6">Schedule  Reports</h2>

      {/* Dropdown to select report type and Search bar */}
      <div className="flex items-center mb-4 space-x-4">
        <select
          className="select select-bordered w-full max-w-xs"
          value={reportType}
          onChange={(e) => setReportType(e.target.value)}
        >
          <option value="Daily-Report">Daily Report</option>
          <option value="Weekly-Report">Weekly Report</option>
          <option value="Monthly-Report">Monthly Report</option>
        </select>

        {/* Search Input */}
        <input
          type="text"
          placeholder="Search by file name..."
          className="input input-bordered w-full max-w-xs"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* Render the table with files */}
      <div className="flex-grow overflow-y-auto">
        {filteredFiles.length > 0 ? (
          <table className="table table-zebra w-full">
            <thead>
              <tr>
                <th>File Name</th>
                <th>Generated Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredFiles.map((file, index) => (
                <tr key={index}>
                  <td>{file}</td>
                  <td>{new Date().toLocaleDateString()}</td>
                  <td>
                    <button
                      className="btn btn-sm btn-info mr-2"
                      onClick={() => handlePreview(reportType.toLowerCase().split('-')[0], file)} // Preview
                    >
                      Preview
                    </button>
                    <button
                      className="btn btn-sm btn-success mr-2"
                      onClick={() => handleDownload(reportType.toLowerCase().split('-')[0], file)} // Download
                    >
                      Download
                    </button>

                    <button
                      className="btn btn-sm btn-secondary mr-2"
                      onClick={() => handleDelete(reportType.toLowerCase().split('-')[0], file)} // Delete
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="text-center">No reports found for {reportType.split('-')[0]} reports.</p>
        )}
      </div>

      {/* Modal to display PDF preview */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white p-6 w-full max-w-4xl rounded-md">
            <h3 className="text-xl font-semibold mb-4">Previewing: {fileName}</h3>

            {/* PDF Viewer with toolbar and default layout */}
            <div className="pdf-viewer-container" style={{ height: '70vh', overflowY: 'auto' }}>
              <Worker workerUrl="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js">
                <Viewer fileUrl={pdfUrl} plugins={[defaultLayoutPluginInstance, toolbarPluginInstance]} />
              </Worker>
            </div>

            {/* Close Preview button */}
            <button
              className="btn btn-sm btn-secondary mt-4"
              onClick={closeModal}
            >
              Close Preview
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
