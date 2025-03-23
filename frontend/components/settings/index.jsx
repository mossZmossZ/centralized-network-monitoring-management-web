import React, { useState } from 'react';

export function Setting() {
  const [isLoading, setIsLoading] = useState(true);

  // Handle iframe load event
  const handleIframeLoad = () => {
    setIsLoading(false);
  };

  // Accessing the environment variables
  const apiUrl = import.meta.env.VITE_UPTIME_URL;
  const configUrl = import.meta.env.VITE_PORTAINER_URL;

  return (
    <div className="relative p-6 flex flex-col items-center justify-center">
      {/* Top Left Text */}
      <div className="absolute top-4 left-4 text-xl font-semibold text-gray-700 ml-10">
        Services Running
      </div>

      {/* Top Right Button */}
      <div className="absolute top-4 right-10">
        <a
          href={configUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn-primary transform transition duration-300 hover:scale-105 hover:rotate-3"
        >
          Edit Configuration
        </a>
      </div>

      {/* Loading Spinner (DaisyUI) */}
      {isLoading && (
        <div className="absolute inset-0 flex justify-center items-center bg-white bg-opacity-50 z-50">
          <div className="loading loading-spinner loading-lg text-blue-500"></div>
        </div>
      )}

      {/* Iframe containing UptimeKuma status page */}
      <iframe
        src={`${apiUrl}/status/services`}
        width="100%"
        height="600px"
        frameBorder="0"
        className="mt-16"
        onLoad={handleIframeLoad} // Trigger the load event
      ></iframe>
    </div>
  );
}
