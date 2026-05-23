import { Link } from "react-router-dom";

export default function CoinCard({ coin }) {
  const price = coin.current_price;
  const change = coin.price_change_percentage_24h;
  const isPositive = change >= 0;

  return (
    <Link to={`/coin/${coin.id}`} className="coin-card">
      <div className="coin-card-rank">
        {coin.market_cap_rank ? `#${coin.market_cap_rank}` : "—"}
      </div>
      <img
        src={coin.image || coin.thumb || coin.large}
        alt={coin.name}
        className="coin-card-icon"
      />
      <div className="coin-card-info">
        <span className="coin-card-name">{coin.name}</span>
        <span className="coin-card-symbol">
          {coin.symbol?.toUpperCase()}
        </span>
      </div>
      <div className="coin-card-price">
        {price != null ? (
          <>
            <span className="coin-card-usd">${price.toLocaleString()}</span>
            <span className={`coin-card-change ${isPositive ? "positive" : "negative"}`}>
              {isPositive ? "▲" : "▼"} {Math.abs(change)?.toFixed(2)}%
            </span>
          </>
        ) : (
          <span className="coin-card-symbol">нет данных</span>
        )}
      </div>
    </Link>
  );
}