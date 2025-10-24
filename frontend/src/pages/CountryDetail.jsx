import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { countriesService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

const CountryDetail = () => {
  const { id } = useParams();
  const [country, setCountry] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchCountryDetail = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await countriesService.getById(id);
      setCountry(response.data);
    } catch (err) {
      setError(err.message || 'Erreur lors du chargement du pays');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCountryDetail();
  }, [id]);

  if (loading) return <LoadingSpinner message="Chargement des détails du pays..." />;
  if (error) return <ErrorMessage message={error} onRetry={fetchCountryDetail} />;
  if (!country) return <ErrorMessage message="Pays non trouvé" />;

  return (
    <>
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>
          <i className="bi bi-globe"></i> {country.country_name}
        </h2>
        <Link to="/countries" className="btn btn-outline-secondary">
          <i className="bi bi-arrow-left"></i> Retour
        </Link>
      </div>

      {/* Country Info Card */}
      <div className="card mb-4">
        <div className="card-header bg-primary text-white">
          <h5 className="mb-0">Informations du Pays</h5>
        </div>
        <div className="card-body">
          <div className="row">
            <div className="col-md-6">
              <p>
                <strong>Nom:</strong> {country.country_name}
              </p>
              <p>
                <strong>Code:</strong> <code>{country.country_code}</code>
              </p>
              <p>
                <strong>Code 3 lettres:</strong> <code>{country.country_3_letter_code}</code>
              </p>
            </div>
            <div className="col-md-6">
              <div className="row">
                <div className="col-6 text-center">
                  <div className="card bg-warning text-white mb-2">
                    <div className="card-body py-2">
                      <i className="bi bi-trophy-fill"></i> Or
                      <h4 className="mb-0">{country.total_gold_medals}</h4>
                    </div>
                  </div>
                </div>
                <div className="col-6 text-center">
                  <div className="card bg-secondary text-white mb-2">
                    <div className="card-body py-2">
                      <i className="bi bi-trophy-fill"></i> Argent
                      <h4 className="mb-0">{country.total_silver_medals}</h4>
                    </div>
                  </div>
                </div>
                <div className="col-6 text-center">
                  <div className="card bg-danger text-white">
                    <div className="card-body py-2">
                      <i className="bi bi-trophy-fill"></i> Bronze
                      <h4 className="mb-0">{country.total_bronze_medals}</h4>
                    </div>
                  </div>
                </div>
                <div className="col-6 text-center">
                  <div className="card bg-success text-white">
                    <div className="card-body py-2">
                      <i className="bi bi-award"></i> Total
                      <h4 className="mb-0">{country.total_medals}</h4>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Medals by Discipline */}
      {country.medals_by_discipline && country.medals_by_discipline.length > 0 && (
        <div className="card mb-4">
          <div className="card-header bg-info text-white">
            <h5 className="mb-0">
              <i className="bi bi-bar-chart"></i> Top 10 Disciplines
            </h5>
          </div>
          <div className="card-body">
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>Discipline</th>
                    <th className="text-center">Nombre de Médailles</th>
                  </tr>
                </thead>
                <tbody>
                  {country.medals_by_discipline.map((discipline, index) => (
                    <tr key={index}>
                      <td>{discipline.discipline_title}</td>
                      <td className="text-center">
                        <span className="badge bg-primary">{discipline.count}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Recent Medals */}
      {country.medals && country.medals.length > 0 && (
        <div className="card">
          <div className="card-header bg-success text-white">
            <h5 className="mb-0">
              <i className="bi bi-trophy"></i> Médailles Récentes (Limité à 50)
            </h5>
          </div>
          <div className="card-body">
            <div className="table-responsive">
              <table className="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>Jeu</th>
                    <th>Discipline</th>
                    <th>Épreuve</th>
                    <th>Athlète</th>
                    <th className="text-center">Médaille</th>
                  </tr>
                </thead>
                <tbody>
                  {country.medals.map((medal) => (
                    <tr key={medal.id}>
                      <td>
                        <small>{medal.game_name || medal.slug_game}</small>
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

export default CountryDetail;
