import { Link, useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore";

export default function Navbar() {
  const { token, user, logout } = useAuthStore();
  const navigate = useNavigate();

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
        {token && <Link to="/favorites">Избранное</Link>}
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