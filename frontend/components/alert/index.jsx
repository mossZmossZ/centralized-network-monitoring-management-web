import { useState } from "react";
import axios from "axios";
import Swal from "sweetalert2";

export function Alert() {
  const [alertMessage, setAlertMessage] = useState("");
  const [loading, setLoading] = useState(false);

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
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center h-full p-6">
      <h1 className="text-3xl font-bold">Alerts</h1>
      <p className="mt-2 text-gray-600">View and send test alerts here.</p>
      
      <input
        type="text"
        className="border p-2 mt-4 w-64 rounded shadow"
        placeholder="Enter test alert message"
        value={alertMessage}
        onChange={(e) => setAlertMessage(e.target.value)}
        disabled={loading}
      />

      <button
        className={`mt-4 px-4 py-2 rounded text-white ${loading ? "bg-gray-400 cursor-not-allowed" : "bg-red-500 hover:bg-red-600"}`}
        onClick={sendTestAlert}
        disabled={loading}
      >
        {loading ? "Sending..." : "Send Test Alert"}
      </button>
    </div>
  );
}
