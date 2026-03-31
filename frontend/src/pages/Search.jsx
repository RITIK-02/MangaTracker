import { useState } from "react";
import API from "../api/axios";
import MangaCard from "../components/MangaCard";

export default function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const search = async () => {
    const res = await API.get(`/search?query=${query}`);
    setResults(res.data.data);
  };

  return (
    <div className="p-6">
      <input onChange={(e) => setQuery(e.target.value)} placeholder="Search manga..." />
      <button onClick={search}>Search</button>

      <div className="grid grid-cols-3 gap-4 mt-4">
        {results.map((manga) => (
          <MangaCard key={manga.anilist_id} manga={manga} />
        ))}
      </div>
    </div>
  );
}