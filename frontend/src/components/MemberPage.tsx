import { Link, useNavigate } from 'react-router-dom';
import beginnerImg from '../assets/cards/Beginner.png';
import advancedImg from '../assets/cards/Advanced.png';
import teacherImg from '../assets/cards/Teacher.png';
import adminImg from '../assets/cards/Admin.png';
import '../styles/member.scss';
import Topbar from './Topbar';


function MemberPage() {
  const navigate = useNavigate();
  const token = localStorage.getItem('access_token');
  const role = localStorage.getItem('user_role');

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_role');
    navigate('/login')
  };

  if (!token || !role) {
    alert('請先登入');
    navigate('/login')
    return;
  }
  return <>
    <Topbar />
    <div className='center-container'>
      {role === "admin" && <img className='card-img' src={adminImg} alt="member card" />}
      {role === "teacher" && <img className='card-img' src={teacherImg} alt="member card" />}
      {role === "student_advanced" && <img className='card-img' src={advancedImg} alt="member card" />}
      {role === "student_beginner" && <img className='card-img' src={beginnerImg} alt="member card" />}
      <div className='btns'>
        {role === 'admin' &&
          <Link to={'/user_manager'}>
            更改社員資訊
          </Link>
        }
        {(role === 'admin' || role === 'teacher') &&
          <Link to={'/trick_manager'}>
            加入/刪除Trick
          </Link>
        }
        <Link to={"/member/edit"} >
          個人資料
        </Link>
        <a className="back-btn" onClick={handleLogout}>
          登出
        </a>
      </div>
    </div>
  </>
}
export default MemberPage
