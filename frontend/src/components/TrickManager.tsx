import '../styles/global.scss';
import React, { useState, useEffect } from "react";
import "../styles/trick-manager.scss";
import Topbar from "./Topbar";
import { useNavigate } from 'react-router-dom';
import Loading from './Loading';

const TrickManager: React.FC = () => {
  const navigate = useNavigate()
  const [mode, setMode] = useState<"add" | "delete">("add");
  const [trickName, setTrickName] = useState<string>("");
  const [trickLevel, setTrickLevel] = useState<string>("");
  const [trickDesc, setTrickDesc] = useState<string>("");
  const [responseMessage, setResponseMessage] = useState<{ text: string; color: string }>({
    text: "",
    color: "white",
  });

  const token = localStorage.getItem('access_token');
  const role = localStorage.getItem('user_role');

  useEffect(() => {
    if (!token) {
      alert('請先登入');
      navigate('/login')
    } else if (role === 'student') {
      alert('學生無法編輯Tricks');
      navigate('/tricktionary')
    }
  }, [token, role, navigate]);

  if ((!token || role === 'student_beginner' || role === 'student_advanced') && location.pathname === "/trick_manager") {
    return <Loading />
  }

  const handleAction = async () => {
    if (mode === "add") {
      // Handle Add Trick
      if (!trickName || !trickLevel) {
        setResponseMessage({ text: "Please provide both trick name and level.", color: "red" });
        return;
      }
      try {
        const response = await fetch("http://localhost:8000/api/v1/tricktionary/add", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name: trickName, level: trickLevel, desc: trickDesc }),
        });
        if (response.ok) {
          setResponseMessage({ text: `Trick '${trickName}' added successfully!`, color: "white" });
          setTrickName(""); // Clear input
        } else {
          const errorData = await response.json();
          setResponseMessage({ text: `Error: ${errorData.detail}`, color: "red" });
        }
      } catch (error) {
        setResponseMessage({ text: "Failed to connect to the server.", color: "red" });
      }
    } else {
      // Handle Delete Trick
      if (!trickName) {
        setResponseMessage({ text: "Please provide a trick name to delete.", color: "white" });
        return;
      }
      try {
        const response = await fetch(`http://localhost:8000/api/v1/tricktionary/delete/${trickName}`, {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
        });
        if (response.ok) {
          setResponseMessage({ text: `Trick '${trickName}' deleted successfully!`, color: "white" });
          setTrickName(""); // Clear input
        } else {
          const errorData = await response.json();
          setResponseMessage({ text: `Error: ${errorData.detail}`, color: "red" });
        }
      } catch (error) {
        setResponseMessage({ text: "Failed to connect to the server.", color: "red" });
      }
    }
  };

  return (
    <>
      <Topbar />
      <div className="center-container">
        <div className="trick-manager-box">
          <h1 className="title">
            加入/刪除Trick
          </h1>

          <div className="trick-radio">
            <label>
              <input
                type="radio"
                value="add"
                checked={mode === "add"}
                onChange={() => setMode("add")}
              />
              加入Trick
            </label>
            <label>
              <input
                type="radio"
                value="delete"
                checked={mode === "delete"}
                onChange={() => setMode("delete")}
              />
              刪除Trick
            </label>
          </div>

          <input
            className="field-input"
            placeholder="名稱"
            type="text"
            value={trickName}
            onChange={(e) => setTrickName(e.target.value)}
          />

          <input
            className="field-input"
            placeholder="難度"
            type="text"
            value={mode === "add" ? trickLevel : " "}
            disabled={mode !== "add"}
            onChange={(e) => setTrickLevel(e.target.value)}
          />
          <textarea
            className="field-input"
            rows={4}
            value={mode === "add" ? trickDesc : " "}
            placeholder="簡介"
            disabled={mode !== "add"}
            onChange={(e) => setTrickDesc(e.target.value)}
          />

          <div className="button-container">
            <button
              className="action-btn"
              onClick={handleAction}
            >
              {mode === "add" ? "加入Trick" : "刪除Trick"}
            </button>
          </div>

          {responseMessage.text && (
            <p style={{ color: responseMessage.color }}>
              {responseMessage.text}
            </p>
          )}
        </div>
      </div>
    </>
  );
};

export default TrickManager;
