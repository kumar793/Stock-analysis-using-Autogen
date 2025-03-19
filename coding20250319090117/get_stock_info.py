# filename: get_stock_info.py
import yfinance as yf
import requests
from bs4 import BeautifulSoup

def get_company_name_and_ticker(company_name):
    search_query = f"{company_name} stock ticker NSE"
    try:
        url = f"https://www.google.com/search?q={search_query}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        ticker_element = soup.find('div', {'class': 'HfMth'})
        if ticker_element:
            ticker = ticker_element.text.strip()
            return company_name, ticker
        else:
            print(f"Could not find ticker for {company_name} using web scraping. Inspect the Google Search page.")
    except Exception as e:
        print(f"Error retrieving ticker for {company_name} using web scraping: {e}")

    return None, None

dlf_name = "DLF"
bajaj_healthcare_name = "BAJAJ HEALTHCARE"

dlf_full_name, dlf_ticker = get_company_name_and_ticker(dlf_name)
bajaj_healthcare_full_name, bajaj_healthcare_ticker = get_company_name_and_ticker(bajaj_healthcare_name)

print(f"DLF Name: {dlf_full_name}")
print(f"DLF Ticker: {dlf_ticker}")
print(f"BAJAJ HEALTHCARE Name: {bajaj_healthcare_full_name}")
print(f"BAJAJ HEALTHCARE Ticker: {bajaj_healthcare_ticker}")