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
