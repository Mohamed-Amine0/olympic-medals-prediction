import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { statsService, countriesService, gamesService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

const Home = () => {
  const [stats, setStats] = useState(null);
  const [topCountries, setTopCountries] = useState([]);
  const [recentGames, setRecentGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const [statsRes, countriesRes, gamesRes] = await Promise.all([
        statsService.getOverview(),
        countriesService.getTop(),
        gamesService.getAll(1),
      ]);

      setStats(statsRes.data);
      setTopCountries(countriesRes.data);
      setRecentGames(gamesRes.data.results?.slice(0, 5) || []);
    } catch (err) {
      setError(err.message || 'Erreur lors du chargement des données');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) return <LoadingSpinner message="Chargement du tableau de bord..." />;
  if (error) return <ErrorMessage message={error} onRetry={fetchData} />;

  return (
    <>
      {/* Hero Section */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="jumbotron bg-primary text-white p-5 rounded">
            <h1 className="display-4">
              <i className="bi bi-trophy-fill"></i> Olympic Medals Prediction
            </h1>
            <p className="lead">
              Système de prédiction des médailles olympiques basé sur l'analyse de données historiques
            </p>
            <hr className="my-4 bg-white opacity-25" />
            <p>
              Explorez les statistiques des jeux olympiques, des pays et des athlètes pour comprendre 
              les tendances et prévoir les futures performances.
            </p>
          </div>
        </div>
      </div>

      {/* Statistics Cards */}
      {stats && (
        <div className="row mb-4">
          <div className="col-md-3 mb-3">
            <div className="card stat-card bg-info text-white h-100">
              <div className="card-body text-center">
                <i className="bi bi-calendar-event fs-1"></i>
                <h3 className="mt-2">{stats.total_games}</h3>
                <p className="mb-0">Jeux Olympiques</p>
              </div>
            </div>
          </div>
          <div className="col-md-3 mb-3">
            <div className="card stat-card bg-success text-white h-100">
              <div className="card-body text-center">
                <i className="bi bi-globe fs-1"></i>
                <h3 className="mt-2">{stats.total_countries}</h3>
                <p className="mb-0">Pays Participants</p>
              </div>
            </div>
          </div>
          <div className="col-md-3 mb-3">
            <div className="card stat-card bg-warning text-white h-100">
              <div className="card-body text-center">
                <i className="bi bi-people fs-1"></i>
                <h3 className="mt-2">{stats.total_athletes}</h3>
                <p className="mb-0">Athlètes</p>
              </div>
            </div>
          </div>
          <div className="col-md-3 mb-3">
            <div className="card stat-card bg-danger text-white h-100">
              <div className="card-body text-center">
                <i className="bi bi-award fs-1"></i>
                <h3 className="mt-2">{stats.total_medals}</h3>
                <p className="mb-0">Médailles</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Top Countries and Recent Games Section */}
      <div className="row mb-4">
        {/* Top Countries */}
        <div className="col-lg-6 mb-3">
          <div className="card h-100">
            <div className="card-header bg-primary text-white">
              <h5 className="mb-0">
                <i className="bi bi-trophy"></i> Top 10 Pays par Médailles
              </h5>
            </div>
            <div className="card-body">
              <div className="table-responsive">
                <table className="table table-hover">
                  <thead>
                    <tr>
                      <th>Rang</th>
                      <th>Pays</th>
                      <th className="text-center">
                        <i className="bi bi-trophy-fill text-warning"></i>
                      </th>
                      <th className="text-center">
                        <i className="bi bi-trophy-fill text-secondary"></i>
                      </th>
                      <th className="text-center">
                        <i className="bi bi-trophy-fill text-danger"></i>
                      </th>
                      <th className="text-center">Total</th>
                    </tr>
                  </thead>
                  <tbody>
                    {topCountries.map((country, index) => (
                      <tr key={country.id}>
                        <td>{index + 1}</td>
                        <td>
                          <Link
                            to={`/countries/${country.id}`}
                            className="text-decoration-none"
                          >
                            {country.country_name}
                          </Link>
                        </td>
                        <td className="text-center">{country.total_gold_medals}</td>
                        <td className="text-center">{country.total_silver_medals}</td>
                        <td className="text-center">{country.total_bronze_medals}</td>
                        <td className="text-center">
                          <strong>{country.total_medals}</strong>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Games */}
        <div className="col-lg-6 mb-3">
          <div className="card h-100">
            <div className="card-header bg-success text-white">
              <h5 className="mb-0">
                <i className="bi bi-calendar-event"></i> Jeux Olympiques Récents
              </h5>
            </div>
            <div className="card-body">
              <div className="list-group">
                {recentGames.map((game) => (
                  <Link
                    key={game.id}
                    to={`/games/${game.id}`}
                    className="list-group-item list-group-item-action"
                  >
                    <div className="d-flex w-100 justify-content-between">
                      <h6 className="mb-1">{game.game_name}</h6>
                      <small className="badge bg-primary">{game.game_year}</small>
                    </div>
                    <p className="mb-1">
                      <i className="bi bi-geo-alt"></i> {game.game_location}
                    </p>
                    <small className="text-muted">
                      <i className="bi bi-calendar3"></i>{' '}
                      {new Date(game.game_start_date).toLocaleDateString('fr-FR')} -{' '}
                      {new Date(game.game_end_date).toLocaleDateString('fr-FR')}
                    </small>
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="row">
        <div className="col-md-4 mb-3">
          <div className="card h-100">
            <div className="card-body text-center">
              <i className="bi bi-graph-up text-primary fs-1"></i>
              <h5 className="card-title mt-3">Analyses Avancées</h5>
              <p className="card-text">
                Explorez les tendances historiques et les performances des pays par discipline.
              </p>
              <Link to="/countries" className="btn btn-outline-primary">
                Explorer
              </Link>
            </div>
          </div>
        </div>
        <div className="col-md-4 mb-3">
          <div className="card h-100">
            <div className="card-body text-center">
              <i className="bi bi-lightbulb text-warning fs-1"></i>
              <h5 className="card-title mt-3">Prédictions Intelligentes</h5>
              <p className="card-text">
                Modèles de machine learning pour prédire les futures performances olympiques.
              </p>
              <Link to="/predictions" className="btn btn-outline-warning">
                Voir Prédictions
              </Link>
            </div>
          </div>
        </div>
        <div className="col-md-4 mb-3">
          <div className="card h-100">
            <div className="card-body text-center">
              <i className="bi bi-people text-success fs-1"></i>
              <h5 className="card-title mt-3">Profils d'Athlètes</h5>
              <p className="card-text">
                Découvrez les parcours des athlètes olympiques et leurs performances.
              </p>
              <Link to="/athletes" className="btn btn-outline-success">
                Découvrir
              </Link>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;
