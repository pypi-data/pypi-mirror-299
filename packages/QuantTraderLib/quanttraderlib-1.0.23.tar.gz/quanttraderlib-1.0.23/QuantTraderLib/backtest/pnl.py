import numpy as np

def check_positions(df, min_days_between_positions=2):
    """
    Check buy and sell positions in the data to ensure they meet the minimum distance requirement between positions.

    Parameters:
        df (pandas.DataFrame): DataFrame containing data with 'close' and 'position' columns. The 'position' column contains value 1 for buy positions and -1 for sell positions.
        min_days_between_positions (int, optional): Minimum number of days required between buy and sell positions. Default is 2 days.

    Returns:
        list: A list of tuples containing the indices of valid buy and sell positions.
    """
    price_diff = df['close'].diff()
    positions = df['position']
    valid_positions = []
    invalid_positions = []
    used_sell_indices = set()
    for i in range(len(positions)):
        if positions[i] == 1:  # If this is a buy position
            # Find the nearest sell position
            for j in range(i + 1, len(positions)):
                if positions[j] == -1 and j not in used_sell_indices:
                    # Check the distance is greater than or equal to 2 days
                    if j - i >= min_days_between_positions:
                        valid_positions.append((i, j))
                        used_sell_indices.add(j)
                    else:
                        invalid_positions.append((i, j))
                    break

    if invalid_positions:
        print("There are some inaccuracies in your position data:")
        for position in invalid_positions:
            buy_date = df.index[position[0]]
            sell_date = df.index[position[1]]
            print(f"Bought on {buy_date}, sold on {sell_date}")
    return valid_positions

def calculate_pnl(df):
    """
    Calculate profit and loss (PnL) based on valid buy and sell positions in the data.

    Parameters:
        df (pandas.DataFrame): DataFrame containing data with 'close' and 'position' columns. The 'position' column contains value 1 for buy positions and -1 for sell positions.

    Returns:
        tuple: A tuple containing two elements:
            - numpy.ndarray: An array of PnL values for the sell indices.
            - list: A list of tuples containing the indices of valid buy and sell positions.
    """
    valid_positions = check_positions(df)

    if not valid_positions:
        return None, None

    prices = df['close'].values
    pnl = np.zeros(len(prices))
    for buy_index, sell_index in valid_positions:
        buy_price = prices[buy_index]
        sell_price = prices[sell_index]
        pnl[sell_index] = sell_price - buy_price

    return pnl, valid_positions
