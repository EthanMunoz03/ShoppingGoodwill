import { useState } from "react";
import { Card, CardContent } from "./components/ui/card";
import { Input } from "./components/ui/input";
import { Button } from "./components/ui/button";

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
    <div className="min-h-screen bg-gray-100">
      <header className="bg-blue-800 text-white py-6 text-center">
        <h1 className="text-4xl font-bold">shopGoodwillBetter</h1>
      </header>

      <main className="max-w-screen-xl mx-auto p-6">
        <div className="flex justify-center mb-6">
          <Input
            type="text"
            placeholder="Search for clothing (e.g. shirt, jeans)"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            className="max-w-xl rounded-l-full"
          />
          <Button
            onClick={() => handleSearch()}
            disabled={loading}
            className="rounded-r-full"
          >
            {loading ? "Searching..." : "Search"}
          </Button>
        </div>

        <div className="flex justify-center gap-2 mb-6 flex-wrap">
          {savedSearches.map((term) => (
            <Button
              key={term}
              onClick={() => handleSearch(term)}
              className="bg-blue-100 text-blue-800 hover:bg-blue-200"
            >
              {term}
            </Button>
          ))}
        </div>

        {loading && (
          <div className="text-center text-lg font-semibold text-blue-800 mb-6">
            Loading results...
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {results.map((item, idx) => (
            <Card key={idx} className="hover:shadow-md">
              <CardContent className="p-4 space-y-2 text-center">
                <img
                  src={item.image}
                  alt={item.title}
                  className="h-48 w-full object-cover mb-4 rounded-md"
                />
                <a href={item.url} target="_blank" rel="noopener noreferrer">
                  <h2 className="text-lg font-semibold text-blue-600 hover:underline">{item.title}</h2>
                </a>
                <p className="text-gray-700">{item.price}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </main>
    </div>
  );
}
