import yfinance as yf
import pandas as pd


class YFinanceService:
    @classmethod
    def get_stock_data(cls, ticker):
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        
        if data.empty:
            raise KeyError(f"Ticker: {ticker} not found in market")
        
        return data.iloc[0]
    
    
    @classmethod
    def get_current_price(cls, ticker):
        data = cls.get_stock_data(ticker)
        print(data, ticker)
        return data['Close'] if not data.empty else None


    @classmethod
    def get_stock_info(cls, ticker):
        stock = yf.Ticker(ticker)
        return stock.history(period="1mo")
    
    
    @classmethod
    def get_available_tickers(cls):
        #TODO: Available Tickers from CSV
        pass