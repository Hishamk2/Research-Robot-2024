import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load the dataset
data = pd.read_csv('Robot Random (H & S & D) - Coded (no fp) (major themes).csv')

# Function to convert numeric dates to datetime
def convert_date(date):
    try:
        date_stamp = pd.to_datetime(date, format="%m/%d/%Y %H:%M")
    except:
        base_date = datetime(1899, 12, 30)
        date_stamp = base_date + timedelta(days=float(date))
    return date_stamp

# Apply the conversion function to the 'questionCreationDate' column
data['questionCreationDate'] = data['questionCreationDate'].apply(convert_date)

# Drop rows where conversion failed (if any)
data.dropna(subset=['questionCreationDate'], inplace=True)

# Extract the year from 'questionCreationDate'
data['Year'] = data['questionCreationDate'].dt.to_period('Y')

# Calculate Absolute Impact for each theme by year
absolute_impact_yearly = data.groupby(['Year', 'code']).size().unstack(fill_value=0)

# Verify the counts for each theme
theme_counts = data['code'].value_counts()
print("\nTotal counts for each theme:\n", theme_counts)

# Check for discrepancies
discrepancies = theme_counts - absolute_impact_yearly.sum()
print("\nDiscrepancies between total counts and calculated counts:\n", discrepancies)

# Convert PeriodIndex to datetime for plotting
absolute_impact_yearly.index = absolute_impact_yearly.index.to_timestamp()

# Print the absolute impact to the terminal
print("Absolute Impact of themes per year:\n", absolute_impact_yearly)

# Print the sum of all major themes
print("\nSum of all major themes over all years:\n", absolute_impact_yearly.sum())

# Plot the absolute impact
plt.figure(figsize=(12, 6))
for column in absolute_impact_yearly.columns:
    plt.plot(absolute_impact_yearly.index, absolute_impact_yearly[column], label=column)

plt.title('Absolute Impact of Themes Over Time (Yearly)')
plt.xlabel('Year')
plt.ylabel('Absolute Impact')
plt.legend(title='Theme')
plt.show()

# Function to calculate relative impact
def calculate_relative_impact(absolute_impact):
    # Calculate total posts per year
    total_posts_per_year = absolute_impact.sum(axis=1)
    # Calculate relative impact by dividing each topic's occurrences by the total posts per year
    relative_impact = absolute_impact.div(total_posts_per_year, axis=0)
    return relative_impact

# Calculate Relative Impact for each theme by year
relative_impact_yearly = calculate_relative_impact(absolute_impact_yearly)

# Print the relative impact to the terminal
print("Relative Impact of themes per year:\n", relative_impact_yearly)

# Print the sum of all major themes (relative impact should sum to 1 for each year if there are no discrepancies)
print("\nSum of all major themes per year (should sum to 1):\n", relative_impact_yearly.sum(axis=1))

# Plot the relative impact
plt.figure(figsize=(12, 6))
for column in relative_impact_yearly.columns:
    plt.plot(relative_impact_yearly.index, relative_impact_yearly[column], label=column)

plt.title('Relative Impact of Themes Over Time (Yearly)')
plt.xlabel('Year')
plt.ylabel('Relative Impact')
plt.legend(title='Theme')
plt.show()
