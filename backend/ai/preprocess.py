"""
Step 2: 데이터 전처리
논문 3.2 구현

입력 feature (총 36차원):
 - 시(hour): 24개 (one-hot)
 - 분(minute): 6개 → 0~9, 10~19, ..., 50~59 (one-hot)
 - 센서번호: 5개 (one-hot)
 - 발생횟수: 1개 (정규화 0~1)
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pickle
    
MINUTE_BINS = [0, 10, 20, 30, 40, 50]  # 6개 구간


def minute_to_bin(m):
    """분 → 구간 인덱스 (0~5)"""
    return m // 10


def preprocess(df):
    """
    DataFrame → numpy array (shape: [n, 36])
    """
    X = []
    for _, row in df.iterrows():
        h, m, s = map(int, row["time"].split(":"))
        sensor = int(row["sensor"])
        count = int(row["count"])
        m_bin = minute_to_bin(m)

        # One-hot: 시 (24차원)
        hour_vec = [0] * 24
        hour_vec[h] = 1

        # One-hot: 분 (6차원)
        min_vec = [0] * 6
        min_vec[m_bin] = 1

        # One-hot: 센서 (5차원)
        sensor_vec = [0] * 5
        sensor_vec[sensor - 1] = 1

        # 발생횟수: 정규화 (1차원) — 최대값 414 가정 (논문 기준)
        count_norm = count / 414.0

        feature = hour_vec + min_vec + sensor_vec + [count_norm]
        assert len(feature) == 36, f"feature 크기 오류: {len(feature)}"
        X.append(feature)

    return np.array(X, dtype=np.float32)


def preprocess_labels(df):
    """라벨 → one-hot (정상:0, 불면:1, 반복:2)"""
    labels = df["label"].values
    n = len(labels)
    Y = np.zeros((n, 3), dtype=np.float32)
    for i, l in enumerate(labels):
        Y[i, int(l)] = 1
    return Y


if __name__ == "__main__":
    # 정상 데이터 전처리
    normal_df = pd.read_csv("data/normal_data.csv")
    X_normal = preprocess(normal_df)
    np.save("X_normal.npy", X_normal)
    print(f"✅ 정상 데이터 전처리 완료: shape={X_normal.shape}")
    print("  앞 3행 예시:")
    print(X_normal[:3])

    # 이상 행동 데이터 전처리
    abnormal_df = pd.read_csv("data/abnormal_data.csv")
    X_abnormal = preprocess(abnormal_df)
    Y_abnormal = preprocess_labels(abnormal_df)
    np.save("data/X_abnormal.npy", X_abnormal)
    np.save("data/Y_abnormal.npy", Y_abnormal)
    print(f"\n이상 행동 데이터 전처리 완료: X={X_abnormal.shape}, Y={Y_abnormal.shape}")

    print("\n📊 라벨 분포:")
    labels = abnormal_df["label"].value_counts().sort_index()
    label_names = {0: "정상", 1: "불면", 2: "반복행동"}
    for k, v in labels.items():
        print(f"  {label_names[k]}: {v}개") # type: ignore