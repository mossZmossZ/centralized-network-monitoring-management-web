import { useState, useEffect } from "react";
import axios from "axios";

const WebAlertTable = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await axios.get(
          "http://10.10.10.11:9200/uptime_kuma_alerts-*/_search?size=100&pretty=true"
        );
        console.log(response.data); // Inspect the response to check its structure
        setAlerts(response.data.hits.hits);
      } catch (error) {
        console.error("Error fetching alerts:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchAlerts();
  }, []);

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Web Alerts</h1>
      </div>

      <div className="overflow-x-auto">
        <table className="table w-full border-collapse border border-gray-300">
          <thead className="bg-gray-200">
            <tr className="border-b border-gray-400">
              <th className="p-3 border-r border-gray-400 text-left">Time</th>
              <th className="p-3 border-r border-gray-400 text-left">Monitor Name</th>
              <th className="p-3 border-r border-gray-400 text-left">Message</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="3" className="p-3 text-center">
                  Loading...
                </td>
              </tr>
            ) : alerts.length === 0 ? (
              <tr>
                <td colSpan="3" className="p-3 text-center">
                  No alerts found
                </td>
              </tr>
            ) : (
              alerts.map((alert, index) => {
                const { timestamp, monitor_name, message } = alert._source;
                return (
                  <tr
                    key={alert._id}
                    className={`border-b border-gray-300 ${
                      index % 2 === 0 ? "bg-gray-50" : "bg-white"
                    }`}
                  >
                    <td className="p-3 border-r border-gray-300">
                      {new Date(timestamp).toLocaleString()}
                    </td>
                    <td className="p-3 border-r border-gray-300">{monitor_name}</td>
                    <td className="p-3 border-r border-gray-300">
                      {message.length > 30 ? message.slice(0, 30) + "..." : message}
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default WebAlertTable;
