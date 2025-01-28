import errorImg from "../assets/serverError.png";
import '../styles/error.scss';

function ErrorPage() {
  return <div className='error-container'>
    <img src={errorImg} alt="error img" />
    Network Error
  </div>;
}
export default ErrorPage
