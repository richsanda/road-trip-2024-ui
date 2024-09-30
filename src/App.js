import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Root from './Root';
import Timeline from './components/Timeline';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Root />} />
        <Route path="/categories" element={<div>hi</div>} />
        <Route path="/timeline" element={<Timeline/>} />
      </Routes>
    </Router>
  );
}

export default App;
