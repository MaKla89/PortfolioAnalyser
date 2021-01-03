# PortfolioAnalyser

This is a small tool that visually summarizes your portfolio consisting of stocks, ETFs and crypto-currencies in a dash-based WebUI.
That WebUI will be accessible on port 8085 of your machine.

<img width="400" alt="Demo" align="center" src="https://user-images.githubusercontent.com/33317175/103465347-edeb6100-4d3a-11eb-85dd-c3a786cc3847.PNG">

# Installation

## Prerequisites

This tool requires "dash", "pandas" and "requests" for python to be installed (via `pip install dash pandas requests`).

### Portfolio-Setup

Please provide a portfolio.csv that contains your portfolio-setup's details: 

  - holdings' names, 
  - trade-symbols, 
  - amount, 
  - asset type (Stock, ETF or Crypto) and 
  - the invested money for each position)
  
For further details on this portfolio-configuration take a look at the included demo-portfolio.csv file!
If no portfolio.csv is provided, the included demo-file will be used for demonstration purposes.
 
### API-Key (for yahoo-finance via RapidAPI.com)
 
Also acquire and provide a rapid-API-key (which is free but requires account-registration at rapidapi.com) in a .txt-file named `api_key.txt` with nothing in it but your api-key. If no `api_key.txt` is provided, the program will not work unless your portfolio does only contain crypto-currencies!

### Where to place these two files
 
Both files (`portfolio.csv` & `api_key.txt`) need to be placed in the same folder as the main.py

# Usage

Start the tool with `python main.py`. Once the flask-server is started, you can access the WebUI via "127.0.0.1:8085" from the same machine or from any other device within the same network by accessing "<server-IP>:8085" via a web-browser. After changing the content in your `portfolio.csv`-file you might have to reload the webUI or click on the "Load / Refresh Data" button.
  
# Usage with Docker

Please mount your `portfolio.csv` & `api_key.txt` files directly into the root folder `/ ` and expose port 8085 or map it to a desired port. After this you can run the container and access the WebUI via "127.0.0.1:8085" from the same machine or from any other device within the same network by accessing "<server-IP>:8085" via a web-browser. After changing the content in your `portfolio.csv`-file you might have to reload the webUI or click on the "Load / Refresh Data" button.
