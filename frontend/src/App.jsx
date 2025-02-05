import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "../components/navbar/index.jsx";
import Footer from "../components/footer/index.jsx";
import Main from "../components/main/index.jsx";
import { Report } from "../components/report/index.jsx";
import { About } from "../components/about/index.jsx";
import { Alert } from "../components/alert/index.jsx";
import { Systems } from "../components/systems/index.jsx";
import { Setting } from "../components/settings/index.jsx";
import { User } from "../components/user/index.jsx";
import DocsIndex from "../components/docs/DocsIndex.jsx";
import { Login } from "../components/login/index.jsx";

export default function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <div className="flex-grow">
          <Routes>
            <Route path="/" element={<Main />} />
            <Route path="/about" element={<About />} />
            <Route path="/report" element={<Report />} />
            <Route path="/alert" element={<Alert />} />
            <Route path="/systems" element={<Systems />} />
            <Route path="/setting" element={<Setting />} />
            <Route path="/user" element={<User />} />
            <Route path="/docs" element={<DocsIndex />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </div>
        <Footer />
      </div>
    </Router>
  );
}
