export function About() {
  const teamMembers = [
    {
      name: "Nattavee",
      surname: "Narischat",
      role: "Developer",
      img: "/img/nattavee.jpg",
    },
    {
      name: "Piyapan",
      surname: "Boonlertanun",
      role: "Developer",
      img: "/img/piyapan.jpg",
    },
    {
      name: "Natthinan",
      surname: "Sakulpakdee",
      role: "Project Advisor",
      img: "/img/natthinan.png",
    },
  ];

  return (
    <div className="flex flex-col items-center justify-center p-6">
      <h1 className="text-4xl font-bold text-gray-800 mb-6">About Us</h1>
      <p className="text-lg text-center text-gray-600 max-w-2xl">
        Our <span className="font-semibold">Centralized Network Monitoring Management System</span> 
        &nbsp;is designed for seamless and efficient network, server, and environmental monitoring. 
        Developed by a dedicated team under expert guidance, it ensures real-time performance tracking, 
        security, and reliability.
      </p>

      <p className="text-lg text-center text-gray-600 max-w-3xl mt-4">
        Key features include <span className="font-semibold">custom automated reporting</span>, 
        an <span className="font-semibold">advanced alert system</span> integrated with 
        <span className="font-semibold"> Google Chat and email</span>, and 
        <span className="font-semibold"> centralized logging</span> with 
        <span className="font-semibold"> OpenSearch (Elastic)</span> and index management.
        Additionally, our <span className="font-semibold">Suricata-powered IDS detection </span> 
        strengthens security by providing real-time threat detection and alerts.
      </p>

      <p className="text-lg text-center text-gray-600 max-w-3xl mt-4">
        This system empowers organizations with <span className="font-semibold">proactive monitoring</span>, 
        <span className="font-semibold"> enhanced security</span>, and 
        <span className="font-semibold"> streamlined management</span>, ensuring 
        <span className="font-semibold"> network integrity</span> and 
        <span className="font-semibold"> operational efficiency</span>.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12 w-full max-w-4xl">
        {teamMembers.map((member, index) => (
          <div
            key={index}
            className="card bg-white shadow-lg rounded-2xl border border-gray-200 p-6 flex flex-col items-center text-center transform transition-transform duration-300 hover:scale-105"
          >
            <img
              src={member.img}
              alt={`${member.name} ${member.surname}`}
              className="w-24 h-24 rounded-full mb-4 shadow transform transition-transform duration-300 hover:scale-90"
            />
            <h2 className="text-xl font-semibold text-gray-800">{`${member.name} ${member.surname}`}</h2>
            {/* Add the typing animation to the role text */}
            <p className="text-gray-500 overflow-hidden whitespace-nowrap animate-typing">
              {member.role}
              <span className="animate-blink">|</span>
            </p>
          </div>
        ))}
      </div>

      {/* Centralized GitHub Button */}
      <a
        href="https://github.com/mossZmossZ/centralized-network-monitoring-management-web" 
        target="_blank"
        rel="noopener noreferrer"
        className="mt-8 btn btn-primary bg-blue-600 text-white px-6 py-3 rounded-lg shadow hover:bg-blue-700 transition-colors duration-300"
      >
        View This Project on GitHub
      </a>
    </div>
  );
}
