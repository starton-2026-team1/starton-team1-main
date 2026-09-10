from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SensorEventCreate(BaseModel):
    person_id: int
    sensor_id: int
    detected_at: datetime
    detected_value: str = Field(min_length=1, max_length=255)
    sensor_status: str = Field(max_length=30)


class SensorEventResponse(SensorEventCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    received_at: datetime
