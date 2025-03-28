import { useState, useEffect } from "react";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";

const WebAlertTable = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedRows, setExpandedRows] = useState({});
  const [showScrollTop, setShowScrollTop] = useState(false);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  useEffect(() => {
    const handleScroll = () => {
      setShowScrollTop(window.scrollY > 200); // Show after 200px scroll
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await axios.post(
          "http://10.10.10.11:9200/uptime_kuma_alerts-*/_search",
          {
            size: 100, // Fetching 100 results
            query: {
              bool: {
                must: [
                  { range: { "@timestamp": { gte: "now-24h", lte: "now" } } }
                ]
              }
            },
            sort: [
              { "@timestamp": { order: "desc" } }
            ]
          },
          {
            headers: { "Content-Type": "application/json" }
          }
        );
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

        <AnimatePresence>
          {showScrollTop && (
            <motion.button
              key="scroll-top-btn"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 30 }}
              transition={{ duration: 1 }}
              onClick={scrollToTop}
              className="fixed bottom-20 right-6 bg-blue-600 text-white px-4 py-2 rounded-full shadow-lg hover:bg-blue-700 z-20"
            >
              Scroll To Top
            </motion.button>
          )}
        </AnimatePresence>
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
                const isExpanded = expandedRows[alert._id];

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
                      <div>
                        <p>
                          {isExpanded
                            ? message
                            : message.length > 30
                            ? message.slice(0, 30) + "..."
                            : message}
                        </p>
                        {message.length > 30 && (
                          <button
                            className="text-blue-600 hover:underline text-sm mt-1"
                            onClick={() =>
                              setExpandedRows((prev) => ({
                                ...prev,
                                [alert._id]: !isExpanded
                              }))
                            }
                          >
                            {isExpanded ? "Hide" : "View"}
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

export default WebAlertTable;