// frontend/src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import CreateAccountPage from './components/CreateAccountPage';
import MemberPage from './components/MemberPage';
import Tricktionary from './components/Tricktionary';
import TrickManager from './components/TrickManager';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/create-account" element={<CreateAccountPage />} />
        <Route path="/member" element={<MemberPage />} />
        <Route path="/tricktionary" element={<Tricktionary />} />
        <Route path="/" element={<Tricktionary />} />
        <Route path="/trick_manager" element={<TrickManager />} />
      </Routes>
    </Router>
  );
}

export default App;
