# Mutual Fund Allocation Tracker

A Python framework to monitor mutual fund allocation changes over time. This tool processes large datasets, allowing users to select funds and date ranges to view changes, with outputs displayed by fund and by month.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Data Preparation](#data-preparation)
- [Installation](#installation)
- [Usage](#usage)
- [Example Output](#example-output)
- [Extending the Project](#extending-the-project)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction

Mutual Fund Allocation Tracker is designed to help investors and analysts monitor changes in mutual fund allocations over time. With this tool, users can:

- Select specific mutual funds to analyze.
- Choose a date range to track allocation changes.
- View detailed insights on how allocations have changed between selected dates.
- Identify new instruments added or removed from the funds.
- Analyze allocation changes on a monthly basis if multiple months are selected.

## Features

- **Data Processing**: Efficiently handles and processes large datasets of mutual fund holdings.
- **User Interaction**: Interactive command-line interface for selecting funds and date ranges.
- **Allocation Analysis**: Calculates changes in fund allocations, including percentage changes and status updates.
- **Insight Generation**: Highlights significant allocation changes, new instruments added, and instruments removed.
- **Modular Design**: Easy to extend and customize for additional funds or datasets.

## Requirements

- Python 3.6 or higher
- Libraries:
  - `pandas`
  - `openpyxl` (for reading Excel files)
  - `tabulate`
- Datasets: Excel files containing mutual fund holding data.

## Data Preparation

- **Data Files**: Prepare your mutual fund data files in Excel (.xlsx) format.
- **File Naming Convention**: Use a consistent naming convention for the files, such as `{FundName}_{YYYYMMDD}.xlsx`.
  - Example: `ZerodhaNiftyLargeMidcap250IndexFund_20230930.xlsx`
- **Data Structure**: Ensure each file contains the following columns starting from row 6 (adjust `skiprows` if needed):
  - Name of the Instrument
  - ISIN
  - Industry
  - Quantity
  - Market Value (Rs. in Lakhs)
  - % to NAV
  - YTM % (if applicable)
- **Consistent Formatting**: Ensure all data files have the same structure and formatting for accurate processing.

## Installation

1. Clone the Repository (if applicable):

   ```bash
   git clone https://github.com/yourusername/mutual-fund-allocation-tracker.git
   cd mutual-fund-allocation-tracker
   ```

2. Install Required Libraries:

   ```bash
   pip install pandas openpyxl tabulate
   ```

   If you use a `requirements.txt` file, you can install dependencies with:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Place Data Files**: Ensure your mutual fund data files are in the same directory as the Python script or update the paths in the code accordingly.

2. **Run the Script**:

   ```bash
   python mutual_fund_allocation_tracker.py
   ```

3. **Follow the Prompts**:
   - Select a Fund: Enter the number corresponding to the fund you wish to analyze.
   - Select Date Range: Enter the numbers corresponding to the start and end dates.
   - View Results: The script will display allocation changes, including increases, decreases, new instruments, and instruments removed.

## Example Output

```
Available Funds:
1. Zerodha Nifty Large Midcap 250 Index Fund
Enter the number corresponding to the fund: 1

Available Dates for Zerodha Nifty Large Midcap 250 Index Fund:
1. 2023-09-30
2. 2023-11-30
Enter the numbers corresponding to the start and end dates (e.g., '1 2'): 1 2

Allocation Changes for Zerodha Nifty Large Midcap 250 Index Fund from 2023-09-30 to 2023-11-30:
+-----------------------------+---------------------+-------------------+-----------------------+-----------+----------------+-------------------+
| Name of the Instrument      |   % to NAV_current  |  % to NAV_next    |  Allocation Change (%)|   Status  | New Instrument | Removed Instrument|
+-----------------------------+---------------------+-------------------+-----------------------+-----------+----------------+-------------------+
| HDFC Bank Limited           |        4.6175       |      5.0741       |         0.4566        | Increased |     False      |       False       |
| ICICI Bank Limited          |        3.1520       |      3.4113       |         0.2593        | Increased |     False      |       False       |
| Reliance Industries Limited |        3.5194       |      3.2639       |        -0.2555        | Decreased |     False      |       False       |
| Infosys Limited             |        3.1231       |      2.9775       |        -0.1456        | Decreased |     False      |       False       |
+-----------------------------+---------------------+-------------------+-----------------------+-----------+----------------+-------------------+

New Instruments Added:
- NewTech Company Limited

Instruments Removed:
- OldCorp Holdings
```

*Note: The output will vary based on the data in your Excel files.*

## Extending the Project

- **Adding More Funds**: Include additional funds by adding their data files to the `data_files` list in the `load_data` function.

  ```python
  data_files = [
      ('Zerodha Nifty Large Midcap 250 Index Fund', 'september_data.xlsx', '2023-09-30'),
      ('Zerodha Nifty Large Midcap 250 Index Fund', 'november_data.xlsx', '2023-11-30'),
      ('Another Fund Name', 'another_fund_data.xlsx', '2023-09-30'),
      # Add more funds and dates as needed
  ]
  ```

- **Including More Dates**: Add more historical data files to analyze allocation changes over longer periods.
- **Customizing Analysis**: Modify the `analyze_allocations` function to include additional metrics or insights.
- **Improving User Interface**: Enhance the script by adding a graphical user interface (GUI) or a web-based interface.

## Contributing

Contributions are welcome! If you'd like to improve or expand this project:

1. **Fork the Repository**: Click the "Fork" button at the top of the repository page.

2. **Create a Branch**: Create a new branch for your feature or bug fix:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commit Your Changes**: Make your changes and commit them with descriptive messages:

   ```bash
   git commit -m "Add your commit message here"
   ```

4. **Push to GitHub**: Push your branch to your forked repository:

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Submit a Pull Request**: Open a pull request on the original repository.

Please ensure your code adheres to the project's coding standards and includes appropriate documentation.



## Acknowledgments

- [pandas](https://pandas.pydata.org/)
- [tabulate](https://pypi.org/project/tabulate/)
