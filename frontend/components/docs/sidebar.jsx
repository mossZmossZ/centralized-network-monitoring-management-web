import { useState } from "react";
import { ChevronDownIcon, ChevronRightIcon } from "@heroicons/react/24/outline";

export default function Sidebar({ topics, activeTopic, setActiveTopic }) {
  const [expandedTopics, setExpandedTopics] = useState({});

  return (
    <aside className="w-1/4 bg-gray-100 p-6 border-r shadow-md">
      <h2 className="text-xl font-semibold text-gray-700">📚 Documentation</h2>
      <ul className="space-y-2 mt-4">
        {topics.map((topic) => (
          <li key={topic.id}>
            <button
              className="w-full text-left px-4 py-2 font-medium text-gray-800 hover:bg-gray-200 flex justify-between items-center"
              onClick={() =>
                setExpandedTopics({ ...expandedTopics, [topic.id]: !expandedTopics[topic.id] })
              }
            >
              {topic.title}
              {expandedTopics[topic.id] ? <ChevronDownIcon className="h-5 w-5" /> : <ChevronRightIcon className="h-5 w-5" />}
            </button>

            {expandedTopics[topic.id] &&
              topic.subtopics.map((sub) => (
                <button
                  key={sub.id}
                  className={`w-full text-left pl-6 py-2 rounded-md ${
                    activeTopic.id === sub.id ? "bg-blue-500 text-white" : "text-gray-700 hover:bg-gray-200"
                  }`}
                  onClick={() => setActiveTopic(sub)}
                >
                  {sub.title}
                </button>
              ))}
          </li>
        ))}
      </ul>
    </aside>
  );
}