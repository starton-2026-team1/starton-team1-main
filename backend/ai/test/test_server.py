"""
server.py: FastAPI 추론 서버 (맥북에서 실행)
실행: uvicorn server:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI
from pydantic import BaseModel
from collections import deque
import numpy as np
from tensorflow import keras

# ── 모델 로드 ─────────────────────────────────────────
print("모델 로딩 중...")
ae        = keras.models.load_model("model/autoencoder_1s.keras")
lstm      = keras.models.load_model("model/lstm_1s.keras")
THRESHOLD = float(np.load("model/threshold_1s.npy")[0])
MSE_MAX   = float(np.load("model/mse_max_1s.npy")[0])
print(f"✅ 모델 로드 완료 | 임계값: {THRESHOLD:.2f}")

# ── 설정 ──────────────────────────────────────────────
SEQ_LEN     = 10
INPUT_DIM   = 31
MAX_DIST    = 450.0
LABEL_NAMES = {0: "정상", 1: "불면", 2: "반복행동"}

seq_buffer = deque(maxlen=SEQ_LEN)

app = FastAPI()


# ── 요청 스키마 ───────────────────────────────────────
class SensorData(BaseModel):
    hour:     int
    minute:   int
    distance: float


# ── 전처리 ────────────────────────────────────────────
def make_feature(hour: int, minute: int, fridge_dist: float) -> np.ndarray:
    h_vec = [0] * 24; h_vec[hour % 24] = 1
    m_vec = [0] * 6;  m_vec[(minute // 10) % 6] = 1
    v = float(np.clip(fridge_dist, 0, MAX_DIST)) / MAX_DIST
    return np.array(h_vec + m_vec + [v], dtype=np.float32)


def anomaly_score(feature: np.ndarray) -> float:
    x = feature.reshape(1, -1)
    x_pred = ae.predict(x, verbose=0)
    mse = float(np.mean(np.power(x - x_pred, 2)))
    return (mse / MSE_MAX) * 100


def classify(seq_buffer: deque) -> tuple[str, float]:
    seq  = np.array(list(seq_buffer), dtype=np.float32).reshape(1, SEQ_LEN, INPUT_DIM)
    pred = lstm.predict(seq, verbose=0)[0]
    label = int(np.argmax(pred))
    return LABEL_NAMES[label], float(pred[label]) * 100


# ── 엔드포인트 ────────────────────────────────────────
@app.post("/api/sensor")
async def infer(data: SensorData):
    feature = make_feature(data.hour, data.minute, data.distance)
    seq_buffer.append(feature)

    score = anomaly_score(feature)
    is_anomaly = score >= THRESHOLD

    if is_anomaly and len(seq_buffer) == SEQ_LEN:
        label, conf = classify(seq_buffer)
    else:
        label = "정상"
        conf  = 0.0

    print(f"[{data.hour:02d}:{data.minute:02d}] dist={data.distance}cm | score={min(score,999.9):.1f} | {label} ({conf:.1f}%)")

    return {
        "label":      label,
        "score":      round(min(score, 999.9), 1),
        "confidence": round(conf, 1),
        "is_anomaly": is_anomaly
    }


@app.get("/health")
async def health():
    return {"status": "ok", "threshold": THRESHOLD}