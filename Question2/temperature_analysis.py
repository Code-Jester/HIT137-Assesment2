import pandas as pd
import glob
import os
 
DATA_FOLDER = "temperatures"
 
def load_data():
    all_files = glob.glob(os.path.join(DATA_FOLDER, "*.csv"))
    print("Found files:", all_files)
    if not all_files:
        print("No CSV files found in the folder:", DATA_FOLDER)
        return pd.DataFrame()
 
    df_list = []
    for file in all_files:
        try:
            df = pd.read_csv(file)  # <-- FIXED: comma-delimited
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue
 
        required_cols = ["STATION_NAME", "STN_ID", "LAT", "LON",
                         "January","February","March","April","May","June",
                         "July","August","September","October","November","December"]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            print(f"File {file} is missing columns: {missing}")
            continue
 
        df_melt = pd.melt(
            df,
            id_vars=["STATION_NAME", "STN_ID", "LAT", "LON"],
            value_vars=["January","February","March","April","May","June",
                        "July","August","September","October","November","December"],
            var_name="MonthName",
            value_name="Temperature"
        )
 
        month_map = {
            "January":1, "February":2, "March":3, "April":4,
            "May":5, "June":6, "July":7, "August":8,
            "September":9, "October":10, "November":11, "December":12
        }
        df_melt["Month"] = df_melt["MonthName"].map(month_map)
        df_list.append(df_melt)
 
    if not df_list:
        print("No valid data loaded from CSV files.")
        return pd.DataFrame()
 
    return pd.concat(df_list, ignore_index=True)
 
def get_season(month):
    if month in [12,1,2]:
        return "Summer"
    elif month in [3,4,5]:
        return "Autumn"
    elif month in [6,7,8]:
        return "Winter"
    elif month in [9,10,11]:
        return "Spring"
    else:
        return None
 
def seasonal_average(df):
    if df.empty:
        print("No data for seasonal average.")
        return
    df["Season"] = df["Month"].apply(get_season)
    season_avg = df.groupby("Season")["Temperature"].mean()
    with open("average_temp.txt", "w") as f:
        for season in ["Summer","Autumn","Winter","Spring"]:
            if season in season_avg:
                f.write(f"{season}: {season_avg[season]:.1f}°C\n")
 
def largest_temp_range(df):
    if df.empty:
        print("No data for temperature range.")
        return
    grouped = df.groupby("STATION_NAME")["Temperature"]
    station_min = grouped.min()
    station_max = grouped.max()
    station_range = station_max - station_min
    max_range = station_range.max()
    winners = station_range[station_range == max_range]
    with open("largest_temp_range_station.txt", "w") as f:
        for station in winners.index:
            f.write(
                f"{station}: Range {station_range[station]:.1f}°C "
                f"(Max: {station_max[station]:.1f}°C, Min: {station_min[station]:.1f}°C)\n"
            )
 
def temperature_stability(df):
    if df.empty:
        print("No data for temperature stability.")
        return
    std_devs = df.groupby("STATION_NAME")["Temperature"].std()
    min_std = std_devs.min()
    max_std = std_devs.max()
    stable = std_devs[std_devs == min_std]
    variable = std_devs[std_devs == max_std]
    with open("temperature_stability_stations.txt", "w") as f:
        for station in stable.index:
            f.write(f"Most Stable: {station}: StdDev {stable[station]:.1f}°C\n")
        for station in variable.index:
            f.write(f"Most Variable: {station}: StdDev {variable[station]:.1f}°C\n")
 
def main():
    df = load_data()
    if df.empty:
        print("No data loaded. Exiting.")
        return
    df = df.dropna(subset=["Temperature"])
    seasonal_average(df)
    largest_temp_range(df)
    temperature_stability(df)
    print("Done! Results saved to text files.")
 
if __name__ == "__main__":
    main()