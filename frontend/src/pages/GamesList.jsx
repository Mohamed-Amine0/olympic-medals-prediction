import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { gamesService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

const GamesList = () => {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);

  const fetchGames = async (pageNum = 1) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await gamesService.getAll(pageNum);
      setGames(response.data.results || []);
      setHasNext(!!response.data.next);
      setPage(pageNum);
    } catch (err) {
      setError(err.message || 'Erreur lors du chargement des jeux olympiques');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGames();
  }, []);

  if (loading) return <LoadingSpinner message="Chargement des jeux olympiques..." />;
  if (error) return <ErrorMessage message={error} onRetry={() => fetchGames(page)} />;

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>
          <i className="bi bi-calendar-event"></i> Jeux Olympiques
        </h2>
        <span className="badge bg-primary fs-6">{games.length} jeux</span>
      </div>

      <div className="row">
        {games.map((game) => (
          <div key={game.id} className="col-md-6 col-lg-4 mb-4">
            <div className="card h-100 shadow-sm">
              <div className={`card-header text-white ${
                game.game_season === 'Summer' ? 'bg-warning' : 'bg-info'
              }`}>
                <div className="d-flex justify-content-between align-items-center">
                  <h5 className="mb-0">{game.game_year}</h5>
                  <span className="badge bg-light text-dark">
                    {game.game_season === 'Summer' ? (
                      <>
                        <i className="bi bi-sun"></i> Été
                      </>
                    ) : (
                      <>
                        <i className="bi bi-snow"></i> Hiver
                      </>
                    )}
                  </span>
                </div>
              </div>
              <div className="card-body">
                <h6 className="card-title">{game.game_name}</h6>
                <p className="card-text">
                  <i className="bi bi-geo-alt text-danger"></i>{' '}
                  <strong>{game.game_location}</strong>
                </p>
                <p className="card-text text-muted">
                  <small>
                    <i className="bi bi-calendar3"></i>{' '}
                    {new Date(game.game_start_date).toLocaleDateString('fr-FR')} -{' '}
                    {new Date(game.game_end_date).toLocaleDateString('fr-FR')}
                  </small>
                </p>
              </div>
              <div className="card-footer bg-transparent">
                <Link
                  to={`/games/${game.id}`}
                  className="btn btn-outline-primary btn-sm w-100"
                >
                  <i className="bi bi-eye"></i> Voir les détails
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Pagination */}
      <div className="d-flex justify-content-between align-items-center mt-3">
        <button
          className="btn btn-outline-primary"
          onClick={() => fetchGames(page - 1)}
          disabled={page === 1}
        >
          <i className="bi bi-chevron-left"></i> Précédent
        </button>
        <span className="text-muted">Page {page}</span>
        <button
          className="btn btn-outline-primary"
          onClick={() => fetchGames(page + 1)}
          disabled={!hasNext}
        >
          Suivant <i className="bi bi-chevron-right"></i>
        </button>
      </div>
    </>
  );
};

export default GamesList;
