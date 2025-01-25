import React, { useState } from "react";
import Logo from "./Logo";
import "../styles/trick-manager.scss";
function goToTricktionary() {
  window.location.href = '/tricktionary';
}

const TrickManager: React.FC = () => {
  const [mode, setMode] = useState<"add" | "delete">("add"); // Add or Delete mode
  const [trickName, setTrickName] = useState<string>(""); // Trick name input
  const [trickLevel, setTrickLevel] = useState<string>(""); // Trick name input
  const [responseMessage, setResponseMessage] = useState<string>(""); // Feedback message

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
          setResponseMessage(`Trick '${trickName}' added successfully!`);
          setTrickName(""); // Clear input
        } else {
          const errorData = await response.json();
          setResponseMessage(`Error: ${errorData.detail}`);
        }
      } catch (error) {
        setResponseMessage("Failed to connect to the server.");
      }
    } else {
      // Handle Delete Trick
      if (!trickName) {
        setResponseMessage("Please provide a trick name to delete.");
        return;
      }
      try {
        const response = await fetch(`http://localhost:8000/api/v1/tricktionary/delete/${trickName}`, {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
        });
        if (response.ok) {
          setResponseMessage(`Trick '${trickName}' deleted successfully!`);
          setTrickName(""); // Clear input
        } else {
          const errorData = await response.json();
          setResponseMessage(`Error: ${errorData.detail}`);
        }
      } catch (error) {
        setResponseMessage("Failed to connect to the server.");
      }
    }
  };

  return (
    <>
      <Logo />
      <div className="center-container">
        <div className="trick-manager-box">
          <h1 className="title">Trick Manager</h1>

          {/* Mode Selector */}
          <div>
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
                style={{ marginLeft: "10px" }}
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
                  style={{ marginLeft: "10px" }}
                />
              </label>
            </div>
          )}

          {/* Submit Button */}
          <div className="button-container">
            <button
              className="action-btn"
              onClick={handleAction}
            >
              {mode === "add" ? "Add Trick" : "Delete Trick"}
            </button>
            <button
              className="action-btn"
              onClick={goToTricktionary}
            >
              Go To Tricktionary
            </button>
          </div>

          {/* Response Message */}
          {responseMessage && (
            <div>{responseMessage}</div>
          )}
        </div>
      </div>
    </>
  );
};

export default TrickManager;
