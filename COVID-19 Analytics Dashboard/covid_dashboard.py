import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "covid_data.csv"  # Replace with your dataset's path
try:
    covid_data = pd.read_csv(file_path)
    print("Data loaded successfully.")
except FileNotFoundError:
    print(f"File not found: {file_path}")
    exit()

# Display basic information about the dataset
print("Dataset Overview:\n")
print(covid_data.info())
print("\nSample Data:\n")
print(covid_data.head())

# Preprocessing
# Ensure the columns for date and cases are named correctly.
date_column = "Date"  # Replace with the actual date column name in your dataset
cases_column = "Confirmed"  # Replace with the actual confirmed cases column name
recoveries_column = "Recovered"  # Replace with the recoveries column name
deaths_column = "Deaths"  # Replace with the deaths column name

# Convert date column to datetime
try:
    covid_data[date_column] = pd.to_datetime(covid_data[date_column])
except KeyError:
    print(f"Column '{date_column}' not found in the dataset.")
    exit()

# Summarize data by date
daily_data = covid_data.groupby(date_column).sum().reset_index()

# Plotting
sns.set(style="whitegrid")
plt.figure(figsize=(14, 7))

# Line chart for trends
plt.plot(daily_data[date_column], daily_data[cases_column], label="Confirmed Cases", color="blue")
plt.plot(daily_data[date_column], daily_data[recoveries_column], label="Recoveries", color="green")
plt.plot(daily_data[date_column], daily_data[deaths_column], label="Deaths", color="red")

# Add titles and labels
plt.title("COVID-19 Trends", fontsize=16)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Count", fontsize=12)
plt.legend(loc="upper left")
plt.xticks(rotation=45)

# Show the plot
plt.tight_layout()
plt.show()

# Heatmap for correlation analysis
plt.figure(figsize=(10, 6))
correlation = daily_data[[cases_column, recoveries_column, deaths_column]].corr()
sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Between Metrics", fontsize=16)
plt.show()

# Bar chart for total cases by country (if applicable)
if "Country" in covid_data.columns:
    country_data = covid_data.groupby("Country").sum().reset_index()
    top_countries = country_data.nlargest(10, cases_column)  # Top 10 countries

    plt.figure(figsize=(12, 6))
    sns.barplot(x=cases_column, y="Country", data=top_countries, palette="viridis")
    plt.title("Top 10 Countries by Confirmed Cases", fontsize=16)
    plt.xlabel("Confirmed Cases", fontsize=12)
    plt.ylabel("Country", fontsize=12)
    plt.show()
else:
    print("Country-level data not found in the dataset.")
