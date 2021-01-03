import pandas as pd
import requests


class Portfolio:
    def __init__(self):
        self.crypto_api_url = "https://api.coingecko.com/api/v3/simple/price?ids="
        self.yahoo_api_url = "https://yahoo-finance-low-latency.p.rapidapi.com/v6/finance/quote"
        self.portfolio = pd.DataFrame()
        self.load_portfolio()
        self.total_worth = 0
        self.total_investment = 0
        self.total_profit_loss = 0
        self.total_profit_loss_rel = 0
        self.f = open("api_key.txt", "r")           # Reads your Rapid-API-Key from .txt-File in same directory
        self.api_key = self.f.read()

    def load_portfolio(self):
        try:
            self.portfolio = pd.read_csv("portfolio.csv", sep=";", decimal=",")     # "portfolio.csv" must be provided!
            print("Loading Portfolio-Information from .csv was successful!")

        except FileNotFoundError:
            print("Could not load any stored Portfolio. Will use DEMO-Portfolio!")
            self.portfolio = pd.read_csv("demo-portfolio.csv", sep=";", decimal=",")

    def update_portfolio(self):
        stocks = []
        for index, position in self.portfolio.iterrows():
            if position["Asset Class"] == "Stock" or position["Asset Class"] == "ETF":
                stocks.append(str(position["Symbol"]))
        stocks = ",".join(stocks)

        querystring = {"symbols": str(stocks), "region": "DE"}
        headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': "yahoo-finance-low-latency.p.rapidapi.com"
        }
        try:
            stocks_response = requests.request("GET", self.yahoo_api_url, headers=headers, params=querystring)
            stocks_response = stocks_response.json()

        except Exception:
            print(" ---------- Exception! ---------- ")
            print("Probably a problem with Yahoo-API. See API-response:")
            print(stocks_response)
            print(" -------------------------------- ")

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
                response_segment = next(x for x in stocks_response["quoteResponse"]["result"] if x["symbol"] == position["Symbol"])
                new_price = float(response_segment["regularMarketPrice"])
                self.portfolio.at[index,"Current Price"] = new_price
                current_value = float(float(position["Amount"])*new_price)
                current_value = round(current_value, 2)
                self.portfolio.at[index, "Current Value"] = current_value
                win_loss = current_value - float(position["Investment"])
                win_loss = round(win_loss, 2)
                self.portfolio.at[index, "Profit / Loss"] = win_loss

        self.total_worth = round(self.portfolio.sum()["Current Value"], 2)
        self.total_investment = round(self.portfolio.sum()["Investment"], 2)
        self.total_profit_loss = round(self.portfolio.sum()["Profit / Loss"], 2)
        self.total_profit_loss_rel = (self.total_worth - self.total_investment)/self.total_investment*100
        self.total_profit_loss_rel = round(self.total_profit_loss_rel, 1)


if __name__ == '__main__':
    port = Portfolio()
    port.update_portfolio()
    print(port.portfolio.to_string())
