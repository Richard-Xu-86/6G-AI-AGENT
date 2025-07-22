import { NavLink } from 'react-router-dom'; //NavLink component from the react-router-dom package.

export default function Navbar() {
  return (
    <header className="navbar-header">
      <NavLink to="/" className="navbar-title"> 
        <h1>OPTIFI.AI</h1>
      </NavLink>
      <nav className="navbar-links"> 
        <NavLink to="/" className={({ isActive }) => isActive ? "nav-link-active" : "nav-link"}>
          Home
        </NavLink>
        <NavLink to="/run" className={({ isActive }) => isActive ? "nav-link-active" : "nav-link"}>
          Run
        </NavLink>
        <NavLink to="/graphs" className={({ isActive }) => isActive ? "nav-link-active" : "nav-link"}>
          Graphs
        </NavLink>
        <NavLink to="/history" className={({ isActive }) => isActive ? "nav-link-active" : "nav-link"}>
          History
        </NavLink>
      </nav>
    </header>
  );
}
