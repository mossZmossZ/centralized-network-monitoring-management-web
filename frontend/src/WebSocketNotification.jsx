// WebSocketNotification.jsx
import { useEffect, useState } from "react";

const WebSocketNotification = () => {
  const [message, setMessage] = useState("");  // To hold incoming notification messages
  const [showNotification, setShowNotification] = useState(false);  // To control visibility

  useEffect(() => {
    // Create a WebSocket connection to the FastAPI backend
    const socket = new WebSocket("ws://localhost:8000/ws/notify");

    // Listen for messages from the WebSocket server
    socket.onmessage = (event) => {
      setMessage(event.data);  // Set the received message
      setShowNotification(true);  // Show notification
      setTimeout(() => setShowNotification(false), 5000);  // Hide after 5 seconds
    };

    socket.onerror = (error) => {
      console.error("WebSocket Error: ", error);
    };

    return () => {
      socket.close();  // Clean up WebSocket connection on unmount
    };
  }, []);

  return (
    <>
      {showNotification && (
        <div className="fixed top-4 right-4 w-full max-w-xs">
          <div className="alert alert-info shadow-lg">
            <div>
              <span>{message}</span>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default WebSocketNotification;
