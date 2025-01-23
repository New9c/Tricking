// frontend/src/components/MemberPage.tsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../styles/member.scss';
import '../styles/global.scss';
import Logo from './Logo';
import defaultAvatar from '../assets/default-avatar.svg';
import cameraIcon from '../assets/camera.svg';

interface MemberData {
  username: string;
  email: string;
  phone: string;
  gender: 'male' | 'female';
  age: number;
  password?: string; // 密碼通常不從後端直接獲取，這裡僅為示範
}

const MemberPage: React.FC = () => {
  const [memberData, setMemberData] = useState<MemberData>({
    username: 'Loading...',
    email: 'Loading...',
    phone: 'Loading...',
    gender: 'male',
    age: 0,
  });
  const [isEditing, setIsEditing] = useState(false);
  const [originalData, setOriginalData] = useState<MemberData | null>(null);

  useEffect(() => {
    const fetchMemberData = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        alert('Please log in first.');
        window.location.href = '/login';
        return;
      }
      // TODO: 從後端 API 獲取會員資料

      const response = await fetch('http://localhost:8000/api/v1/me', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`, // Add the token to the Authorization header
          'Content-Type': 'application/json',
        },
      });
      if (response.ok) {
        const data = await response.json();
        setMemberData(data);
        setOriginalData(data);
      } else {
        console.error('無法獲取會員資料');
      }
    };

    fetchMemberData();
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setMemberData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleGenderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setMemberData((prevData) => ({
      ...prevData,
      gender: e.target.value as 'male' | 'female',
    }));
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = async () => {
    // TODO: 將修改後的資料送回後端 API
    if (originalData == null)
      return
    if (JSON.stringify(memberData) === JSON.stringify(originalData)) {
      setIsEditing(false);
      return;
    }
    const { password, ...noPwdData } = memberData;
    const response = await fetch(`http://localhost:8000/api/v1/me?username=${encodeURIComponent(originalData.username)}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(noPwdData),
    });

    if (response.ok) {
      setIsEditing(false);
      setOriginalData(memberData);
      alert('儲存成功!');
    } else {
      console.error('儲存失敗');
    }
  };

  const handleLogout = () => {
    if (JSON.stringify(memberData) !== JSON.stringify(originalData)) {
      alert('請先儲存您的變更');
      return;
    }
    localStorage.removeItem('access_token');
    window.location.href = '/login';
  };

  return (
    <>
      <Logo />
      <div className="profile-container">
        <div className="profile-box">
          <div className="profile-title">個人資料</div>
          <div className="profile-section">
            <div className="profile-picture">
              <img src={defaultAvatar} alt="User Avatar" />
              <button className="change-picture-btn">
                <img src={cameraIcon} alt="Change Picture" />
              </button>
            </div>
          </div>
          <div className="info-container">
            <input
              type="text"
              className="info-input"
              placeholder="Username"
              name="username"
              value={memberData.username}
              onChange={handleChange}
              readOnly={!isEditing}
            />
            <input
              type="email"
              className="info-input"
              placeholder="Email"
              name="email"
              value={memberData.email}
              onChange={handleChange}
              readOnly={!isEditing}
            />
            <input
              type="tel"
              className="info-input"
              placeholder="Phone Number"
              name="phone"
              value={memberData.phone}
              onChange={handleChange}
              readOnly={!isEditing}
            />
            <div className="info-gender">
              <label>
                <input
                  type="radio"
                  name="gender"
                  value="male"
                  checked={memberData.gender === 'male'}
                  onChange={handleGenderChange}
                  disabled={!isEditing}
                />{' '}
                男性
              </label>
              <label>
                <input
                  type="radio"
                  name="gender"
                  value="female"
                  checked={memberData.gender === 'female'}
                  onChange={handleGenderChange}
                  disabled={!isEditing}
                />{' '}
                女性
              </label>
            </div>
            <input
              type="number"
              className="info-input"
              placeholder="Age"
              name="age"
              value={memberData.age}
              onChange={handleChange}
              readOnly={!isEditing}
            />
            <input
              type="password"
              className="info-input"
              placeholder="Password"
              value="******" // 隱藏密碼
              readOnly
              onClick={() => alert('請到其他頁面修改密碼')} // 提示修改密碼
            />
          </div>
          <div className="button-container">
            <button className="back-btn" onClick={handleLogout}>
              登出
            </button>
            {isEditing ? (
              <button className="save-btn" onClick={handleSave}>
                儲存
              </button>
            ) : (
              <button className="save-btn" onClick={handleEdit}>
                編輯
              </button>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default MemberPage;
