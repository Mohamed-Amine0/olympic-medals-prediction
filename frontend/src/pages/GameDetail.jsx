import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { gamesService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

const GameDetail = () => {
  const { id } = useParams();
  const [game, setGame] = useState(null);
  const [topCountries, setTopCountries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchGameDetail = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const [gameRes, topCountriesRes] = await Promise.all([
        gamesService.getById(id),
        gamesService.getTopCountries(id),
      ]);
      
      setGame(gameRes.data);
      setTopCountries(topCountriesRes.data);
    } catch (err) {
      setError(err.message || 'Erreur lors du chargement du jeu olympique');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGameDetail();
  }, [id]);

  if (loading) return <LoadingSpinner message="Chargement des détails du jeu..." />;
  if (error) return <ErrorMessage message={error} onRetry={fetchGameDetail} />;
  if (!game) return <ErrorMessage message="Jeu olympique non trouvé" />;

  return (
    <>
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>
          <i className="bi bi-calendar-event"></i> {game.game_name}
        </h2>
        <Link to="/games" className="btn btn-outline-secondary">
          <i className="bi bi-arrow-left"></i> Retour
        </Link>
      </div>

      {/* Game Info Card */}
      <div className="card mb-4">
        <div className={`card-header text-white ${
          game.game_season === 'Summer' ? 'bg-warning' : 'bg-info'
        }`}>
          <h5 className="mb-0">Informations du Jeu Olympique</h5>
        </div>
        <div className="card-body">
          <div className="row">
            <div className="col-md-6">
              <p>
                <strong>Année:</strong> {game.game_year}
              </p>
              <p>
                <strong>Lieu:</strong> <i className="bi bi-geo-alt text-danger"></i>{' '}
                {game.game_location}
              </p>
              <p>
                <strong>Saison:</strong>{' '}
                {game.game_season === 'Summer' ? (
                  <span className="badge bg-warning text-dark">
                    <i className="bi bi-sun"></i> Été
                  </span>
                ) : (
                  <span className="badge bg-info">
                    <i className="bi bi-snow"></i> Hiver
                  </span>
                )}
              </p>
            </div>
            <div className="col-md-6">
              <p>
                <strong>Date de début:</strong>{' '}
                {new Date(game.game_start_date).toLocaleDateString('fr-FR', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}
              </p>
              <p>
                <strong>Date de fin:</strong>{' '}
                {new Date(game.game_end_date).toLocaleDateString('fr-FR', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}
              </p>
              <p>
                <strong>Slug:</strong> <code>{game.game_slug}</code>
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Top Countries */}
      {topCountries && topCountries.length > 0 && (
        <div className="card mb-4">
          <div className="card-header bg-primary text-white">
            <h5 className="mb-0">
              <i className="bi bi-trophy"></i> Top 10 Pays - Classement
            </h5>
          </div>
          <div className="card-body">
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>Rang</th>
                    <th>Pays</th>
                    <th className="text-center">Nombre de Médailles</th>
                    <th className="text-center">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {topCountries.map((country, index) => (
                    <tr key={country.country__id}>
                      <td>
                        {index === 0 && <i className="bi bi-trophy-fill text-warning fs-5"></i>}
                        {index === 1 && <i className="bi bi-trophy-fill text-secondary fs-5"></i>}
                        {index === 2 && <i className="bi bi-trophy-fill text-danger fs-5"></i>}
                        {index > 2 && <span>{index + 1}</span>}
                      </td>
                      <td>
                        <strong>{country.country__country_name}</strong>
                      </td>
                      <td className="text-center">
                        <span className="badge bg-primary fs-6">
                          {country.medal_count}
                        </span>
                      </td>
                      <td className="text-center">
                        <Link
                          to={`/countries/${country.country__id}`}
                          className="btn btn-sm btn-outline-primary"
                        >
                          <i className="bi bi-eye"></i> Voir
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Medals */}
      {game.medals && game.medals.length > 0 && (
        <div className="card">
          <div className="card-header bg-success text-white">
            <h5 className="mb-0">
              <i className="bi bi-award"></i> Médailles (Limité à 50)
            </h5>
          </div>
          <div className="card-body">
            <div className="table-responsive">
              <table className="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>Pays</th>
                    <th>Discipline</th>
                    <th>Épreuve</th>
                    <th>Athlète</th>
                    <th className="text-center">Médaille</th>
                  </tr>
                </thead>
                <tbody>
                  {game.medals.slice(0, 50).map((medal) => (
                    <tr key={medal.id}>
                      <td>
                        <Link
                          to={`/countries/${medal.country}`}
                          className="text-decoration-none"
                        >
                          {medal.country_name}
                        </Link>
                      </td>
                      <td>{medal.discipline_title}</td>
                      <td>
                        <small>{medal.event_title}</small>
                      </td>
                      <td>
                        <small>{medal.athlete_name || medal.participant_title}</small>
                      </td>
                      <td className="text-center">
                        {medal.medal_type === 'GOLD' && (
                          <span className="badge bg-warning text-dark">Or</span>
                        )}
                        {medal.medal_type === 'SILVER' && (
                          <span className="badge bg-secondary">Argent</span>
                        )}
                        {medal.medal_type === 'BRONZE' && (
                          <span className="badge bg-danger">Bronze</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default GameDetail;
