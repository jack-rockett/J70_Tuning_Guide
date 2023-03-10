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
                                        'TENSION UPPERS': str, 'TRAVELLER_POSITION': str, 'WIND_SPEED': int, 'BACKSTAY': str}
                            )

JIB_df = pd.read_excel(excel_file,
                            sheet_name=sheet_name_2,
                            usecols='A:G',
                            header=0,
                            converters={'KEY': str, 'INHAUL': str, 'HALYARD': str, 'JIB_CUT': str, 'WIND_SPEED': int, 'CAR_POSITION': str}
                            )
wind_speed_filter = st.slider("Wind Speed Filter (Kts)", 0, 20, 10)
    # st.number_input("Wind Speed Filter", min_value=0, max_value=20, value=0)
    # st.slider("Wind Speed Filter", 0, 20, (0, 20))
jib_cut_filter = st.selectbox("Jib Cut Selection", ["J6","J2+"])


filtered_JIB_df = JIB_df[(JIB_df['WIND_SPEED'] == wind_speed_filter) & (JIB_df['JIB_CUT'] == jib_cut_filter)]
filtered_RIG_df = RIG_df[(RIG_df['WIND_SPEED'] == wind_speed_filter)]

# --- STREAMLIT SELECTION

st.metric(label='Uppers Turns', value=filtered_RIG_df['UPPERS_TURNS'].max())
st.metric(label='Lowers Turns', value=filtered_RIG_df['LOWERS_TURNS'].max())
st.metric(label='Car Position', value=filtered_JIB_df['CAR_POSITION'].max())
st.metric(label='Jib Inhaul', value=filtered_JIB_df['INHAUL'].max())
st.metric(label='Jib Halyard', value=filtered_JIB_df['HALYARD'].max())

# DATABASE DF Blocks
# st.header("JIB Tuning Database")
# st.write(filtered_JIB_df.style.hide_index())
#
# st.header("RIG Tuning Database")
# st.write(filtered_RIG_df.style.hide_index())

# stock metric example:
# st.metric(label="Temperature", value="70 ??F", delta="1.2 ??F")

# ADDING DOWNLOAD BUTTON FOR FULL GUIDE CSV
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(RIG_df)
csv1 = convert_df(JIB_df)


st.subheader("Download options")
st.download_button(
    label="Rig tune data as CSV",
    data=csv,
    file_name='tuning_guide_j70_rig_df.csv',
    mime='text/csv',
)
st.download_button(
    label="Jib tune data as CSV",
    data=csv1,
    file_name='tuning_guide_j70_jib_df.csv',
    mime='text/csv',
)
