# Portfolio Management System

A Python application for managing stock portfolios with automatic rebalancing capabilities using real-time stock data from Alpha Vantage API.

## Features

- Real-time stock price fetching
- Portfolio value calculation
- Automatic rebalancing recommendations
- Support for multiple stocks
- Error handling for API failures

## Setup Instructions

### 1. Create Virtual Environment

#### Windows
```bash
python -m venv venv
```

#### macOS/Linux
```bash
python3 -m venv venv
```

### 2. Activate Virtual Environment

#### Windows
```bash
venv\Scripts\activate
```

#### macOS/Linux
```bash
source venv/bin/activate
```

### 3. Install Required Dependencies

```bash
pip install requests python-dotenv
```

### 4. Get Free API Key

1. Visit [Alpha Vantage API](https://www.alphavantage.co/support/#api-key)
2. Follow the instructions
3. Copy your API key

### 5. Create Environment File

Create a `.env` file in the project root and add your API key:

```env
API_KEY=your_api_key_here
```

### 6. Run the Application

```bash
python Portfolio.py
```

## Usage Example

The application will automatically:
- Fetch current stock prices for NVDA, AAPL, META, and TSLA
- Calculate portfolio total value
- Display buy/sell actions needed to reach target allocation

## Project Structure

```
Portfolio.py          # Main application file
README.md            # This file
.env                 # Environment variables (create this)
venv/                # Virtual environment folder
```

## Requirements

- Python 3.7+
- Internet connection for API calls
- Alpha Vantage API key (free)

## Disclaimer

- The API have a rate limit of 25 requests per day.
- The portfolio assume a current price of 100 when the API request fail.