import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Globe, Play, Pause, RefreshCw, FileText, Loader, X } from "lucide-react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const services = {
  Services: [
    { name: "Docker Server", webUrl: import.meta.env.VITE_DOCKER_SERVER_WEB },
    { name: "Zabbix", webUrl: import.meta.env.VITE_ZABBIX_WEB },
    { name: "Prometheus", webUrl: import.meta.env.VITE_PROMETHEUS_WEB },
  ],
  Logging: [
    { name: "Fluentd", webUrl: import.meta.env.VITE_FLUENTD_WEB },
    { name: "OpenSearch", webUrl: import.meta.env.VITE_OPENSEARCH_WEB },
  ],
  Dashboard: [
    { name: "Grafana", webUrl: import.meta.env.VITE_GRAFANA_WEB },
    { name: "Uptime Kuma", webUrl: import.meta.env.VITE_UPTIMEKUMA_WEB },
  ],
};

export function Systems() {
  const [statusData, setStatusData] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedService, setSelectedService] = useState(null);
  const [logs, setLogs] = useState("");

  useEffect(() => {
    const fetchStatuses = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/ping`);
        const data = await response.json();
        setStatusData(data);
        setLoading(false);
      } catch (error) {
        console.error("❌ Error fetching service statuses:", error);
      }
    };

    fetchStatuses();
    const interval = setInterval(fetchStatuses, 10000);
    return () => clearInterval(interval);
  }, []);

  // Fetch Dummy Logs for Each Service
  const handleViewLogs = (serviceName) => {
    setSelectedService(serviceName);
    setLogs(`
[INFO] ${serviceName} started successfully...
[INFO] ${serviceName} is running smoothly...
[WARNING] Minor latency detected in ${serviceName}...
[ERROR] ${serviceName} encountered a small network issue...
[INFO] Restarting ${serviceName} fixed the issue.
    `);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 w-full  pt-0">
      {Object.keys(services).map((category) => (
        <div key={category} className="w-full max-w-5xl mt-6 border rounded-lg shadow-lg bg-white p-4">
          <h2 className="text-2xl font-semibold text-gray-700">{category}</h2>
          <table className="min-w-full bg-white border border-gray-200 shadow-md rounded-lg mt-3">
            <thead className="bg-gray-200 text-gray-700 font-semibold">
              <tr>
                <th className="px-6 py-3 text-left">Service</th>
                <th className="px-6 py-3 text-center">Status</th>
                <th className="px-6 py-3 text-center">Actions</th>
                <th className="px-6 py-3 text-center">Web</th>
              </tr>
            </thead>
            <tbody>
              {services[category].map((service) => (
                <tr key={service.name} className="border-b hover:bg-gray-50">
                  <td className="px-6 py-4">{service.name}</td>
                  <td className="px-6 py-4 text-center">
                    {loading ? (
                      <Loader className="animate-spin text-gray-500" size={18} />
                    ) : (
                      <span className={`font-bold ${statusData[category]?.find(s => s.name === service.name)?.status.includes("✅") ? "text-green-600" : "text-red-600"}`}>
                        {statusData[category]?.find(s => s.name === service.name)?.status || "❌ Down"}
                      </span>
                    )}
                  </td>

                  {/* Centered Actions */}
                  <td className="px-6 py-4">
                    <div className="flex justify-center gap-2">
                      <button className="btn btn-sm btn-success flex justify-center items-center" onClick={() => console.log("Start")}>
                        <Play size={16} />
                      </button>
                      <button className="btn btn-sm btn-warning flex justify-center items-center" onClick={() => console.log("Stop")}>
                        <Pause size={16} />
                      </button>
                      <button className="btn btn-sm btn-error flex justify-center items-center" onClick={() => console.log("Restart")}>
                        <RefreshCw size={16} />
                      </button>
                      <button className="btn btn-sm btn-info flex justify-center items-center" onClick={() => handleViewLogs(service.name)}>
                        <FileText size={16} />
                      </button>
                    </div>
                  </td>

                  {/* Centered Web Column */}
                  <td className="px-6 py-4 text-center">
                    {service.webUrl ? (
                      <a href={service.webUrl} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800 flex justify-center">
                        <Globe size={20} />
                      </a>
                    ) : (
                      <Globe size={20} className="opacity-50" />
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}

      {/* Logs Modal */}
      <AnimatePresence>
        {selectedService && (
          <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ duration: 0.3, ease: "easeOut" }}
              className="bg-white w-[80%] max-w-3xl p-6 rounded-lg shadow-lg max-h-[70vh] overflow-auto"
            >
              <div className="flex justify-between items-center">
                <h3 className="text-xl font-bold text-gray-800">Logs - {selectedService}</h3>
                <button className="btn btn-sm btn-error" onClick={() => setSelectedService(null)}>
                  <X size={20} />
                </button>
              </div>
              <pre className="bg-gray-900 text-white p-4 mt-4 text-sm rounded-lg whitespace-pre-wrap max-h-60 overflow-auto">
                {logs}
              </pre>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
