import { Activity, FileClock, Home, UserRound, UsersRound } from 'lucide-react'
import '../styles/main.css'

const navigationItems = [
  { id: 'home', label: '홈', icon: Home },
  { id: 'people', label: '대상자', icon: UsersRound },
  { id: 'sensor', label: '센서', icon: Activity },
  { id: 'history', label: '기록', icon: FileClock },
  { id: 'profile', label: '내정보', icon: UserRound },
]

function MainPage() {
  return (
    <main className="main-page">
      <section className="main-panel" aria-label="메인">
        <nav className="bottom-navigation" aria-label="주요 메뉴">
          {navigationItems.map(({ id, label, icon: Icon }) => {
            const isActive = id === 'home'
            const className = 'bottom-navigation__item'
              + (isActive ? ' bottom-navigation__item--active' : '')

            return (
              <button
                key={id}
                className={className}
                type="button"
                aria-current={isActive ? 'page' : undefined}
              >
                <Icon aria-hidden="true" />
                <span>{label}</span>
              </button>
            )
          })}
        </nav>
      </section>
    </main>
  )
}

export default MainPage
