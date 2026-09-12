import pandas as pd
import numpy as np
 
MAX_DIST = 450.0
SENSORS  = ["fridge"]
 
 
def minute_to_bin(m):
    return m // 10
 
 
def make_feature(hour, minute_bin, sensor_vals: dict):
    h_vec = [0] * 24
    h_vec[int(hour) % 24] = 1
 
    m_vec = [0] * 6
    m_vec[int(minute_bin) % 6] = 1
 
    s_vec = []
    for s in SENSORS:
        v = sensor_vals.get(s, MAX_DIST)
        if v is None or (isinstance(v, float) and np.isnan(v)) or v < 0:
            v = MAX_DIST
        s_vec.append(float(np.clip(v, 0, MAX_DIST)) / MAX_DIST)
 
    feature = h_vec + m_vec + s_vec
    assert len(feature) == 31, f"feature 크기 오류: {len(feature)}"
    return feature
 
 
def preprocess(df):
    """
    DataFrame → numpy array (shape: [n, 31])
    df 필수 컬럼: time (HH:MM:SS), fridge_dist (float, cm)
    """
    X = []
    for _, row in df.iterrows():
        h, m, _ = map(int, row["time"].split(":"))
        m_bin = minute_to_bin(m)
        sensor_vals = {"fridge": row.get("fridge_dist", MAX_DIST)}
        feature = make_feature(h, m_bin, sensor_vals)
        X.append(feature)
    return np.array(X, dtype=np.float32)
 
 
def preprocess_labels(df):
    label_map = {"정상": 0, "불면": 1, "반복행동": 2}
    labels = df["label"].map(label_map).values
    Y = np.zeros((len(labels), 3), dtype=np.float32)
    for i, l in enumerate(labels):
        Y[i, int(l)] = 1
    return Y
 
 
if __name__ == "__main__":
    # 정상 데이터 (fridge 컬럼만 사용)
    normal_df = pd.read_csv("data/normal_data.csv")
    X_normal = preprocess(normal_df)
    np.save("test/data/X_normal_1s.npy", X_normal)
    print(f"✅ 정상 데이터 전처리 완료: shape={X_normal.shape}")
 
    # 이상 데이터
    abnormal_df = pd.read_csv("data/abnormal_data.csv")
    X_abnormal = preprocess(abnormal_df)
    Y_abnormal = preprocess_labels(abnormal_df)
    np.save("test/data/X_abnormal_1s.npy", X_abnormal)
    np.save("test/data/Y_abnormal_1s.npy", Y_abnormal)
    print(f"✅ 이상 데이터 전처리 완료: X={X_abnormal.shape}, Y={Y_abnormal.shape}")
 
    print("\n라벨 분포:")
    for name, count in abnormal_df["label"].value_counts().items():
        print(f"  {name}: {count}개")
