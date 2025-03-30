import { useEffect, useState, useRef } from "react";

const WebSocketNotification = () => {
  const [message, setMessage] = useState("");
  const [showNotification, setShowNotification] = useState(false);
  const [connectionError, setConnectionError] = useState(false);
  const hasShownError = useRef(false);
  const socketRef = useRef(null);

  // ✅ Use VITE_API_URL from .env for WebSocket URL
  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    connectWebSocket();
    return () => socketRef.current?.close();
  }, []);

  const connectWebSocket = () => {
    // ✅ Dynamically use WebSocket URL based on API URL
    const wsUrl = API_URL.replace("http", "ws") + "/ws/notify";
    const socket = new WebSocket(wsUrl);
    socketRef.current = socket;

    socket.onopen = () => {
      console.log("✅ WebSocket connected.");
      setConnectionError(false);
    };

    socket.onmessage = (event) => {
      setMessage(event.data);
      setShowNotification(true);
      setTimeout(() => setShowNotification(false), 5000);
    };

    socket.onerror = (error) => {
      console.error("❌ WebSocket error:", error);
      if (!hasShownError.current) {
        setConnectionError(true);
        hasShownError.current = true;
      }
    };

    socket.onclose = (event) => {
      console.warn("🔁 WebSocket closed, retrying...");
      if (!hasShownError.current && !event.wasClean) {
        setConnectionError(true);
        hasShownError.current = true;
      }

      // Try to reconnect after a delay
      setTimeout(() => {
        connectWebSocket();
      }, 3000);
    };
  };

  return (
    <>
      {/* Sliding Message Notification */}
      {showNotification && (
        <div className="fixed top-4 right-4 z-50 animate-slide-in">
          <div className="alert alert-info shadow-lg w-full max-w-xs">
            <div>
              <span>{message}</span>
            </div>
          </div>
        </div>
      )}

      {/* Persistent Warning Notification */}
      {connectionError && (
        <div className="fixed top-20 right-4 z-40 animate-slide-in">
          <div className="alert alert-warning shadow-lg w-full max-w-xs">
            <div>
              <span>
                ⚠️ Cannot connect to backend WebSocket (ERRCON). Retrying silently...
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Animation Styles */}
      <style>
        {`
          @keyframes slide-in {
            0% {
              transform: translateX(100%);
              opacity: 0;
            }
            100% {
              transform: translateX(0);
              opacity: 1;
            }
          }
          .animate-slide-in {
            animation: slide-in 0.5s ease-out forwards;
          }
        `}
      </style>
    </>
  );
};

export default WebSocketNotification;
