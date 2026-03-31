import API from "../api/axios";

export default function MangaCard({ manga }) {
  const addToLibrary = async () => {
    await API.post("/add", {
      manga_id: manga._id,
      status: "reading",
      current_chapter: 0,
    });
  };

  return (
    <div className="border p-4 rounded">
      <img src={manga.cover_image} alt="" />
      <h3>{manga.title}</h3>
      <button onClick={addToLibrary}>Add</button>
    </div>
  );
}