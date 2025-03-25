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
            <p>Monitor and analyze system and application activities, aligned with ISO/IEC 27001 A.8.16 and TIA-942 Monitoring & Alerting standards.</p>
            <div className="card-actions justify-end">
              <a
                href="#get-started"
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
            <p>Self-hosted status monitoring solution to ensure redundancy and uptime in your services, in line with TIA-942 Redundant Cabling standards.</p>
            <div className="card-actions justify-end">
              <a
                href="#get-started"
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
            <p>Monitor IT infrastructure and network services, aligning with ISO/IEC 27001 A.8.21 and A.8.22, and ensuring network security and segregation, in line with TIA-942 standards.</p>
            <div className="card-actions justify-end">
              <a
                href="#get-started"
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
            <p>Search, analyze, and visualize logs for auditing and internal compliance, aligned with ISO/IEC 27001 A.9.2 Internal Audit and A.10.2 Corrective Action standards.</p>
            <div className="card-actions justify-end">
              <a
                href="#get-started"
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
            <p>Generate scheduled reports with ISO 27001 compliance, supporting performance monitoring, and compliance evaluation as per A.9.1.</p>
            <div className="card-actions justify-end">
              <a
                href="#get-started"
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
            <p>Receive real-time alerts for temperature anomalies, power failures, or suspicious activities, meeting both ISO 27001 A.8.15 Logging and TIA-942 standards for monitoring.</p>
            <div className="card-actions justify-end">
              <a
                href="#get-started"
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
