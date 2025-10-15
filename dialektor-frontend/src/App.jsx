import Layout from './components/Layout';
import './App.css';

function App() {
  return (
    <Layout>
      <div className="welcome-container">
        <h1>Welcome to Dialektor</h1>
        <p className="subtitle">
          Discover how words are said and spelled across different dialects of the Albanian language
        </p>
        <div className="info-cards">
          <div className="info-card">
            <div className="card-icon">📖</div>
            <h3>Dictionary</h3>
            <p>Explore words and their meanings across various Albanian dialects</p>
          </div>
          <div className="info-card">
            <div className="card-icon">🗺️</div>
            <h3>Dialects</h3>
            <p>Learn about different Albanian dialects and their unique characteristics</p>
          </div>
          <div className="info-card">
            <div className="card-icon">🔍</div>
            <h3>Search</h3>
            <p>Find and compare words between different dialects</p>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default App;

