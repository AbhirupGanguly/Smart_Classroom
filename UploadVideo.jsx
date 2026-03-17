import { useState } from "react";
import axios from "axios";

export default function UploadVideo() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Select a video first");
      return;
    }

    const formData = new FormData();
    formData.append("video", file);

    try {
      setLoading(true);

      const res = await axios.post(
        "http://localhost:5000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      // redirect to result page
      window.location.href = `/video-result?id=${res.data.id}`;

    } catch (err) {
      console.error(err);
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#5A0F0F] text-white">
      
      <div className="bg-[#7A1F1F] p-8 rounded-2xl shadow-2xl w-[420px]">

        <h2 className="text-2xl font-semibold mb-6">
          Upload Video
        </h2>

        <input
          type="file"
          accept="video/*"
          onChange={(e) => setFile(e.target.files[0])}
          className="w-full mb-6 text-sm"
        />

        <button
          onClick={handleUpload}
          className="w-full bg-[#22C55E] py-2 rounded-lg font-medium hover:opacity-90 transition"
        >
          {loading ? "Uploading..." : "Upload"}
        </button>

      </div>
    </div>
  );
}
