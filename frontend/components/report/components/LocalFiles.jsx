import { useState, useEffect } from "react";
import axios from "axios";

export function LocalFiles() {
  const [files, setFiles] = useState([]);
  const [search, setSearch] = useState("");
  const [sortAsc, setSortAsc] = useState(true);

  const fetchFiles = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/files");
      setFiles(response.data);
    } catch (error) {
      console.error("Error fetching files:", error);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  const filteredFiles = files
    .filter((file) => file.toLowerCase().includes(search.toLowerCase()))
    .sort((a, b) => (sortAsc ? a.localeCompare(b) : b.localeCompare(a)));

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Local Files</h2>
      <div className="flex space-x-4 mb-4">
        <input
          type="text"
          className="input input-bordered"
          placeholder="Search files..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <button className="btn" onClick={() => setSortAsc(!sortAsc)}>
          {sortAsc ? "Sort Desc" : "Sort Asc"}
        </button>
      </div>
      <ul>
        {filteredFiles.map((file, index) => (
          <li key={index}>{file}</li>
        ))}
      </ul>
    </div>
  );
}