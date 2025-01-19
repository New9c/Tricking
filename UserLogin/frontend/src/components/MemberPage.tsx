import React, { useState, ChangeEvent, FormEvent } from "react";
import axios from "axios";

interface LoginFormData {
  account: string;
  password: string;
}

const Login: React.FC = () => {
  const [formData, setFormData] = useState<LoginFormData>({
    account: "",
    password: "",
  });

  const [responseMessage, setResponseMessage] = useState<string>("");

  const handleChange = (e: ChangeEvent<HTMLInputElement>): void => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: FormEvent): Promise<void> => {
    e.preventDefault();
    setResponseMessage("Processing...");
    try {
      const response = await axios.post("http://localhost:8000/api/v1/login", formData);
      if (response.status === 200) {
        setResponseMessage("Login successful!");
        // Handle further actions, like saving a token or redirecting
      }
    } catch (error: any) {
      if (error.response) {
        const { data } = error.response;
        if (data.detail) setResponseMessage(data.detail);
        else setResponseMessage("An unexpected error occurred.");
      } else {
        setResponseMessage("Failed to connect to the server.");
      }
    }
  };

  return (
    <div style={{ margin: "20px", textAlign: "center" }}>
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "15px" }}>
          <label htmlFor="account">Account:</label>
          <input
            type="text"
            id="account"
            name="account"
            value={formData.account}
            onChange={handleChange}
            required
            style={{ marginLeft: "10px", padding: "5px" }}
          />
        </div>
        <div style={{ marginBottom: "15px" }}>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            style={{ marginLeft: "10px", padding: "5px" }}
          />
        </div>
        <button type="submit" style={{ padding: "10px 20px" }}>
          Login
        </button>
      </form>
      {responseMessage && <p style={{ marginTop: "20px" }}>{responseMessage}</p>}
    </div>
  );
};

export default Login;
