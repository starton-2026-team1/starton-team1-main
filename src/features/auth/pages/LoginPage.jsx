import { useState } from 'react'
import { Check, Eye, EyeOff } from 'lucide-react'
import BackButton from '../../../components/common/BackButton'
import UnderlinedInput from '../../../components/common/UnderlinedInput'
import { getEmailError, isValidEmail } from '../utils/emailValidation'
import '../styles/login.css'

function LoginPage({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [emailConfirmed, setEmailConfirmed] = useState(false)
  const [passwordVisible, setPasswordVisible] = useState(false)
  const [emailError, setEmailError] = useState('')

  const confirmEmail = () => {
    const validationError = getEmailError(email)

    if (validationError) {
      setEmailError(validationError)
      return
    }

    setEmailError('')
    setEmailConfirmed(true)
  }

  const handleEmailChange = (event) => {
    const nextEmail = event.target.value
    setEmail(nextEmail)
    setEmailError('')

    if (isValidEmail(nextEmail)) {
      setEmailConfirmed(true)
    }
  }

  const handleConfirmedEmailChange = (event) => {
    const nextEmail = event.target.value
    setEmail(nextEmail)
    setEmailError(getEmailError(nextEmail))
  }

  const handleSubmit = (event) => {
    event.preventDefault()

    if (!emailConfirmed) {
      confirmEmail()
      return
    }

    const validationError = getEmailError(email)

    if (validationError) {
      setEmailError(validationError)
      return
    }

    if (password && onLogin) {
      onLogin({ email, password })
    }
  }

  const handleBack = () => {
    if (emailConfirmed) {
      setEmailConfirmed(false)
      setPassword('')
      setPasswordVisible(false)
      return
    }

    if (window.history.length > 1) {
      window.history.back()
    }
  }

  return (
    <main className="login-page">
      <section className="login-panel" aria-label="로그인">
        <BackButton onClick={handleBack} />

        <form className="login-form" onSubmit={handleSubmit} noValidate>
          {!emailConfirmed ? (
            <UnderlinedInput
              id="email"
              type="email"
              value={email}
              placeholder="이메일"
              autoComplete="email"
              autoFocus
              aria-invalid={Boolean(emailError)}
              aria-describedby={emailError ? 'email-error' : undefined}
              error={emailError}
              onChange={handleEmailChange}
              action={isValidEmail(email) ? <Check className="input-check" aria-label="입력 완료" /> : null}
            />
          ) : (
            <>
              <UnderlinedInput
                id="password"
                type={passwordVisible ? 'text' : 'password'}
                value={password}
                placeholder="비밀번호"
                autoComplete="current-password"
                autoFocus
                onChange={(event) => setPassword(event.target.value)}
                action={(
                  <button
                    className="visibility-button"
                    type="button"
                    aria-label={passwordVisible ? '비밀번호 숨기기' : '비밀번호 보기'}
                    onClick={() => setPasswordVisible((visible) => !visible)}
                  >
                    {passwordVisible ? <EyeOff aria-hidden="true" /> : <Eye aria-hidden="true" />}
                  </button>
                )}
              />

              <div className={`confirmed-email${emailError ? ' confirmed-email--error' : ''}`}>
                <input
                  id="confirmed-email"
                  type="email"
                  value={email}
                  aria-label="이메일 수정"
                  autoComplete="email"
                  aria-invalid={Boolean(emailError)}
                  aria-describedby={emailError ? 'confirmed-email-error' : undefined}
                  onChange={handleConfirmedEmailChange}
                />
                {!emailError && <Check className="input-check" aria-hidden="true" />}
              </div>
              {emailError && <p className="confirmed-email-error" id="confirmed-email-error">{emailError}</p>}

              <button className="login-button" type="submit" disabled={!password || Boolean(emailError)}>
                로그인
              </button>
            </>
          )}
        </form>
      </section>
    </main>
  )
}

export default LoginPage
