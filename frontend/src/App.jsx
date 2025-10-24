import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import CountriesList from './pages/CountriesList';
import CountryDetail from './pages/CountryDetail';
import GamesList from './pages/GamesList';
import GameDetail from './pages/GameDetail';
import AthletesList from './pages/AthletesList';
import PredictionsList from './pages/PredictionsList';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="countries" element={<CountriesList />} />
          <Route path="countries/:id" element={<CountryDetail />} />
          <Route path="games" element={<GamesList />} />
          <Route path="games/:id" element={<GameDetail />} />
          <Route path="athletes" element={<AthletesList />} />
          <Route path="predictions" element={<PredictionsList />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
