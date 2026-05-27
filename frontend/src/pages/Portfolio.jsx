import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getPortfolio, addPortfolioAsset, removePortfolioAsset } from "../api/coins";

export default function Portfolio() {
  const queryClient = useQueryClient();
  const [form, setForm] = useState({
    coin_id: "",
    coin_symbol: "",
    coin_name: "",
    amount: "",
  });
  const [error, setError] = useState("");

  const { data: portfolio, isLoading } = useQuery({
    queryKey: ["portfolio"],
    queryFn: () => getPortfolio().then((r) => r.data),
    refetchInterval: 60000, // обновляем каждую минуту
  });

  const addMutation = useMutation({
    mutationFn: addPortfolioAsset,
    onSuccess: () => {
      queryClient.invalidateQueries(["portfolio"]);
      setForm({ coin_id: "", coin_symbol: "", coin_name: "", amount: "" });
      setError("");
    },
    onError: (err) => setError(err.response?.data?.detail || "Ошибка"),
  });

  const removeMutation = useMutation({
    mutationFn: removePortfolioAsset,
    onSuccess: () => queryClient.invalidateQueries(["portfolio"]),
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.coin_id || !form.amount || parseFloat(form.amount) <= 0) {
      setError("Заполните все поля");
      return;
    }
    addMutation.mutate({
      ...form,
      coin_symbol: form.coin_symbol || form.coin_id.toUpperCase(),
      coin_name: form.coin_name || form.coin_id,
      amount: parseFloat(form.amount),
    });
  };

  const formatValue = (value) => {
    if (!value) return "—";
    return "$" + value.toLocaleString("ru-RU", { maximumFractionDigits: 2 });
  };

  const formatAmount = (amount) => {
    if (amount >= 1) return amount.toLocaleString("ru-RU", { maximumFractionDigits: 4 });
    return amount.toFixed(8);
  };

  const totalValue = portfolio?.total_value || 0;

  return (
    <div className="page">
      <h1>Мой портфель</h1>

      {/* Общая стоимость */}
      <div className="portfolio-total">
        <span className="portfolio-total-label">Общая стоимость</span>
        <span className="portfolio-total-value">{formatValue(totalValue)}</span>
      </div>

      {/* Форма добавления */}
      <div className="alert-form-card">
        <h2>Добавить монету</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit} className="alert-form">
          <div className="alert-form-row">
            <div className="form-group">
              <label className="form-label">ID монеты</label>
              <input
                className="input"
                placeholder="bitcoin, ethereum..."
                value={form.coin_id}
                onChange={(e) =>
                  setForm({ ...form, coin_id: e.target.value.toLowerCase() })
                }
              />
            </div>
            <div className="form-group">
              <label className="form-label">Символ</label>
              <input
                className="input"
                placeholder="BTC"
                value={form.coin_symbol}
                onChange={(e) =>
                  setForm({ ...form, coin_symbol: e.target.value.toUpperCase() })
                }
              />
            </div>
            <div className="form-group">
              <label className="form-label">Название</label>
              <input
                className="input"
                placeholder="Bitcoin"
                value={form.coin_name}
                onChange={(e) => setForm({ ...form, coin_name: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Количество</label>
              <input
                className="input"
                type="number"
                step="any"
                min="0"
                placeholder="0.5"
                value={form.amount}
                onChange={(e) => setForm({ ...form, amount: e.target.value })}
              />
            </div>
            <button
              className="btn btn-primary"
              type="submit"
              disabled={addMutation.isPending}
            >
              {addMutation.isPending ? "..." : "Добавить"}
            </button>
          </div>
        </form>
      </div>

      {/* Список активов */}
      {isLoading && <div className="loading">Загрузка...</div>}

      {portfolio?.assets?.length === 0 && (
        <p className="empty-state">Портфель пуст — добавьте первую монету</p>
      )}

      {portfolio?.assets?.length > 0 && (
        <div className="portfolio-table">
          <div className="portfolio-table-header">
            <span>Монета</span>
            <span>Количество</span>
            <span>Цена</span>
            <span>Стоимость</span>
            <span>24ч</span>
            <span></span>
          </div>
          {portfolio.assets.map((asset) => (
            <div key={asset.id} className="portfolio-row">
              <div className="portfolio-coin">
                <span className="alert-symbol">{asset.coin_symbol}</span>
                <span className="portfolio-coin-name">{asset.coin_name}</span>
              </div>
              <span className="portfolio-amount">
                {formatAmount(asset.amount)}
              </span>
              <span className="portfolio-price">
                {asset.current_price
                  ? "$" + asset.current_price.toLocaleString()
                  : "—"}
              </span>
              <span className="portfolio-value">
                {formatValue(asset.total_value)}
              </span>
              <span
                className={`portfolio-change ${
                  asset.change_24h >= 0 ? "positive" : "negative"
                }`}
              >
                {asset.change_24h != null
                  ? (asset.change_24h >= 0 ? "▲ " : "▼ ") +
                    Math.abs(asset.change_24h).toFixed(2) + "%"
                  : "—"}
              </span>
              <button
                className="btn btn-danger"
                onClick={() => removeMutation.mutate(asset.coin_id)}
              >
                Удалить
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}