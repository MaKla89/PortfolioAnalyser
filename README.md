# PortfolioAnalyser

This is a small tool that visually summarizes your porfolio consisting of stocks, ETFs and Crypto-Currencies in a dash-based WebUI.
That WebUI will be accessible on port 8085 of your machine.

# Installation

This tool requires "dash", "pandas" and "requests" for python to be installed (via ''pip install dash, pandas, requests'')

# Usage

Please provide a portfolio.csv that contains your portfolio-setup's details: 
  - holdings' names, 
  - trade-symbols, 
  - amount, 
  - type (stock or crypto) and 
  - the invested money for each position)
  
 For details have a look at the included demo-portfolio.csv file
 
 Also acquire and provide a rapid-API-key (which is free but requires registration) in a .txt-file named "api_key.txt" with nothing in it but your api-key.
 
 Both files (porfolio.csv & api_key.txt) need to be placed in the same folder as the main.py
 
 If no api_key.txt is provided, the program will not work. If no portfolio.csv is provided, the included demo-file will be used for demonstration purposes.
 
 Once the flask-server is started, you can access the WebUI via "127.0.0.1:8085" (or from any other device within the same network by accessing "<server-IP>:8085")
