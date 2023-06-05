import logo from './logo.svg';
import './App.css';
import List from './apps/list'
import React from 'react';

import { BrowserRouter as Router, Routes, Route}
    from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<List/>}/>
      </Routes>
    </Router>
  );
}

export default App;
