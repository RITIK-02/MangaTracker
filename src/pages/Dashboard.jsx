import { useEffect, useState } from "react";
import API from "../api/axios";
import LibraryCard from "../components/LibraryCard";

export default function Dashboard() {
  const [data, setData] = useState([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const limit = 5;

  useEffect(() => {
    fetchLibrary(page);
  }, [page]);

  const fetchLibrary = async (pageNum) => {
    const res = await API.get(`/my-list?page=${pageNum}&limit=${limit}`);
    setData(res.data.data);
    setTotal(res.data.total);
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">My Library</h2>

      <div className="grid gap-4">
        {data.map((item) => (
          <LibraryCard key={item._id} item={item} refresh={() => fetchLibrary(page)} />
        ))}
      </div>

      {/* Pagination Controls */}
      <div className="flex justify-between mt-4">
        <button
          disabled={page === 1}
          onClick={() => setPage(page - 1)}
          className="bg-gray-200 px-3 py-1 rounded"
        >
          Previous
        </button>

        <span>Page {page}</span>

        <button
          disabled={page * limit >= total}
          onClick={() => setPage(page + 1)}
          className="bg-gray-200 px-3 py-1 rounded"
        >
          Next
        </button>
      </div>
    </div>
  );
}