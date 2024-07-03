import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import seaborn as sns

def load_and_prepare_data(file_path):
    # Load the dataset
    data = pd.read_csv(file_path)

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
    
    return data

def calculate_absolute_impact(data):
    # Calculate Absolute Impact for each theme by year
    absolute_impact_yearly = data.groupby(['Year', 'code']).size().unstack(fill_value=0)
    return absolute_impact_yearly

def calculate_relative_impact(absolute_impact):
    # Calculate total posts per year
    total_posts_per_year = absolute_impact.sum(axis=1)
    # Calculate relative impact by dividing each topic's occurrences by the total posts per year
    relative_impact = absolute_impact.div(total_posts_per_year, axis=0)
    return relative_impact

def plot_impact(impact_df, title, ylabel):
    # Ensure the index is in datetime format
    if isinstance(impact_df.index, pd.PeriodIndex):
        impact_df.index = impact_df.index.to_timestamp()

    # Plot styles
    styles = ["-", "--", "-.", ":", "-", "--", "-.", ":"]
    marks = ["^", "d", "o", "v", "p", "s", "<", ">"]
    width = [3, 3, 3, 3, 3, 3, 3, 3]
    marks_size = [8, 8, 8, 8, 8, 8, 8, 8]
    marker_color = sns.color_palette("husl", len(impact_df.columns))

    # Plot the impact
    plt.figure(figsize=(12, 6))
    for idx, column in enumerate(impact_df.columns):
        plt.plot(impact_df.index, impact_df[column], label=column,
                 linestyle=styles[idx % len(styles)],
                 marker=marks[idx % len(marks)],
                 linewidth=width[idx % len(width)],
                 markersize=marks_size[idx % len(marks_size)],
                 color=marker_color[idx])

    plt.title(title, fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.legend(title='Theme', fontsize=10)
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.show()

def main():
    file_path = 'Robot Random (H & S & D) - Coded (no fp) (major themes) (should be updated).csv'
    data = load_and_prepare_data(file_path)

    # Calculate and plot absolute impact
    absolute_impact_yearly = calculate_absolute_impact(data)

    # Verify the counts for each theme
    theme_counts = data['code'].value_counts()
    print("\nTotal counts for each theme:\n", theme_counts)

    # Check for discrepancies
    discrepancies = theme_counts - absolute_impact_yearly.sum()
    print("\nDiscrepancies between total counts and calculated counts:\n", discrepancies)

    # Print the absolute impact to the terminal
    print("Absolute Impact of themes per year:\n", absolute_impact_yearly)

    # Print the sum of all major themes
    print("\nSum of all major themes over all years:\n", absolute_impact_yearly.sum())

    plot_impact(absolute_impact_yearly, 'Absolute Impact of Themes Over Time (Yearly)', 'Absolute Impact')

    # Calculate and plot relative impact
    relative_impact_yearly = calculate_relative_impact(absolute_impact_yearly)

    # Print the relative impact to the terminal
    print("Relative Impact of themes per year:\n", relative_impact_yearly)

    # Print the sum of all major themes (relative impact should sum to 1 for each year if there are no discrepancies)
    print("\nSum of all major themes per year (should sum to 1):\n", relative_impact_yearly.sum(axis=1))

    plot_impact(relative_impact_yearly, 'Relative Impact of Themes Over Time (Yearly)', 'Relative Impact')

    # Calculate and print average absolute and relative impact for each theme to two decimal places
    average_absolute_impact = absolute_impact_yearly.mean().round(2)
    average_relative_impact = relative_impact_yearly.mean().round(2)

    print("\nAverage Absolute Impact for each theme (to two decimal places):\n", average_absolute_impact)
    print("\nAverage Relative Impact for each theme (to two decimal places):\n", average_relative_impact)

    # Set display options to show all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    # Print values for each theme for each year
    print("\nAbsolute Impact for each theme by year:\n", absolute_impact_yearly.round(2))
    print("\nRelative Impact for each theme by year:\n", relative_impact_yearly.round(2))

    # Print the total number of questions in for each year (so sum up absolute impact for all themes)
    print("\nTotal number of questions for each year:\n", absolute_impact_yearly.sum(axis=1))

if __name__ == "__main__":
    main()
