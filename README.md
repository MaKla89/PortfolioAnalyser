# PortfolioAnalyser

This is a small tool that visually summarizes your portfolio consisting of stocks, ETFs and crypto-currencies in a dash-based WebUI.
That WebUI will be accessible on port 8085 of your machine. It uses the free version of the coingecko-API and the yahoofinancials library for fetching current price data.

<img width="400" alt="Demo" align="center" src="https://github.com/MaKla89/PortfolioAnalyser/blob/main/assets/screenshot.PNG?raw=true">

# Installation

## Prerequisites

This tool requires "dash", "dash-auth", "pandas", "beautifulsoup4", "waitress", "fake-useragent" and "requests" for python to be installed (via `pip install dash dash-auth pandas requests beautifulsoup4 fake-useragent`).

### Portfolio-Setup

Please provide a portfolio.csv that contains your portfolio-setup's details: 

  - holdings' names, 
  - trade-symbols, 
  - amount, 
  - asset type (Cash, Stock, ETF or Crypto) and 
  - the invested money for each position ("Amount" and "Invested" are equal for Cash)
  - previously realised profits and losses per position (set 0 otherwise)
  
For further details on this portfolio-configuration take a look at the included demo-portfolio.csv file!
If no portfolio.csv is provided, the included demo-file will be used for demonstration purposes.
 
The `portfolio.csv` file needs to be placed in the data-folder.


### Enabling Basic-Auth (Optional)

You can optionally use basic-auth to have some rudimentary login required to access your Dashboard. Create a text-file called `basic_auth.txt` that has a Username in its first line and a Password in its second line. Place that file in the data-folder.

# Usage

Start the tool with `python main.py`. Once the flask-server is started, you can access the WebUI via "127.0.0.1:8085" from the same machine or from any other device within the same network by accessing "<server-IP>:8085" via a web-browser. After changing the content in your `portfolio.csv`-file you might have to reload the webUI or click on the "Load / Refresh Data" button.
  
# Usage with Docker

Please mount a folder containing `portfolio.csv` and optionally the `basic-auth.txt` file as the data folder `/data ` and expose port 8085 or map it to a desired port. After this you can run the container and access the WebUI via "127.0.0.1:8085" from the same machine or from any other device within the same network by accessing "<server-IP>:8085" via a web-browser. After changing the content in your `portfolio.csv`-file you might have to reload the webUI or click on the "Load / Refresh Data" button.
