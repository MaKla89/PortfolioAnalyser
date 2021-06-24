import pandas as pd
import requests
import yfinance as yf


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

    def load_portfolio(self):
        try:
            self.portfolio = pd.read_csv("portfolio.csv", sep=";", decimal=",")     # "portfolio.csv" must be provided!
            print("Loading portfolio-information from 'portfolio.csv' was successful!")

        except FileNotFoundError:
            print("WARNING: Could not load or find 'portfolio.csv' file, resuming with DEMO-Portfolio!")
            self.portfolio = pd.read_csv("demo-portfolio.csv", sep=";", decimal=",")

    def update_portfolio(self):
        for index, position in self.portfolio.iterrows():

            if position["Asset Class"] == "Crypto":

                try:
                    crypto_response = requests.get((str(self.crypto_api_url) +
                                              str(position["Symbol"]) +
                                              "&vs_currencies=eur"))
                    crypto_response = crypto_response.json()
                    new_price = crypto_response[str(position["Symbol"])]["eur"]

                except Exception:
                    print(" ---------- Exception! ---------- ")
                    print("Probably a problem with CoinGecko-API. See API-response:")
                    print(crypto_response)
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

                ticker = yf.Ticker(ticker=position["Symbol"])
                new_price = float(ticker.info["regularMarketPrice"])
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
        # print(self.total_investment)
        # print(self.total_profit_loss)
        # print(self.total_profit_loss_rel)


if __name__ == '__main__':
    port = Portfolio()
    port.update_portfolio()
    print(port.portfolio.to_string())
