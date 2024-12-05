import pandas as pd
import requests
from yahoofinancials import YahooFinancials


class Portfolio:
    def __init__(self):
        self.crypto_api_url = "https://api.coingecko.com/api/v3/simple/price?ids="
        self.portfolio = pd.DataFrame()
        self.load_portfolio()
        self.total_worth = 0
        self.total_investment = 0
        self.total_profit_loss = 0
        self.total_profit_loss_rel = 0
        self.total_realized_pl = 0

    def get_price(self, symbol):

        try:
            price_yf = YahooFinancials(symbol).get_current_price()

        except Exception as e:
            print(f"Getting new price for {symbol} did fail. Error-Message:")
            print(e)

        return price_yf

    def load_portfolio(self):
        try:
            self.portfolio = pd.read_csv("data/portfolio.csv", sep=";", decimal=",")     # "portfolio.csv" must be provided!
            print("Loading portfolio-information from 'portfolio.csv' was successful!")

        except FileNotFoundError:
            print("WARNING: Could not load or find 'portfolio.csv' file, resuming with DEMO-Portfolio!")
            self.portfolio = pd.read_csv("data/demo-portfolio.csv", sep=";", decimal=",")

    def update_portfolio(self):
        cryptos = []
        stocks = []

        # Create lists of stock- and crypto-symbols to request prices for later:
        for index, position in self.portfolio.iterrows():

            if position["Asset Class"] == "Crypto":
                cryptos.append(position["Symbol"])

            elif position["Asset Class"] == "Stock" or position["Asset Class"] == "ETF":
                stocks.append(position["Symbol"])

        # Requesting current prices for all cryptos in one request:
        crypto_request_url = str(self.crypto_api_url)

        for crypto in cryptos:
            crypto_request_url = crypto_request_url + str(crypto) + "%2C"

        crypto_request_url = crypto_request_url[:-3]
        crypto_request_url = crypto_request_url + "&vs_currencies=eur"
        # print("Crypto-Request-URL:")
        # print(crypto_request_url)

        try:
            crypto_response = requests.get(crypto_request_url)
        except Exception:
            print(" ---------- Exception! ---------- ")
            print("Probably a problem with CoinGecko-API. See API-response:")
            print(crypto_response)
            print(" -------------------------------- ")

        crypto_new_prices = crypto_response.json()
        # print("Crypto Response:")
        # print(crypto_new_prices)
        # print(crypto_new_prices['bitcoin']['eur'])


        # Enter new prices into main asset DB:
        for index, position in self.portfolio.iterrows():
            if position["Asset Class"] == "Crypto":
                try:
                    new_price = crypto_new_prices[str(position["Symbol"])]["eur"]

                except Exception:
                    print(" ---------- Exception! ---------- ")
                    print(" A problem occured in mapping new crypto prices from API response")
                    print(" -------------------------------- ")
                    new_price = 0

                new_price = float(new_price)
                self.portfolio.at[index,"Current Price"] = new_price
                current_value = float(float(position["Amount"])*new_price)
                current_value = round(current_value, 2)
                self.portfolio.at[index, "Current Value"] = current_value
                win_loss = current_value - float(position["Investment"])
                win_loss = round(win_loss, 2)
                self.portfolio.at[index, "Profit / Loss"] = win_loss

            elif position["Asset Class"] == "Stock" or position["Asset Class"] == "ETF":
                new_price = self.get_price(position["Symbol"])
                self.portfolio.at[index,"Current Price"] = new_price
                current_value = float(float(position["Amount"])*new_price)
                current_value = round(current_value, 2)
                self.portfolio.at[index, "Current Value"] = current_value
                win_loss = current_value - float(position["Investment"])
                win_loss = round(win_loss, 2)
                self.portfolio.at[index, "Profit / Loss"] = win_loss

            elif position["Asset Class"] == "Cash":
                new_price = 1.0
                self.portfolio.at[index,"Current Price"] = new_price
                current_value = float(float(position["Amount"])*new_price)
                current_value = round(current_value, 2)
                self.portfolio.at[index, "Current Value"] = current_value
                win_loss = current_value - float(position["Investment"])
                win_loss = round(win_loss, 2)
                self.portfolio.at[index, "Profit / Loss"] = win_loss

        self.total_worth = round(self.portfolio.sum()["Current Value"], 2)
        self.total_investment = round(self.portfolio.sum()["Investment"], 2)
        self.total_realized_pl = round(self.portfolio.sum()["Realized P/L"], 2)
        self.total_profit_loss = round(self.portfolio.sum()["Profit / Loss"] + self.total_realized_pl, 2)
        self.total_profit_loss_rel = (self.total_worth + self.total_realized_pl - self.total_investment) /self.total_investment*100
        self.total_profit_loss_rel = round(self.total_profit_loss_rel, 1)


if __name__ == '__main__':
    port = Portfolio()
    port.update_portfolio()
    print(port.portfolio.to_string())
