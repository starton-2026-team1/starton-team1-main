import mascot from '../../../assets/mascot.png'
import '../styles/authLanding.css'

function AuthLandingPage({ onEmailLogin, onSignUp, onGoHome }) {
  return (
    <main className="auth-landing">
      <section className="auth-landing__panel" aria-labelledby="auth-welcome-title">
        <header className="auth-landing__hero">
          <h1 id="auth-welcome-title">
            소중한 일상에
            <br />
            <strong>안심</strong>을 더하세요
          </h1>
          <p className="auth-landing__description">
            생활 패턴을 감지하고
            <br />
            이상 징후를 빠르게 알려드려요
          </p>
        </header>

        <div className="auth-landing__mascot-wrap">
          <img className="auth-landing__mascot" src={mascot} alt="손을 흔드는 살핌이 캐릭터" />
        </div>

        <div className="auth-landing__sheet">
          <button className="auth-landing__login" type="button" onClick={onEmailLogin}>
            이메일 로그인
          </button>
          <button className="auth-landing__signup" type="button" onClick={onSignUp}>
            처음이신가요? <span>회원가입</span>
          </button>
          <button className="auth-landing__home-link" type="button" onClick={onGoHome}>
            임시 홈 바로가기
          </button>
        </div>
      </section>
    </main>
  )
}

export default AuthLandingPage
