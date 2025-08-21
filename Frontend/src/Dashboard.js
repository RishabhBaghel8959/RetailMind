import React, { useState } from "react";
import {
  PieChart, Pie, Cell, Tooltip, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid
} from "recharts";

function Dashboard({ results }) {
  const [filter, setFilter] = useState("all");

  if (!results || results.length === 0) {
    return (
      <div className="text-center mt-10 text-gray-500 text-lg">
        No analysis results yet. Please enter reviews above.
      </div>
    );
  }

  // Apply Filter
  const filteredResults =
    filter === "all"
      ? results
      : results.filter(r => r.sentiment === filter);

  // Summary Counts
  const total = results.length;
  const positives = results.filter(r => r.sentiment === "positive").length;
  const negatives = results.filter(r => r.sentiment === "negative").length;

  // Sentiment Data for Pie Chart
  const sentimentData = [
    { name: "Positive", value: positives },
    { name: "Negative", value: negatives },
  ];
  const COLORS = ["#22c55e", "#ef4444"];

  // Topic Counts
  const topicCounts = {};
  filteredResults.forEach(r => {
    if (r.topics) {
      r.topics.split(",").forEach(topic => {
        const t = topic.trim();
        if (t) topicCounts[t] = (topicCounts[t] || 0) + 1;
      });
    }
  });

  const topicData = Object.entries(topicCounts).map(([topic, count]) => ({
    topic,
    count,
  }));

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h2 className="text-3xl font-bold mb-6 text-center text-indigo-700">
        📊 Customer Feedback Analysis Dashboard
      </h2>

      {/* Summary Section */}
      <div className="grid grid-cols-3 gap-6 text-center mb-8">
        <div className="bg-white p-4 rounded-xl shadow">
          <p className="text-gray-500">Total Reviews</p>
          <p className="text-2xl font-bold">{total}</p>
        </div>
        <div className="bg-green-100 p-4 rounded-xl shadow">
          <p className="text-gray-500">Positive</p>
          <p className="text-2xl font-bold text-green-700">{positives}</p>
        </div>
        <div className="bg-red-100 p-4 rounded-xl shadow">
          <p className="text-gray-500">Negative</p>
          <p className="text-2xl font-bold text-red-700">{negatives}</p>
        </div>
      </div>

      {/* Filter */}
      <div className="flex justify-center mb-6">
        <button
          onClick={() => setFilter("all")}
          className={`px-4 py-2 mx-2 rounded-lg ${
            filter === "all" ? "bg-indigo-600 text-white" : "bg-gray-200"
          }`}
        >
          All
        </button>
        <button
          onClick={() => setFilter("positive")}
          className={`px-4 py-2 mx-2 rounded-lg ${
            filter === "positive" ? "bg-green-600 text-white" : "bg-gray-200"
          }`}
        >
          Positive
        </button>
        <button
          onClick={() => setFilter("negative")}
          className={`px-4 py-2 mx-2 rounded-lg ${
            filter === "negative" ? "bg-red-600 text-white" : "bg-gray-200"
          }`}
        >
          Negative
        </button>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Pie Chart */}
        <div className="bg-white shadow-lg rounded-2xl p-6">
          <h3 className="text-lg font-semibold mb-4 text-center text-gray-700">Sentiment Distribution</h3>
          <PieChart width={400} height={300}>
            <Pie
              data={sentimentData}
              cx={200}
              cy={150}
              innerRadius={70}
              outerRadius={120}
              dataKey="value"
              label
            >
              {sentimentData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </div>

        {/* Bar Chart */}
        <div className="bg-white shadow-lg rounded-2xl p-6">
          <h3 className="text-lg font-semibold mb-4 text-center text-gray-700">Top Topics</h3>
          <BarChart width={400} height={300} data={topicData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="topic" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#3b82f6" />
          </BarChart>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white shadow-lg rounded-2xl p-6 mt-10">
        <h3 className="text-lg font-semibold mb-4 text-center text-gray-700">Review Details</h3>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse border border-gray-200 text-sm">
            <thead>
              <tr className="bg-indigo-100">
                <th className="p-2 border">Review</th>
                <th className="p-2 border">Summary</th>
                <th className="p-2 border">Sentiment</th>
                <th className="p-2 border">Topics</th>
              </tr>
            </thead>
            <tbody>
              {filteredResults.map((r, i) => (
                <tr key={i} className="hover:bg-gray-50 transition duration-200 text-center">
                  <td className="p-2 border">{r.review}</td>
                  <td className="p-2 border">{r.summary}</td>
                  <td className={`p-2 border font-bold ${
                      r.sentiment === "positive" ? "text-green-600" : "text-red-600"
                    }`}>
                    {r.sentiment}
                  </td>
                  <td className="p-2 border">{r.topics}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
