import loadingImg from '../assets/loading.gif'; // 導入圖片
import '../styles/loading.scss'

function Loading() {
  return <div className='loading-container'>
    <img src={loadingImg} alt="loading spinner" />
  </div>;
}
export default Loading
