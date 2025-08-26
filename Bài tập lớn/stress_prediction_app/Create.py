import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import pickle

# Đọc dữ liệu
data = pd.read_csv(r'D:\Project_2\stress_detection.csv')

# Tiền xử lý dữ liệu
columns_to_process = [
    'Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness',
    'Neuroticism', 'sleep_time', 'wake_time', 'sleep_duration',
    'PSQI_score', 'call_duration', 'num_calls', 'num_sms',
    'screen_on_time', 'skin_conductance', 'accelerometer',
    'mobility_radius', 'mobility_distance'
]

# Xử lý outliers
def handle_outliers_iqr(data, columns):
    for col in columns:
        if data[col].dtype in ['int64', 'float64']:
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            data[col] = np.clip(data[col], lower_bound, upper_bound)
    return data

data_cleaned = handle_outliers_iqr(data, columns_to_process)

# Chuyển đổi cột PSS_score thành nhãn nhị phân
data_cleaned['PSS_score_category'] = pd.cut(
    data['PSS_score'], bins=[0, 13, 40], labels=[0, 1]
).astype(int)

# Loại bỏ cột không cần thiết
data_cleaned.drop(columns=['PSS_score'], inplace=True)

# Tách feature và target
X = data_cleaned[columns_to_process].values
y = data_cleaned['PSS_score_category'].values

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Chia tập dữ liệu
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Huấn luyện mô hình
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Đánh giá mô hình
y_pred = model.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Lưu mô hình vào file model.pkl
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)
    
# Lưu scaler (nếu cần chuẩn hóa dữ liệu trong tương lai)
with open('scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)

print("Mô hình đã được lưu thành công vào file model.pkl!")

import joblib

# Lưu mô hình vào file
joblib.dump(model, 'model.pkl')
# import pickle
# from sklearn.linear_model import LogisticRegression
# from sklearn.preprocessing import StandardScaler

# # Tạo dữ liệu mẫu và huấn luyện
# X_train = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# y_train = [0, 1, 0]

# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)

# model = LogisticRegression()
# model.fit(X_train_scaled, y_train)

# # Lưu mô hình và scaler
# with open('model.pkl', 'wb') as f:
#     pickle.dump(model, f)

# with open('scaler.pkl', 'wb') as f:
#     pickle.dump(scaler, f)
