import { useState } from "react";
import { Card, CardContent } from "./components/ui/card";
import { Input } from "./components/ui/input";
import { Button } from "./components/ui/button";

export default function ScraperPage() {
  const [keyword, setKeyword] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!keyword) return;
    setLoading(true);
    try {
      const response = await fetch(`https://shoppinggoodwill.onrender.com/scrape?keyword=${encodeURIComponent(keyword)}`);
      const data = await response.json();
      setResults(data.results);
    } catch (err) {
      console.error("Error fetching results:", err);
      setResults([]);
    }
    setLoading(false);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold text-center">ShopGoodwill Scraper</h1>
      <div className="flex space-x-2">
        <Input
          type="text"
          placeholder="Search for clothing (e.g. shirt, jeans)"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
        />
        <Button onClick={handleSearch} disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </Button>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        {results.map((item, idx) => (
          <Card key={idx} className="hover:shadow-md">
            <CardContent className="p-4 space-y-2">
              <a href={item.url} target="_blank" rel="noopener noreferrer">
                <h2 className="text-lg font-semibold text-blue-600 hover:underline">{item.title}</h2>
              </a>
              <p className="text-gray-700">{item.price}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
