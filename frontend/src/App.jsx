import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "../components/navbar/Navbar.jsx";
import Footer from "../components/footer/index.jsx";
import Main from "../components/main/index.jsx";
import { Report } from "../components/report/index.jsx";
import { About } from "../components/about/index.jsx";
import { Alert } from "../components/alert/index.jsx";
import { Services } from "../components/Services/index.jsx";
import { Setting } from "../components/settings/index.jsx";
import { User } from "../components/user/index.jsx";
import DocsIndex from "../components/docs/DocsIndex.jsx";
import { Login } from "../components/login/index.jsx";
import { Maintenance } from "../components/maintenance/index.jsx";
import WebSocketNotification from "./WebSocketNotification";
import ProtectedRoute from "./ProtectedRoute";

export default function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <WebSocketNotification />
        <div className="flex-grow">
          <Routes>
            {/* Public routes */}
            <Route path="/" element={<Main />} />
            <Route path="/login" element={<Login />} />

            {/* Protected routes */}
            <Route
              path="/about"
              element={
                <ProtectedRoute>
                  <About />
                </ProtectedRoute>
              }
            />
            <Route
              path="/report"
              element={
                <ProtectedRoute>
                  <Report />
                </ProtectedRoute>
              }
            />
            <Route
              path="/alert"
              element={
                <ProtectedRoute>
                  <Alert />
                </ProtectedRoute>
              }
            />
            <Route
              path="/services"
              element={
                <ProtectedRoute>
                  <Services />
                </ProtectedRoute>
              }
            />
            <Route
              path="/setting"
              element={
                <ProtectedRoute>
                  <Setting />
                </ProtectedRoute>
              }
            />
            <Route
              path="/user"
              element={
                <ProtectedRoute>
                  <User />
                </ProtectedRoute>
              }
            />
            <Route
              path="/docs"
              element={
                <ProtectedRoute>
                  <DocsIndex />
                </ProtectedRoute>
              }
            />
            <Route
              path="/maintenance"
              element={
                <ProtectedRoute>
                  <Maintenance />
                </ProtectedRoute>
              }
            />
          </Routes>
        </div>
        <Footer />
      </div>
    </Router>
  );
}
