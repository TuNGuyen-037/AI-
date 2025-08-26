from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

# Tạo ứng dụng Flask
app = Flask(__name__)

# Load mô hình và scaler đã lưu
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

# Đường dẫn chính (Home Page)
@app.route('/')
def home():
    return render_template('D:/AI-/Bài tập lớn/stress_prediction_app/templates/index.htm')  # Hiển thị giao diện người dùng

# API xử lý dự đoán
@app.route('/predict', methods=['POST'])
def predict():
    # Lấy dữ liệu từ request JSON
    data = request.get_json()
    features = np.array(data['features']).reshape(1, -1)
    
    # Chuẩn hóa dữ liệu
    features = scaler.transform(features)
    
    # Dự đoán
    prediction = model.predict(features)
    stress_level = 'High Stress' if prediction[0] == 1 else 'Low Stress'
    
    return jsonify({'stress_level': stress_level})

if __name__ == "__main__":
    app.run(debug=True)
