import { useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

function GoogleLoginBtn() {
  const navigate = useNavigate();

  useEffect(() => {
    // Load the Google Sign-In script dynamically
    const script = document.createElement("script");
    script.src = "https://accounts.google.com/gsi/client";
    script.async = true;
    script.defer = true;
    document.body.appendChild(script);

    // Define the callback globally
    window.handleCallbackResponse = async (response: { credential: string }) => {
      try {
        const jwt: { name: string, picture: string } = jwtDecode(response.credential);
        const res = await fetch("http://localhost:8000/api/v1/login", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({ username: jwt.name, password: "" }),
        });

        if (res.ok) {
          // 登入成功，跳轉到會員頁面
          const data = await res.json();
          localStorage.setItem('user_img', jwt.picture);
          localStorage.setItem('access_token', data.access_token);
          localStorage.setItem('user_role', data.role);
          navigate('/member')
        } else {
          localStorage.setItem("jwt", response.credential);
          navigate("/create-account");
        }
      } catch (error) {
        console.error("Error: ", error);
      }
    };

    return () => {
      // Cleanup script when component unmounts
      document.body.removeChild(script);
      delete window.handleCallbackResponse;
    };
  }, []);

  return <>
    <div id="g_id_onload"
      data-client_id="505413386201-6d0f37k7a56cptuhq9semvh4l4hrl7hf.apps.googleusercontent.com"
      data-context="signin"
      data-ux_mode="popup"
      data-callback="handleCallbackResponse"
      data-itp_support="true"
      data-auto_prompt="false">
    </div>

    <div className="g_id_signin"
      data-type="standard"
      data-shape="pill"
      data-theme="filled_blue"
      data-text="signin_with"
      data-size="large"
      data-logo_alignment="left">
    </div>
  </>
}

export default GoogleLoginBtn
