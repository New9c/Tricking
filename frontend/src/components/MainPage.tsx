import '../styles/global.scss';
import '../styles/main-page.scss';
import MainPageTricks from './MainPageTricks';
import Topbar from "./Topbar"

function MainPage() {
  return <div className='main-page'>
    <Topbar />
    <div className='main-title'>
      <h1>NCKU TRICKING</h1>

      <h1>台灣第一個tricking社</h1>
    </div>
    <div className='main-mid'>
      <div className='what-is-tricking'>
        <h1>What is tricking?</h1>
        <h2>Tricking focuses on performing dynamic, acrobatic moves such as kicks, flips, and twists in a fluid and aesthetic manner. Unlike traditional martial arts, which emphasize combat, tricking is primarily about self-expression and style.</h2>
      </div>
      <div className='slide-bar'>
        <MainPageTricks desc="pat" url="/src/assets/cats/pat.gif" />
        <MainPageTricks desc="love" url="/src/assets/cats/love.gif" />
        <MainPageTricks desc="pat" url="/src/assets/cats/pat.gif" />
        <MainPageTricks desc="love" url="/src/assets/cats/love.gif" />
        <MainPageTricks desc="pat" url="/src/assets/cats/pat.gif" />
        <MainPageTricks desc="love" url="/src/assets/cats/love.gif" />
      </div>
    </div>
    <h1 className='beginner'>入門班</h1>
    <h1 className='advanced'>進階班</h1>
    <div className='advanced-crit'><h1>進階班門檻</h1>
      <div className='slide-bar'>
        <MainPageTricks desc="pat" url="/src/assets/cats/pat.gif" />
        <MainPageTricks desc="love" url="/src/assets/cats/love.gif" />
        <MainPageTricks desc="pat" url="/src/assets/cats/pat.gif" />
        <MainPageTricks desc="love" url="/src/assets/cats/love.gif" />
        <MainPageTricks desc="pat" url="/src/assets/cats/pat.gif" />
        <MainPageTricks desc="love" url="/src/assets/cats/love.gif" />
      </div>
    </div>
    <h1 className='how-to-join'>如何加入我們</h1>
    <div className='footer'>
      <a href="https://www.instagram.com/ncku_tricking/" target="_blank" rel="noopener noreferrer">
        <i className="fa-brands fa-instagram"></i>
      </a>
    </div>
  </div>
}
export default MainPage
