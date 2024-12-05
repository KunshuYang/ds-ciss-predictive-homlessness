import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

# 读取数据

data = pd.read_csv("Merged_Data.csv")

# 过滤只包含 2010-2023 年的数据
data = data[(data['Year'] >= 2010) & (data['Year'] <= 2023)]

# 检查数据，去除缺失值
print(data.info())
data = data.dropna()

# 对非数值型特征进行编码
label_encoders = {}
for column in data.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

# 定义不同的目标变量列表
targets = ['Overall Homeless', 'Overall Homeless Individuals', 'Overall Homeless People in Families', 'Unsheltered Homeless', 'Sheltered Total Homeless']

# 创建空的结果列表用于存储每个目标变量的评估结果
results = []

# 对每个目标变量进行预测和评估
for target in targets:
    # 特征和目标变量选择
    X = data.drop(columns=targets)
    y = data[target]
    
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 创建随机森林回归模型
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    # 训练模型
    model.fit(X_train, y_train)
    
    # 进行预测
    y_pred = model.predict(X_test)
    
    # 评估模型性能
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    results.append((target, mse, r2))

# 打印所有目标变量的评估结果
for target, mse, r2 in results:
    print(f"{target} - Mean Squared Error: {mse:.2e}, R-squared: {r2:.4f}")
