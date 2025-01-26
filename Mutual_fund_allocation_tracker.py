import pandas as pd
from datetime import datetime
from tabulate import tabulate
import os

def load_data():
    """
    Loads mutual fund data from Excel files in the current directory.

    Returns:
        pd.DataFrame: Combined DataFrame of all mutual fund data.
    """
    data_frames = []

    # List of data files (you can add more files here)
    data_files = [
        ('Zerodha Nifty Large Midcap 250 Index Fund', 'september_data.xlsx', '2023-09-30'),
        ('Zerodha Nifty Large Midcap 250 Index Fund', 'november_data.xlsx', '2023-11-30')
    ]

    for fund_name, file_path, date_str in data_files:
        # Parse the date string
        date = datetime.strptime(date_str, '%Y-%m-%d')

        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"File {file_path} not found.")
            continue

        # Parse the portfolio statement
        df = parse_portfolio_statement(file_path, date)
        if df is not None:
            df['FundName'] = fund_name
            data_frames.append(df)
        else:
            print(f"Failed to parse {file_path}.")

    if data_frames:
        df_all = pd.concat(data_frames, ignore_index=True)
        return df_all
    else:
        print("No data files loaded.")
        return pd.DataFrame()

def parse_portfolio_statement(file_path, date):
    """
    Parses a portfolio statement Excel file and returns a cleaned DataFrame.

    Args:
        file_path (str): The path to the Excel file.
        date (datetime): The date associated with the data.

    Returns:
        pd.DataFrame: The cleaned DataFrame with added date column.
    """
    try:
        # Read the Excel file
        df = pd.read_excel(file_path, header=None, skiprows=5)

        # Remove unnecessary columns (assuming columns 0 and 1 are NaN)
        df = df.iloc[:, 2:]  # Adjust based on your data structure

        # Define column names based on the data
        column_names = [
            'Name of the Instrument', 'ISIN', 'Industry', 'Quantity',
            'Market Value (Rs. in Lakhs)', '% to NAV', 'YTM %'
        ]
        num_columns = df.shape[1]
        if num_columns >= 7:
            df = df.iloc[:, :7]  # Keep only the first 7 columns if more are present
            df.columns = column_names
        else:
            print(f"Unexpected number of columns in {file_path}: {num_columns}")
            return None

        # Clean and convert data types
        df['Quantity'] = df['Quantity'].replace({',': '', '"': ''}, regex=True)
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
        df['Market Value (Rs. in Lakhs)'] = df['Market Value (Rs. in Lakhs)'].replace({',': '', '"': ''}, regex=True)
        df['Market Value (Rs. in Lakhs)'] = pd.to_numeric(df['Market Value (Rs. in Lakhs)'], errors='coerce')
        df['% to NAV'] = df['% to NAV'].replace({'%': '', ',': '', '"': ''}, regex=True)
        df['% to NAV'] = pd.to_numeric(df['% to NAV'], errors='coerce')

        # Add date column
        df['Date'] = date

        # Remove rows with NaN values in 'Name of the Instrument' and '% to NAV' columns
        df = df.dropna(subset=['Name of the Instrument', '% to NAV'])

        # Reset index
        df = df.reset_index(drop=True)

        return df
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def get_user_input(df):
    """
    Gets fund name and date range input from the user.

    Args:
        df (pd.DataFrame): The DataFrame containing all mutual fund data.

    Returns:
        tuple: Selected fund name, start date, and end date.
    """
    # Get list of available funds
    available_funds = df['FundName'].unique()
    print("\nAvailable Funds:")
    for idx, fund in enumerate(available_funds, start=1):
        print(f"{idx}. {fund}")

    # User selects a fund
    while True:
        fund_input = input("Enter the number corresponding to the fund: ").strip()
        try:
            fund_idx = int(fund_input)
            if 1 <= fund_idx <= len(available_funds):
                selected_fund = available_funds[fund_idx - 1]
                break
            else:
                print("Invalid selection. Please choose a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Get available dates for the selected fund
    fund_dates = df[df['FundName'] == selected_fund]['Date'].unique()
    fund_dates = sorted(fund_dates)
    print(f"\nAvailable Dates for {selected_fund}:")
    for idx, date in enumerate(fund_dates, start=1):
        print(f"{idx}. {date.strftime('%Y-%m-%d')}")

    # User selects date range
    while True:
        date_range_input = input("Enter the numbers corresponding to the start and end dates (e.g., '1 2'): ")
        try:
            start_idx, end_idx = map(int, date_range_input.strip().split())
            if 1 <= start_idx <= len(fund_dates) and 1 <= end_idx <= len(fund_dates):
                start_date = fund_dates[start_idx - 1]
                end_date = fund_dates[end_idx - 1]
                if start_date > end_date:
                    start_date, end_date = end_date, start_date  # Swap if the user inputs are reversed
                break
            else:
                print("Invalid selection. Please choose numbers from the list.")
        except (ValueError, IndexError):
            print("Invalid date range selection. Please try again.")

    return selected_fund, start_date, end_date

def filter_data(df, fund_name, start_date, end_date):
    """
    Filters the DataFrame based on the selected fund and date range.

    Args:
        df (pd.DataFrame): The DataFrame containing all mutual fund data.
        fund_name (str): Selected fund name.
        start_date (datetime): Start date of the date range.
        end_date (datetime): End date of the date range.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    mask = (
        (df['FundName'] == fund_name) &
        (df['Date'] >= start_date) &
        (df['Date'] <= end_date)
    )
    df_filtered = df[mask].copy()
    return df_filtered

def analyze_allocations(df_filtered):
    """
    Analyzes changes in fund allocations over the selected date range.

    Args:
        df_filtered (pd.DataFrame): Filtered DataFrame containing data for the selected fund and date range.

    Returns:
        dict: A dictionary with date pairs as keys and DataFrames of allocation changes as values.
    """
    allocation_changes = {}
    dates = sorted(df_filtered['Date'].unique())

    for i in range(len(dates) - 1):
        date_current = dates[i]
        date_next = dates[i + 1]

        df_current = df_filtered[df_filtered['Date'] == date_current]
        df_next = df_filtered[df_filtered['Date'] == date_next]

        # Merge with outer join to include all instruments
        df_merged = pd.merge(
            df_current[['Name of the Instrument', '% to NAV']],
            df_next[['Name of the Instrument', '% to NAV']],
            on='Name of the Instrument',
            how='outer',
            suffixes=('_current', '_next')
        )

        # Fill NaNs with zeros for allocation percentages
        df_merged['% to NAV_current'] = df_merged['% to NAV_current'].fillna(0)
        df_merged['% to NAV_next'] = df_merged['% to NAV_next'].fillna(0)

        # Calculate allocation change
        df_merged['Allocation Change (%)'] = df_merged['% to NAV_next'] - df_merged['% to NAV_current']

        # Determine status
        df_merged['Status'] = df_merged['Allocation Change (%)'].apply(
            lambda x: 'Increased' if x > 0 else ('Decreased' if x < 0 else 'No Change')
        )

        # Identify new and removed instruments
        df_merged['New Instrument'] = df_merged['% to NAV_current'] == 0
        df_merged['Removed Instrument'] = df_merged['% to NAV_next'] == 0

        allocation_changes[(date_current, date_next)] = df_merged

    return allocation_changes

def display_changes(allocation_changes, fund_name):
    """
    Displays the allocation changes by fund and by month.

    Args:
        allocation_changes (dict): Dictionary containing allocation changes per date pair.
        fund_name (str): Name of the selected fund.
    """
    for date_pair, df_changes in allocation_changes.items():
        date_current, date_next = date_pair
        print(f"\nAllocation Changes for {fund_name} from {date_current.strftime('%Y-%m-%d')} to {date_next.strftime('%Y-%m-%d')}:")
        df_display = df_changes[['Name of the Instrument', '% to NAV_current', '% to NAV_next', 'Allocation Change (%)', 'Status', 'New Instrument', 'Removed Instrument']]

        # Sort by absolute allocation change
        df_display_sorted = df_display.sort_values(by='Allocation Change (%)', key=lambda x: x.abs(), ascending=False)

        # Display significant changes
        print(tabulate(df_display_sorted, headers='keys', tablefmt='pretty', showindex=False))

        # Display new instruments
        new_instruments = df_display_sorted[df_display_sorted['New Instrument'] == True]['Name of the Instrument']
        if not new_instruments.empty:
            print("\nNew Instruments Added:")
            for instrument in new_instruments:
                print(f"- {instrument}")

        # Display removed instruments
        removed_instruments = df_display_sorted[df_display_sorted['Removed Instrument'] == True]['Name of the Instrument']
        if not removed_instruments.empty:
            print("\nInstruments Removed:")
            for instrument in removed_instruments:
                print(f"- {instrument}")

def main():
    # Load data
    df_all = load_data()
    if df_all.empty:
        return

    # Get user input
    selected_fund, start_date, end_date = get_user_input(df_all)

    # Filter data based on user input
    df_filtered = filter_data(df_all, selected_fund, start_date, end_date)
    if df_filtered.empty:
        print("No data available for the selected fund and date range.")
        return

    # Analyze allocation changes
    allocation_changes = analyze_allocations(df_filtered)

    # Display the results
    display_changes(allocation_changes, selected_fund)

if __name__ == '__main__':
    main()