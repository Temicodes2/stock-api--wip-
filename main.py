
import yfinance as yf
dat = yf.Ticker("MSFT")



print(dat.info)



from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
#from typing import Optional, List
#from newspaper import Article
#import httpx
#import traceback

app = FastAPI(
    title="stockshock",
    description="stock api"
)


class scraperequest(BaseModel):
    name: str


class currentstockprice(BaseModel):
    stockname: str
    stockprice: float

class comparestockprice(BaseModel):
    firststock: str
    secondstock: str
    firststockprice: float
    secondstockprice: float
    pricedifference: str

@app.post("/v1/getcurrentprice/{stockname}", response_model=currentstockprice)
async def getcurrentprice(stockname: str):
    try:
        dat = yf.Ticker(stockname)
        print(dat.info["regularMarketPrice"])

        return currentstockprice(stockname=dat.info["symbol"], stockprice=dat.info["regularMarketPrice"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/v1/comparestocks/{stockname}/{secondstock}", response_model=comparestockprice)
async def comparestocks(stockname: str, secondstock: str):
    try:
        dat1 = yf.Ticker(stockname)
        dat2 = yf.Ticker(secondstock)
        print(dat1.info["previousClose"])
        print(dat2.info["previousClose"])

        return comparestockprice(
            firststock=dat1.info["symbol"],
            secondstock=dat2.info["symbol"],
            firststockprice=dat1.info["previousClose"],
            secondstockprice=dat2.info["previousClose"],
            pricedifference="~" + str(round(abs(dat1.info["previousClose"] - dat2.info["previousClose"])))  
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

