import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getTopCoins, searchCoins } from "../api/coins";
import CoinCard from "../components/CoinCard";

export default function Home() {
  const [search, setSearch] = useState("");

  const { data: topCoins, isLoading } = useQuery({
    queryKey: ["topCoins"],
    queryFn: () => getTopCoins().then((r) => r.data),
  });

  const { data: searchResults } = useQuery({
    queryKey: ["search", search],
    queryFn: () => searchCoins(search).then((r) => r.data),
    enabled: search.length > 1,
  });

  const coins = search.length > 1 ? searchResults : topCoins;

  return (
    <div className="page">
      <div className="page-header">
        <h1>Криптовалютный рынок</h1>
        <input
          className="search-input"
          placeholder="Поиск монеты..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {isLoading && <div className="loading">Загрузка...</div>}

      <div className="coins-grid">
        {coins?.map((coin) => (
          <CoinCard key={coin.id} coin={coin} />
        ))}
      </div>
    </div>
  );
}