import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { predictionsService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

const PredictionsList = () => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);

  const fetchPredictions = async (pageNum = 1) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await predictionsService.getAll(pageNum);
      setPredictions(response.data.results || []);
      setHasNext(!!response.data.next);
      setPage(pageNum);
    } catch (err) {
      setError(err.message || 'Erreur lors du chargement des prédictions');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPredictions();
  }, []);

  if (loading) return <LoadingSpinner message="Chargement des prédictions..." />;
  if (error) return <ErrorMessage message={error} onRetry={() => fetchPredictions(page)} />;

  return (
    <>
      <div className="mb-4">
        <h2>
          <i className="bi bi-lightbulb"></i> Prédictions des Médailles
        </h2>
        <p className="text-muted">
          Prédictions basées sur l'analyse des données historiques et des modèles de machine learning.
        </p>
      </div>

      {predictions.length === 0 ? (
        <div className="alert alert-info">
          <i className="bi bi-info-circle"></i> Aucune prédiction disponible pour le moment.
          Les prédictions seront générées prochainement.
        </div>
      ) : (
        <>
          <div className="row">
            {predictions.map((prediction) => (
              <div key={prediction.id} className="col-md-6 col-lg-4 mb-4">
                <div className="card h-100 shadow-sm">
                  <div className="card-header bg-primary text-white">
                    <h5 className="mb-0">{prediction.country_name}</h5>
                    <small>{prediction.predicted_game}</small>
                  </div>
                  <div className="card-body">
                    <div className="row text-center mb-3">
                      <div className="col-4">
                        <div className="p-2 bg-warning text-white rounded">
                          <i className="bi bi-trophy-fill"></i>
                          <h4 className="mb-0">{prediction.predicted_gold}</h4>
                          <small>Or</small>
                        </div>
                      </div>
                      <div className="col-4">
                        <div className="p-2 bg-secondary text-white rounded">
                          <i className="bi bi-trophy-fill"></i>
                          <h4 className="mb-0">{prediction.predicted_silver}</h4>
                          <small>Argent</small>
                        </div>
                      </div>
                      <div className="col-4">
                        <div className="p-2 bg-danger text-white rounded">
                          <i className="bi bi-trophy-fill"></i>
                          <h4 className="mb-0">{prediction.predicted_bronze}</h4>
                          <small>Bronze</small>
                        </div>
                      </div>
                    </div>
                    <div className="text-center">
                      <h5>
                        Total: <span className="badge bg-success fs-5">
                          {prediction.predicted_total}
                        </span>
                      </h5>
                      <small className="text-muted">
                        Confiance: {(prediction.confidence_score * 100).toFixed(1)}%
                      </small>
                    </div>
                  </div>
                  <div className="card-footer bg-transparent">
                    <Link
                      to={`/countries/${prediction.country}`}
                      className="btn btn-outline-primary btn-sm w-100"
                    >
                      <i className="bi bi-eye"></i> Voir le pays
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
              onClick={() => fetchPredictions(page - 1)}
              disabled={page === 1}
            >
              <i className="bi bi-chevron-left"></i> Précédent
            </button>
            <span className="text-muted">Page {page}</span>
            <button
              className="btn btn-outline-primary"
              onClick={() => fetchPredictions(page + 1)}
              disabled={!hasNext}
            >
              Suivant <i className="bi bi-chevron-right"></i>
            </button>
          </div>
        </>
      )}
    </>
  );
};

export default PredictionsList;
