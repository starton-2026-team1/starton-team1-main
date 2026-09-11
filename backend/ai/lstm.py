"""
Step 4: LSTM 구현 및 학습
논문 3.3 구현

- 오토인코더가 "이상 의심"으로 분류한 데이터를 입력받아
- 0(정상) / 1(불면) / 2(반복행동) 분류
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

SEQUENCE_LEN = 10  # 한 번에 볼 로그 수 (논문: "일정 개수 묶음")


def make_sequences(X, Y, seq_len=SEQUENCE_LEN):
    """
    연속 로그 seq_len개 묶어 시퀀스 데이터 생성
    LSTM 입력: (batch, seq_len, feature_dim)
    """
    Xs, Ys = [], []
    for i in range(len(X) - seq_len):
        Xs.append(X[i:i+seq_len])
        Ys.append(Y[i+seq_len-1])  # 마지막 로그의 라벨 사용
    return np.array(Xs), np.array(Ys)


def build_lstm(seq_len=SEQUENCE_LEN, feature_dim=36, n_classes=3):
    """LSTM 모델 (논문: 은닉층 32, 출력 3)"""
    model = keras.Sequential([
        layers.LSTM(32, input_shape=(seq_len, feature_dim)),
        layers.Dense(n_classes, activation="softmax")
    ], name="lstm_classifier")

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model


if __name__ == "__main__":
    # 이상 행동 데이터 로드
    X = np.load("data/X_abnormal.npy")
    Y = np.load("data/Y_abnormal.npy")

    print(f"전체 이상행동 데이터: X={X.shape}, Y={Y.shape}")

    # 시퀀스 생성
    X_seq, Y_seq = make_sequences(X, Y, SEQUENCE_LEN)
    print(f"시퀀스 데이터: X={X_seq.shape}, Y={Y_seq.shape}")

    # Train/Test 분할
    split = int(len(X_seq) * 0.8)
    X_train, X_test = X_seq[:split], X_seq[split:]
    Y_train, Y_test = Y_seq[:split], Y_seq[split:]

    # 모델 학습
    lstm = build_lstm()
    lstm.summary()

    history = lstm.fit(
        X_train, Y_train,
        epochs=50,
        batch_size=32,
        validation_split=0.1,
        verbose=1
    )

    # 평가
    loss, acc = lstm.evaluate(X_test, Y_test, verbose=0)
    print(f"\nLSTM 테스트 정확도: {acc*100:.2f}%")

    # 모델 저장
    lstm.save("model/lstm_classifier.keras")
    print("LSTM 저장 완료: lstm_classifier.keras")

    # 예측 결과 샘플 출력
    Y_pred = lstm.predict(X_test[:10], verbose=0)
    label_names = {0: "정상", 1: "불면", 2: "반복행동"}
    print("\n📋 예측 결과 샘플 (10개):")
    for i in range(10):
        pred = np.argmax(Y_pred[i])
        true = np.argmax(Y_test[i])
        match = "✅" if pred == true else "❌"
        print(f"  {match} 실제: {label_names[true]:<5} | 예측: {label_names[pred]}") # type: ignore