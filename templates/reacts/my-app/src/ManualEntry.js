import React from 'react';
import { useNavigate } from 'react-router-dom';
import './ManualEntry.css'; // Import the CSS file for styling

const ManualEntry = () => {
  const navigate = useNavigate();

  return (
    <div className="container">
      <aside className="sidebar">
        <div className="sidebar-header">QuikSend</div>
        <div className="sidebar-content">
          <button className="menu-button" onClick={() => navigate('/dashboard')}>Dashboard</button>
          <button className="menu-button">Campaigns</button>
          <button className="menu-button">Audience</button>
          <button className="menu-button">Analytics</button>
        </div>
      </aside>

      <div className="manual-entry-content">
        <h1 className="header">Add Contacts Manually</h1>
        <form method="POST" action="/manual">
          <div className="form-box">
            <label htmlFor="name">Name:</label>
            <input type="text" id="name" className="text" name="name" />
            <br />
            <label htmlFor="email">Email:</label>
            <input type="email" id="email" className="email" name="email" />
            <br />
            <br />
          </div>
          <div className="buttons-container">
            <button className="import">Save</button>
            <button className="import cancel">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ManualEntry;
