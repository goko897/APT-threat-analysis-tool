import React from 'react';
import './NavBar.css'; // Separate CSS file for the navigation bar styling

const Navbar = ({ timeSpent }) => {
  return (
    <nav className="navbar">
      <ul className="nav-links">
        <li><a href="#home">Home</a></li>
        <li><a href="#upload">Upload File</a></li>
        <li><a href="#about">About</a></li>
      </ul>
      <div className="time-spent">
        Time spent: {timeSpent}
      </div>
    </nav>
  );
};

export default Navbar;
