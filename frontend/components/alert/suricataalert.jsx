import { useState, useEffect } from "react";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";

const SuricataAlertTable = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showScrollTop, setShowScrollTop] = useState(false);

  // Scroll to top function
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  // Handle scroll for scroll-to-top button visibility
  useEffect(() => {
    const handleScroll = () => {
      setShowScrollTop(window.scrollY > 200);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Fetch Suricata alerts from OpenSearch
  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await axios.post(
          "http://10.10.10.11:9200/suricata-*/_search?pretty=true",
          {
            size: 100, // Fetching 100 results
            query: {
              bool: {
                must: [
                  { match: { event_type: "alert" } },
                  { terms: { "alert.severity": [2, 3] } },
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
        console.error("Error fetching Suricata alerts:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchAlerts();
  }, []);

  // Format time in 24-hour format (DD/MM/YYYY, HH:mm:ss) with Thailand's local time
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString("en-GB", {
      hour12: false // 24-hour format
    });
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Suricata Alerts</h1>

        {/* Scroll-to-top button with animation */}
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

      {/* Table Container */}
      <div className="overflow-x-auto">
        <table className="table w-full border-collapse border border-gray-300">
          <thead className="bg-gray-200">
            <tr className="border-b border-gray-400">
              <th className="p-3 border-r border-gray-400 text-left">Time</th>
              <th className="p-3 border-r border-gray-400 text-left">Src IP</th>
              <th className="p-3 border-r border-gray-400 text-left">Dest IP</th>
              <th className="p-3 border-r border-gray-400 text-left">Signature</th>
              <th className="p-3 border-r border-gray-400 text-left">Severity</th>
            </tr>
          </thead>

          {/* Show loading indicator */}
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="5" className="p-3 text-center">
                  Loading...
                </td>
              </tr>
            ) : alerts.length === 0 ? (
              <tr>
                <td colSpan="5" className="p-3 text-center">
                  No alerts found
                </td>
              </tr>
            ) : (
              alerts.map((alert, index) => {
                const {
                  timestamp,
                  src_ip,
                  dest_ip,
                  alert: alertData
                } = alert._source || {};

                const signature = alertData?.signature || "N/A";
                const severity =
                  alertData?.severity !== undefined ? alertData.severity : "N/A";

                return (
                  <tr
                    key={alert._id}
                    className={`border-b border-gray-300 ${
                      index % 2 === 0 ? "bg-gray-50" : "bg-white"
                    }`}
                  >
                    <td className="p-3 border-r border-gray-300">
                      {timestamp ? formatTime(timestamp) : "N/A"}
                    </td>
                    <td className="p-3 border-r border-gray-300">{src_ip}</td>
                    <td className="p-3 border-r border-gray-300">{dest_ip}</td>
                    <td className="p-3 border-r border-gray-300">{signature}</td>
                    <td className="p-3 border-r border-gray-300">{severity}</td>
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

export default SuricataAlertTable;
