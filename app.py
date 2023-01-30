import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='J70 Interactive Tuning Guide')
st.header('J70 Tuning Guide')
st.subheader('Developed by GBR937 Powder Monkey Sailing Team')

### --- LOAD DATAFRAME
excel_file = 'Tuning Database.xlsx'
sheet_name_1 = 'Rig Tuning Database'
sheet_name_2 = 'JIB Tuning Database'

RIG_df = pd.read_excel(excel_file,
                            sheet_name=sheet_name_1,
                            usecols='A:I',
                            header=0,
                            converters={'KEY': str, 'UPPERS_TURNS': str, 'LOWERS_TURNS': str, 'TENSION_LOWERS': str,
                                        'TENSION UPPERS': str, 'TRAVELLER_POSITION': str, 'BACKSTAY': str}
                            )

JIB_df = pd.read_excel(excel_file,
                            sheet_name=sheet_name_2,
                            usecols='A:G',
                            header=0,
                            converters={'KEY': str, 'INHAUL': str, 'HALYARD': str, 'JIB_CUT': str, 'CAR_POSITION': str}
                            )
wind_speed_filter = st.slider("Wind Speed Filter", 0, 20, (0, 20))
    # st.number_input("Wind Speed Filter", min_value=0, max_value=20, value=0)
    # st.slider("Wind Speed Filter", 0, 20, (0, 20))
jib_cut_filter = st.selectbox("Jib Cut Selection", ["J2+", "J6"])

# --- STREAMLIT SELECTION

filtered_JIB_df = JIB_df[(JIB_df['WIND_SPEED'] >= wind_speed_filter[0]) & (JIB_df['WIND_SPEED'] <= wind_speed_filter[1]) & (JIB_df['JIB_CUT'] == jib_cut_filter)]
filtered_RIG_df = RIG_df[(RIG_df['WIND_SPEED'] >= wind_speed_filter[0]) & (RIG_df['WIND_SPEED'] <= wind_speed_filter[1])]

st.header("JIB Tuning Database")
st.write(filtered_JIB_df, index=False)

st.header("RIG Tuning Database")
st.dataframe(filtered_RIG_df, index=False)
