import { Link, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getAlerts } from "../api/coins";
import useAuthStore from "../store/authStore";

export default function Navbar() {
  const { token, user, logout } = useAuthStore();
  const navigate = useNavigate();

  const { data: alerts } = useQuery({
    queryKey: ["alerts"],
    queryFn: () => getAlerts().then((r) => r.data),
    enabled: !!token,
    refetchInterval: 30000, // опрашиваем каждые 30 секунд
  });

  const triggeredCount = alerts?.filter((a) => !a.is_active).length || 0;

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        CryptoHub
      </Link>
      <div className="navbar-links">
        <Link to="/">Рынок</Link>
        <Link to="/converter">Конвертер</Link>
        {token && <Link to="/favorites">Избранное</Link>}
        {token && (
          <Link to="/alerts" className="navbar-alerts-link">
            Уведомления
            {triggeredCount > 0 && (
              <span className="alerts-badge">{triggeredCount}</span>
            )}
          </Link>
        )}
        {token ? (
          <div className="navbar-user">
            <span>{user?.username}</span>
            <button onClick={handleLogout} className="btn btn-outline">
              Выйти
            </button>
          </div>
        ) : (
          <div className="navbar-auth">
            <Link to="/login" className="btn btn-outline">Войти</Link>
            <Link to="/register" className="btn btn-primary">Регистрация</Link>
          </div>
        )}
      </div>
    </nav>
  );
}