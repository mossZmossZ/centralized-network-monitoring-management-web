import { useState, useEffect } from "react"; 
import { motion } from "framer-motion";
import { Globe, Play, Pause, RefreshCw, FileText } from "lucide-react"; // Import icons

const services = {
  Services: [
    { 
      name: "Docker Server", 
      pingUrl: import.meta.env.VITE_DOCKER_SERVER_PING, 
      webUrl: import.meta.env.VITE_DOCKER_SERVER_WEB 
    },
    { 
      name: "Zabbix", 
      pingUrl: import.meta.env.VITE_ZABBIX_PING, 
      webUrl: import.meta.env.VITE_ZABBIX_WEB 
    },
    { 
      name: "Prometheus", 
      pingUrl: import.meta.env.VITE_PROMETHEUS_PING, 
      webUrl: import.meta.env.VITE_PROMETHEUS_WEB 
    },
  ],
  Logging: [
    { 
      name: "Fluentd", 
      pingUrl: import.meta.env.VITE_FLUENTD_PING, 
      webUrl: import.meta.env.VITE_FLUENTD_WEB 
    },
    { 
      name: "OpenSearch", 
      pingUrl: import.meta.env.VITE_OPENSEARCH_PING, 
      webUrl: import.meta.env.VITE_OPENSEARCH_WEB 
    },
  ],
  Dashboard: [
    { 
      name: "Grafana", 
      pingUrl: import.meta.env.VITE_GRAFANA_PING, 
      webUrl: import.meta.env.VITE_GRAFANA_WEB 
    },
    { 
      name: "Uptime Kuma", 
      pingUrl: import.meta.env.VITE_UPTIMEKUMA_PING, 
      webUrl: import.meta.env.VITE_UPTIMEKUMA_WEB 
    },
  ],
};


export function Systems() {
  const [statusData, setStatusData] = useState({});
  const [selectedService, setSelectedService] = useState(null);
  const [logs, setLogs] = useState("");

  useEffect(() => {
    console.log("🔍 Environment Variables Loaded:");
    console.log("Docker Ping:", import.meta.env.VITE_DOCKER_SERVER_PING);
    console.log("Docker Web:", import.meta.env.VITE_DOCKER_SERVER_WEB);
    console.log("Zabbix Ping:", import.meta.env.VITE_ZABBIX_PING);
    console.log("Zabbix Web:", import.meta.env.VITE_ZABBIX_WEB);
    console.log("Prometheus Ping:", import.meta.env.VITE_PROMETHEUS_PING);
    console.log("Prometheus Web:", import.meta.env.VITE_PROMETHEUS_WEB);
    console.log("OpenSearch Ping:", import.meta.env.VITE_OPENSEARCH_PING);
    console.log("OpenSearch Web:", import.meta.env.VITE_OPENSEARCH_WEB);
    console.log("Grafana Ping:", import.meta.env.VITE_GRAFANA_PING);
    console.log("Grafana Web:", import.meta.env.VITE_GRAFANA_WEB);
    console.log("Uptime Kuma Ping:", import.meta.env.VITE_UPTIMEKUMA_PING);
    console.log("Uptime Kuma Web:", import.meta.env.VITE_UPTIMEKUMA_WEB);
    const fetchStatuses = async () => {
      const categoryResults = {};

      for (const category in services) {
        categoryResults[category] = await Promise.all(
          services[category].map(async (service) => {
            if (!service.url) return { name: service.name, status: "⚠️ URL Not Set" };
            try {
              const response = await fetch(service.url);
              if (!response.ok) throw new Error("Service down");
              return { name: service.name, status: "✅ Running" };
            } catch (error) {
              return { name: service.name, status: "❌ Down" };
            }
          })
        );
      }

      setStatusData(categoryResults);
    };

    fetchStatuses();
    const interval = setInterval(fetchStatuses, 10000); // Refresh every 10s
    return () => clearInterval(interval);
  }, []);

  // Mock Start/Stop/Restart Actions
  const handleAction = (serviceName, action) => {
    console.log(`${action} executed for ${serviceName}`);
    alert(`${action} executed for ${serviceName}`);
  };

  // Mock Logs Fetch
  const handleViewLogs = (serviceName) => {
    setSelectedService(serviceName);
    setLogs(`📜 Logs for ${serviceName}:\n[INFO] Service started...\n[INFO] Running smooth...\n[ERROR] Minor issue detected.`);
  };

  return (
    <div className="flex flex-col items-center justify-center h-full p-6 w-full">
      <p className="mt-2 text-gray-600">Monitor and manage your systems here.</p>

      {/* Render separate tables for each category */}
      {Object.keys(statusData).map((category) => (
        <div key={category} className="w-full max-w-5xl mt-6 border rounded-lg shadow-lg bg-white p-4">
          <h2 className="text-2xl font-semibold text-gray-700">{category}</h2>
          <table className="min-w-full bg-white border border-gray-200 shadow-md rounded-lg mt-3">
          <thead className="bg-gray-100">
          <tr>
            <th className="px-4 py-2 text-left border-b">Service</th>
            <th className="px-4 py-2 text-left border-b">Status</th>
            <th className="px-4 py-2 text-left border-b">Actions</th>
            <th className="px-4 py-2 text-left border-b">Web</th> {/* New Web Column */}
          </tr>
          </thead>
          <tbody>
            {statusData[category].map((service) => (
              <tr key={service.name} className="border-b">
                <td className="px-4 py-2">{service.name}</td>
                <td className={`px-4 py-2 font-semibold ${service.status.includes("✅") ? "text-green-600" : "text-red-600"}`}>
                  {service.status}
                </td>
                <td className="px-4 py-2 flex gap-2">
                  {/* Start Icon */}
                  <button className="btn btn-xs btn-success flex items-center gap-1" onClick={() => handleAction(service.name, "Start")}>
                    <Play size={14} />
                  </button>

                  {/* Stop Icon */}
                  <button className="btn btn-xs btn-warning flex items-center gap-1" onClick={() => handleAction(service.name, "Stop")}>
                    <Pause size={14} />
                  </button>

                  {/* Restart Icon */}
                  <button className="btn btn-xs btn-error flex items-center gap-1" onClick={() => handleAction(service.name, "Restart")}>
                    <RefreshCw size={14} />
                  </button>

                  {/* View Logs Icon */}
                  <button className="btn btn-xs btn-info flex items-center gap-1" onClick={() => handleViewLogs(service.name)}>
                    <FileText size={14} />
                  </button>
                </td>

                {/* Web Column */}
                <td className="px-4 py-2">
                  {service.webUrl ? (
                    <a href={service.webUrl} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800">
                      <Globe size={18} />
                    </a>
                  ) : (
                    <span className="text-gray-400">N/A</span>
                  )}
                </td>
              </tr>
            ))}


            </tbody>
          </table>
        </div>
      ))}

      {/* Logs Modal */}
      {selectedService && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
            className="bg-white w-[80%] max-w-3xl p-6 rounded-lg shadow-lg max-h-[70vh] overflow-auto"
          >
            <h3 className="text-xl font-bold text-gray-800">Logs - {selectedService}</h3>
            <pre className="bg-gray-900 text-white p-4 mt-4 text-sm rounded-lg whitespace-pre-wrap max-h-60 overflow-auto">
              {logs}
            </pre>
            <div className="flex justify-end mt-4">
              <button className="btn btn-sm btn-error" onClick={() => setSelectedService(null)}>
                Close
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
}
