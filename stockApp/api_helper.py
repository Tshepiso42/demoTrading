import requests
import urllib.parse

def stockSearch(symbol):
    API_KEY = ####
    # print(urllib.parse.quote_plus(symbol))
    try:
        response = requests.get(f"https://sandbox.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={API_KEY}")
        response.raise_for_status
    except requests.RequestException:
        return None
    
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None
