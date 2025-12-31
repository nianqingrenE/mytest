# 学生成绩预测示例代码
import joblib
import pandas as pd
import numpy as np

# 加载模型
model = joblib.load('D:\\streamlit_env\\student_performance_model.pkl')

# 创建测试数据 (示例)
# 格式: [性别, 专业, 特征1, 特征2, 特征3, 特征4]
test_data = pd.DataFrame([{
    '性别': '男',
    '专业': '人工智能',
    '特征1': 20.5,
    '特征2': 0.85,
    '特征3': 85.0,
    '特征4': 0.9
}])

# 预测
prediction = model.predict(test_data)
print(f'预测成绩: {prediction[0]:.2f}')

# 批量预测示例
batch_data = pd.DataFrame([
    {'性别': '女', '专业': '大数据管理', '特征1': 18.3, '特征2': 0.92, '特征3': 90.5, '特征4': 0.85},
    {'性别': '男', '专业': '电子商务', '特征1': 22.1, '特征2': 0.78, '特征3': 75.2, '特征4': 0.91},
    {'性别': '女', '专业': '工商管理', '特征1': 15.8, '特征2': 0.88, '特征3': 82.3, '特征4': 0.79}
])

predictions = model.predict(batch_data)
for i, pred in enumerate(predictions):
    print(f'学生 {i+1} 预测成绩: {pred:.2f}')
