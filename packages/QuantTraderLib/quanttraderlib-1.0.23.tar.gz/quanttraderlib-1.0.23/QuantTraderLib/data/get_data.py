import datetime as dt
import yfinance as yfin
import pandas as pd
from vnstock import stock_historical_data
import requests

# __all__ = ['get_vn_index', 'get_vn_derivative', 'get_vnstock', 'get_crypto', 'get_forex', 'get_stock', 'get_vn30f_minute', 'get_forex_minute']

def get_vn_index(symbol, start_date, resolution='1D', end_date=None):
    """
    Retrieve historical data of the VN index from the Vietnamese stock market.

    Parameters:
        symbol (str): Symbol of the VN index.
        start_date (str or datetime): Start date for the historical data. Format: 'YYYY-MM-DD'.
        resolution (str, optional): The resolution of the data. For example, '1D' for daily data. Default is '1D'.
        end_date (str or datetime, optional): End date for the historical data. If not provided, defaults to the current date.

    Returns:
        pandas.DataFrame: DataFrame containing the historical data of the VN index with columns 'Date', 'Open', 'High', 'Low', 'Close'.
    """
    if end_date is None:
        end_date = dt.datetime.now()
    df = stock_historical_data(symbol=symbol,
                            start_date=str(start_date)[0:10],
                            end_date=str(end_date)[0:10], resolution=resolution, type='index', beautify=False, decor=False, source='DNSE')
    if 'time' in df.columns:
        df.rename(columns={'time': 'Date', 'open': 'Open', 'high':'High', 'low':'Low', 'close':'Close',}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])

    # Keep only the OHLC columns
    ohlc_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    df = df[ohlc_columns]
    return df

def get_vn_derivative(symbol, start_date, resolution='1D', end_date=None):
    """
    Retrieve historical data for VN derivatives contracts from the Vietnam stock market.

    Parameters:
        symbol (str): The symbol of the VN derivatives contract.
        start_date (str or datetime): Start date for the historical data. Format: 'YYYY-MM-DD'.
        resolution (str, optional): The resolution of the data. For example, '1D' for daily. Default is '1D'.
        end_date (str or datetime, optional): End date for the historical data. If not provided, the current date is used.

    Returns:
        pandas.DataFrame: A DataFrame containing historical data for VN derivatives with columns 'Date', 'Open', 'High', 'Low', 'Close'.
    """
    if end_date is None:
        end_date = dt.datetime.now()
    df = stock_historical_data(symbol=symbol,
                               start_date=str(start_date)[0:10],
                               end_date=str(end_date)[0:10], resolution=resolution, type='derivative', beautify=False, decor=False, source='DNSE')
    if 'time' in df.columns:
        df.rename(columns={'time': 'Date', 'open': 'Open', 'high':'High', 'low':'Low', 'close':'Close'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])

    # Retain only OHLC columns
    ohlc_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    df = df[ohlc_columns]
    return df

def get_vnstock(symbol, start_date, resolution='1D', end_date=None):
    """
    Retrieve historical data for VN stocks from the Vietnam stock market.

    Parameters:
        symbol (str): The symbol of the VN stock.
        start_date (str or datetime): Start date for the historical data. Format: 'YYYY-MM-DD'.
        resolution (str, optional): The resolution of the data. For example, '1D' for daily. Default is '1D'.
        end_date (str or datetime, optional): End date for the historical data. If not provided, the current date is used.

    Returns:
        pandas.DataFrame: A DataFrame containing historical data for VN stocks with columns 'Date', 'Open', 'High', 'Low', 'Close'.
    """
    if end_date is None:
        end_date = dt.datetime.now()
    df = stock_historical_data(symbol=symbol,
                               start_date=str(start_date)[0:10],
                               end_date=str(end_date)[0:10], resolution=resolution, type='stock', beautify=False, decor=False, source='DNSE')
    if 'time' in df.columns:
        df.rename(columns={'time': 'Date', 'open': 'Open', 'high':'High', 'low':'Low', 'close':'Close'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])

    # Retain only OHLC columns
    ohlc_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    df = df[ohlc_columns]
    return df

def get_forex(symbol, start_date, end_date=None):
    """
    Retrieve historical data for a currency pair from Yahoo Finance.

    Parameters:
        symbol (str): The symbol of the currency pair. For example: 'EURUSD'.
        start_date (str or datetime): Start date for the historical data. Format: 'YYYY-MM-DD'.
        end_date (str or datetime, optional): End date for the historical data. If not provided, the current date is used.

    Returns:
        pandas.DataFrame: A DataFrame containing historical data for the currency pair with columns 'Date', 'Open', 'High', 'Low', 'Close'.
    """
    if end_date is None:
        end_date = dt.datetime.now()
    forex_data = yfin.download(symbol, start=start_date, end=end_date)

    # Reset index to 'Date' column and convert to pd.Datetime
    forex_data.index = pd.to_datetime(forex_data.index)
    forex_data.reset_index(inplace=True)
    forex_data['Date'] = pd.to_datetime(forex_data['Date']).dt.date

    # Retain only OHLC columns
    ohlc_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    forex_data = forex_data[ohlc_columns]

    return forex_data

def get_crypto(crypto_currency, start_date, end_date=None):
    """
    Retrieve historical data for a specific cryptocurrency in USD from Yahoo Finance.

    Parameters:
        crypto_currency (str): The symbol or name of the cryptocurrency. For example: 'BTC-USD'.
        start_date (str or datetime): Start date for the historical data. Format: 'YYYY-MM-DD'.
        end_date (str or datetime, optional): End date for the historical data. If not provided, the current date is used.

    Returns:
        pandas.DataFrame: A DataFrame containing historical data for the cryptocurrency with columns 'Date', 'Open', 'High', 'Low', 'Close'.
    """
    if end_date is None:
        end_date = dt.datetime.now()
    df = yfin.download(crypto_currency, start=start_date, end=end_date)

    # Reset index to 'Date' column and convert to pd.Datetime
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    # Retain only OHLC columns
    ohlc_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    df = df[ohlc_columns]

    return df

def get_stock(symbol, start_date, end_date=None):
    """
    Retrieve historical data for a stock from Yahoo Finance for a specific time period.

    Parameters:
        symbol (str): The stock symbol. For example: 'AAPL'.
        start (str or datetime): Start date for the historical data. Format: 'YYYY-MM-DD'.
        end (str or datetime, optional): End date for the historical data. If not provided, the current date is used.

    Returns:
        pandas.DataFrame: A DataFrame containing historical data for the stock with columns 'Date', 'Open', 'High', 'Low', 'Close'.
    """
    ticker = yfin.Ticker(symbol)
    if end_date is None:
        end_date = dt.datetime.now()
    todays_data = ticker.history(period='1d', start=start_date, end=end_date)

    # Reset index to 'Date' column and convert to pd.Datetime
    todays_data.reset_index(inplace=True)
    todays_data['Date'] = pd.to_datetime(todays_data['Date']).dt.date

    # Retain only OHLC columns
    ohlc_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    todays_data = todays_data[ohlc_columns]

    return todays_data

def get_vn30f_minute(symbol, start_date, end_date=None):
    """
    Retrieve minute-level data for the VN30F1M contract from the EnTrade service.

    Parameters:
        symbol (str): The symbol of the VN30F1M contract.
        start_date (str or datetime): Start date for the historical data. Format: 'YYYY-MM-DD'.
        end_date (str or datetime, optional): End date for the historical data. If not provided, the current date is used.

    Returns:
        pandas.DataFrame: A DataFrame containing minute-level historical data with columns 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'.
    """
    # Convert start_date to datetime if it is a string
    if isinstance(start_date, str):
        start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')

    # Convert start_date to timestamp
    start_time = int((start_date - dt.timedelta(hours=7)).timestamp())

    # Convert end_date to datetime if it is a string, otherwise use the provided end_date
    if end_date:
        if isinstance(end_date, str):
            end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')
        end_time = int((end_date - dt.timedelta(hours=7)).timestamp())
    else:
        end_time = 9999999999  # A future point to get data up to the present

    # Function to retrieve data from the EnTrade service
    def vn30f():
        return requests.get(f"https://services.entrade.com.vn/chart-api/chart?from={start_time}&resolution=1&symbol={symbol}&to={end_time}").json()

    # Create DataFrame from retrieved data
    vn30fm = pd.DataFrame(vn30f()).iloc[:, :6]
    vn30fm['t'] = vn30fm['t'].astype(int).apply(lambda x: dt.datetime.utcfromtimestamp(x) + dt.timedelta(hours=7))
    vn30fm.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

    # Convert start_time and end_time to datetime for logging
    dt_object = dt.datetime.utcfromtimestamp(start_time) + dt.timedelta(hours=7)
    now_object = dt.datetime.utcfromtimestamp(end_time) + dt.timedelta(hours=7)

    print(f'===> Data {symbol} from {dt_object} to {now_object} has been appended')

    # Retain only OHLC columns
    ohlc_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    return vn30fm[ohlc_columns]

def get_forex_minute(symbol, period='1d', interval='5m'):
    """
    Retrieve minute-level data for a specific currency pair from Yahoo Finance.

    Parameters:
        symbol (str): The symbol of the currency pair. For example: 'EURUSD=X'.
        period (str, optional): Time period for the historical data. Default is '1d'.
        interval (str, optional): Data interval. For example: '5m'. Default is '5m'.

    Returns:
        pandas.DataFrame: A DataFrame containing minute-level historical data with columns 'Date', 'Open', 'High', 'Low', 'Close'.
    """
    ticker = yfin.Ticker(symbol)
    todays_data = ticker.history(period=period, interval=interval)

    # Reset index to 'Date' column and convert to pd.Datetime
    todays_data.reset_index(inplace=True)
    todays_data['Date'] = pd.to_datetime(todays_data['Datetime']).dt.date

    # Retain only OHLC columns
    ohlc_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    return todays_data[ohlc_columns]

def get_crypto_minute(symbol, period='1d', interval='5m'):
    """
    Retrieve minute-level data for a cryptocurrency from Yahoo Finance.

    Parameters:
        symbol (str): The symbol or name of the cryptocurrency. For example: 'BTC-USD'.
        period (str, optional): Time period for the historical data. Default is '1d'.
        interval (str, optional): Data interval. For example: '5m'. Default is '5m'.

    Returns:
        pandas.DataFrame: A DataFrame containing minute-level historical data with columns 'Date', 'Open', 'High', 'Low', 'Close'.
    """
    ticker = yfin.Ticker(symbol)
    todays_data = ticker.history(period=period, interval=interval)

    # Reset index to 'Date' column and convert to pd.Datetime
    todays_data.reset_index(inplace=True)
    todays_data['Date'] = pd.to_datetime(todays_data['Datetime']).dt.date

    # Retain only OHLC columns
    ohlc_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    return todays_data[ohlc_columns]