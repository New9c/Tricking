import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/login.scss';
import '../styles/global.scss';
import Topbar from './Topbar';

const LoginPage: React.FC = () => {
  const [account, setAccount] = useState('');
  const [password, setPassword] = useState('');
  const [responseMessage, setResponseMessage] = useState<{ text: string; color: string }>({
    text: "",
    color: "white",
  });
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleLogin();
    }
  };

  const handleLogin = async () => {
    // TODO: 在這裡呼叫後端 API 進行登入驗證
    // 假設後端 API 端點是 /api/v1/login，使用 POST 方法
    setResponseMessage({ text: "Processing...", color: "white" });
    try {
      const response = await fetch("http://localhost:8000/api/v1/login", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ username: account, password }),
      });

      if (response.ok) {
        // 登入成功，跳轉到會員頁面
        const data = await response.json();
        localStorage.setItem('access_token', data.access_token);
        window.location.href = '/member';
      } else {
        // 登入失敗，顯示錯誤訊息
        const errorData = await response.json();
        setResponseMessage({ text: errorData.detail || "An unexpected error occurred.", color: "red" });
      }
    } catch (error) {
      setResponseMessage({ text: "Failed to connect to the server.", color: "red" });
    }
  };

  return (
    <>
      <Topbar />
      <div className="center-container">
        <div className="login-box">
          <div className="welcome-title">Welcome to NCKU Tricking</div>
          <input
            type="text"
            className="account-input"
            placeholder="Username, phone or email"
            value={account}
            onChange={(e) => setAccount(e.target.value)}
          />
          <input
            type="password"
            className="account-input"
            placeholder="Password"
            value={password}
            onKeyDown={handleKeyDown}
            onChange={(e) => setPassword(e.target.value)}
          />
          {responseMessage.text && (
            <p style={{ color: responseMessage.color }}>
              {responseMessage.text}
            </p>
          )}
          <div className="button-container">
            <button className="login-btn" onClick={handleLogin}>
              登入
            </button>
            <Link to="/create-account">
              <button className="create-account-btn">加入會員</button>
            </Link>
          </div>
        </div>
      </div>
    </>
  );
};

export default LoginPage;
