import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor

excel_file = 'Tuning Database.xlsx'
sheet_name_3 = 'Rig_by_weight'

RIG_ML_df = pd.read_excel(excel_file,
                            sheet_name=sheet_name_3,
                            usecols='A:I',
                            header=0,
                            converters={'KEY': str, 'UPPERS_TURNS': str, 'LOWERS_TURNS': str, 'TENSION_LOWERS': str,
                                        'TENSION UPPERS': str, 'TRAVELLER_POSITION': str, 'WIND_SPEED': int, 'BACKSTAY': str}
                            )

data = RIG_ML_df
X = data.iloc[:, [1, 8]].values
Y = data.iloc[:, [2, 3]]

scaler = StandardScaler()
X = scaler.fit_transform(X)

model = KNeighborsRegressor()
model.fit(X, Y)

st.title("Nearest Neighbour Model")
new_value_for_column2 = st.slider("Windspeed (Kts)", 0, 20, 12)
new_value_for_column9 = st.slider("Crew Weight (Kg)", 360, 500, 430)

prediction = model.predict(np.array([[new_value_for_column2, new_value_for_column9]]))

# st.write("Predicted values for columns 3 and 4:", prediction[0][0], prediction[0][1])

# uppers_turns = prediction[0][0]
# lowers_turns = prediction[0][1]
#
# st.metric(label='Uppers Turns', value= round(np.ceil(uppers_turns * 2) / 2, 1))
# st.metric(label='Lowers Turns', value= round(np.ceil(lowers_turns * 2) / 2, 1))

st.metric(label='Uppers Turns', value= round((np.ceil(prediction[0][0] * 2)/2),1))
st.metric(label='Lowers Turns', value= round((np.ceil(prediction[0][1] * 2)/2),1))