import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getAlerts, createAlert, deleteAlert } from "../api/coins";

export default function Alerts() {
  const queryClient = useQueryClient();
  const [form, setForm] = useState({
    coin_id: "",
    coin_symbol: "",
    target_price: "",
    direction: "above",
  });
  const [error, setError] = useState("");

  const { data: alerts, isLoading } = useQuery({
    queryKey: ["alerts"],
    queryFn: () => getAlerts().then((r) => r.data),
  });

  const createMutation = useMutation({
    mutationFn: createAlert,
    onSuccess: () => {
      queryClient.invalidateQueries(["alerts"]);
      setForm({ coin_id: "", coin_symbol: "", target_price: "", direction: "above" });
      setError("");
    },
    onError: (err) => setError(err.response?.data?.detail || "Ошибка"),
  });

  const deleteMutation = useMutation({
    mutationFn: deleteAlert,
    onSuccess: () => queryClient.invalidateQueries(["alerts"]),
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.coin_id || !form.target_price) {
      setError("Заполните все поля");
      return;
    }
    createMutation.mutate({
      ...form,
      coin_symbol: form.coin_symbol || form.coin_id.toUpperCase(),
      target_price: parseFloat(form.target_price),
    });
  };

  return (
    <div className="page">
      <h1>Уведомления по цене</h1>

      {/* Форма создания */}
      <div className="alert-form-card">
        <h2>Новое уведомление</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit} className="alert-form">
          <div className="alert-form-row">
            <div className="form-group">
              <label className="form-label">ID монеты</label>
              <input
                className="input"
                placeholder="bitcoin, ethereum..."
                value={form.coin_id}
                onChange={(e) => setForm({ ...form, coin_id: e.target.value.toLowerCase() })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Символ (необязательно)</label>
              <input
                className="input"
                placeholder="BTC, ETH..."
                value={form.coin_symbol}
                onChange={(e) => setForm({ ...form, coin_symbol: e.target.value.toUpperCase() })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Цена ($)</label>
              <input
                className="input"
                type="number"
                placeholder="100000"
                value={form.target_price}
                onChange={(e) => setForm({ ...form, target_price: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Условие</label>
              <select
                className="input"
                value={form.direction}
                onChange={(e) => setForm({ ...form, direction: e.target.value })}
              >
                <option value="above">Выше ▲</option>
                <option value="below">Ниже ▼</option>
              </select>
            </div>
            <button
              className="btn btn-primary"
              type="submit"
              disabled={createMutation.isPending}
            >
              {createMutation.isPending ? "..." : "Добавить"}
            </button>
          </div>
        </form>
      </div>

      {/* Активные уведомления */}
      <div className="alerts-section">
        <h2>Активные уведомления</h2>
        {isLoading && <div className="loading">Загрузка...</div>}
        {alerts?.filter((a) => a.is_active).length === 0 && (
          <p className="empty-state">Нет активных уведомлений</p>
        )}
        <div className="alerts-list">
          {alerts?.filter((a) => a.is_active).map((alert) => (
            <div key={alert.id} className="alert-item">
              <div className="alert-item-info">
                <span className="alert-symbol">{alert.coin_symbol}</span>
                <span className="alert-condition">
                  {alert.direction === "above" ? "▲ выше" : "▼ ниже"}
                </span>
                <span className="alert-price">${parseFloat(alert.target_price).toLocaleString()}</span>
              </div>
              <div className="alert-item-meta">
                <span className="alert-date">
                  {new Date(alert.created_at).toLocaleDateString("ru-RU")}
                </span>
                <button
                  className="btn btn-danger"
                  onClick={() => deleteMutation.mutate(alert.id)}
                >
                  Удалить
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* История срабатываний */}
      <AlertHistory />
    </div>
  );

    function AlertHistory() {
    const { data: alerts } = useQuery({
        queryKey: ["alerts"],
        queryFn: () => getAlerts().then((r) => r.data),
    });

    const triggered = alerts?.filter((a) => !a.is_active) || [];

    if (triggered.length === 0) return null;

    return (
        <div className="alerts-section">
        <h2>История срабатываний</h2>
        <div className="alerts-list">
            {triggered.map((alert) => (
            <div key={alert.id} className="alert-item alert-item-triggered">
                <div className="alert-item-info">
                <span className="alert-triggered-badge">✓ Сработало</span>
                <span className="alert-symbol">{alert.coin_symbol}</span>
                <span className="alert-condition">
                    {alert.direction === "above" ? "▲ выше" : "▼ ниже"}
                </span>
                <span className="alert-price">
                    ${parseFloat(alert.target_price).toLocaleString()}
                </span>
                </div>
                <span className="alert-date">
                {new Date(alert.created_at).toLocaleDateString("ru-RU")}
                </span>
            </div>
            ))}
        </div>
        </div>
    );
    }
}