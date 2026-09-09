import numpy as np
from tensorflow.keras.models import load_model


# 저장된 모델 파일 불러오기
print("저장된 모델을 불러오는 중...")
autoencoder = load_model("autoencoder_model.keras")
lstm_model = load_model("lstm_model.keras")
print("모델 로드 완료!\n")


# 2. 센서 입력 벡터 생성 헬퍼 함수
def make_sensor_input(hour, minute_group, sensor_id, count_norm):
    """
    hour: 0~23 (시)
    minute_group: 0~5 (0: 0~9분, 1: 10~19분, ..., 5: 50~59분)
    sensor_id: 0~4 (0: 문, 1: 창문, 2: 냉장고, 3: 서랍, 4: 보조침대)
    count_norm: 0.0~1.0 (정규화된 동작 횟수)
    """
    vec = np.zeros(36)
    vec[hour] = 1.0
    vec[24 + minute_group] = 1.0
    vec[30 + sensor_id] = 1.0
    vec[35] = count_norm
    return vec.reshape(1, 36)

# 이상 행동 감지 추론
def detect_abnormal_behavior(data_sample: np.ndarray) -> str:
    timesteps = 1
    input_dim = 36
    reconstructed = autoencoder.predict(data_sample, verbose=0)

    loss = np.mean(
        - (
            data_sample * np.log(reconstructed + 1e-7)
            + (1 - data_sample) * np.log(1 - reconstructed + 1e-7)
        )
    )

    threshold = 0.03  # 논문 기준 임계값 3%[cite: 1]

    if loss <= threshold:
        return f"[정상] 정상 행동입니다. (Loss: {loss:.4f})"
    else:
        lstm_input = np.reshape(data_sample, (1, timesteps, input_dim))
        prediction = lstm_model.predict(lstm_input, verbose=0)
        class_idx = int(np.argmax(prediction))

        labels = {0: "정상", 1: "불면", 2: "반복 행동"}
        detected_label = labels.get(class_idx, "알 수 없음")
        return f"[이상 감지] {detected_label} 패턴이 의심됩니다. (Loss: {loss:.4f})"


# 테스트 실행
if __name__ == "__main__":
    # Case 1: 오전 8시(8), 10~19분(1), 냉장고 센서(2) 작동 -> 정상 테스트
    sample_normal = make_sensor_input(hour=8, minute_group=1, sensor_id=2, count_norm=0.1)
    print("1. 정상 상황 테스트:")
    print(detect_abnormal_behavior(sample_normal))

    print("-" * 50)

    # Case 2: 새벽 3시(3), 40~49분(4), 문 센서(0) 잦은 작동 -> 이상 패턴 테스트
    sample_abnormal = make_sensor_input(hour=3, minute_group=4, sensor_id=0, count_norm=0.8)
    print("2. 이상 상황 테스트:")
    print(detect_abnormal_behavior(sample_abnormal))