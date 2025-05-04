import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
  const [activeMenu, setActiveMenu] = useState(null);
  const [selectedOption, setSelectedOption] = useState(''); // For select option
  const navigate = useNavigate();

  const handleButton = (menu) => {
    setActiveMenu(activeMenu === menu ? null : menu); // Toggle menu
  };

  const handleSubmit = (path) => {
    navigate(path); // Navigate to the given path
  };

  const handleOptionChange = (e) => {
    setSelectedOption(e.target.value);
    if (e.target.value === 'csv') {
      navigate('/csv_file');
    } else if (e.target.value === 'manual') {
      navigate('/manual');
    }
  };

  return (
    <div className="container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">QuikSend</div>
        <div className="sidebar-content">
          <button onClick={() => handleButton('Campaigns')} className="menu-button">
            Campaigns
          </button>
          {activeMenu === 'Campaigns' && (
            <ul className="submenu">
              <li><Link to="/select_template">Create template</Link></li>
              <li><Link to="/scheduling">Schedule</Link></li>
              <li><Link to="/saved_template">Saved Template</Link></li>
              <li><Link to="/campaign_list">List Of Campaign</Link></li>
            </ul>
          )}

          <button onClick={() => handleButton('Audience')} className="menu-button">
            Audience
          </button>
          {activeMenu === 'Audience' && (
            <ul className="submenu">
              <li><Link to="/contact_option">Add Contacts</Link></li>
              <li><Link to="/list">All Contacts</Link></li>
            </ul>
          )}

          <button onClick={() => handleSubmit('/analytics')} className="menu-button">
            Analytics
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="dashboard-content">
        <h1 className="header">Dashboard</h1>
        <div className="top-header">
          <input className="search-bar" type="text" placeholder="Search for..." />
          <button className="profile-button">
            <img
              src="https://static.vecteezy.com/system/resources/previews/026/730/189/original/user-button-icon-avatar-and-account-button-vector.jpg"
              alt="profile"
            />
          </button>
        </div>

        <div className="content-area">
          <h1>Audience</h1>
          <form method="POST" action="/contact_option">
            <p>Add contact:
              <select id="contactOption" className="options" onChange={handleOptionChange} value={selectedOption}>
                <option value="">Select Option:</option>
                <option value="csv">CSV file</option>
                <option value="manual">Manually</option>
              </select>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
