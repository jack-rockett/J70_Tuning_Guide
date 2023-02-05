import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# load the dataset
data = pd.read_csv('data.csv')
excel_file = 'Tuning Database.xlsx'
sheet_name_1 = 'Rig Tuning Database'
sheet_name_2 = 'JIB Tuning Database'

RIG_df = pd.read_excel(excel_file,
                            sheet_name=sheet_name_1,
                            usecols='A:I',
                            header=0,
                            converters={'KEY': str, 'UPPERS_TURNS': str, 'LOWERS_TURNS': str, 'TENSION_LOWERS': str,
                                        'TENSION UPPERS': str, 'TRAVELLER_POSITION': str, 'WIND_SPEED': int, 'BACKSTAY': str}
                            )

JIB_df = pd.read_excel(excel_file,
                            sheet_name=sheet_name_2,
                            usecols='A:G',
                            header=0,
                            converters={'KEY': str, 'INHAUL': str, 'HALYARD': str, 'JIB_CUT': str, 'WIND_SPEED': int, 'CAR_POSITION': str}
                            )
# split the data into dependent (y) and independent (X) variables
X = data.iloc[:, 3].values.reshape(-1, 1)
y = data.iloc[:, :3].values

# train a linear regression model
model = LinearRegression()
model.fit(X, y)

# predict values for column1, column2, and column3 based on a new value for column4
new_value_for_column4 = 10
prediction = model.predict(np.array(new_value_for_column4).reshape(-1, 1))

# print the predicted values for column1, column2, and column3
print('Predicted values for column1, column2, and column3:', prediction[0][0], prediction[0][1], prediction[0][2])
