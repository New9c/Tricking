import logoImg from '../assets/trickingLogo.png'; // 導入圖片
import "../styles/logo.scss";

function Logo() {
  return <div className="logo">
    <img src={logoImg} alt="ncku tricking club logo" />
    <div className="club-name">NCKU Tricking</div>
  </div>;
}
export default Logo
