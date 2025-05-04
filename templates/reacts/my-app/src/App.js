import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CsvFile from './CsvFile';
import ManualEntry from './ManualEntry';
import Dashboard from './Dashboard';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/csv_file" element={<CsvFile />} />
        <Route path="/manual" element={<ManualEntry />} />
        <Route path="/dashboard" element={<Dashboard />} />
        {/* Add other routes as needed */}
      </Routes>
    </Router>
  );
}

export default App;
