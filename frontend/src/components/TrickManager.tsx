import '../styles/global.scss';
import React, { useState } from "react";
import "../styles/trick-manager.scss";
import Topbar from "./Topbar";

const TrickManager: React.FC = () => {
  const [mode, setMode] = useState<"add" | "delete">("add"); // Add or Delete mode
  const [trickName, setTrickName] = useState<string>(""); // Trick name input
  const [trickLevel, setTrickLevel] = useState<string>(""); // Trick name input
  const [responseMessage, setResponseMessage] = useState<{ text: string; color: string }>({
    text: "",
    color: "white",
  });

  const token = localStorage.getItem('access_token');
  const role = localStorage.getItem('user_role');
  if (!token) {
    alert('請先登入');
    window.location.href = '/login';
  } else if (role === 'student') {
    alert('學生無法編輯Tricks');
    window.location.href = '/tricktionary';
  }
  const handleAction = async () => {
    if (mode === "add") {
      // Handle Add Trick
      if (!trickName || !trickLevel) {
        setResponseMessage("Please provide both trick name and level.");
        return;
      }
      try {
        const response = await fetch("http://localhost:8000/api/v1/tricktionary/add", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name: trickName, level: trickLevel }),
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
          <h1 className="title">Trick Manager</h1>

          {/* Mode Selector */}
          <div className="trick-radio">
            <label>
              <input
                type="radio"
                value="add"
                checked={mode === "add"}
                onChange={() => setMode("add")}
              />
              Add Trick
            </label>
            <label>
              <input
                type="radio"
                value="delete"
                checked={mode === "delete"}
                onChange={() => setMode("delete")}
              />
              Delete Trick
            </label>
          </div>

          {/* Form */}
          <div>
            <label>
              <input
                className="field-input"
                placeholder="Trick Name"
                type="text"
                value={trickName}
                onChange={(e) => setTrickName(e.target.value)}
              />
            </label>
          </div>

          {mode === "add" && (
            <div>
              <label>
                <input
                  className="field-input"
                  placeholder="Trick Level"
                  type="text"
                  value={trickLevel}
                  onChange={(e) => setTrickLevel(e.target.value)}
                />
              </label>
            </div>
          )}

          <div className="button-container">
            <button
              className="action-btn"
              onClick={handleAction}
            >
              {mode === "add" ? "Add Trick" : "Delete Trick"}
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
