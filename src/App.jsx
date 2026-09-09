import { useState } from 'react'
import AuthLandingPage from './features/auth/pages/AuthLandingPage'
import LoginPage from './features/auth/pages/LoginPage'

function App() {
  const [page, setPage] = useState('landing')

  if (page === 'login') {
    return <LoginPage onBack={() => setPage('landing')} />
  }

  return (
    <AuthLandingPage
      onEmailLogin={() => setPage('login')}
    />
  )
}

export default App
