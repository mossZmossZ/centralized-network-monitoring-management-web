import { useEffect, useState } from "react";
import Swal from "sweetalert2";
import axios from "axios";

export function Maintenance() {
  const [changes, setChanges] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [editMode, setEditMode] = useState(false); // 🆕
  const [editingId, setEditingId] = useState(null); // 🆕
  const [newChange, setNewChange] = useState({
    device: "",
    event: "",
    changedBy: "",
    notes: "",
    status: "pending",
  });

  // ✅ Use VITE_API_URL from .env file
  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

  const sendAlert = async (message) => {
    if (!message.trim()) return;

    try {
      await axios.post(`${API_URL}/send_alert`, {
        message,
      });
      console.log("Alert sent.");
    } catch (error) {
      console.error("Failed to send alert:", error);
    }
  };

  const token = localStorage.getItem("token");

  const fetchChanges = async () => {
    try {
      const res = await axios.get(`${API_URL}/maintenance/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setChanges(res.data);
    } catch (err) {
      console.error("Error fetching maintenance:", err);
      Swal.fire("Error", "Unable to fetch maintenance logs", "error");
    }
  };

  const handleSubmit = async () => {
    const { device, event, changedBy, notes, status } = newChange;

    if (!device || !event || !changedBy || !notes) {
      return Swal.fire("Missing Info", "Please fill all fields", "warning");
    }

    try {
      if (editMode && editingId) {
        // 🆕 PUT update
        await axios.put(`${API_URL}/maintenance/${editingId}`, newChange, {
          headers: { Authorization: `Bearer ${token}` },
        });
        Swal.fire("Updated", "Change updated successfully", "success");
      } else {
        // POST new
        await axios.post(`${API_URL}/maintenance/`, newChange, {
          headers: { Authorization: `Bearer ${token}` },
        });
        Swal.fire("Created", "Change added successfully", "success");
        await sendAlert(
          `🛠 New maintenance by ${newChange.changedBy} on ${newChange.device} (${newChange.event})`
        );
      }

      setModalOpen(false);
      resetForm();
      fetchChanges();
    } catch (error) {
      console.error("Submit error:", error);
      Swal.fire("Error", "Failed to save change", "error");
    }
  };

  const resetForm = () => {
    setEditMode(false);
    setEditingId(null);
    setNewChange({
      device: "",
      event: "",
      changedBy: "",
      notes: "",
      status: "pending",
    });
  };

  const handleInputChange = (e) => {
    setNewChange({ ...newChange, [e.target.name]: e.target.value });
  };

  const handleDelete = async (id) => {
    const result = await Swal.fire({
      title: "Are you sure?",
      text: "This change will be deleted permanently.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Yes, delete it!",
    });

    if (result.isConfirmed) {
      try {
        await axios.delete(`${API_URL}/maintenance/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        Swal.fire("Deleted", "Log deleted successfully", "success");
        fetchChanges();
      } catch (error) {
        console.error("Delete error:", error);
        Swal.fire("Error", "Failed to delete log", "error");
      }
    }
  };

  const handleEdit = (entry) => {
    setNewChange(entry);
    setEditingId(entry.id);
    setEditMode(true);
    setModalOpen(true);
  };

  useEffect(() => {
    fetchChanges();
  }, []);

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Configuration Changes</h1>
        <button
          className="btn btn-primary"
          onClick={() => {
            resetForm();
            setModalOpen(true);
          }}
        >
          + Add Change
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="table w-full border-collapse border border-gray-300">
          <thead className="bg-gray-200">
            <tr className="border-b border-gray-400">
              <th className="p-3 border-r border-gray-400">Time</th>
              <th className="p-3 border-r border-gray-400">Device</th>
              <th className="p-3 border-r border-gray-400">Event</th>
              <th className="p-3 border-r border-gray-400">Changed By</th>
              <th className="p-3 border-r border-gray-400">Status</th>
              <th className="p-3 border-r border-gray-400">Notes</th>
              <th className="p-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {changes.map((change) => (
              <tr key={change.id} className="border-b border-gray-300">
                <td className="p-3 border-r border-gray-300">
                  {new Date(change.time).toLocaleString("th-TH")}
                </td>
                <td className="p-3 border-r border-gray-300">{change.device}</td>
                <td className="p-3 border-r border-gray-300">{change.event}</td>
                <td className="p-3 border-r border-gray-300">{change.changedBy}</td>
                <td className="p-3 border-r border-gray-300">
                  <span className={`badge ${getStatusStyle(change.status)}`}>{change.status}</span>
                </td>
                <td className="p-3 border-r border-gray-300">{change.notes}</td>
                <td className="p-3 space-x-2">
                  <button className="btn btn-xs btn-info" onClick={() => handleEdit(change)}>
                    Edit
                  </button>
                  <button className="btn btn-xs btn-error" onClick={() => handleDelete(change.id)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {modalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50 z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-96">
            <h2 className="text-lg font-bold mb-4">
              {editMode ? "Edit Change" : "Add Configuration Change"}
            </h2>

            <label className="block mb-2">Device</label>
            <input
              type="text"
              name="device"
              className="input input-bordered w-full mb-3"
              onChange={handleInputChange}
              value={newChange.device}
            />

            <label className="block mb-2">Event</label>
            <input
              type="text"
              name="event"
              className="input input-bordered w-full mb-3"
              onChange={handleInputChange}
              value={newChange.event}
            />

            <label className="block mb-2">Changed By</label>
            <input
              type="text"
              name="changedBy"
              className="input input-bordered w-full mb-3"
              onChange={handleInputChange}
              value={newChange.changedBy}
            />

            <label className="block mb-2">Notes</label>
            <input
              type="text"
              name="notes"
              className="input input-bordered w-full mb-3"
              onChange={handleInputChange}
              value={newChange.notes}
            />

            <label className="block mb-2">Status</label>
            <select
              name="status"
              className="select select-bordered w-full mb-3"
              onChange={handleInputChange}
              value={newChange.status}
            >
              <option value="pending">Pending</option>
              <option value="in progress">In Progress</option>
              <option value="completed">Completed</option>
            </select>

            <div className="flex justify-end space-x-2 mt-4">
              <button className="btn btn-ghost" onClick={() => setModalOpen(false)}>
                Cancel
              </button>
              <button className="btn btn-primary" onClick={handleSubmit}>
                {editMode ? "Update" : "Save"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function getStatusStyle(status) {
  switch (status) {
    case "completed":
      return "badge-success";
    case "in progress":
      return "badge-warning";
    case "pending":
    default:
      return "badge-neutral";
  }
}
