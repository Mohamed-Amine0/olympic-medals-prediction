import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">
          <i className="bi bi-trophy-fill"></i> Olympic Medals Prediction
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <Link className={`nav-link ${isActive('/')}`} to="/">
                <i className="bi bi-house-fill"></i> Accueil
              </Link>
            </li>
            <li className="nav-item">
              <Link className={`nav-link ${isActive('/countries')}`} to="/countries">
                <i className="bi bi-globe"></i> Pays
              </Link>
            </li>
            <li className="nav-item">
              <Link className={`nav-link ${isActive('/games')}`} to="/games">
                <i className="bi bi-calendar-event"></i> Jeux Olympiques
              </Link>
            </li>
            <li className="nav-item">
              <Link className={`nav-link ${isActive('/athletes')}`} to="/athletes">
                <i className="bi bi-people"></i> Athlètes
              </Link>
            </li>
            <li className="nav-item">
              <Link className={`nav-link ${isActive('/predictions')}`} to="/predictions">
                <i className="bi bi-lightbulb"></i> Prédictions
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
