# Yahoo Finance Client

Asynchronous Yahoo Finance client without returning pandas dataframes.

### TODO
- ~~[x] create postman collection from findings - yfinance urls + openapi spec~~
- ~~[x] create tests within the postman collection~~
- ~~[x] compare to the bruno collection~~
- ~~[x] AsyncClient - get crumb only once~~
    - crumb set as attribute in the constructor: TypeError: __init__() should return None, not 'coroutine'
    - crumb cached_property: RuntimeError: cannot reuse already awaited coroutine
    - fetch crumb via synchronous session - not possible session (cookies) and crumb have to 1:1 (otherwise HTTP401)
- ~~[x] modules as enum~~ - Module.QUOTE_TYPE.value usage is meh
- ~~[x] client as a separate module~~
- [ ] args wrapper decorator
- ~~[x] fetch multiple tickers at once?~~ - used wheerever could
- [ ] get_finance_chart implement period1 and period2
- [ ] (Sync) client
- ~~[x] rest of found postman endpoints?~~
    - ~~[x] finance quote~~
    - ~~[x] finance quote summary market~~
    - ~~[x] finance trending~~
    - ~~[x] finance recommendations~~
    - ~~[x] finance currencies~~
    - ~~[x] finance insights~~
- ~~[x] quoteSummary single modules~~
- ~~[x] modules and types as str, instead of list~~
- [ ] unit tests ??
- [ ] lint, format
- ~~[x] remove finance from method names~~
- [ ] process response method?

```python
import asyncio
import datetime

from src import Stonk, AsyncClient

async def main() -> None:

    start_ts = datetime.datetime(2020, 1, 1).timestamp()
    now_ts = datetime.datetime.now().timestamp()

    aapl = Stonk('AAPL')
    meta = Stonk('NETA')

    aapl_finance_chart_1y = await aapl.get_finance_chart(period_range='1y', interval='1d', events='div,split')
    print(f'{aapl_finance_chart_1y=}\n')
    aapl_finance_chart_ytd = await aapl.get_finance_chart(period_range='ytd', interval='1d', events='div')
    print(f'{aapl_finance_chart_ytd=}\n')
    meta_finance_chart_1mo = await meta.get_finance_chart(period_range='1mo', interval='1d')
    print(f'{meta_finance_chart_1mo=}\n')
    meta_finance_chart_5d = await meta.get_finance_chart(period_range='5d', interval='1h')
    print(f'{meta_finance_chart_5d=}\n')

    aapl_finance_quote_summary_all_modules = await aapl.get_finance_quote_summary_all_modules()
    print(f'{aapl_finance_quote_summary_all_modules=}\n')

    aapl_quote_type = await aapl.get_quote_type()
    print(f'{aapl_quote_type=}\n')

    aapl_asset_profile = await aapl.get_asset_profile()
    print(f'{aapl_asset_profile=}\n')

    aapl_summary_profile = await aapl.get_summary_profile()
    print(f'{aapl_summary_profile=}\n')

    aapl_summary_detail = await aapl.get_summary_detail()
    print(f'{aapl_summary_detail=}\n')

    aapl_income_statement_history = await aapl.get_income_statement_history()
    print(f'{aapl_income_statement_history=}\n')

    aapl_incomeStatementHistoryQuarterly = await aapl.get_income_statement_history_quarterly()
    print(f'{aapl_incomeStatementHistoryQuarterly=}\n')

    aapl_balance_sheet_history = await aapl.get_balance_sheet_history()
    print(f'{aapl_balance_sheet_history=}\n')

    aapl_balance_sheet_history_quarterly = await aapl.get_balance_sheet_history_quarterly()
    print(f'{aapl_balance_sheet_history_quarterly=}\n')

    aapl_cashflow_statement_history = await aapl.get_cashflow_statement_history()
    print(f'{aapl_cashflow_statement_history=}\n')

    aapl_cashflow_statement_history_quarterly = await aapl.get_cashflow_statement_history_quarterly()
    print(f'{aapl_cashflow_statement_history_quarterly=}\n')

    aapl_esg_scores = await aapl.get_esg_scores()
    print(f'{aapl_esg_scores=}\n')

    aapl_price = await aapl.get_price()
    print(f'{aapl_price=}\n')

    aapl_default_key_statistics = await aapl.get_default_key_statistics()
    print(f'{aapl_default_key_statistics=}\n')

    aapl_financial_data = await aapl.get_financial_data()
    print(f'{aapl_financial_data=}\n')

    aapl_calendar_events = await aapl.get_calendar_events()
    print(f'{aapl_calendar_events=}\n')

    aapl_sec_filings = await aapl.get_sec_filings()
    print(f'{aapl_sec_filings=}\n')

    aapl_upgrade_downgrade_history = await aapl.get_upgrade_downgrade_history()
    print(f'{aapl_upgrade_downgrade_history=}\n')

    aapl_institution_ownership = await aapl.get_institution_ownership()
    print(f'{aapl_institution_ownership=}\n')

    aapl_fund_ownership = await aapl.get_fund_ownership()
    print(f'{aapl_fund_ownership=}\n')

    aapl_major_direct_holders = await aapl.get_major_direct_holders()
    print(f'{aapl_major_direct_holders=}\n')

    aapl_major_holders_breakdown = await aapl.get_major_holders_breakdown()
    print(f'{aapl_major_holders_breakdown=}\n')

    aapl_insider_transactions = await aapl.get_insider_transactions()
    print(f'{aapl_insider_transactions=}\n')

    aapl_insider_holders = await aapl.get_insider_holders()
    print(f'{aapl_insider_holders=}\n')

    aapl_net_share_purchase_activity = await aapl.get_net_share_purchase_activity()
    print(f'{aapl_net_share_purchase_activity=}\n')

    aapl_earnings = await aapl.get_earnings()
    print(f'{aapl_earnings=}\n')

    aapl_earnings_history = await aapl.get_earnings_history()
    print(f'{aapl_earnings_history=}\n')

    aapl_earnings_trend = await aapl.get_earnings_trend()
    print(f'{aapl_earnings_trend=}\n')

    aapl_industry_trend = await aapl.get_industry_trend()
    print(f'{aapl_industry_trend=}\n')

    aapl_index_trend = await aapl.get_index_trend()
    print(f'{aapl_index_trend=}\n')

    aapl_sector_trend = await aapl.get_sector_trend()
    print(f'{aapl_sector_trend=}\n')

    aapl_recommendation_trend = await aapl.get_recommendation_trend()
    print(f'{aapl_recommendation_trend=}\n')

    aapl_page_views = await aapl.get_page_views()
    print(f'{aapl_page_views=}\n')

    aapl_ttm_income_stmt = await aapl.get_income_statement(
        frequency='trailing', period1=start_ts, period2=now_ts
    )
    print(f'{aapl_ttm_income_stmt=}\n')
    
    meta_annual_balance_sheet = await meta.get_balance_sheet(frequency='annual')
    print(f'{meta_annual_balance_sheet=}\n')
    
    aapl_quarterly_cash_flow = await aapl.get_cash_flow(frequency='quarterly')
    print(f'{aapl_quarterly_cash_flow=}\n')

    aapl_finance_options = await aapl.get_finance_options()
    print(f'{aapl_finance_options=}\n')

    aapl_finance_search = await aapl.get_finance_search()
    print(f'{aapl_finance_search=}\n')

    yf_client = AsyncClient()

    aapl_finance_chart_1y = await yf_client.get_finance_chart(
        ticker='AAPL', period_range='1y', interval='1d', events='div,split'
    )
    print(f'{aapl_finance_chart_1y=}\n')
    aapl_finance_chart_ytd = await yf_client.get_finance_chart(
        ticker='AAPL', period_range='ytd', interval='1d', events='div'
    )
    print(f'{aapl_finance_chart_ytd=}\n')
    meta_finance_chart_1mo = await yf_client.get_finance_chart(ticker='META', period_range='1mo', interval='1d')
    print(f'{meta_finance_chart_1mo=}\n')
    meta_finance_chart_5d = await yf_client.get_finance_chart(ticker='META', period_range='5d', interval='1h')
    print(f'{meta_finance_chart_5d=}\n')

    aapl_finance_quote_summary = await yf_client.get_finance_quote_summary(
        ticker='AAPL', modules='assetProfile,price,defaultKeyStatistics,calendarEvents'
    )
    print(f'{aapl_finance_quote_summary=}\n')

    aapl_ttm_income_stmt = await yf_client.get_finance_timeseries(
        ticker='AAPL',
        types=['trailingNetIncome', 'trailingPretaxIncome', 'trailingEBIT', 'trailingEBITDA', 'trailingGrossProfit'],
        period1=start_ts,
        period2=now_ts
    )
    print(f'{aapl_ttm_income_stmt=}\n')

    meta_annual_balance_sheet = await yf_client.get_finance_timeseries(ticker='META', types=['annualNetDebt', 'annualTotalDebt'])
    print(f'{meta_annual_balance_sheet=}\n')
    
    aapl_quarterly_cash_flow = await yf_client.get_finance_timeseries(ticker='AAPL', types=['quarterlyFreeCashFlow', 'quarterlyOperatingCashFlow'])
    print(f'{aapl_quarterly_cash_flow=}\n')

    aapl_finance_options = await yf_client.get_finance_options(ticker='AAPL')
    print(f'{aapl_finance_options=}\n')

    aapl_finance_search = await yf_client.get_finance_search(ticker='AAPL')
    print(f'{aapl_finance_search=}\n')

if __name__ == '__main__':
    asyncio.run(main())
```

# gh yfinance
https://github.com/ranaroussi/yfinance

# gh open api
https://github.com/pasdam/yahoo-finance-openapi/blob/main/query2.yml
https://github.com/pasdam/yahoo-finance-openapi/blob/main/query1.yml

# gh yahoo-finance-api-collection (bruno)
https://github.com/Scarvy/yahoo-finance-api-collection
