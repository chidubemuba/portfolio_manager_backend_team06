import yfinance as yf
import pandas as pd


class YfinanceService:
    @classmethod
    def get_stock_data(cls, ticker):
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        return data
    
    
    @classmethod
    def get_current_price(cls, ticker):
        data = cls.get_stock_data(ticker)
        return data['Close'].iloc[-1] if not data.empty else None


    @classmethod
    def get_stock_info(cls, ticker):
        stock = yf.Ticker(ticker)
        return stock.history(period="1mo")