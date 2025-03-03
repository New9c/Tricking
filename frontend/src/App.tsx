// frontend/src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import CreateAccountPage from './components/CreateAccountPage';
import MemberPage from './components/MemberPage';
import Tricktionary from './components/Tricktionary';
import TrickManager from './components/TrickManager';
import MainPage from './components/MainPage';
import UserManager from './components/UserManager';
import Loading from './components/Loading';
import ErrorPage from './components/Error';
import EditMemberPage from './components/EditMemberPage';
import GoogleLoginBtn from './components/Google';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/create-account" element={<CreateAccountPage />} />
        <Route path="/member" element={<MemberPage />} />
        <Route path="/member/edit" element={<EditMemberPage />} />
        <Route path="/user_manager" element={<UserManager />} />
        <Route path="/tricktionary" element={<Tricktionary />} />
        <Route path="/trick_manager" element={<TrickManager />} />
        <Route path="/loading" element={<Loading />} />
        <Route path="/error" element={<ErrorPage />} />
        <Route path="/google" element={<GoogleLoginBtn />} />
      </Routes>
    </Router>
  );
}

export default App;
