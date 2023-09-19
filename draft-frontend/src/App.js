import logo from './logo.svg';
import './App.css';
import PokemonList from './apps/list'
import React from 'react';

import { BrowserRouter as Router, Routes, Route}
    from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<PokemonList/>}/>
      </Routes>
    </Router>
  );
}

export default App;
