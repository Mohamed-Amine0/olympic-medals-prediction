const LoadingSpinner = ({ message = 'Chargement...' }) => {
  return (
    <div className="d-flex justify-content-center align-items-center py-5">
      <div className="text-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="mt-3 text-muted">{message}</p>
      </div>
    </div>
  );
};

export default LoadingSpinner;
