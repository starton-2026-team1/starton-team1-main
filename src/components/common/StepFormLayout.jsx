import BackButton from './BackButton'
import './stepFormLayout.css'

function StepFormLayout({ actionDisabled, actionLabel, ariaLabel, children, currentStep, onBack, onSubmit, totalSteps }) {
  return (
    <main className="step-form-page">
      <section className="step-form-panel" aria-label={ariaLabel}>
        <header className="step-form-header">
          <BackButton onClick={onBack} />
          <span>{currentStep + 1} / {totalSteps}</span>
        </header>
        <div className="step-form-progress" aria-hidden="true">
          <span style={{ width: `${((currentStep + 1) / totalSteps) * 100}%` }} />
        </div>
        <form className="step-form" onSubmit={onSubmit} noValidate>
          <div className="step-form-content">{children}</div>
          <button className="step-form-action" type="submit" disabled={actionDisabled}>
            {actionLabel}
          </button>
        </form>
      </section>
    </main>
  )
}

export default StepFormLayout
