import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { convertCurrency, getPopularCoins, getFiatList } from "../api/coins";

export default function Converter() {
  const [fromId, setFromId] = useState("bitcoin");
  const [toId, setToId] = useState("usd");
  const [amount, setAmount] = useState("1");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const { data: popularCoins } = useQuery({
    queryKey: ["popularCoins"],
    queryFn: () => getPopularCoins().then((r) => r.data),
  });

  const { data: fiatList } = useQuery({
    queryKey: ["fiatList"],
    queryFn: () => getFiatList().then((r) => r.data),
  });

  const allOptions = [
    ...(popularCoins || []).map((c) => ({
      id: c.id,
      label: `${c.symbol} — ${c.name}`,
      type: "crypto",
    })),
    ...(fiatList || []).map((f) => ({
      id: f.id,
      label: f.name,
      type: "fiat",
    })),
  ];

  const handleConvert = async () => {
    if (!amount || isNaN(amount) || parseFloat(amount) <= 0) {
      setError("Введите корректную сумму");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const { data } = await convertCurrency(fromId, toId, parseFloat(amount));
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Ошибка конвертации");
    } finally {
      setLoading(false);
    }
  };

  // конвертируем автоматически при изменении полей
  useEffect(() => {
    if (amount && parseFloat(amount) > 0) {
      const timer = setTimeout(handleConvert, 500);
      return () => clearTimeout(timer);
    }
  }, [fromId, toId, amount]);

  const swap = () => {
    setFromId(toId);
    setToId(fromId);
    setResult(null);
  };

  const formatResult = (value) => {
    if (!value) return "0";
    if (value >= 1000) return value.toLocaleString("ru-RU", { maximumFractionDigits: 2 });
    if (value >= 1) return value.toFixed(4);
    return value.toFixed(8);
  };

  const getLabel = (id) => allOptions.find((o) => o.id === id)?.label || id;

  return (
    <div className="page">
      <div className="converter-header">
        <h1>Конвертер валют</h1>
        <p className="converter-subtitle">
          Конвертируйте криптовалюты и фиатные валюты по актуальному курсу
        </p>
      </div>

      <div className="converter-card">
        {/* Поле FROM */}
        <div className="converter-field">
          <label className="form-label">Отдаёте</label>
          <div className="converter-input-row">
            <input
              className="input converter-amount"
              type="number"
              min="0"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="1"
            />
            <select
              className="input converter-select"
              value={fromId}
              onChange={(e) => setFromId(e.target.value)}
            >
              <optgroup label="Криптовалюты">
                {popularCoins?.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.symbol} — {c.name}
                  </option>
                ))}
              </optgroup>
              <optgroup label="Фиат">
                {fiatList?.map((f) => (
                  <option key={f.id} value={f.id}>{f.name}</option>
                ))}
              </optgroup>
            </select>
          </div>
        </div>

        {/* Кнопка swap */}
        <div className="converter-swap">
          <button className="swap-btn" onClick={swap} title="Поменять местами">
            ⇅
          </button>
        </div>

        {/* Поле TO */}
        <div className="converter-field">
          <label className="form-label">Получаете</label>
          <div className="converter-input-row">
            <div className="converter-result-box">
              {loading ? (
                <span className="converter-loading">...</span>
              ) : result ? (
                <span className="converter-result-value">
                  {formatResult(result.result)}
                </span>
              ) : (
                <span className="converter-placeholder">0</span>
              )}
            </div>
            <select
              className="input converter-select"
              value={toId}
              onChange={(e) => setToId(e.target.value)}
            >
              <optgroup label="Фиат">
                {fiatList?.map((f) => (
                  <option key={f.id} value={f.id}>{f.name}</option>
                ))}
              </optgroup>
              <optgroup label="Криптовалюты">
                {popularCoins?.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.symbol} — {c.name}
                  </option>
                ))}
              </optgroup>
            </select>
          </div>
        </div>

        {/* Курс обмена */}
        {result && !loading && (
          <div className="converter-rate">
            1 {getLabel(fromId).split(" — ")[0]} ={" "}
            {formatResult(result.rate)}{" "}
            {getLabel(toId).split(" — ")[0]}
          </div>
        )}

        {error && <div className="error-message">{error}</div>}
      </div>

      {/* Быстрые суммы */}
      <div className="converter-quick">
        <span className="form-label">Быстрый выбор:</span>
        {[0.1, 0.5, 1, 5, 10, 100].map((v) => (
          <button
            key={v}
            className={`btn btn-outline quick-btn ${parseFloat(amount) === v ? "active" : ""}`}
            onClick={() => setAmount(String(v))}
          >
            {v}
          </button>
        ))}
      </div>
    </div>
  );
}