import { useState } from "react";
import { Card, CardContent } from "./components/ui/card";
import { Input } from "./components/ui/input";
import { Button } from "./components/ui/button";
import './app.css';

export default function ScraperPage() {
  const [keyword, setKeyword] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const savedSearches = ["jackets", "sweaters", "shirts", "pants", "shorts", "shoes"];

  const handleSearch = async (searchTerm = keyword) => {
    if (!searchTerm) return;
    setLoading(true);
    try {
      const response = await fetch(`https://app-cool-waterfall-6282.fly.dev/scrape?keyword=${encodeURIComponent(searchTerm)}`);
      const data = await response.json();
      setResults(data.results);
    } catch (err) {
      console.error("Error fetching results:", err);
      setResults([]);
    }
    setLoading(false);
  };

  return (
    <div className="page-container">
      <header className="page-header">
        <h1 className="header-title">shopGoodwillBetter</h1>
      </header>

      <main className="main-content">
        <div className="search-container">
          <div className="search-box">
            <Input
              type="text"
              placeholder="Search for clothing (e.g. shirt, jeans)"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              className="input-style"
            />
            <Button
              onClick={() => handleSearch()}
              disabled={loading}
              className="search-button"
            >
              {loading ? "Searching..." : "Search"}
            </Button>
          </div>
        </div>

        <div className="saved-searches">
          {savedSearches.map((term) => (
            <Button
              key={term}
              onClick={() => handleSearch(term)}
              className="saved-button"
            >
              {term}
            </Button>
          ))}
        </div>

        {loading && (
          <div className="loading-text">
            Loading results...
          </div>
        )}

        <div className="results-grid">
          {results.map((item, idx) => (
            <Card key={idx} className="result-card">
              <CardContent className="card-content">
                <img
                  src={item.image}
                  alt={item.title}
                  className="card-image"
                />
                <a href={item.url} target="_blank" rel="noopener noreferrer">
                  <h2 className="card-title">{item.title}</h2>
                </a>
                <p className="card-price">{item.price}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </main>
    </div>
  );
}
