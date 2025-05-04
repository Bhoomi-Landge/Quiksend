import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './CsvFile.css'; // Import the CSS file for styling


const CsvFile = () => {
  const [selectedOption, setSelectedOption] = useState('');
  const navigate = useNavigate();

  const handleOptionChange = (e) => {
    setSelectedOption(e.target.value);
    if (e.target.value === 'manual') {
      navigate('/manual');
    }
  };

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

      <div className="csv-file-content">
        <h1 className="header">Add Contacts via CSV</h1>
        <form method="POST" action="/csv_file" encType="multipart/form-data">
          <p>
            Add contact:
            <select id="contactOption" className="options" onChange={handleOptionChange} value={selectedOption}>
              <option value="">Select Option:</option>
              <option value="csv">CSV file</option>
              <option value="manual">Manually</option>
            </select>
          </p>
          <div className="filename">
            <input type="file" name="file" />
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

export default CsvFile;
