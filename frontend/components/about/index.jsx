export function About() {
  const teamMembers = [
    {
      name: "Nattavee",
      surname: "Narischat",
      role: "Developer",
      img: "/images/john.jpg",
    },
    {
      name: "Piyapan",
      surname: "Boonlertanun",
      role: "Developer",
      img: "/images/jane.jpg",
    },
    {
      name: "Natthinan",
      surname: "Sakulpakdee",
      role: "Professor & Project Advisor",
      img: "/images/alan.jpg",
    },
  ];

  return (
    <div className="flex flex-col items-center justify-center p-6">
      <h1 className="text-4xl font-bold text-gray-800 mb-6">About Us</h1>
      <p className="text-lg text-center text-gray-600 max-w-2xl">
        Welcome to the About page of our{" "}
        <span className="font-semibold">
          Centralized Network Monitoring Management System
        </span>
        . This project is developed by two dedicated developers under the
        guidance of an experienced professor. Our system is designed to
        streamline and centralize network monitoring, ensuring seamless
        performance and reliability.
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
              className="w-24 h-24 rounded-full mb-4 shadow"
            />
            <h2 className="text-xl font-semibold text-gray-800">{`${member.name} ${member.surname}`}</h2>
            <p className="text-gray-500">{member.role}</p>
          </div>
        ))}
      </div>

      {/* Centralized GitHub Button */}
      <a
        href="https://github.com/mossZmossZ/centralized-network-monitoring-management-web" // Replace with your project repo link
        target="_blank"
        rel="noopener noreferrer"
        className="mt-8 btn btn-primary bg-blue-600 text-white px-6 py-3 rounded-lg shadow hover:bg-blue-700 transition-colors duration-300"
      >
        View This Project on GitHub
      </a>
    </div>
  );
}
