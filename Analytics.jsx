import { useEffect, useState } from "react";
import axios from "axios";

export default function Analytics() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios
      .get("http://localhost:5000/analytics")
      .then((res) => setData(res.data))
      .catch((err) => console.error(err));
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#5A0F0F] text-white">
        Loading...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#5A0F0F] text-white p-10">

      <h1 className="text-3xl font-semibold mb-8">
        Analytics Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        <div className="bg-[#7A1F1F] p-6 rounded-2xl shadow-xl">
          <h3 className="text-lg mb-2">Total Videos</h3>
          <p className="text-3xl font-bold">{data.totalVideos}</p>
        </div>

        <div className="bg-[#7A1F1F] p-6 rounded-2xl shadow-xl">
          <h3 className="text-lg mb-2">Average Confidence</h3>
          <p className="text-3xl font-bold">{data.avgConfidence}%</p>
        </div>

        <div className="bg-[#7A1F1F] p-6 rounded-2xl shadow-xl">
          <h3 className="text-lg mb-2">Average Clarity</h3>
          <p className="text-3xl font-bold">{data.avgClarity}%</p>
        </div>

        <div className="bg-[#7A1F1F] p-6 rounded-2xl shadow-xl">
          <h3 className="text-lg mb-2">Eye Contact Score</h3>
          <p className="text-3xl font-bold">{data.eyeContact}%</p>
        </div>

      </div>
    </div>
  );
}
