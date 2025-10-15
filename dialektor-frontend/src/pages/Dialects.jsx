import './Dialects.css';

function Dialects() {
  return (
    <div className="page-container">
      <h1>Dialects</h1>
      <p className="page-description">
        Learn about different Albanian dialects and their unique characteristics
      </p>
      <div className="dialects-grid">
        <div className="dialect-card">
          <div className="dialect-icon">🗣️</div>
          <h3>Gheg</h3>
          <p>The northern Albanian dialect spoken in Albania, Kosovo, and Montenegro</p>
        </div>
        <div className="dialect-card">
          <div className="dialect-icon">💬</div>
          <h3>Tosk</h3>
          <p>The southern Albanian dialect, which forms the basis of standard Albanian</p>
        </div>
        <div className="dialect-card">
          <div className="dialect-icon">🌍</div>
          <h3>Regional Variations</h3>
          <p>Explore local variations and unique linguistic features across regions</p>
        </div>
      </div>
    </div>
  );
}

export default Dialects;
