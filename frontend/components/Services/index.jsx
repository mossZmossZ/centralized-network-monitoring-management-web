

export function Services() {
  return (
    <div className="container mx-auto p-4">
      <h2 className="text-3xl font-bold text-center mb-8">Our Services</h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Grafana Card */}
        <div className="card w-full bg-base-100 shadow-xl transform transition-all duration-300 hover:scale-105 hover:shadow-2xl">
          <figure>
            <img
              src="path/to/grafana-image.jpg"
              alt="Grafana"
              className="h-48 w-full object-cover transition-all duration-300 hover:scale-105"
            />
          </figure>
          <div className="card-body">
            <h3 className="card-title">Grafana</h3>
            <p>Monitor and analyze your metrics and logs in one place with Grafana.</p>
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
              src="path/to/uptimekuma-image.jpg"
              alt="Uptimekuma"
              className="h-48 w-full object-cover transition-all duration-300 hover:scale-105"
            />
          </figure>
          <div className="card-body">
            <h3 className="card-title">Uptimekuma</h3>
            <p>A self-hosted status monitoring solution to keep track of your services.</p>
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
              src="path/to/zabbix-image.jpg"
              alt="Zabbix"
              className="h-48 w-full object-cover transition-all duration-300 hover:scale-105"
            />
          </figure>
          <div className="card-body">
            <h3 className="card-title">Zabbix</h3>
            <p>Powerful open-source software for monitoring IT infrastructure.</p>
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
              src="path/to/opensearch-image.jpg"
              alt="Opensearch"
              className="h-48 w-full object-cover transition-all duration-300 hover:scale-105"
            />
          </figure>
          <div className="card-body">
            <h3 className="card-title">Opensearch</h3>
            <p>Search, analyze, and visualize your data with OpenSearch.</p>
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
              src="path/to/Report-image.jpg"
              alt="Report"
              className="h-48 w-full object-cover transition-all duration-300 hover:scale-105"
            />
          </figure>
          <div className="card-body">
            <h3 className="card-title">Report</h3>
            <p>Search, analyze, and visualize your data with Report.</p>
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
              src="path/to/Alert-image.jpg"
              alt="Alert"
              className="h-48 w-full object-cover transition-all duration-300 hover:scale-105"
            />
          </figure>
          <div className="card-body">
            <h3 className="card-title">Alert</h3>
            <p>Search, analyze, and visualize your data with Alert.</p>
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
