import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.dates import DateFormatter
from matplotlib.ticker import FixedLocator
import matplotlib.dates as mdates
import datetime
from scipy import stats
import subprocess as sp
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
import netCDF4
import requests
from bs4 import BeautifulSoup # Import BeautifulSoup
import statsmodels.api as sm
import os.path
import matplotlib.dates as mdates

# Set the base URL for downloading files
base_url = "https://www.ncei.noaa.gov/data/total-solar-irradiance/access/monthly/"


# Ask the user for the beginning and end years and months
begin_year_month = input("Enter the beginning year-month (e.g. 1978-11): ")
end_year_month = input("Enter the end year-month (e.g. 2023-03): ")

begin_year, begin_month = begin_year_month.split("-")
end_year, end_month = end_year_month.split("-")
begin_year=int(begin_year)
end_year=int(end_year)
begin_month=int(begin_month)
end_month=int(end_month)
# Create empty lists to store the data for plotting
dates = []
tsi_values = []

# Loop through each year in the specified range to download files
for year in range(begin_year,end_year + 1):
    # Construct the partial filename based on the year
    if year == 2024:
        partial_filename = f"tsi_v02r01-preliminary_monthly_s{year}"
    else:
        partial_filename = f"tsi_v02r01_monthly_s{year}01"

    # Get the list of available files from the website
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    available_files = [link.get('href') for link in soup.find_all('a')]

    # Find all matching files from the list of available files
    matching_files = []
    for file in available_files:
        if partial_filename in file:
            matching_files.append(file.strip())

    # Check if any matching files were found
    if len(matching_files) == 0:
        print(f"No matching files found for {partial_filename}")
        continue

    # Loop through each matching file to download and process it
    for matching_file in matching_files:
        # Use the matching file as the filename
        filename = matching_file

        # Check if the file already exists on disk
        if not os.path.exists(filename):
            # Construct the full URL for downloading the file
            url = base_url + filename

            # Download the file using requests
            response = requests.get(url)

            # Check if the download was successful
            if response.status_code == 200:
                # Save the downloaded file to disk
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded {filename}")
            else:
                print(f"Failed to download {filename}")

        # Open the file using netCDF4
        with netCDF4.Dataset(filename) as dataset:
            # Read the time and TSI variables
            time_var = dataset.variables["time"]
            tsi_var = dataset.variables["TSI"]

            # Convert the time values to dates
            time_dates = netCDF4.num2date(time_var[:], time_var.units)

            # Append only dates and TSI values within specified range to lists.
            for date, tsi_value in zip(time_dates, tsi_var[:]):
                if date.year == begin_year and date.month < begin_month:
                    continue

                if date.year == end_year and date.month > end_month:
                    continue

                dates.append(datetime.datetime(date.year, date.month, date.day))
                tsi_values.append(tsi_value)
X = sm.add_constant(range(len(tsi_values)))
y = tsi_values
model = sm.OLS(y,X)
results = model.fit()

r_squared_tsi = results.rsquared_adj

p_value_intercept_tsi, p_value_slope_tsi = results.pvalues
df = pd.DataFrame({ 'date': dates, 'tsi': tsi_values }) 
df['date'] = pd.to_datetime(df['date'])
df['date'] = df['date'].dt.to_period('M')
df.to_csv('tsi.csv', index=False)

url = 'https://www.ncei.noaa.gov/data/noaa-global-surface-temperature/v5.1/access/timeseries/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a')
for link in links:
    href = link.get('href')
    if href and 'aravg.mon.land_ocean.90S.90N' in href:
     filenm=href
print(url+filenm)
sp.call(f'wget -nc {url+filenm}', shell=True)
d=pd.read_csv(filenm,sep='\\s+',header=None)
d=d.iloc[:, :3]
d.to_csv('noaa.csv',index=False)
noaa = pd.read_csv('noaa.csv',comment='#')
noaa.columns=['year','month','change']
noaa['date'] = pd.to_datetime(noaa[['year', 'month']].assign(DAY=1)).dt.to_period('M').astype(str)

begin_year, begin_month = begin_year_month.split("-")
end_year, end_month = end_year_month.split("-")

start_date = begin_year+'-'+begin_month
end_date = end_year+'-'+end_month
print('start_date=',start_date)
print('end_date=',end_date)

mask = (noaa['date'] >= start_date) & (noaa['date'] <= end_date)
noaa = noaa.loc[mask]
noaa.to_csv('noaa.csv',index=False)
#---------------------------------


# Load the CSV files
df_tsi = pd.read_csv('tsi.csv')
df_noaa = pd.read_csv('noaa.csv')

# Convert 'date' columns to datetime
df_tsi['date'] = pd.to_datetime(df_tsi['date'])
df_noaa['date'] = pd.to_datetime(df_noaa['date'])

# Create a figure and a set of subplots
fig, ax1 = plt.subplots()

# Plot 'change' from noaa.csv using 'date'
lns1 = ax1.plot(df_noaa['date'], df_noaa['change'], color='black', linestyle='-')
ax1.set_ylabel('Global Temperature Anomalies (K: Kelvin')

# Calculate and plot linear regression lines
slope1, intercept1, r_value1, p_value1, _ = stats.linregress(range(len(df_noaa)), df_noaa['change'])
lns3 = ax1.plot(df_noaa['date'], intercept1 + slope1*range(len(df_noaa)), color='black', linestyle=':')

# Create a twin Axes sharing the x-axis with ax1
ax2 = ax1.twinx()

# Plot 'tsi' from tsi.csv using 'date'
lns2 = ax2.plot(df_tsi['date'], df_tsi['tsi'], color='black', linestyle='--')
ax2.set_ylabel('Total Solar Irradiance W$m^-2$')

# Calculate and plot linear regression lines
slope2, intercept2, r_value2, p_value2, _ = stats.linregress(range(len(df_tsi)), df_tsi['tsi'])
lns4 = ax2.plot(df_tsi['date'], intercept2 + slope2*range(len(df_tsi)), color='black', linestyle='-.')

# Let matplotlib choose the x-ticks automatically
ax1.xaxis_date()

# Format the x-tick labels as 'YYYY-MM'
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Rotate x-axis labels
plt.setp(ax1.get_xticklabels(), rotation=90)

# Add r-squared, p-value, intercept, and slope to the plot
ax1.text(0.01, 0.95, f"gstemp: r-squared = {r_value1**2:.2f}, p-value = {p_value1:.3f}, intercept = {intercept1:.2f}, slope = {slope1:.2f}", transform=ax1.transAxes, fontsize=8)
ax2.text(0.01, 0.85, f"tsi: r-squared = {r_value2**2:.2f}, p-value = {p_value2:.3f}, intercept = {intercept2:.2f}, slope = {slope2:.2f}", transform=ax2.transAxes, fontsize=8)

# Show the plot
def main():
 plt.tight_layout()
 plt.savefig(begin_year+begin_month+'_'+end_year+end_month+'.png',dpi=300)
 plt.show()

if __name__ == "__main__":
 main()
