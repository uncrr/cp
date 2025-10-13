import { useState } from 'react';

export default function SearchComponent({ products }) {
  const [query, setQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [results, setResults] = useState([]);

  // Get unique categories from products for dropdown
  const categories = [...new Set(products.map(p => p.category))];

  const handleSearch = () => {
    const filtered = products.filter(p => {
      const matchesQuery = query ? p.name.toLowerCase().includes(query.toLowerCase()) : true;
      const matchesCategory = selectedCategory ? p.category === selectedCategory : true;
      return matchesQuery && matchesCategory;
    });
    setResults(filtered);
  };

  return (
    <div className="w-full max-w-md bg-white p-6 rounded-lg shadow-md">
      <div className="flex flex-col space-y-4">
        {/* Categories Dropdown */}
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="border border-gray-300 p-2 rounded"
        >
          <option value="">All Categories</option>
          {categories.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>

        {/* Search Bar and Button */}
        <div className="flex">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search products..."
            className="flex-1 border border-gray-300 p-2 rounded-l"
          />
          <button
            onClick={handleSearch}
            className="bg-blue-500 text-white p-2 rounded-r hover:bg-blue-600"
          >
            Search
          </button>
        </div>
      </div>

      {/* Results List */}
      <div className="mt-6">
        {results.length > 0 ? (
          <ul className="space-y-4">
            {results.map(product => (
              <li key={product.id} className="border-b pb-2">
                <h3 className="font-semibold">{product.name}</h3>
                <p>Price: ${product.price.toFixed(2)}</p>
                <p>Source: {product.source}</p>
                <a href={product.url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
                  View on {product.source}
                </a>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-500">No results found. Try a different search!</p>
        )}
      </div>
    </div>
  );
}