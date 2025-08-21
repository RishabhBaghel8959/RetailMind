import React, { useState } from "react";
import axios from "axios";
import Dashboard from "./Dashboard";

function App() {
  const [reviews, setReviews] = useState("");
  const [results, setResults] = useState([]);

  const handleAnalyze = async () => {
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/analyze`,
        { reviews: reviews.split("\n") }
      );
      setResults(response.data);
    } catch (error) {
      console.error("Error analyzing reviews:", error);
    }
  };

  return (
    <div className="App" style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>🛒 Customer Feedback Dashboard</h1>

      <textarea
        rows="5"
        cols="60"
        value={reviews}
        onChange={(e) => setReviews(e.target.value)}
        placeholder="Enter one review per line..."
      />
      <br />
      <button onClick={handleAnalyze}>Analyze</button>

      {results.length > 0 && <Dashboard results={results} />}
    </div>
  );
}

export default App;
