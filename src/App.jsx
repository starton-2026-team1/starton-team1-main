import { useState } from 'react'
import AuthLandingPage from './features/auth/pages/AuthLandingPage'
import LoginPage from './features/auth/pages/LoginPage'
import SignUpPage from './features/auth/pages/SignUpPage'

function App() {
  const [page, setPage] = useState('landing')

  if (page === 'login') {
    return <LoginPage onBack={() => setPage('landing')} />
  }

  if (page === 'signup') {
    return <SignUpPage onBack={() => setPage('landing')} />
  }

  return (
    <AuthLandingPage
      onEmailLogin={() => setPage('login')}
      onSignUp={() => setPage('signup')}
    />
  )
}

export default App
