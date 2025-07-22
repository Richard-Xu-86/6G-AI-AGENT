import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import ScrollToTop from './components/ScrollToTop';
import HomePage from './pages/HomePage';
import RunAI from './pages/RunAI';
import GraphsPage from './pages/GraphsPage';
import HistoryPage from './pages/HistoryPage';

export default function App() {
  return (
    <Router>
      <ScrollToTop />
      <div className="app-screen">
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/run" element={<RunAI />} />
          <Route path="/graphs" element={<GraphsPage />} />
          <Route path="/history" element={<HistoryPage />} />
        </Routes>
      </div>
    </Router>
  );
}

