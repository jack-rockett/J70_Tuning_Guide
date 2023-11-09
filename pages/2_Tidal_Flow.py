import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import pytz
from datetime import date
import os
from streamlit_autorefresh import st_autorefresh

# Run the autorefresh about every 2000 milliseconds (2 seconds) and stop
# after it's been refreshed 100 times.
count = st_autorefresh(interval=60000, limit=100, key="fizzbuzzcounter")

def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')
    headers = [header.text for header in table.find_all('th')]
    # Rename duplicate headers
    seen = {}
    for i, header in enumerate(headers):
        if header not in seen:
            seen[header] = 1
        else:
            seen[header] += 1
            headers[i] = header + str(seen[header])

    rows = table.find_all('tr')
    data = []
    for row in rows[1:]:
        values = [value.text for value in row.find_all('td')]
        # If a row has fewer values than headers, fill the rest with None
        values += [None] * (len(headers) - len(values))
        data.append(values)

    df = pd.DataFrame(data, columns=headers)
    return df

url = "https://www.bbc.co.uk/weather/coast-and-sea/tide-tables/8/65"
df = scrape_data(url)

# Select the first two columns and rename them
df = df.iloc[:, :2]
df.columns = ['Time', 'Height']
# Convert the 'Height' column to float type
df['Height'] = df['Height'].astype(float)

# Add the 'Phase' column based on the conditions
df['Phase'] = df['Height'].apply(lambda x: 'High' if x >= 3 else 'Low' )

# Convert the 'Time' column to datetime format
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M').dt.time

# Display current time alongside data
now = datetime.now(pytz.timezone('GMT'))

# Format the time as a string
time_string = now.strftime("%H:%M")

# Calculate the absolute difference between the current time and each time in the 'Time' column in seconds
df['TimeDifferenceHRS'] = abs(df['Time'].apply(lambda x: (datetime.combine(date.today(), x) - datetime.combine(date.today(), now.time())).total_seconds()))

# Convert the 'Time' column back to 'HH:MM' format
df['Time'] = df['Time'].apply(lambda x: x.strftime('%H:%M'))

# Convert the 'TimeDifference' column to hours with one decimal place
df['TimeDifferenceHRS'] = (df['TimeDifferenceHRS'] / 3600).round(1)

# Filter the DataFrame to find the row with the 'High' phase and the smallest time difference
closest_high_tide = df[df['Phase'] == 'High'].nsmallest(1, 'TimeDifferenceHRS')


# Tidal Flow Chart
# Define the path to the directory where the images are stored
image_dir = 'Images'

# Calculate the rounded time difference
rounded_time_difference = round(float(closest_high_tide['TimeDifferenceHRS'].values[0]) * 2) / 2

# Construct the path to the image
image_path = os.path.join(image_dir, f'{rounded_time_difference}.jpg')


# Display final page

st.header('Tide Flow NOW')
st.caption('Page will auto-refresh each minute')
st.image(image_path)
st.header('Tide Times Portsmouth TODAY')
st.caption('Data Scraped live from BBC Weather presentation of UK Hydrographic Office Data')
st.caption('All Times quoted in GMT')
st.write(f"Current time (GMT): {time_string}")
st.caption('Closest HW:')
st.write(closest_high_tide)
st.caption('App developed by Powder Monkey Sailing Team')
st.write(f"Refreshed: {count} times")