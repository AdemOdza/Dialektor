import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Dictionary from './pages/Dictionary';
import Dialects from './pages/Dialects';
import './App.css';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dictionary" element={<Dictionary />} />
          <Route path="/dialects" element={<Dialects />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;

