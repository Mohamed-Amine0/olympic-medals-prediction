const ErrorMessage = ({ message = 'Une erreur est survenue', onRetry }) => {
  return (
    <div className="alert alert-danger d-flex align-items-center" role="alert">
      <i className="bi bi-exclamation-triangle-fill me-2"></i>
      <div className="flex-grow-1">{message}</div>
      {onRetry && (
        <button className="btn btn-sm btn-outline-danger ms-3" onClick={onRetry}>
          <i className="bi bi-arrow-clockwise"></i> Réessayer
        </button>
      )}
    </div>
  );
};

export default ErrorMessage;
