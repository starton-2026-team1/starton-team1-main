import { useState } from 'react'
import {
  Activity,
  Bell,
  ChevronRight,
  CircleHelp,
  FileClock,
  Home,
  Info,
  LogOut,
  Plus,
  Settings,
  ShieldCheck,
  UserRound,
  UsersRound,
} from 'lucide-react'
import mascot from '../../../assets/mascot.png'
import emptyMascot from '../../../assets/mascot/empty.png'
import '../styles/main.css'

const navigationItems = [
  { id: 'home', label: '홈', icon: Home },
  { id: 'people', label: '대상자', icon: UsersRound },
  { id: 'sensor', label: '센서', icon: Activity },
  { id: 'history', label: '기록', icon: FileClock },
  { id: 'profile', label: '내정보', icon: UserRound },
]

const profileItems = [
  { label: '내 프로필', icon: UserRound },
  { label: '알림 설정', icon: Bell },
  { label: '보호자 및 가족 관리', icon: UsersRound },
  { label: '앱 권한 설정', icon: Settings },
  { label: '고객센터', icon: CircleHelp },
  { label: '이용약관 및 개인정보 처리방침', icon: ShieldCheck },
]

function EmptyState({ actionLabel, description, onAction, title }) {
  return (
    <div className="empty-state">
      <div className="empty-state__image-wrap">
        <img src={emptyMascot} alt="기다리고 있는 캐릭터" />
      </div>
      <h2>{title}</h2>
      <p>{description}</p>
      {actionLabel && (
        <button className="primary-action" type="button" onClick={onAction}>
          <Plus aria-hidden="true" />
          {actionLabel}
        </button>
      )}
    </div>
  )
}

function HomePage({ onAddPerson }) {
  return (
    <div className="home-view">
      <header className="page-header home-view__header">
        <p>안녕하세요!</p>
        <h1>안심 모니터링을<br />시작해 볼까요?</h1>
      </header>

      <section className="onboarding-card" aria-labelledby="onboarding-title">
        <div className="onboarding-card__illustration">
          <img src={mascot} alt="손을 흔드는 살핌이 캐릭터" />
        </div>
        <h2 id="onboarding-title">먼저 대상자를 등록해 주세요</h2>
        <p className="onboarding-card__description">
          가족을 등록한 다음 센서를 연결할 수 있어요.
        </p>

        <ol className="onboarding-progress" aria-label="모니터링 시작 단계">
          <li className="onboarding-progress__item onboarding-progress__item--active">
            <span>1</span>
            <strong>대상자 등록</strong>
          </li>
          <li className="onboarding-progress__line" aria-hidden="true" />
          <li className="onboarding-progress__item">
            <span>2</span>
            <strong>센서 연결</strong>
          </li>
          <li className="onboarding-progress__line" aria-hidden="true" />
          <li className="onboarding-progress__item">
            <span>3</span>
            <strong>준비 완료</strong>
          </li>
        </ol>

        <button className="primary-action primary-action--wide" type="button" onClick={onAddPerson}>
          대상자 등록하기
          <ChevronRight aria-hidden="true" />
        </button>
      </section>
    </div>
  )
}

function ProfilePage() {
  return (
    <div className="profile-view">
      <header className="page-header">
        <h1>내정보</h1>
      </header>

      <section className="profile-card" aria-label="사용자 정보">
        <div className="profile-card__avatar"><UserRound aria-hidden="true" /></div>
        <div><strong>사용자</strong><span>계정 정보를 확인해 주세요</span></div>
        <ChevronRight aria-hidden="true" />
      </section>

      <section className="settings-list" aria-label="설정">
        {profileItems.map(({ label, icon: Icon }) => (
          <button key={label} type="button">
            <Icon aria-hidden="true" />
            <span>{label}</span>
            <ChevronRight aria-hidden="true" />
          </button>
        ))}
      </section>

      <button className="logout-button" type="button">
        <LogOut aria-hidden="true" />
        로그아웃
      </button>
      <p className="app-version"><Info aria-hidden="true" /> 앱 버전 1.0.0</p>
    </div>
  )
}

function MainPage() {
  const [activePage, setActivePage] = useState('home')
  const activeItem = navigationItems.find(({ id }) => id === activePage)

  const renderPage = () => {
    if (activePage === 'home') {
      return <HomePage onAddPerson={() => setActivePage('people')} />
    }

    if (activePage === 'people') {
      return (
        <EmptyState
          title="등록된 대상자가 없어요"
          description="돌봄이 필요한 가족을 등록해 주세요."
          actionLabel="대상자 등록하기"
        />
      )
    }

    if (activePage === 'sensor') {
      return (
        <EmptyState
          title="먼저 대상자를 등록해 주세요"
          description="대상자를 등록한 다음 센서를 연결할 수 있어요."
          actionLabel="대상자 등록하기"
          onAction={() => setActivePage('people')}
        />
      )
    }

    if (activePage === 'history') {
      return (
        <EmptyState
          title="아직 기록이 없어요"
          description="센서를 연결하면 활동과 알림 기록이 쌓여요."
        />
      )
    }

    return <ProfilePage />
  }

  return (
    <main className="main-page">
      <section className="main-panel" aria-label={activeItem?.label}>
        <div className="main-content" role="region" aria-label={`${activeItem?.label} 페이지`}>
          {renderPage()}
        </div>

        <nav className="bottom-navigation" aria-label="주요 메뉴">
          {navigationItems.map(({ id, label, icon: Icon }) => {
            const isActive = id === activePage
            const className = 'bottom-navigation__item'
              + (isActive ? ' bottom-navigation__item--active' : '')

            return (
              <button
                key={id}
                className={className}
                type="button"
                aria-current={isActive ? 'page' : undefined}
                onClick={() => setActivePage(id)}
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
