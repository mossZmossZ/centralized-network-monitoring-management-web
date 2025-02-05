import ReactMarkdown from "react-markdown";
import PropTypes from "prop-types";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { atomDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { ClipboardIcon, CheckIcon } from "@heroicons/react/24/outline";
import { useState } from "react";

export default function Content({ activeTopic }) {
  const [copiedCode, setCopiedCode] = useState(null);

  const copyToClipboard = (code, id) => {
    navigator.clipboard.writeText(code).then(() => {
      setCopiedCode(id);
      setTimeout(() => setCopiedCode(null), 1500);
    });
  };

  return (
    <main className="w-3/4 p-8 bg-white shadow-md">
      {activeTopic ? (
        <>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">{activeTopic.title}</h1>
          <ReactMarkdown
            className="prose max-w-full text-gray-800"
            components={{
              code({ className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || "");
                const codeText = String(children).replace(/\n$/, "");
                const codeId = `${activeTopic.id}-${codeText.substring(0, 10)}`;
                return match ? (
                  <div className="relative">
                    <button
                      className="absolute top-2 right-2 bg-gray-700 text-white text-sm px-2 py-1 rounded hover:bg-gray-800 transition"
                      onClick={() => copyToClipboard(codeText, codeId)}
                    >
                      {copiedCode === codeId ? <CheckIcon className="h-4 w-4 inline-block mr-1" /> : <ClipboardIcon className="h-4 w-4 inline-block mr-1" />}
                    </button>
                    <SyntaxHighlighter style={atomDark} language={match[1]} PreTag="div" {...props}>
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
        </>
      ) : (
        <p className="text-gray-600">Please select a topic from the sidebar.</p>
      )}
    </main>
  );
}

// ✅ Prop Type Validation
Content.propTypes = {
  activeTopic: PropTypes.shape({
    id: PropTypes.string,
    title: PropTypes.string,
    content: PropTypes.string,
  }),
};