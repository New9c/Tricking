import '../styles/global.scss';
import React, { useEffect, useState } from "react";
import { Link, useNavigate } from 'react-router-dom';
import '../styles/user_manager.scss';
import '../styles/global.scss';
import Topbar from './Topbar';
import Loading from './Loading';

interface UsersData {
  [role: string]: string[];
}

const UserManager: React.FC = () => {
  const navigate = useNavigate();
  const [users, setUsers] = useState<UsersData | null>(null);
  const [userRoles, setUserRoles] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(true); // Tracks loading state
  const token = localStorage.getItem('access_token');
  const role = localStorage.getItem('user_role');

  const fetchUsers = async () => {
    setIsLoading(true);
    if (!token) {
      alert('請先登入');
      navigate('/login')
    } else if (role !== 'admin') {
      alert('只有幹部可以改他人權限');
      navigate('/')
    }
    const response = await fetch("http://localhost:8000/api/v1/users", {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    setIsLoading(false);
    if (response.ok) {
      const data: UsersData = await response.json();
      setUsers(data);

      const initialRoles: Record<string, string> = {};
      Object.entries(data).forEach(([role, usernames]) => {
        usernames.forEach((username) => {
          initialRoles[username] = role;
        });
      });
      setUserRoles(initialRoles);
    } else {
      alert("請重新登入");
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_role');
      navigate('/login')
    }
  };

  const handleRoleChange = (username: string, role: string) => {
    setUserRoles((prevRoles) => ({
      ...prevRoles,
      [username]: role,
    }));
    saveRoleChange(username, role);
    fetchUsers();
  };

  const saveRoleChange = (username: string, role: string) => {
    const confirmation = confirm(
      "確定更改權限？"
    );
    if (!confirmation) {
      return
    }
    fetch("http://localhost:8000/api/v1/update_role", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: username, role: role }),
    })
      .then((response) => {
        fetchUsers();
        if (!response.ok) {
          return response.json().then((errorData) => {
            console.error("Failed to update role:", errorData);
          });
        }
      })
      .catch((error) => {
        console.error("Error updating role:", error);
      });
  };

  const handleUserDelete = (username: string) => {
    const confirmation = confirm(
      "確定刪除用戶？"
    );
    if (!confirmation) {
      fetchUsers();
      return
    }
    fetch(`http://localhost:8000/api/v1/delete/${username}`, {
      method: "DELETE"
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((errorData) => {
            console.error("Failed to delete user:", errorData);
          });
        }
      })
      .catch((error) => {
        console.error("Error deleting user:", error);
      });
    fetchUsers();
  };

  useEffect(() => {
    fetchUsers();
  }, []);
  if (isLoading)
    return <Loading />

  return (
    <>
      <Topbar />
      {users &&
        Object.entries(users).map(([_, usernames]) => (
          <div className="user-container" key={_}>
            {usernames.map((name) => (
              <div className="user-box" key={name}>
                <div className="info-top">
                  {name}
                  <button className="delete-btn" onClick={() => handleUserDelete(name)}>
                    刪除
                  </button>
                </div>
                <div className="info-role">
                  <label>
                    <input
                      type="radio"
                      name={`${name}-role`}
                      value="admin"
                      checked={userRoles[name] === 'admin'}
                      onChange={() => handleRoleChange(name, 'admin')}
                    />{' '}
                    幹部
                  </label>
                  <label>
                    <input
                      type="radio"
                      name={`${name}-role`}
                      value="teacher"
                      checked={userRoles[name] === 'teacher'}
                      onChange={() => handleRoleChange(name, 'teacher')}
                    />{' '}
                    教師
                  </label>
                  <label>
                    <input
                      type="radio"
                      name={`${name}-role`}
                      value="student"
                      checked={userRoles[name] === 'student'}
                      onChange={() => handleRoleChange(name, 'student')}
                    />{' '}
                    學生
                  </label>
                </div>
              </div>
            ))}
          </div>
        ))}
    </>
  );
};

export default UserManager;
