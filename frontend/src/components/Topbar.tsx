import Logo from "./Logo";
import dictImg from '../assets/dictionary.png';
import '../styles/topbar.scss';

function goToTricktionary() {
  if (window.location.pathname.toString() != '/tricktionary')
    window.location.href = '/tricktionary';
}

function Topbar() {
  return (
    <div className="topbar">
      <Logo />
      <button className="tricktionary-btn" onClick={goToTricktionary}>
        Tricktionary
        <img className="dict-img" src={dictImg} alt="dictionary image" />
      </button>
    </div>
  );
}
export default Topbar
