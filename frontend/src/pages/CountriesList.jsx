import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { countriesService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

const CountriesList = () => {
  const [countries, setCountries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);

  const fetchCountries = async (pageNum = 1) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await countriesService.getAll(pageNum);
      setCountries(response.data.results || []);
      setHasNext(!!response.data.next);
      setPage(pageNum);
    } catch (err) {
      setError(err.message || 'Erreur lors du chargement des pays');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCountries();
  }, []);

  if (loading) return <LoadingSpinner message="Chargement des pays..." />;
  if (error) return <ErrorMessage message={error} onRetry={() => fetchCountries(page)} />;

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>
          <i className="bi bi-globe"></i> Pays Participants
        </h2>
        <span className="badge bg-primary fs-6">{countries.length} pays</span>
      </div>

      <div className="card">
        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-hover">
              <thead>
                <tr>
                  <th>Rang</th>
                  <th>Pays</th>
                  <th>Code</th>
                  <th className="text-center">
                    <i className="bi bi-trophy-fill text-warning"></i> Or
                  </th>
                  <th className="text-center">
                    <i className="bi bi-trophy-fill text-secondary"></i> Argent
                  </th>
                  <th className="text-center">
                    <i className="bi bi-trophy-fill text-danger"></i> Bronze
                  </th>
                  <th className="text-center">Total</th>
                  <th className="text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                {countries.map((country, index) => (
                  <tr key={country.id}>
                    <td>{(page - 1) * 100 + index + 1}</td>
                    <td>
                      <strong>{country.country_name}</strong>
                    </td>
                    <td>
                      <code>{country.country_3_letter_code}</code>
                    </td>
                    <td className="text-center">{country.total_gold_medals}</td>
                    <td className="text-center">{country.total_silver_medals}</td>
                    <td className="text-center">{country.total_bronze_medals}</td>
                    <td className="text-center">
                      <strong>{country.total_medals}</strong>
                    </td>
                    <td className="text-center">
                      <Link
                        to={`/countries/${country.id}`}
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

          {/* Pagination */}
          <div className="d-flex justify-content-between align-items-center mt-3">
            <button
              className="btn btn-outline-primary"
              onClick={() => fetchCountries(page - 1)}
              disabled={page === 1}
            >
              <i className="bi bi-chevron-left"></i> Précédent
            </button>
            <span className="text-muted">Page {page}</span>
            <button
              className="btn btn-outline-primary"
              onClick={() => fetchCountries(page + 1)}
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

export default CountriesList;
