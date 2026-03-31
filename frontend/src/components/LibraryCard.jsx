import { useState } from "react";
import UpdateModal from "./UpdateModal";

export default function LibraryCard({ item, refresh }) {
  const [showModal, setShowModal] = useState(false);
  return (
    <div className="bg-white shadow-md rounded-xl p-4 flex gap-4">
      <img src={item.cover_image} className="w-24 h-32 rounded" />

      <div className="flex flex-col justify-between w-full">
        <h3 className="text-lg font-semibold">{item.title}</h3>

        <p>Status: {item.status}</p>
        <p>
          Progress: {item.current_chapter} / {item.total_chapters || "?"}
        </p>
        <p>⭐ {item.rating || "N/A"}</p>

        <button
          className="bg-gray-200 px-2 py-1 rounded w-fit"
          onClick={() => setShowModal(true)}
        >
          Update
        </button>
      </div>

      {showModal && (
        <UpdateModal
          item={item}
          onClose={() => setShowModal(false)}
          onUpdate={refresh}
        />
      )}
    </div>
  );
}