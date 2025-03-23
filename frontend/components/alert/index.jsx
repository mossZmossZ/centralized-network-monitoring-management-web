import { useState } from "react";
import axios from "axios";
import Swal from "sweetalert2";
import WebAlertTable from "./webalert";

export function Alert() {
  const [alertMessage, setAlertMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedTable, setSelectedTable] = useState("Zabbix");
  const [isModalOpen, setIsModalOpen] = useState(false);

  const sendTestAlert = async () => {
    if (!alertMessage.trim()) {
      Swal.fire("Warning", "Please enter a message before sending!", "warning");
      return;
    }
  
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/send_alert", {
        message: alertMessage,
      });
  
      if (response.status === 200) {
        Swal.fire("Success!", "Alert sent successfully to Google Chat!", "success");
        setAlertMessage(""); // Clear input after success
      }
    } catch (error) {
      Swal.fire("Error", "Failed to send alert. Please try again!", "error");
      console.error("Error sending alert:", error);
      setAlertMessage(""); // Clear input after success
    }
    setLoading(false);
    setIsModalOpen(false); // Close the modal after sending the alert
  };

  const renderTable = () => {
    switch (selectedTable) {
      case "Zabbix":
        return <div>Content for Zabbix Alert</div>;
      case "Web":
        return <WebAlertTable />; // Render the WebAlertTable component
      case "Suricata":
        return <div>Content for Suricata Alert</div>;
      default:
        return <div>Select a table</div>;
    }
  };

  return (
    <div className="flex flex-col items-center justify-start h-full p-6">
      {/* Submenu with Enhanced Buttons */}
      <div className="flex justify-between w-full mb-6">
        <div className="flex space-x-4">
          <button
            className={`px-4 py-2 rounded-full text-lg font-medium transition duration-300 ease-in-out transform hover:scale-105 ${
              selectedTable === "Zabbix" ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-700"
            }`}
            onClick={() => setSelectedTable("Zabbix")}
          >
            Zabbix Alert
          </button>
          <button
            className={`px-4 py-2 rounded-full text-lg font-medium transition duration-300 ease-in-out transform hover:scale-105 ${
              selectedTable === "Web" ? "bg-green-500 text-white" : "bg-gray-200 text-gray-700"
            }`}
            onClick={() => setSelectedTable("Web")}
          >
            Web Alert
          </button>
          <button
            className={`px-4 py-2 rounded-full text-lg font-medium transition duration-300 ease-in-out transform hover:scale-105 ${
              selectedTable === "Suricata" ? "bg-yellow-500 text-white" : "bg-gray-200 text-gray-700"
            }`}
            onClick={() => setSelectedTable("Suricata")}
          >
            Suricata Alert
          </button>
        </div>

        {/* Send Alert Button */}
        <button
          className={`mr-5 px-6 py-3 rounded-full text-white bg-red-600 hover:bg-red-700 transition duration-300 ease-in-out transform hover:scale-105 ${
            loading ? "cursor-not-allowed opacity-50" : ""
          }`}
          onClick={() => setIsModalOpen(true)}
          disabled={loading}
        >
          {loading ? "Sending..." : "Send Alert"}
        </button>
      </div>

      {/* Selected Table Content */}
      <div className="w-full">
        {renderTable()}
      </div>

      {/* Default Modal for Alert Input */}
      {isModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-50">
          {/* Modal Content */}
          <div className="relative p-8 bg-white rounded-lg shadow-lg w-96">
            <h2 className="text-2xl font-semibold text-center mb-4">Enter Alert Message</h2>

            {/* Input for Alert Message */}
            <input
              type="text"
              className="w-full p-2 border border-gray-300 rounded-md mb-4"
              placeholder="Enter your alert message here..."
              value={alertMessage}
              onChange={(e) => setAlertMessage(e.target.value)}
              disabled={loading}
            />

            {/* Modal Buttons */}
            <div className="flex justify-between">
              <button
                className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition"
                onClick={() => setIsModalOpen(false)} // Close the modal when Cancel is clicked
              >
                Cancel
              </button>
              <button
                className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition"
                onClick={sendTestAlert} // Send the alert when clicked
                disabled={loading}
              >
                Send Alert
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
