import Logo from "./Logo";
import dictImg from '../assets/dictionary.png';
import userImg from '../assets/default-avatar.svg';
import '../styles/topbar.scss';
import { Link } from "react-router-dom";

function Topbar() {
  const token = localStorage.getItem('access_token');
  const googleImg = localStorage.getItem('user_img');

  return (
    <div className="topbar">
      <Logo />
      <div className="right-btns">
        <Link to={'/tricktionary'}>
          <button className="tricktionary-btn">
            Tricktionary
            <img className="dict-img" src={dictImg} alt="dictionary image" />
          </button>
        </Link>
        <Link to={token ? '/member' : '/login'} >
          {!token ? (
            <button className="user-btn">
              登入
            </button>
          ) : (
            <button className="user-btn">
              你
              <img className="user-img" src={googleImg ? googleImg : userImg} alt="user image" />
            </button>
          )}
        </Link>
      </div>
    </div>
  );
}
export default Topbar
