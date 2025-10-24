import { useState, useEffect } from 'react';
import { athletesService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

const AthletesList = () => {
  const [athletes, setAthletes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);

  const fetchAthletes = async (pageNum = 1) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await athletesService.getAll(pageNum);
      setAthletes(response.data.results || []);
      setHasNext(!!response.data.next);
      setPage(pageNum);
    } catch (err) {
      setError(err.message || 'Erreur lors du chargement des athlètes');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAthletes();
  }, []);

  if (loading) return <LoadingSpinner message="Chargement des athlètes..." />;
  if (error) return <ErrorMessage message={error} onRetry={() => fetchAthletes(page)} />;

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>
          <i className="bi bi-people"></i> Athlètes Olympiques
        </h2>
        <span className="badge bg-primary fs-6">{athletes.length} athlètes</span>
      </div>

      <div className="card">
        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-hover">
              <thead>
                <tr>
                  <th>Nom</th>
                  <th className="text-center">Année de Naissance</th>
                  <th className="text-center">Participations</th>
                  <th>Premier Jeu</th>
                </tr>
              </thead>
              <tbody>
                {athletes.map((athlete) => (
                  <tr key={athlete.id}>
                    <td>
                      <strong>{athlete.athlete_full_name}</strong>
                    </td>
                    <td className="text-center">
                      {athlete.athlete_year_birth || 'N/A'}
                    </td>
                    <td className="text-center">
                      <span className="badge bg-info">
                        {athlete.games_participations}
                      </span>
                    </td>
                    <td>
                      <small>{athlete.first_game || 'N/A'}</small>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="d-flex justify-content-between align-items-center mt-3">
            <button
              className="btn btn-outline-primary"
              onClick={() => fetchAthletes(page - 1)}
              disabled={page === 1}
            >
              <i className="bi bi-chevron-left"></i> Précédent
            </button>
            <span className="text-muted">Page {page}</span>
            <button
              className="btn btn-outline-primary"
              onClick={() => fetchAthletes(page + 1)}
              disabled={!hasNext}
            >
              Suivant <i className="bi bi-chevron-right"></i>
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default AthletesList;
