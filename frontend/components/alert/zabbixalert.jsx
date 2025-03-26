import { useState, useEffect } from "react";
import axios from "axios";

const ZabbixAlertTable = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedRows, setExpandedRows] = useState({});

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await axios.get(
          "http://10.10.10.11:9200/zabbix_alerts-*/_search?pretty=true",
          {
            headers: { "Content-Type": "application/json" },
            data: {
              size: 10,
              query: { match_all: {} },
            },
          }
        );
        setAlerts(response.data.hits.hits);
      } catch (error) {
        console.error("Error fetching Zabbix alerts:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchAlerts();
  }, []);

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString("en-GB", {
      hour12: false,
      timeZone: "UTC",
    });
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Zabbix Alerts</h1>
      </div>

      <div className="overflow-x-auto">
        <table className="table w-full border-collapse border border-gray-300">
          <thead className="bg-gray-200">
            <tr className="border-b border-gray-400">
              <th className="p-3 border-r border-gray-400 text-left">Time</th>
              <th className="p-3 border-r border-gray-400 text-left">Status</th>
              <th className="p-3 border-r border-gray-400 text-left">Host</th>
              <th className="p-3 border-r border-gray-400 text-left">Problem</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="4" className="p-3 text-center">
                  Loading...
                </td>
              </tr>
            ) : alerts.length === 0 ? (
              <tr>
                <td colSpan="4" className="p-3 text-center">
                  No alerts found
                </td>
              </tr>
            ) : (
              alerts.map((alert, index) => {
                const { timestamp, status, host, trigger } = alert._source;

                return (
                  <tr
                    key={alert._id}
                    className={`border-b border-gray-300 ${
                      index % 2 === 0 ? "bg-gray-50" : "bg-white"
                    }`}
                  >
                    <td className="p-3 border-r border-gray-300">
                      {formatTime(timestamp)}
                    </td>
                    <td className="p-3 border-r border-gray-300">{status}</td>
                    <td className="p-3 border-r border-gray-300">{host}</td>
                    <td className="p-3 border-r border-gray-300">
                    <div>
                        <p>
                        {expandedRows[alert._id]
                            ? trigger
                            : trigger.length > 30
                            ? trigger.slice(0, 30) + "..."
                            : trigger}
                        </p>
                        {trigger.length > 30 && (
                        <button
                            className="text-blue-600 hover:underline text-sm mt-1"
                            onClick={() =>
                            setExpandedRows((prev) => ({
                                ...prev,
                                [alert._id]: !prev[alert._id],
                            }))
                            }
                        >
                            {expandedRows[alert._id] ? "Hide" : "View"}
                        </button>
                        )}
                    </div>
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

export default ZabbixAlertTable;
