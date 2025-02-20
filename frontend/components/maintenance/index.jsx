import { useState } from "react";
import Swal from "sweetalert2";
import axios from "axios";

export function Maintenance() {
  // Dummy data for configuration changes
  const [changes, setChanges] = useState([
    { time: "09:00 น.", device: "Firewall A", parameter: "Blocked Port 3389", changedBy: "Admin-Security", notes: "Prevent RDP Attack" },
    { time: "14:30 น.", device: "Router 1", parameter: "Updated Firmware", changedBy: "IT-Team", notes: "Fixed security vulnerability" },
    { time: "21:00 น.", device: "Switch Core", parameter: "Changed VLAN Mapping", changedBy: "Network-Engineer", notes: "Segment improvement" },
  ]);

  // Modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [newChange, setNewChange] = useState({
    time: "",
    device: "",
    parameter: "",
    changedBy: "",
    notes: "",
  });

  // Handle input changes
  const handleInputChange = (e) => {
    setNewChange({ ...newChange, [e.target.name]: e.target.value });
  };

  // Handle form submission
  const handleSubmit = async () => {
    if (!newChange.time || !newChange.device || !newChange.parameter || !newChange.changedBy || !newChange.notes) {
      Swal.fire({
        icon: "warning",
        title: "Missing Information",
        text: "Please fill in all fields.",
      });
      return;
    }

    try {
      // Simulated API call (Replace with real API later)
      await axios.post("https://jsonplaceholder.typicode.com/posts", newChange);

      // Add to state
      setChanges([...changes, newChange]);

      // Success alert
      Swal.fire({
        icon: "success",
        title: "Configuration Change Added",
        text: "The new change has been logged successfully.",
      });

      // Close modal & reset form
      setModalOpen(false);
      setNewChange({ time: "", device: "", parameter: "", changedBy: "", notes: "" });
    } catch (error) {
        console.error("API Error:", error); // Log the error to the console
        Swal.fire({
          icon: "error",
          title: "Failed to Save",
          text: "There was an issue saving the change. Try again later.",
        });
      }
  };

  return (
    <div className="p-6">
      {/* Header with Add Button */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Configuration Changes</h1>
        <button className="btn btn-primary" onClick={() => setModalOpen(true)}>+ Add Change</button>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="table w-full border-collapse border border-gray-300">
          <thead className="bg-gray-200">
            <tr className="border-b border-gray-400">
              <th className="p-3 border-r border-gray-400">Time</th>
              <th className="p-3 border-r border-gray-400">Device</th>
              <th className="p-3 border-r border-gray-400">Changed Parameter</th>
              <th className="p-3 border-r border-gray-400">Changed By</th>
              <th className="p-3">Notes</th>
            </tr>
          </thead>
          <tbody>
            {changes.map((change, index) => (
              <tr key={index} className="border-b border-gray-300">
                <td className="p-3 border-r border-gray-300">{change.time}</td>
                <td className="p-3 border-r border-gray-300">{change.device}</td>
                <td className="p-3 border-r border-gray-300">{change.parameter}</td>
                <td className="p-3 border-r border-gray-300">{change.changedBy}</td>
                <td className="p-3">{change.notes}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {modalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-96">
            <h2 className="text-lg font-bold mb-4">Add Configuration Change</h2>

            <label className="block mb-2">Time</label>
            <input type="text" name="time" className="input input-bordered w-full mb-3" onChange={handleInputChange} />

            <label className="block mb-2">Device</label>
            <input type="text" name="device" className="input input-bordered w-full mb-3" onChange={handleInputChange} />

            <label className="block mb-2">Changed Parameter</label>
            <input type="text" name="parameter" className="input input-bordered w-full mb-3" onChange={handleInputChange} />

            <label className="block mb-2">Changed By</label>
            <input type="text" name="changedBy" className="input input-bordered w-full mb-3" onChange={handleInputChange} />

            <label className="block mb-2">Notes</label>
            <input type="text" name="notes" className="input input-bordered w-full mb-3" onChange={handleInputChange} />

            <div className="flex justify-end space-x-2 mt-4">
              <button className="btn btn-ghost" onClick={() => setModalOpen(false)}>Cancel</button>
              <button className="btn btn-primary" onClick={handleSubmit}>Save</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}