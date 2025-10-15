import './Dictionary.css';

function Dictionary() {
  return (
    <div className="page-container">
      <h1>Dictionary</h1>
      <p className="page-description">
        Explore words and their meanings across various Albanian dialects
      </p>
      <div className="content-card">
        <div className="search-section">
          <input 
            type="text" 
            placeholder="Search for a word..." 
            className="search-input"
          />
          <button className="search-button">Search</button>
        </div>
        <div className="placeholder-text">
          <p>🔍 Search for Albanian words to see their meanings and usage across different dialects</p>
        </div>
      </div>
    </div>
  );
}

export default Dictionary;
