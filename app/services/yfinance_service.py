import os
import csv
import yfinance as yf
import pandas as pd

from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor


from app.models import db
from app.models.stock import Stock

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
        return data['Close'] if not data.empty else None


    @classmethod
    def get_stock_info(cls, ticker):
        stock = yf.Ticker(ticker)
        return stock.history(period="1mo")
    
    @classmethod
    @lru_cache()
    def __populate_data_db(cls):
        with open('app/ressources/russell.csv', 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            
            for row in reader:
                try:
                    if '--' not in (row[0], row[1], row[2], row[8]):
                        db.session.add(
                            Stock(
                                ticker=row[0],
                                name=row[1],
                                asset_class=row[2],
                                sector=row[8]
                            )
                        )
                except Exception as e:
                    print(e)
                    
        db.session.commit()
        
    
    @classmethod
    def __delete_delisted(cls, delisted):
        db.session.query(Stock).filter(Stock.ticker.in_(delisted)).delete(synchronize_session=False)
        db.session.commit()
        
        csv_path = 'app/ressources/russell.csv'
        with open(csv_path, 'r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader if row[0] not in delisted]

        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
                    
    @classmethod
    def get_available_tickers(cls):
        stocks = Stock.query.all()
        
        if not stocks:
            cls.__populate_data_db()
            
        return [s.to_dict() for s in stocks]
    
    @classmethod
    def get_available_tickers_yf(cls):
        stocks = Stock.query.all()
        
        if not stocks:
            cls.__populate_data_db()
            
        data = []
        delisted = []
        for stock in stocks:
            try:
                price = cls.get_current_price(stock.ticker)
            except Exception as e:
                delisted.append(stock.ticker)
                continue
            
            res = stock.to_dict()
            res['price'] = price
            data.append(res)
        
        cls.__delete_delisted(delisted)
                
    
        
        