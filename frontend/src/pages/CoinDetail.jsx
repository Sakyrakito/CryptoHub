// src/pages/CoinDetail.jsx
import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer,
} from "recharts";
import {
  getCoinDetail,
  getCoinChart,
  checkFavorite,
  addFavorite,
  removeFavorite,
} from "../api/coins";
import useAuthStore from "../store/authStore";

export default function CoinDetail() {
  const { coinId } = useParams();
  const navigate = useNavigate();
  const token = useAuthStore((s) => s.token);
  const queryClient = useQueryClient();
  const [days, setDays] = useState(7);

  const { data: coin, isLoading } = useQuery({
    queryKey: ["coin", coinId],
    queryFn: () => getCoinDetail(coinId).then((r) => r.data),
  });

  const { data: chart } = useQuery({
    queryKey: ["chart", coinId, days],
    queryFn: () => getCoinChart(coinId, days).then((r) => r.data),
  });

  const { data: favData } = useQuery({
    queryKey: ["isFavorite", coinId],
    queryFn: () => checkFavorite(coinId).then((r) => r.data),
    enabled: !!token,
  });

  const addMutation = useMutation({
    mutationFn: () =>
      addFavorite({
        coin_id: coin.id,
        coin_symbol: coin.symbol,
        coin_name: coin.name,
      }),
    onSuccess: () => queryClient.invalidateQueries(["isFavorite", coinId]),
  });

  const removeMutation = useMutation({
    mutationFn: () => removeFavorite(coinId),
    onSuccess: () => queryClient.invalidateQueries(["isFavorite", coinId]),
  });

  if (isLoading) return <div className="loading">Загрузка...</div>;
  if (!coin) return <div className="loading">Монета не найдена</div>;

  const price = coin.market_data?.current_price?.usd;
  const change24h = coin.market_data?.price_change_percentage_24h;
  const marketCap = coin.market_data?.market_cap?.usd;
  const volume24h = coin.market_data?.total_volume?.usd;
  const isFav = favData?.is_favorite;

  const chartData = chart?.prices?.map(([timestamp, price]) => ({
    time: new Date(timestamp).toLocaleDateString("ru-RU"),
    price: parseFloat(price.toFixed(2)),
  }));

  return (
    <div className="page">
      {/* Шапка */}
      <div className="coin-detail-header">
        <button className="btn btn-outline" onClick={() => navigate(-1)}>
          ← Назад
        </button>
        <div className="coin-detail-title">
          <img src={coin.image?.large} alt={coin.name} className="coin-detail-icon" />
          <div>
            <h1>{coin.name}</h1>
            <span className="coin-card-symbol">{coin.symbol?.toUpperCase()}</span>
          </div>
        </div>
        {token && (
          <button
            className={`btn ${isFav ? "btn-danger" : "btn-outline"}`}
            onClick={() => isFav ? removeMutation.mutate() : addMutation.mutate()}
          >
            {isFav ? "★ В избранном" : "☆ Добавить"}
          </button>
        )}
      </div>

      {/* Цена и статистика */}
      <div className="coin-stats">
        <div className="coin-stat-main">
          <span className="coin-detail-price">${price?.toLocaleString()}</span>
          <span className={`coin-card-change ${change24h >= 0 ? "positive" : "negative"}`}>
            {change24h >= 0 ? "▲" : "▼"} {Math.abs(change24h)?.toFixed(2)}% за 24ч
          </span>
        </div>
        <div className="coin-stat-grid">
          <div className="coin-stat-item">
            <span className="stat-label">Рыночная капитализация</span>
            <span className="stat-value">${marketCap?.toLocaleString()}</span>
          </div>
          <div className="coin-stat-item">
            <span className="stat-label">Объём торгов (24ч)</span>
            <span className="stat-value">${volume24h?.toLocaleString()}</span>
          </div>
          <div className="coin-stat-item">
            <span className="stat-label">Место в рейтинге</span>
            <span className="stat-value">#{coin.market_cap_rank}</span>
          </div>
          <div className="coin-stat-item">
            <span className="stat-label">Сайт</span>
            {coin.links?.homepage?.[0] ? (
              <a
                href={coin.links.homepage[0]}
                target="_blank"
                rel="noreferrer"
                className="stat-link"
              >
                {coin.links.homepage[0]
                  .replace("https://", "")
                  .replace("http://", "")
                  .replace(/\/$/, "")}
              </a>
            ) : (
              <span className="stat-value">—</span>
            )}
          </div>
        </div>
      </div>

      {/* График */}
      <div className="chart-section">
        <div className="chart-header">
          <h2>График цены</h2>
          <div className="chart-days">
            {[1, 7, 30, 90].map((d) => (
              <button
                key={d}
                className={`btn ${days === d ? "btn-primary" : "btn-outline"}`}
                onClick={() => setDays(d)}
              >
                {d === 1 ? "1д" : d === 7 ? "7д" : d === 30 ? "1м" : "3м"}
              </button>
            ))}
          </div>
        </div>
        {chartData && (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <XAxis
                dataKey="time"
                tick={{ fill: "#8892a4", fontSize: 11 }}
                tickLine={false}
                interval="preserveStartEnd"
              />
              <YAxis
                tick={{ fill: "#8892a4", fontSize: 11 }}
                tickLine={false}
                axisLine={false}
                tickFormatter={(v) => `$${v.toLocaleString()}`}
                width={90}
              />
              <Tooltip
                contentStyle={{ background: "#1a1d2e", border: "1px solid #2d3055" }}
                labelStyle={{ color: "#8892a4" }}
                formatter={(v) => [`$${v.toLocaleString()}`, "Цена"]}
              />
              <Line
                type="monotone"
                dataKey="price"
                stroke="#6c63ff"
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* Описание */}
      {coin.description?.ru || coin.description?.en ? (
        <div className="coin-description">
          <h2>О проекте</h2>
          <p
            dangerouslySetInnerHTML={{
              __html: (coin.description?.ru || coin.description?.en)?.slice(0, 800) + "...",
            }}
          />
        </div>
      ) : null}
    </div>
  );
}