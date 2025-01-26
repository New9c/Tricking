import Logo from "./Logo";
import dictImg from '../assets/dictionary.png';
import userImg from '../assets/default-avatar.svg';
import '../styles/topbar.scss';

const token = localStorage.getItem('access_token');
function goToTricktionary() {
  if (window.location.pathname.toString() != '/tricktionary')
    window.location.href = '/tricktionary';
}
function handleUser() {
  if (!token) {
    window.location.href = '/login';
  } else {
    window.location.href = '/member';
  }
}

function Topbar() {

  return (
    <div className="topbar">
      <Logo />
      <div className="right-btns">
        <button className="tricktionary-btn" onClick={goToTricktionary}>
          Tricktionary
          <img className="dict-img" src={dictImg} alt="dictionary image" />
        </button>
        {!token ? (
          <button className="user-btn" onClick={handleUser}>
            登入
          </button>
        ) : (
          <button className="user-btn" onClick={handleUser}>
            你
            <img className="user-img" src={userImg} alt="user image" />
          </button>
        )}
      </div>
    </div>
  );
}
export default Topbar
