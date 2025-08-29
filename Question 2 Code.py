import pandas as pd      # pandas is used for handling and analyzing data
import glob              # glob helps find files matching a pattern
import os                # os is used for file and folder operations

# The folder where your CSV files are stored
DATA_FOLDER = "temperatures"

# This function loads and combines all CSV files in the folder
def load_data():
    # Find all CSV files in the folder
    all_files = glob.glob(os.path.join(DATA_FOLDER, "*.csv"))
    print("Found files:", all_files)  # Print the files found for debugging
    if not all_files:
        print("No CSV files found in the folder:", DATA_FOLDER)
        return pd.DataFrame()  # Return empty DataFrame if no files found

    df_list = []  # List to store data from each file
    for file in all_files:
        try:
            df = pd.read_csv(file)  # Read each CSV file
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue  # Skip files that can't be read

        # Check if all required columns are present
        required_cols = ["STATION_NAME", "STN_ID", "LAT", "LON",
                         "January","February","March","April","May","June",
                         "July","August","September","October","November","December"]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            print(f"File {file} is missing columns: {missing}")
            continue  # Skip files missing columns

        # Reshape the data so each month becomes a row instead of a column
        df_melt = pd.melt(
            df,
            id_vars=["STATION_NAME", "STN_ID", "LAT", "LON"],
            value_vars=["January","February","March","April","May","June",
                        "July","August","September","October","November","December"],
            var_name="MonthName",
            value_name="Temperature"
        )

        # Map month names to numbers (January=1, ..., December=12)
        month_map = {
            "January":1, "February":2, "March":3, "April":4,
            "May":5, "June":6, "July":7, "August":8,
            "September":9, "October":10, "November":11, "December":12
        }
        df_melt["Month"] = df_melt["MonthName"].map(month_map)
        df_list.append(df_melt)  # Add processed data to the list

    if not df_list:
        print("No valid data loaded from CSV files.")
        return pd.DataFrame()  # Return empty DataFrame if no valid data

    # Combine all data into one DataFrame
    return pd.concat(df_list, ignore_index=True)

# This function converts a month number to an Australian season
def get_season(month):
    # Summer: December, January, February
    if month in [12,1,2]:
        return "Summer"
    # Autumn: March, April, May
    elif month in [3,4,5]:
        return "Autumn"
    # Winter: June, July, August
    elif month in [6,7,8]:
        return "Winter"
    # Spring: September, October, November
    elif month in [9,10,11]:
        return "Spring"
    else:
        return None  # For invalid month numbers

# This function calculates the average temperature for each season
def seasonal_average(df):
    if df.empty:
        print("No data for seasonal average.")
        return
    # Add a 'Season' column based on the month
    df["Season"] = df["Month"].apply(get_season)
    # Calculate the average temperature for each season
    season_avg = df.groupby("Season")["Temperature"].mean()
    # Write results to a text file
    with open("average_temp.txt", "w") as f:
        for season in ["Summer","Autumn","Winter","Spring"]:
            if season in season_avg:
                f.write(f"{season}: {season_avg[season]:.1f}°C\n")

# This function finds the station(s) with the largest temperature range
def largest_temp_range(df):
    if df.empty:
        print("No data for temperature range.")
        return
    # Group data by station name
    grouped = df.groupby("STATION_NAME")["Temperature"]
    station_min = grouped.min()  # Minimum temperature for each station
    station_max = grouped.max()  # Maximum temperature for each station
    station_range = station_max - station_min  # Range for each station
    max_range = station_range.max()  # Largest range found
    winners = station_range[station_range == max_range]  # Stations with largest range
    # Write results to a text file
    with open("largest_temp_range_station.txt", "w") as f:
        for station in winners.index:
            f.write(
                f"{station}: Range {station_range[station]:.1f}°C "
                f"(Max: {station_max[station]:.1f}°C, Min: {station_min[station]:.1f}°C)\n"
            )

# This function finds the most stable and most variable stations
def temperature_stability(df):
    if df.empty:
        print("No data for temperature stability.")
        return
    # Calculate standard deviation for each station
    std_devs = df.groupby("STATION_NAME")["Temperature"].std()
    min_std = std_devs.min()  # Smallest standard deviation
    max_std = std_devs.max()  # Largest standard deviation
    stable = std_devs[std_devs == min_std]  # Most stable stations
    variable = std_devs[std_devs == max_std]  # Most variable stations
    # Write results to a text file
    with open("temperature_stability_stations.txt", "w") as f:
        for station in stable.index:
            f.write(f"Most Stable: {station}: StdDev {stable[station]:.1f}°C\n")
        for station in variable.index:
            f.write(f"Most Variable: {station}: StdDev {variable[station]:.1f}°C\n")

# This is the main function that runs everything
def main():
    df = load_data()  # Load and combine all data
    if df.empty:
        print("No data loaded. Exiting.")
        return
    df = df.dropna(subset=["Temperature"])  # Ignore missing temperature values
    seasonal_average(df)        # Calculate and save seasonal averages
    largest_temp_range(df)      # Find and save largest temperature ranges
    temperature_stability(df)   # Find and save stability results
    print("Done! Results saved to text files.")  # Let the user know it's finished

# This runs the main function when you run the script
if __name__ == "__main__":
    main()