import pandas as pd
from datetime import datetime, timedelta

def convert_date(date):
    try:
        # If date is already in datetime format
        date_stamp = pd.to_datetime(date, format="%m/%d/%Y %H:%M")
    except (ValueError, TypeError):
        # Convert Excel numeric date to datetime
        base_date = datetime(1899, 12, 30)
        date_stamp = base_date + timedelta(days=float(date))
    return date_stamp.strftime("%m/%d/%Y %H:%M")

# Load the CSV file
file_path = 'Robot Random (H & S & D) - Coded (no fp) (major themes).csv'
data = pd.read_csv(file_path)

# Apply the conversion function to the 'questionCreationDate' column
data['questionCreationDate'] = data['questionCreationDate'].apply(convert_date)

# Save the updated DataFrame to a new CSV file
output_file_path = 'sfdsdfsdfsdfsdf.csv'
data.to_csv(output_file_path, index=False)

print(f"Dates have been converted and saved to {output_file_path}")
