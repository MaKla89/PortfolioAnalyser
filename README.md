# PortfolioAnalyser

This is a small tool that visually summarizes your porfolio consisting of stocks, ETFs and Crypto-Currencies in a dash-based WebUI.
That WebUI will be accessible on port 8085 of your machine.

# Installation

## Prerequisites

This tool requires "dash", "pandas" and "requests" for python to be installed (via `pip install dash pandas requests`).

### Portfolio-Setup

Please provide a portfolio.csv that contains your portfolio-setup's details: 

  - holdings' names, 
  - trade-symbols, 
  - amount, 
  - type (stock or crypto) and 
  - the invested money for each position)
  
 For further details on this portfolio-configuration take a look at the included demo-portfolio.csv file!
 If no portfolio.csv is provided, the included demo-file will be used for demonstration purposes.
 
### API-Key (for yahoo-finance via RapidAPI.com)
 
Also acquire and provide a rapid-API-key (which is free but requires account-registration at rapidapi.com) in a .txt-file named `api_key.txt` with nothing in it but your api-key. If no `api_key.txt` is provided, the program will not work unless your portfolio does only contain crypto-currencies!

### Where to place these two files
 
Both files (`porfolio.csv` & `api_key.txt`) need to be placed in the same folder as the main.py

# Usage

Start the tool with `python main.py`. Once the flask-server is started, you can access the WebUI via "127.0.0.1:8085" from the same machine or from any other device within the same network by accessing "<server-IP>:8085" via a web-browser.
