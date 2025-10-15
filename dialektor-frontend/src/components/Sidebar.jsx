import './Sidebar.css';

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo-container">
          <div className="logo">D</div>
        </div>
        <h1 className="app-title">Dialektor</h1>
      </div>
      <nav className="sidebar-nav">
        <ul>
          <li className="nav-item active">
            <span className="nav-icon">🏠</span>
            <span className="nav-text">Home</span>
          </li>
          <li className="nav-item">
            <span className="nav-icon">📖</span>
            <span className="nav-text">Dictionary</span>
          </li>
          <li className="nav-item">
            <span className="nav-icon">🗺️</span>
            <span className="nav-text">Dialects</span>
          </li>
        </ul>
      </nav>
    </aside>
  );
}

export default Sidebar;
