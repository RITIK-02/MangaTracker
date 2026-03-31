import { useState } from "react";
import API from "../api/axios";

export default function UpdateModal({ item, onClose, onUpdate }) {
  const [status, setStatus] = useState(item.status);
  const [chapter, setChapter] = useState(item.current_chapter);
  const [rating, setRating] = useState(item.rating || "");

  const handleUpdate = async () => {
    await API.put(`/update/${item.manga_id}`, {
      status,
      current_chapter: Number(chapter),
      rating: rating ? Number(rating) : null,
    });

    onUpdate(); // refresh dashboard
    onClose();  // close modal
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-center">
      <div className="bg-white p-6 rounded-xl w-96">
        <h2 className="text-xl font-bold mb-4">Update Progress</h2>

        <label>Status</label>
        <select
          className="w-full mb-2"
          value={status}
          onChange={(e) => setStatus(e.target.value)}
        >
          <option value="reading">Reading</option>
          <option value="completed">Completed</option>
          <option value="plan">Plan to Read</option>
        </select>

        <label>Chapter</label>
        <input
          type="number"
          className="w-full mb-2"
          value={chapter}
          onChange={(e) => setChapter(e.target.value)}
        />

        <label>Rating</label>
        <input
          type="number"
          className="w-full mb-4"
          value={rating}
          onChange={(e) => setRating(e.target.value)}
        />

        <div className="flex justify-end gap-2">
          <button onClick={onClose}>Cancel</button>
          <button
            className="bg-blue-500 text-white px-3 py-1 rounded"
            onClick={handleUpdate}
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
}