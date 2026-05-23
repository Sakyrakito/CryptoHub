import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { getFavorites, removeFavorite } from "../api/coins";

export default function Favorites() {
  const queryClient = useQueryClient();

  const { data: favorites, isLoading } = useQuery({
    queryKey: ["favorites"],
    queryFn: () => getFavorites().then((r) => r.data),
  });

  const removeMutation = useMutation({
    mutationFn: removeFavorite,
    onSuccess: () => queryClient.invalidateQueries(["favorites"]),
  });

  if (isLoading) return <div className="loading">Загрузка...</div>;

  return (
    <div className="page">
      <h1>Избранные монеты</h1>
      {favorites?.length === 0 && (
        <p className="empty-state">
          Нет избранных монет. <Link to="/">Добавить с рынка</Link>
        </p>
      )}
      <div className="favorites-list">
        {favorites?.map((fav) => (
          <div key={fav.id} className="favorite-item">
            <Link to={`/coin/${fav.coin_id}`} className="favorite-link">
              <span className="favorite-symbol">{fav.coin_symbol}</span>
              <span className="favorite-name">{fav.coin_name}</span>
            </Link>
            <button
              className="btn btn-danger"
              onClick={() => removeMutation.mutate(fav.coin_id)}
            >
              Удалить
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}