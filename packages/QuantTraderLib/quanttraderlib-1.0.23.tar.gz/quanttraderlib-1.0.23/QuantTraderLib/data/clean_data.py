from datetime import datetime, timedelta
import lunardate
import pandas as pd
import numpy as np

######################################## helper functions #######################################
def _find_date_column(df):
    possible_date_columns = ['date', 'Date', 'time', 'Time']
    for col in possible_date_columns:
        if col in df.columns:
            return col
    raise ValueError("No date column found in DataFrame.")

def _find_column(df, column_names):
    for col in column_names:
        if col in df.columns:
            return col
    raise ValueError("No column found in DataFrame with names: " + ", ".join(column_names))

def _generate_time_slots(start, end, interval_minutes):
    time_slots = []
    current_time = start
    while current_time < end:
        time_slots.append(current_time)
        current_time += timedelta(minutes=interval_minutes)
    return time_slots

def _create_valid_minutes():
    valid_times = []
    morning_session = _generate_time_slots(datetime.strptime("09:00", "%H:%M"), datetime.strptime("11:30", "%H:%M"), 1)
    afternoon_session_1 = _generate_time_slots(datetime.strptime("13:00", "%H:%M"), datetime.strptime("14:30", "%H:%M"), 1)
    valid_times.extend(morning_session)
    valid_times.extend(afternoon_session_1)
    valid_times.append(datetime.strptime("14:45", "%H:%M"))
    return valid_times

def drop_duplicated_values(df):

    data = df.set_index('Date') #, inplace =True)
    data.columns = ['Open','High','Low','Close','Volume']

    data['Date'] = [str(i)[:10] for i in data.index]
    data['time'] = [str(i)[11:] for i in data.index]
    # Handling duplicate
    data = data[~data.index.duplicated(keep='first')]

    return data

############################################ CLEAN DAILY DATA ##############################################################
def get_vietnam_trading_days(start_date, end_date):
    """
    Create a list of trading days in Vietnam within a specific date range, excluding weekends and holidays.

    Parameters:
        start_date (str or datetime): The start date for the list of trading days. Format: 'YYYY-MM-DD'.
        end_date (str or datetime): The end date for the list of trading days. Format: 'YYYY-MM-DD'.

    Returns:
        list: A list of trading days in the specified date range.
    """
    # Create a list of dates in the specified date range
    date_range = pd.date_range(start_date, end_date)

    # Exclude weekend days (Saturday, Sunday)
    trading_days = date_range[date_range.weekday < 5]

    # Get the years in the date range
    years = list(set(date_range.year))

    all_holidays = []

    for year in years:
        # List of holidays (in datetime format)
        holidays = [
            datetime(year, 1, 1),  # New Year's Day
            datetime(year, 4, 30),  # Reunification Day
            datetime(year, 5, 1),  # International Labor Day
            datetime(year, 9, 2)  # National Day
        ]

        # Calculate the Lunar New Year
        lunar_new_year = lunardate.LunarDate(year, 1, 1).toSolarDate()
        tet_holidays = [lunar_new_year + timedelta(days=i) for i in range(7)]  # Lunar New Year lasts 7 days
        holidays.extend(tet_holidays)

        # Calculate Hung Kings' Temple Festival (10th day of the 3rd lunar month)
        hung_vuong_anniversary = lunardate.LunarDate(year, 3, 10).toSolarDate()
        holidays.append(hung_vuong_anniversary)

        # Add holidays to the overall list
        all_holidays.extend(holidays)

    # Exclude holidays from the list of trading days
    trading_days = [day for day in trading_days if day not in all_holidays]

    return trading_days

def check_missing_trading_dates(df):
    """
    Check for missing trading dates in the DataFrame compared to the list of trading days in Vietnam.

    Parameters:
        df (pandas.DataFrame): DataFrame containing trading data with at least one date column.

    Returns:
        pandas.DataFrame: DataFrame containing the missing trading dates.
    """
    date_col = _find_date_column(df)

    # Ensure the date column has datetime data type
    df[date_col] = pd.to_datetime(df[date_col])

    # Determine the start and end dates from the date column of the DataFrame
    start_date = df[date_col].min()
    end_date = df[date_col].max()

    # Get the list of trading days
    trading_days = get_vietnam_trading_days(start_date, end_date)

    # Convert the list of trading days to a DataFrame for easier comparison
    trading_days_df = pd.DataFrame(trading_days, columns=[date_col])

    # Check for missing dates in the data
    missing_dates = trading_days_df[~trading_days_df[date_col].isin(df[date_col])]

    return missing_dates

def fill_missing_days(df):
    """
    Fill in the missing trading days in the DataFrame by adding the missing days and using the forward-fill method.

    Parameters:
        df (pandas.DataFrame): DataFrame containing trading data with at least one date column.

    Returns:
        pandas.DataFrame: DataFrame with missing trading days filled in and data filled.
    """
    date_col = _find_date_column(df)

    # Ensure the date column has datetime data type
    df[date_col] = pd.to_datetime(df[date_col])

    # Determine the start and end dates from the date column of the DataFrame
    start_date = df[date_col].min()
    end_date = df[date_col].max()

    # Get the list of trading days
    trading_days = get_vietnam_trading_days(start_date, end_date)

    # Convert the list of trading days to a DataFrame for easier comparison
    trading_days_df = pd.DataFrame(trading_days, columns=[date_col])
    trading_days_df[date_col] = pd.to_datetime(trading_days_df[date_col])

    # Find the missing trading days in the data
    missing_dates = trading_days_df[~trading_days_df[date_col].isin(df[date_col])]

    if not missing_dates.empty:
        # Create a DataFrame for the missing days and assign NaN values to the other columns
        missing_dates = missing_dates.set_index(date_col)
        missing_df = pd.DataFrame(index=missing_dates.index, columns=df.columns.drop(date_col))
        missing_df.reset_index(inplace=True)

        # Combine the original DataFrame with the missing days DataFrame
        df = pd.concat([df, missing_df]).sort_values(by=date_col).reset_index(drop=True)

        # Apply the forward-fill method to fill in the OHLCV values
        df.fillna(method='ffill', inplace=True)

    return df

############################################ CLEAN MINUTE DATA ##############################################################
def check_missing_minutes(data, date_col_candidates=['date', 'Date'], time_col_candidates=['time', 'Time']):
    """
    Check for missing minutes in the data on a per-minute basis.

    Parameters:
        data (pandas.DataFrame): DataFrame containing minute-by-minute data with at least one date column and one time column.
        date_col_candidates (list, optional): List of possible column names that may contain the date. Default is ['date', 'Date'].
        time_col_candidates (list, optional): List of possible column names that may contain the time. Default is ['time', 'Time'].

    Returns:
        dict: A dictionary with the date as the key and the list of missing minutes on that day as the value.
    """
    try:
        # Find the separate date and time columns
        date_column = _find_column(data, date_col_candidates)
        time_column = _find_column(data, time_col_candidates)
        # Convert the date and time columns
        data[date_column] = pd.to_datetime(data[date_column])
        data[time_column] = pd.to_datetime(data[time_column], format='%H:%M:%S').dt.time

        # Create a temporary list of datetime
        datetimes = data.apply(lambda row: datetime.combine(row[date_column].date(), row[time_column]), axis=1)
    except ValueError:
        # If there is no time column, check if there is a datetime column
        datetime_column = _find_column(data, date_col_candidates)
        datetimes = pd.to_datetime(data[datetime_column])

    valid_times = _create_valid_minutes()

    missing_times_per_day = {}

    for day in datetimes.dt.date.unique():
        day_data = datetimes[datetimes.dt.date == day]
        day_times = day_data.dt.strftime('%H:%M').tolist()
        valid_day_times = [datetime.combine(day, time.time()).strftime('%H:%M') for time in valid_times]

        missing_times = set(valid_day_times) - set(day_times)

        # Delete future times
        now = datetime.now()
        if day >= now.date():
            # Ensure times are only relevant if they are today or earlier
            missing_times = {time for time in missing_times if datetime.combine(day, datetime.strptime(time, '%H:%M').time()) <= now}

        if missing_times:  # Only add if there are missing times
            missing_times_per_day[day] = sorted(list(missing_times))

    return missing_times_per_day

def fill_missing_minutes(df, verbose=1):
    """
    Fill in missing minutes in the data on a per-minute basis.

    Parameters:
        df (pandas.DataFrame): DataFrame containing minute-by-minute data with at least one date column and one time column.
        verbose (int, optional): Level of verbosity for printing information. Default is 1.

    Returns:
        pandas.DataFrame: DataFrame with missing minutes filled in and data completed.
    """
    # Ensure the columns are named correctly
    df_copy = df.copy()
    df_copy.columns = [col.capitalize() for col in df_copy.columns]

    # Check and add required columns with NaN values
    required_columns = ['Open', 'High', 'Low', 'Close']
    for col in required_columns:
        if col not in df_copy.columns:
            df_copy.loc[:, col] = np.nan
    
    # Set 'Date' as the index and reset the index for easier processing
    data = df_copy.set_index(_find_date_column(df))
    
    # Extract date and time from the index, using .loc to avoid warnings
    data.loc[:, 'Date'] = data.index.astype(str).str[:10]  # Get the date part from the datetime index
    data.loc[:, 'Time'] = data.index.astype(str).str[11:]  # Get the time part from the datetime index

    # Handle duplicates
    data = data[~data.index.duplicated(keep='first')]

    # Convert data into pivot format for easier handling of missing data
    data_model = data.pivot(index='Date', columns='Time', values=required_columns)

    if verbose > 0:
        print("Filling:")
        for index, row in data_model.iterrows():
            if pd.isnull(row).any():  # Check if there are any missing values in the row
                missing_times = row[pd.isnull(row)].index.tolist()  # Get the list of missing times
                for time in missing_times:
                    time = time[1]
                    if isinstance(time, str):  # Ensure 'time' is a string
                        try:
                            index_date = datetime.strptime(index, "%Y-%m-%d").date()  # Convert index to date
                            time_of_day = datetime.strptime(time, "%H:%M:%S").time()  # Convert time to time object
                            if index_date <= datetime.now().date() and time_of_day <= datetime.now().time():
                                print(f"At {index} {time}")
                        except ValueError:
                            print(f"Invalid time format at {index} {time}")
                    else:
                        print(f"Unexpected type for time at {index}: {type(time)}")

    # Get the rows that are still missing and calculate the ratio of missing rows
    filled_rows = data_model[data_model.isnull().any(axis=1)]
    filled_count = len(filled_rows)
    total_rows = len(data)
    fill_ratio = filled_count / total_rows

    if fill_ratio > 0.03:
        print("Warning: The fill ratio exceeds 3%, which may affect the results.")

    # Forward-fill and backward-fill missing values for all columns
    data_model = data_model.ffill(axis=1).bfill(axis=1).stack(future_stack=True).reset_index()

    # Fill remaining NaN values
    data_model = data_model.ffill()

    # Filter future data
    valid_index = np.all([data_model['Date'] == str(datetime.now().date()), data_model['Time'] <= str(datetime.now().time())], axis=0)
    valid_index = valid_index | (data_model['Date'] < str(datetime.now().date()))
    data_model = data_model[valid_index]

    return data_model