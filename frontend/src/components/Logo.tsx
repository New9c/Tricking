import logoImg from '../assets/trickingLogo.png'; // 導入圖片
import "../styles/logo.scss";

function Logo() {
  return <button className="logo" onClick={() => window.location.href = '/'}>
    <img src={logoImg} alt="ncku tricking club logo" />
    <div className="club-name">NCKU Tricking</div>
  </button>;
}
export default Logo
