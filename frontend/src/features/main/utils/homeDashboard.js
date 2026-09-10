const warningStatuses = new Set(['WARNING', 'ALERT', 'ANOMALY'])
const inactivityLimitMinutes = 30

const toDate = (value) => {
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? null : date
}

const formatTime = (date) => new Intl.DateTimeFormat('ko-KR', {
  hour: '2-digit',
  minute: '2-digit',
  hour12: false,
}).format(date)

const formatElapsed = (date) => {
  const minutes = Math.max(0, Math.floor((Date.now() - date.getTime()) / 60000))
  if (minutes < 1) return '방금 전'
  if (minutes < 60) return `${minutes}분 전`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}시간 전`
  return `${Math.floor(hours / 24)}일 전`
}

export function createHomeDashboard(person, sensors, events) {
  const linkedSensors = sensors.filter(({ personId }) => personId === person.id)
  const linkedSensorIds = new Set(linkedSensors.map(({ id }) => id))
  const linkedEvents = events
    .filter((event) => event.personId === person.id || linkedSensorIds.has(event.sensorId))
    .sort((a, b) => (toDate(b.detectedAt)?.getTime() || 0) - (toDate(a.detectedAt)?.getTime() || 0))
  const latestEvent = linkedEvents[0]
  const latestDate = toDate(latestEvent?.detectedAt)
  const latestSensor = linkedSensors.find(({ id }) => id === latestEvent?.sensorId) || linkedSensors[0]
  const disconnectedSensor = linkedSensors.find(({ status }) => status === 'disconnected')
  const warningStatus = warningStatuses.has(latestEvent?.sensorStatus?.toUpperCase())
  const inactiveMinutes = latestDate ? Math.max(0, Math.floor((Date.now() - latestDate.getTime()) / 60000)) : 0
  const inactiveTooLong = Boolean(latestDate) && inactiveMinutes >= inactivityLimitMinutes
  const isWarning = Boolean(disconnectedSensor || warningStatus || inactiveTooLong)

  return {
    person,
    sensors: linkedSensors,
    events: linkedEvents,
    latestEvent,
    latestSensor,
    latestTime: latestDate ? formatTime(latestDate) : '--:--',
    latestElapsed: latestDate ? formatElapsed(latestDate) : '기록 없음',
    isWarning,
    warning: isWarning ? {
      sensor: disconnectedSensor || latestSensor,
      title: disconnectedSensor ? '센서 연결 상태 확인' : '장시간 움직임 없음',
      description: disconnectedSensor
        ? `${disconnectedSensor.name}의 연결이 끊겼어요.`
        : `평소보다 ${inactiveMinutes}분간 움직임이 없어요.`,
      connectionMessage: disconnectedSensor ? '센서 연결 상태를 확인해 주세요.' : '센서 연결 상태는 정상입니다.',
      evidence: latestEvent?.detectedValue || '최근 감지 기록 없음',
    } : null,
  }
}
