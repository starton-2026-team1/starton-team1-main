import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
 
THRESHOLD = 0.03  # 이상치 기준 3%
 
 
def build_autoencoder(input_dim=35, hidden_dim=16):
    """단층 오토인코더"""
    inputs = keras.Input(shape=(input_dim,))
    # Encoder
    encoded = layers.Dense(hidden_dim, activation="relu")(inputs)
    # Decoder
    decoded = layers.Dense(input_dim, activation="sigmoid")(encoded)
 
    model = keras.Model(inputs, decoded, name="autoencoder")
    model.compile(
        optimizer="adadelta",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )
    return model
 
 
def compute_anomaly_score(model, X):
    """
    이상치 점수 계산 (MSE 기반)
    반환값: 0~100 스케일 (논문 그림 10 기준)
    """
    X_pred = model.predict(X, verbose=0)
    mse = np.mean(np.power(X - X_pred, 2), axis=1)
    # 0~100 스케일로 정규화
    score = (mse / mse.max()) * 100
    return score
 
 
if __name__ == "__main__":
    # 데이터 로드
    X_normal = np.load("data/X_normal.npy")
    X_abnormal = np.load("data/X_abnormal.npy")
 
    # Train/Test 분할 (약 80% 학습용)
    split = int(len(X_normal) * 0.8)
    X_train = X_normal[:split]
    X_test_normal = X_normal[split:]
 
    print(f"학습 데이터: {X_train.shape}")
    print(f"테스트 정상: {X_test_normal.shape}")
    print(f"테스트 이상: {X_abnormal.shape}")
 
    # 모델 빌드 및 학습
    ae = build_autoencoder(input_dim=35, hidden_dim=16)
    ae.summary()
 
    history = ae.fit(
        X_train, X_train,          # 입력 = 출력 (자기지도학습)
        epochs=50,
        batch_size=32,
        validation_split=0.1,
        verbose=1
    )
 
    # 모델 저장
    ae.save("autoencoder.keras")
    print("\n오토인코더 저장 완료: autoencoder.keras")
 
    # ── 이상치 점수 계산 ──────────────────────────────
    score_normal = compute_anomaly_score(ae, X_test_normal)
    score_abnormal = compute_anomaly_score(ae, X_abnormal)
 
    print(f"\n이상치 점수 (정상 데이터): 평균={score_normal.mean():.2f}, 최대={score_normal.max():.2f}")
    print(f"이상치 점수 (이상 데이터): 평균={score_abnormal.mean():.2f}, 최대={score_abnormal.max():.2f}")
 
    # 임계값 기준 분류 정확도
    normal_correct = np.sum(score_normal < THRESHOLD * 100) / len(score_normal)
    abnormal_detected = np.sum(score_abnormal >= THRESHOLD * 100) / len(score_abnormal)
    print(f"\n정상 데이터 정상 판별율: {normal_correct*100:.2f}%")
    print(f"이상 데이터 탐지율: {abnormal_detected*100:.2f}%")
 
    # ── 시각화 ──────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
 
    ax1 = axes[0]
    ax1.plot(history.history["accuracy"], label="Train Accuracy")
    ax1.plot(history.history["val_accuracy"], label="Val Accuracy")
    ax1.set_title("Autoencoder Accuracy")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Accuracy")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
 
    ax2 = axes[1]
    ax2.plot(score_abnormal[:200], color="blue", alpha=0.7, label="Anomaly Score")
    ax2.axhline(y=THRESHOLD * 100, color="red", linestyle="--", label=f"Threshold ({THRESHOLD*100}%)")
    ax2.set_title("Anomaly Score on Abnormal Data")
    ax2.set_xlabel("Logs")
    ax2.set_ylabel("Score (0~100)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
 
    plt.tight_layout()
    plt.savefig("autoencoder_result.png", dpi=150)
    print("\n그래프 저장: autoencoder_result.png")
 