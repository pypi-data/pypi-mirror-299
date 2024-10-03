import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from app.table_data_process_lib import mlp_classifier, model_evaluation

df = pd.read_csv('ecg_data.csv', delimiter=';')
X = df.drop(['Healthy Status', 'subject_id', 'study_id', 'cart_id', 'eeg_time ', 'eeg_date '], axis=1)
y = df['Healthy Status']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


model = mlp_classifier(
    X_train_scaled,
    y_train,
    hidden_layer_sizes=(100, 50),  # Пример: два скрытых слоя с 100 и 50 нейронов
    activation='relu',
    max_iter=500
)

mlp_report = model_evaluation(model, X_test_scaled, y_test, regression_task=False)
print(mlp_report)
