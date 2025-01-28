import { Link } from 'react-router-dom';
import logoImg from '../assets/trickingLogo.png'; // 導入圖片
import "../styles/logo.scss";

function Logo() {
  return <Link to={'/'} style={{ textDecoration: 'none' }}>
    <button className="logo">
      <img src={logoImg} alt="ncku tricking club logo" />
      <div className="club-name">NCKU Tricking</div>
    </button>
  </Link>
}
export default Logo
