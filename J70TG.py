import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# load the dataset
excel_file = 'Tuning Database.xlsx'
sheet_name_1 = 'Rig Tuning Database'
sheet_name_2 = 'JIB Tuning Database'
sheet_name_3 = 'Rig_by_weight'

RIG_df = pd.read_excel(excel_file,
                            sheet_name=sheet_name_1,
                            usecols='A:I',
                            header=0,
                            converters={'KEY': str, 'UPPERS_TURNS': str, 'LOWERS_TURNS': str, 'TENSION_LOWERS': str,
                                        'TENSION UPPERS': str, 'TRAVELLER_POSITION': str, 'WIND_SPEED': int, 'BACKSTAY': str}
                            )

RIG_ML_df = pd.read_excel(excel_file,
                            sheet_name=sheet_name_3,
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

data = RIG_ML_df
# split the data into dependent (y) and independent (X) variables
X = data.iloc[:, [1, 8]].values
y = data.iloc[:, [0, 2, 3, 4, 5, 6, 7]]

# train a linear regression model
model = LinearRegression()
model.fit(X, y)

# predict values for columns 1, 3, 4, 5, 6, 7, and 8 based on new values for columns 2 and 9
new_value_for_column2 = 5
new_value_for_column9 = 10
prediction = model.predict(np.array([[new_value_for_column2, new_value_for_column9]]))

# print the predicted values for columns 1, 3, 4, 5, 6, 7, and 8
print('Predicted values for columns 1, 3, 4, 5, 6, 7, and 8:', prediction[0][0], prediction[0][1], prediction[0][2], prediction[0][3], prediction[0][4], prediction[0][5], prediction[0][6])