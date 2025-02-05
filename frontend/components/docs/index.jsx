import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { atomDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { ClipboardIcon, CheckIcon, ChevronDownIcon, ChevronRightIcon } from "@heroicons/react/24/outline";

export function Docs() {
  // Dummy documentation topics with subtopics
  const topics = [
    {
      id: "intro",
      title: "Introduction",
      subtopics: [
        {
          id: "overview",
          title: "Overview",
          content: `
# 📖 Introduction

Welcome to the documentation. This guide will help you get started.

## Why use this framework?
- 🚀 **Fast**: Optimized for performance
- 🎨 **Styled**: Built-in TailwindCSS & DaisyUI support
- 🔧 **Easy to Use**: Clear API and component structure
        `,
        },
        {
          id: "features",
          title: "Key Features",
          content: `
# 🚀 Key Features

This project includes:

\`\`\`jsx
function Feature() {
  return <h1>Awesome Feature!</h1>;
}
\`\`\`

## Installation
Run the following command:

\`\`\`bash
npm install my-package
\`\`\`
        `,
        },
      ],
    },
    {
      id: "setup",
      title: "Setup Guide",
      subtopics: [
        {
          id: "installation",
          title: "Installation",
          content: `
# 🔧 Installation

## 1️⃣ Install Dependencies
Run:

\`\`\`bash
npm install
\`\`\`

## 2️⃣ Start Development Server
\`\`\`bash
npm run dev
\`\`\`
        `,
        },
        {
          id: "configuration",
          title: "Configuration",
          content: `
# ⚙️ Configuration

Modify \`config.js\` as follows:

\`\`\`javascript
const config = {
  apiKey: "YOUR_API_KEY",
  mode: "development",
};
export default config;
\`\`\`
        `,
        },
      ],
    },
  ];

  const [activeTopic, setActiveTopic] = useState(topics[0].subtopics[0]); // Default to first subtopic
  const [expandedTopics, setExpandedTopics] = useState({}); // Track expanded/collapsed topics
  const [copiedCode, setCopiedCode] = useState(null);

  // Copy code to clipboard
  const copyToClipboard = (code, id) => {
    navigator.clipboard.writeText(code).then(() => {
      setCopiedCode(id);
      setTimeout(() => setCopiedCode(null), 1500);
    });
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar - Navigation */}
      <aside className="w-1/4 bg-gray-100 p-6 border-r shadow-md">
        <h2 className="text-xl font-semibold text-gray-700">📚 Documentation</h2>
        <ul className="space-y-2 mt-4">
          {topics.map((topic) => (
            <li key={topic.id}>
              {/* Main Topic */}
              <button
                className="w-full text-left px-4 py-2 font-medium text-gray-800 hover:bg-gray-200 flex justify-between items-center"
                onClick={() => setExpandedTopics({ ...expandedTopics, [topic.id]: !expandedTopics[topic.id] })}
              >
                {topic.title}
                {expandedTopics[topic.id] ? <ChevronDownIcon className="h-5 w-5" /> : <ChevronRightIcon className="h-5 w-5" />}
              </button>

              {/* Subtopics */}
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

      {/* Main Content */}
      <main className="w-3/4 p-8 bg-white shadow-md">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">{activeTopic.title}</h1>
        <ReactMarkdown
          className="prose max-w-full text-gray-800"
          components={{
            code({ node, inline, className, children, ...props }) {
              const match = /language-(\w+)/.exec(className || "");
              const codeText = String(children).replace(/\n$/, "");
              const codeId = `${activeTopic.id}-${codeText.substring(0, 10)}`; // Unique ID for each code block
              return match ? (
                <div className="relative">
                  {/* Copy Button */}
                  <button
                    className="absolute top-2 right-2 bg-gray-700 text-white text-sm px-2 py-1 rounded hover:bg-gray-800 transition"
                    onClick={() => copyToClipboard(codeText, codeId)}
                  >
                    {copiedCode === codeId ? (
                      <>
                        <CheckIcon className="h-4 w-4 inline-block mr-1" /> Copied!
                      </>
                    ) : (
                      <>
                        <ClipboardIcon className="h-4 w-4 inline-block mr-1" /> Copy
                      </>
                    )}
                  </button>

                  {/* Code Block */}
                  <SyntaxHighlighter
                    style={atomDark}
                    language={match[1]}
                    PreTag="div"
                    {...props}
                  >
                    {codeText}
                  </SyntaxHighlighter>
                </div>
              ) : (
                <code className="bg-gray-200 text-red-500 px-1 py-0.5 rounded" {...props}>
                  {children}
                </code>
              );
            },
          }}
        >
          {activeTopic.content}
        </ReactMarkdown>
      </main>
    </div>
  );
}