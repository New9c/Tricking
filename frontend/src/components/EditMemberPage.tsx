// frontend/src/components/MemberPage.tsx
import '../styles/global.scss';
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/member.scss';
import defaultAvatar from '../assets/default-avatar.svg';
import cameraIcon from '../assets/camera.svg';
import Topbar from './Topbar';

interface MemberData {
  username: string;
  email: string;
  phone: string;
  gender: 'male' | 'female';
  age: number;
  password?: string; // 密碼通常不從後端直接獲取，這裡僅為示範
  role: 'admin' | 'teacher' | 'student_advanced' | 'student_beginner';
}

const EditMemberPage: React.FC = () => {
  const navigate = useNavigate()
  const [memberData, setMemberData] = useState<MemberData>({
    username: 'Loading...',
    email: 'Loading...',
    phone: 'Loading...',
    gender: 'male',
    age: 0,
    role: 'student_beginner'
  });
  const [isEditing, setIsEditing] = useState(false);
  const [originalData, setOriginalData] = useState<MemberData | null>(null);

  useEffect(() => {
    const fetchMemberData = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        alert('請先登入');
        navigate('/login')
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
        alert("請重新登入");
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_role');
        navigate('/login')
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
  const handleRoleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setMemberData((prevData) => ({
      ...prevData,
      role: e.target.value as 'admin' | 'teacher' | 'student_advanced' | 'student_beginner',
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
    if (memberData.role !== 'admin' && originalData.role === 'admin') {
      const confirmation = confirm(
        "你確定要成為非幹部？會失去幹部的權限。"
      );
      if (!confirmation) {
        setMemberData(originalData);
        return;
      }
    }

    const { password, ...noPwdData } = memberData;
    const token = localStorage.getItem('access_token');
    const response = await fetch("http://localhost:8000/api/v1/me", {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`, // Add the token to the Authorization header
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(noPwdData),
    });

    if (response.ok) {
      setIsEditing(false);
      setOriginalData(memberData);
      alert('儲存成功!');
    } else {
      alert('儲存失敗');
    }
  };

  const handleLogout = () => {
    if (JSON.stringify(memberData) !== JSON.stringify(originalData)) {
      alert('請先儲存您的變更');
      return;
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_role');
    navigate('/login')
  };

  return (
    <>
      <Topbar />
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
            <div className="info-role">
              <label>
                <input
                  type="radio"
                  name="role"
                  value="admin"
                  checked={memberData.role === 'admin'}
                  onChange={handleRoleChange}
                  disabled={!(isEditing && originalData != null && originalData.role === 'admin')}
                />{' '}
                幹部
              </label>
              <label>
                <input
                  type="radio"
                  name="role"
                  value="teacher"
                  checked={memberData.role === 'teacher'}
                  onChange={handleRoleChange}
                  disabled={!(isEditing && originalData != null && originalData.role === 'admin')}
                />{' '}
                教師
              </label>
              <label>
                <input
                  type="radio"
                  name="role"
                  value="student_advanced"
                  checked={memberData.role === 'student_advanced'}
                  onChange={handleRoleChange}
                  disabled={!(isEditing && originalData != null && originalData.role === 'admin')}
                />{' '}
                進階班
              </label>
              <label>
                <input
                  type="radio"
                  name="role"
                  value="student_beginner"
                  checked={memberData.role === 'student_beginner'}
                  onChange={handleRoleChange}
                  disabled={!(isEditing && originalData != null && originalData.role === 'admin')}
                />{' '}
                入門班
              </label>
            </div>
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

export default EditMemberPage;
