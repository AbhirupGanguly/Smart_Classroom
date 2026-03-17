import { useEffect, useState } from "react";
import axios from "axios";

export default function StudentReport() {
  const [students, setStudents] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/students")
      .then((res) => setStudents(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="min-h-screen bg-[#5A0F0F] text-white p-10">

      <h1 className="text-3xl font-semibold mb-8">
        Student Report
      </h1>

      <div className="bg-[#7A1F1F] rounded-2xl shadow-xl overflow-hidden">

        <table className="w-full text-left">

          <thead className="bg-[#6B1A1A]">
            <tr>
              <th className="p-4">Name</th>
              <th className="p-4">Class</th>
              <th className="p-4">Roll No</th>
              <th className="p-4">Attention</th>
              <th className="p-4">Confidence</th>
            </tr>
          </thead>

          <tbody>
            {students.map((s, index) => (
              <tr key={index} className="border-t border-gray-700">

                <td className="p-4">{s.name}</td>
                <td className="p-4">{s.class}%</td>
                <td className="p-4">{s.rollno}%</td>
                <td className="p-4">{s.attention}%</td>
                <td className="p-4">{s.confidence}%</td>


              </tr>
            ))}
          </tbody>

        </table>
      </div>
    </div>
  );
}
