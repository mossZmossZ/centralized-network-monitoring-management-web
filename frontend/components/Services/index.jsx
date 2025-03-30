export function Services() {
  return (
    <div className="container mx-auto p-4">
      <h2 className="text-3xl font-bold text-center mb-8">Our Services</h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Grafana Card */}
        <div className="card w-full bg-base-100 shadow-xl transform transition-all duration-300 hover:scale-105 hover:shadow-2xl">
          <figure>
            <img
              src="/img/grafana.png"
              alt="Grafana"
              className="h-48 w-full object-cover transition-all duration-300 hover:scale-105"
            />
          </figure>
          <div className="card-body">
            <h3 className="card-title">Grafana</h3>
            <p>Grafana delivers real-time system and application monitoring, ensuring compliance with ISO/IEC 27001 A.8.16 Monitoring Activities and TIA-942 6.6.3 Monitoring and Surveillance.</p>
            <div className="card-actions justify-end">
            <a
              href={`${import.meta.env.VITE_GRAFANA_URL}`}
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-primary transition-transform duration-200 hover:scale-105 active:scale-95"
            >
              Get Started
            </a>
            </div>
          </div>
        </div>

        {/* Uptimekuma Card */}
        <div className="card w-full bg-base-100 shadow-xl transform transition-all duration-300 hover:scale-105 hover:shadow-2xl">
          <figure>
            <img
              src="/img/uptime.png"
              alt="Uptimekuma"
              className="h-48 w-full object-cover transition-all duration-300 hover:scale-105"
            />
          </figure>
          <div className="card-body">
            <h3 className="card-title">Uptimekuma</h3>
            <p>Uptimekuma maintains continuous service availability, supporting TIA-942 Redundant Cabling standards to ensure redundancy and prevent downtime.</p>
            <div className="card-actions justify-end">
            <a
              href={`${import.meta.env.VITE_UPTIME_URL}`} 
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-primary transition-transform duration-200 hover:scale-105 active:scale-95"
            >
              Get Started
            </a>
            </div>
          </div>
        </div>

        {/* Zabbix Card */}
        <div className="card w-full bg-base-100 shadow-xl transform transition-all duration-300 hover:scale-105 hover:shadow-2xl">
          <figure>
            <img
              src="/img/zabbix.png"
              alt="Zabbix"
              className="h-48 w-full object-cover transition-all duration-300 hover:scale-105"
            />
          </figure>
          <div className="card-body">
            <h3 className="card-title">Zabbix</h3>
            <p>Zabbix safeguards IT infrastructure with proactive monitoring, aligning with ISO/IEC 27001 A.8.21 Security of Network Services and A.8.22 Segregation of Networks.</p>
            <div className="card-actions justify-end">
            <a
              href={`${import.meta.env.VITE_ZABBIX_URL}`} 
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-primary transition-transform duration-200 hover:scale-105 active:scale-95"
            >
              Get Started
            </a>
            </div>
          </div>
        </div>

        {/* Opensearch Card */}
        <div className="card w-full bg-base-100 shadow-xl transform transition-all duration-300 hover:scale-105 hover:shadow-2xl">
          <figure>
            <img
              src="/img/opensearch.png"
              alt="Opensearch"
              className="h-48 w-full object-cover transition-all duration-300 hover:scale-105"
            />
          </figure>
          <div className="card-body">
            <h3 className="card-title">Opensearch</h3>
            <p>Opensearch enhances compliance by enabling log analysis and audit reviews, meeting ISO/IEC 27001 A.9.2 Internal Audit and A.10.2 Corrective Action standards.</p>
            <div className="card-actions justify-end">
            <a
              href={`${import.meta.env.VITE_OEPNSEARCH_URL}`}
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-primary transition-transform duration-200 hover:scale-105 active:scale-95"
            >
              Get Started
            </a>
            </div>
          </div>
        </div>

        {/* Report Card */}
        <div className="card w-full bg-base-100 shadow-xl transform transition-all duration-300 hover:scale-105 hover:shadow-2xl">
          <figure>
            <img
              src="/img/Report.png"
              alt="Report"
              className="h-48 w-full object-cover transition-all duration-300 hover:scale-105"
            />
          </figure>
          <div className="card-body">
            <h3 className="card-title">Report</h3>
            <p>Report automates compliance evaluation and performance tracking, adhering to ISO/IEC 27001 A.9.1 Monitoring, Measurement, Analysis, and Evaluation.</p>
            <div className="card-actions justify-end">
              <a
                href="/report"
                className="btn btn-primary transition-transform duration-200 hover:scale-105 active:scale-95"
              >
                Get Started
              </a>
            </div>
          </div>
        </div>

        {/* Alert Card */}
        <div className="card w-full bg-base-100 shadow-xl transform transition-all duration-300 hover:scale-105 hover:shadow-2xl">
          <figure>
            <img
              src="/img/googlechat.png"
              alt="Alert"
              className="h-48 w-full object-cover transition-all duration-300 hover:scale-105"
            />
          </figure>
          <div className="card-body">
            <h3 className="card-title">Alert</h3>
            <p>Alert provides real-time notifications for anomalies and security threats, aligned with ISO/IEC 27001 A.8.15 Logging and TIA-942 Monitoring and Alerting standards.</p>
            <div className="card-actions justify-end">
              <a
                href={`${import.meta.env.VITE_GOOGLECHAT_URL}`}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary transition-transform duration-200 hover:scale-105 active:scale-95"
              >
                Get Started
              </a>
            </div>
          </div>
        </div>

        {/* Vcenter Card */}
        <div className="card w-full bg-base-100 shadow-xl transform transition-all duration-300 hover:scale-105 hover:shadow-2xl">
          <figure>
            <img
              src="/img/vcenter.png"
              alt="Report"
              className="h-48 w-full object-cover transition-all duration-300 hover:scale-105"
            />
          </figure>
          <div className="card-body">
            <h3 className="card-title">Vcenter</h3>
            <p>VCenter Server manages and virtualizes critical infrastructure, supporting ISO/IEC 27001 A.8.12 Data Leakage Prevention and ensuring secure resource segregation.</p>
            <div className="card-actions justify-end">
              <a
                href={`${import.meta.env.VITE_VCENTER_URL}`}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary transition-transform duration-200 hover:scale-105 active:scale-95"
              >
                Get Started
              </a>
            </div>
          </div>
        </div>

        {/* Proxmox Card */}
        <div className="card w-full bg-base-100 shadow-xl transform transition-all duration-300 hover:scale-105 hover:shadow-2xl">
          <figure>
            <img
              src="/img/proxmox.png"
              alt="Report"
              className="h-48 w-full object-cover transition-all duration-300 hover:scale-105"
            />
          </figure>
          <div className="card-body">
            <h3 className="card-title">Proxmox</h3>
            <p>Proxmox provides virtualization and high-availability clustering, aligning with ISO/IEC 27001 A.8.21 Network Security and TIA-942 Redundant Cabling standards.</p>
            <div className="card-actions justify-end">
              <a
                href={`${import.meta.env.VITE_PROXMOX_URL}`}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary transition-transform duration-200 hover:scale-105 active:scale-95"
              >
                Get Started
              </a>
            </div>
          </div>
        </div>


      </div>
    </div>
  );
}
