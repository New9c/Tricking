import "../styles/main-page-tricks.scss"
function MainPageTricks({ desc, url }: { desc: string, url: string }) {
  return <div className="main-page-trick">
    {desc}
    <img src={url}></img>
  </div>
}
export default MainPageTricks
