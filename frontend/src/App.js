import { useState, useEffect } from "react";
import { Card, CardContent } from "./components/ui/card";
import { Input } from "./components/ui/input";
import { Button } from "./components/ui/button";
import './App.css';

export default function ScraperPage() {
  const defaultSearches = ["jacket", "sweater", "shirt", "pants", "shorts", "boots"];
  const [keyword, setKeyword] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [savedSearches, setSavedSearches] = useState(defaultSearches);

  useEffect(() => {
    const stored = localStorage.getItem("savedSearches");
    if (stored) {
      setSavedSearches(JSON.parse(stored));
    } else {
      localStorage.setItem("savedSearches", JSON.stringify(defaultSearches));
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("savedSearches", JSON.stringify(savedSearches));
  }, [savedSearches]);

  const handleSearch = async (searchTerm = keyword) => {
    if (!searchTerm) return;
    setLoading(true);
    try {
      const response = await fetch(
        `https://app-cool-waterfall-6282.fly.dev/scrape?term=${encodeURIComponent(searchTerm)}`
      );
      const data = await response.json();
      setResults(data.results);
    } catch (err) {
      console.error("Error fetching results:", err);
      setResults([]);
    }
    setLoading(false);
  };

  const handleSaveSearch = () => {
    const term = keyword.trim();
    if (term && !savedSearches.includes(term)) {
      setSavedSearches([...savedSearches, term]);
    }
  };

  const handleRemoveSearch = (termToRemove) => {
    setSavedSearches((prevSearches) =>
      prevSearches.filter((term) => term !== termToRemove)
    );
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="header-title">shopGoodwillBetter</h1>
      </div>

      <div className="page-container">
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
              <div key={term} className="saved-search-wrapper">
                <Button
                  onClick={() => handleSearch(term)}
                  className="saved-button"
                >
                  {term}
                </Button>
                <div
                  className="remove-button"
                  onClick={() => handleRemoveSearch(term)}
                >
                  —
                </div>
              </div>
            ))}
            {keyword.trim() && (
              <Button onClick={handleSaveSearch} className="save-search-button">
                +
              </Button>
            )}
          </div>

          {loading && <div className="loading-text">Loading results...</div>}

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
    </div>
  );
}
