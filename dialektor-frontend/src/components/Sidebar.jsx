import { NavLink } from 'react-router-dom';
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
          <li>
            <NavLink to="/" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
              <span className="nav-icon">🏠</span>
              <span className="nav-text">Home</span>
            </NavLink>
          </li>
          <li>
            <NavLink to="/dictionary" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
              <span className="nav-icon">📖</span>
              <span className="nav-text">Dictionary</span>
            </NavLink>
          </li>
          <li>
            <NavLink to="/dialects" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
              <span className="nav-icon">🗺️</span>
              <span className="nav-text">Dialects</span>
            </NavLink>
          </li>
        </ul>
      </nav>
    </aside>
  );
}

export default Sidebar;
