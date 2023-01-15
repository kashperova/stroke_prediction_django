import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from stroke.base.views import data_processing
pd.options.mode.chained_assignment = None
import xgboost as xgb


final_dataset = data_processing('train.csv')
sc = StandardScaler()
numerical_features_list = ['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi']
final_dataset[numerical_features_list] = sc.fit_transform(final_dataset[numerical_features_list])

X = final_dataset.drop(['stroke'], axis=1)
y = final_dataset['stroke']

model = xgb.XGBClassifier(learning_rate=0.1, max_depth=2, max_leaves=10, n_estimators=100, seed=42)
model.fit(X, y)
pickle.dump(model, open("model.sav", "wb"))
pickle.dump(sc, open("scaler.sav", "wb"))



