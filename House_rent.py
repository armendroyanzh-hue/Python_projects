
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LinearRegression

SEED     = 509
TEST_SIZE = 0.2

df = pd.read_csv('House_Rent_Dataset.csv')

# Encoding
# 1. Posted On -> cyclical month encoding
df['Posted On']  = pd.to_datetime(df['Posted On'])
df['post_month'] = df['Posted On'].dt.month
df['month_sin']  = np.sin(2 * np.pi * df['post_month'] / 12)
df['month_cos']  = np.cos(2 * np.pi * df['post_month'] / 12)
df.drop(columns=['Posted On', 'post_month'], inplace=True)

# 2. BHK -> keep as-is

# 3. Rent -> log transformation
df['Rent'] = np.log(df['Rent'])

# 4. Size -> log transformation
df['Size'] = np.log(df['Size'])

# 5. Floor -> get floor ratio
df['floor_number'] = df['Floor'].str.extract(r'^(Upper Basement|Lower Basement|Ground|\d+)')[0]
floor_map = {'Lower Basement': -2, 'Upper Basement': -1, 'Ground': '0'}
df['floor_number'] = df['floor_number'].replace(floor_map).astype(float)
df['total_floors'] = df['Floor'].str.extract(r'out of (\d+)')[0].astype(float)
df['total_floors'] = df['total_floors'].fillna(df['total_floors'].median())
df['floor_ratio']  = df['floor_number'] / df['total_floors'].replace(0, np.nan)
df['floor_ratio']  = df['floor_ratio'].fillna(df['floor_ratio'].median())
df.drop(columns=['Floor', 'floor_number', 'total_floors'], inplace=True)

# 6. Area Type -> merge rare category and one-hot encode
df['Area Type'] = df['Area Type'].replace('Built Area', 'Carpet Area')
df = pd.get_dummies(df, columns=['Area Type'], drop_first=True, dtype=int)

# 7. Area Locality -> smoothed target encoding, since many localities appear only once or twice which can be a problem for regular target encoding
global_mean      = df['Rent'].mean()
stats            = df.groupby('Area Locality')['Rent'].agg(['mean', 'count'])
k                = 10
stats['smoothed']     = (stats['count'] * stats['mean'] + k * global_mean) / (stats['count'] + k)
stats['smoothed_log'] = np.log(stats['smoothed'])
df['Area Locality']   = df['Area Locality'].map(stats['smoothed_log'])

# 8. City -> target encoding with log
mean_rent  = df.groupby('City')['Rent'].mean()
df['City'] = df['City'].map(np.log(mean_rent))

# 9. Furnishing Status and Tenant Preferred -> one-hot encode
df = pd.get_dummies(df, columns=['Furnishing Status', 'Tenant Preferred'], drop_first=True, dtype=int)

# 10. Bathroom -> keep as-is

# 11. Point of Contact -> drop 
df.drop(columns=['Point of Contact'], inplace=True)


X = df.drop(columns=['Rent'])   # input features
y = df['Rent']                  # target (log transformed)

# Train / test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=SEED)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)


# K-Fold Cross Validation
kf     = KFold(n_splits=5, shuffle=True, random_state=SEED)
scores = cross_val_score(model, X, y, cv=kf, scoring='r2')
print('R2 per fold:  ', scores.round(3))

# Final evaluation on holdout test set
final_score = model.score(X_test, y_test)
print('Final R2 on test set:', round(final_score, 3))

# Predict
y_pred        = model.predict(X_test)
y_pred_actual = np.exp(y_pred)
y_test_actual = np.exp(y_test)



