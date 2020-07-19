# Comparable Companies
These scripts were originally created to automate the comps process (web scraping the information from various sources). It would do all the calculations automatically and append the information to a Company object.

## comps.py
- Place the script in your folder
- `from comps import Company`
  - This is the main class that does all backend calculations and scrapes information
- Creating a company object
  - `apple = Company('AAPL')`
  - That's it! The class will automatically run scrapers to get information about the stock
- Attributes of the Company object
  - market_cap
  - eps
  - debt_to_equity
  - beta
  - preferred_stock
  - minority_interest
  - total_debt
  - cash_and_cash_equivalents
  - shares_outstanding
  - revenue
  - fcf
  - ebitda
  - ebit
  - net_income
  - enterprise_value
  - price_per_share 
  - price_to_earnings
  - ev_to_revenue
  - ev_to_ebitda
  - ev_to_ebit
  - ev_to_fcf
- Accessing attributes
  - `apple = Company('AAPL')`
  - 'apple_info = apple.ev_to_fcf'
  - That's it! You automatically have all the financial metrics at your fingertips If you have a suggestion or find a bug, reach out to me and we can make this better!

  
