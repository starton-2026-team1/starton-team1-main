import { apiRequest } from './client'

const statusToView = {
  CONNECTED: 'normal',
  CONNECTING: 'connecting',
  UNSTABLE: 'unstable',
  DISCONNECTED: 'disconnected',
  PAUSED: 'disconnected',
}

const toSensor = (sensor) => ({
  id: sensor.id,
  serialNumber: sensor.device_id,
  personId: sensor.person_id ?? null,
  name: sensor.name,
  type: sensor.type || 'ultrasonic',
  targetObject: sensor.target_object || '-',
  location: sensor.location,
  status: statusToView[sensor.status] || 'disconnected',
})

export async function getSensors() {
  const sensors = await apiRequest('/sensors')
  return sensors.map(toSensor)
}

export async function createSensor(sensor) {
  const payload = {
    name: sensor.name,
    location: sensor.location,
    device_id: sensor.serialNumber,
    status: 'CONNECTED',
    person_id: sensor.personId,
    target_object: sensor.targetObject,
  }
  const created = await apiRequest('/sensors', {
    method: 'POST',
    body: JSON.stringify(payload),
  })

  // person_id와 target_object가 백엔드에 반영되기 전에도 현재 등록 화면은 유지한다.
  return toSensor({ ...payload, ...created })
}

export async function deleteSensor(sensorId) {
  await apiRequest(`/sensors/${sensorId}`, { method: 'DELETE' })
}
