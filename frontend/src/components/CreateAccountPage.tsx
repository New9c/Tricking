// frontend/src/components/CreateAccountPage.tsx
import '../styles/global.scss';
import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/create-account.scss';
import Topbar from './Topbar';
import { jwtDecode } from 'jwt-decode';

const CreateAccountPage: React.FC = () => {
  const navigate = useNavigate();


  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [gender, setGender] = useState('');
  const [age, setAge] = useState('');
  const [password, setPassword] = useState('');
  const [responseMessage, setResponseMessage] = useState<{ text: string; color: string }>({
    text: "",
    color: "white",
  });

  const jwt = localStorage.getItem("jwt")
  const user_info = jwt ? jwtDecode(jwt) : null;
  useEffect(() => {
    console.log(user_info)
    if (user_info) {
      setUsername(user_info.name);
      setEmail(user_info.email);
    }
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  };
  const handleSubmit = async () => {
    // TODO: 在這裡呼叫後端 API 進行帳號創建
    setResponseMessage({ text: "Processing...", color: "white" });
    try {
      const response = await fetch("http://localhost:8000/api/v1/register", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, phone, gender, age, password }),
      });

      if (response.ok) {
        // 創建成功，跳轉回登入頁面
        setResponseMessage({ text: "Success!", color: "white" });
        navigate('/login');
      } else {
        // 登入失敗，顯示錯誤訊息
        const errorData = await response.json();
        setResponseMessage({
          text: Array.isArray(errorData.detail)
            ? errorData.detail.map((err: { msg: string }) => err.msg).join(", ")  // Extract messages from all errors
            : errorData.detail || "An unexpected error occurred.",
          color: "red",
        });
      }
    } catch (error) {
      setResponseMessage({ text: "Failed to connect to the server.", color: "red" });
    }
  };

  return (
    <>
      <Topbar />
      <div className="center-container">
        <div className="create-account-box">
          <div className="instruction">{jwt ? "請輸入剩下資訊" : "請輸入你的資訊"}</div>
          <input
            type="text"
            className="account-input"
            placeholder="使用者名稱"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="email"
            className="account-input"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="tel"
            className="account-input"
            placeholder="手機號碼"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
          />
          <div className="sex-radio">
            <div>你的生理性別</div>
            <input
              type="radio"
              name="gender"
              value="male"
              checked={gender === 'male'}
              onChange={(e) => setGender(e.target.value)}
            />{' '}
            男性
            <input
              type="radio"
              name="gender"
              value="female"
              checked={gender === 'female'}
              onChange={(e) => setGender(e.target.value)}
            />{' '}
            女性
          </div>
          <input
            type="number"
            className="account-input"
            placeholder="年紀"
            value={age}
            onChange={(e) => setAge(e.target.value)}
          />
          <input
            type="password"
            className="account-input"
            placeholder="密碼"
            value={password}
            disabled={jwt !== null}
            onKeyDown={handleKeyDown}
            onChange={(e) => setPassword(e.target.value)}
          />
          {responseMessage.text && (
            <p style={{ color: responseMessage.color }}>
              {responseMessage.text}
            </p>
          )}
          <div className="button-container">
            <Link to="/login">
              <button className="back-to-login-btn">返回登入</button>
            </Link>
            <button className="submit-btn" onClick={handleSubmit}>
              送出
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default CreateAccountPage;
