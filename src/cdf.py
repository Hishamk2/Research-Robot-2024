import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Data extracted from the provided text (Relative Impact)
data_relative = {
    'Year':             ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
    'Actuator':         [0.00,    0.18,   0.05,   0.14,   0.15,   0.11,   0.16,   0.19,   0.18,   0.13,   0.08,   0.12,   0.12,   0.14,   0.23,   0.23],
    'Connections':      [0.10,    0.00,   0.05,   0.00,   0.04,   0.00,   0.05,   0.03,   0.05,   0.08,   0.05,   0.12,   0.00,   0.05,   0.02,   0.15],
    'Coordinates':      [0.00,    0.12,   0.00,   0.04,   0.12,   0.07,   0.11,   0.00,   0.15,   0.11,   0.10,   0.19,   0.18,   0.08,   0.07,   0.00],
    'Error':            [0.00,    0.00,   0.00,   0.04,   0.00,   0.00,   0.11,   0.06,   0.08,   0.05,   0.18,   0.05,   0.09,   0.08,   0.12,   0.15],
    'Incoming':         [0.10,    0.06,   0.19,   0.14,   0.15,   0.32,   0.13,   0.23,   0.15,   0.13,   0.12,   0.09,   0.21,   0.19,   0.18,   0.15],
    'Moving':           [0.10,    0.06,   0.24,   0.21,   0.15,   0.29,   0.13,   0.19,   0.18,   0.18,   0.22,   0.09,   0.15,   0.08,   0.23,   0.00],
    'Other':            [0.20,    0.29,   0.14,   0.04,   0.00,   0.04,   0.05,   0.06,   0.00,   0.16,   0.02,   0.09,   0.00,   0.11,   0.07,   0.08],
    'Programming':      [0.00,    0.00,   0.00,   0.00,   0.04,   0.04,   0.00,   0.00,   0.03,   0.03,   0.02,   0.09,   0.03,   0.03,   0.00,   0.08],
    'Remote':           [0.10,    0.18,   0.14,   0.11,   0.08,   0.04,   0.16,   0.13,   0.10,   0.11,   0.10,   0.12,   0.21,   0.16,   0.07,   0.08],
    'Specifications':   [0.30,    0.12,   0.19,   0.18,   0.15,   0.04,   0.05,   0.06,   0.05,   0.00,   0.08,   0.05,   0.03,   0.03,   0.00,   0.08],
    'Timing':           [0.10,    0.00,   0.00,   0.11,   0.12,   0.07,   0.05,   0.03,   0.03,   0.03,   0.02,   0.00,   0.00,   0.05,   0.02,   0.00]
}

# Data extracted from the provided text (Absolute Impact)
data_absolute = {
    'Year': ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
    'Actuator': [0, 3, 1, 4, 4, 3, 6, 6, 7, 5, 3, 5, 4, 5, 13, 3],
    'Connections': [1, 0, 1, 0, 1, 0, 2, 1, 2, 3, 2, 5, 0, 2, 1, 2],
    'Coordinates': [0, 2, 0, 1, 3, 2, 4, 0, 6, 4, 4, 8, 6, 4, 4, 0],
    'Error': [0, 0, 0, 1, 0, 0, 4, 2, 3, 2, 7, 2, 3, 3, 7, 2],
    'Incoming': [1, 1, 4, 4, 4, 9, 5, 7, 6, 5, 5, 4, 7, 7, 10, 2],
    'Moving': [1, 1, 5, 6, 4, 8, 5, 6, 7, 7, 9, 4, 5, 3, 13, 0],
    'Other': [2, 5, 3, 1, 0, 1, 2, 2, 0, 6, 1, 4, 0, 4, 4, 1],
    'Programming': [0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 4, 1, 1, 0, 1],
    'Remote': [1, 3, 3, 3, 2, 1, 6, 4, 4, 4, 4, 5, 7, 6, 4, 1],
    'Specifications': [3, 2, 4, 5, 4, 1, 2, 2, 2, 0, 3, 2, 1, 1, 0, 1],
    'Timing': [1, 0, 0, 3, 3, 2, 2, 1, 1, 1, 1, 0, 0, 2, 1, 0]
}

# Convert Year to datetime and create DataFrames
data_relative['Year'] = pd.to_datetime(data_relative['Year'])
df_relative = pd.DataFrame(data_relative)
df_relative.set_index('Year', inplace=True)

data_absolute['Year'] = pd.to_datetime(data_absolute['Year'])
df_absolute = pd.DataFrame(data_absolute)
df_absolute.set_index('Year', inplace=True)

# Compute CDF for each theme
themes_relative = df_relative.columns
themes_absolute = df_absolute.columns

for theme in themes_relative:
    df_relative[f'{theme}_CDF'] = df_relative[theme].cumsum() / df_relative[theme].sum()

for theme in themes_absolute:
    df_absolute[f'{theme}_CDF'] = df_absolute[theme].cumsum() / df_absolute[theme].sum()

# Plot CDF for relative impact
plt.figure(figsize=(14, 10))
styles = ["-", "--", "-.", ":", "-", "--", "-.", ":"]
marks = ["^", "d", "o", "v", "p", "s", "<", ">"]
width = [3, 3, 3, 3, 3, 3, 3, 3]
marks_size = [8, 8, 8, 8, 8, 8, 8, 8]
marker_color = sns.color_palette("husl", len(themes_relative))

for idx, theme in enumerate(themes_relative):
    plt.plot(df_relative.index, df_relative[f'{theme}_CDF'], label=theme, 
             linestyle=styles[idx % len(styles)], 
             marker=marks[idx % len(marks)], 
             linewidth=width[idx % len(width)], 
             markersize=marks_size[idx % len(marks_size)], 
             color=marker_color[idx])

plt.xlabel('Year', fontsize=14)
plt.ylabel('CDF', fontsize=14)
plt.title('CDF of Relative Impact of Themes Over Time', fontsize=16)
plt.legend(fontsize=10)
plt.grid(True)
plt.tight_layout()
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()

# Plot CDF for absolute impact
plt.figure(figsize=(14, 10))

for idx, theme in enumerate(themes_absolute):
    plt.plot(df_absolute.index, df_absolute[f'{theme}_CDF'], label=theme, 
             linestyle=styles[idx % len(styles)], 
             marker=marks[idx % len(marks)], 
             linewidth=width[idx % len(width)], 
             markersize=marks_size[idx % len(marks_size)], 
             color=marker_color[idx])

plt.xlabel('Year', fontsize=14)
plt.ylabel('CDF', fontsize=14)
plt.title('CDF of Absolute Impact of Themes Over Time', fontsize=16)
plt.legend(fontsize=10)
plt.grid(True)
plt.tight_layout()
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()

# Compute CDF for each theme and print values
print("CDF Values for Relative Impact (rounded to two decimal places):")
for theme in themes_relative:
    df_relative[f'{theme}_CDF'] = df_relative[theme].cumsum() / df_relative[theme].sum()
    print(f"{theme} CDF:")
    print(df_relative[[f'{theme}_CDF']].round(2))

print("\nCDF Values for Absolute Impact (rounded to two decimal places):")
for theme in themes_absolute:
    df_absolute[f'{theme}_CDF'] = df_absolute[theme].cumsum() / df_absolute[theme].sum()
    print(f"{theme} CDF:")
    print(df_absolute[[f'{theme}_CDF']].round(2))

