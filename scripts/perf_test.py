import asyncio
import json
from datetime import datetime

from logging_config import setup_logging

from yafin import Stonk
from yafin.utils import track_time_performance

@track_time_performance()
async def main() -> None:  # noqa: D103
    setup_logging()

    meta = Stonk('META')

    meta_1y_chart = await meta.get_chart(period_range='1y', interval='1d')

    meta_quote = await meta.get_quote()

    meta_quote_summary_all_modules = await meta.get_quote_summary_all_modules()

    meta_quote_type = await meta.get_quote_type()

    meta_asset_profile = await meta.get_asset_profile()

    meta_summary_profile = await meta.get_summary_profile()

    meta_summary_detail = await meta.get_summary_detail()

    meta_income_statement_history = await meta.get_income_statement_history()

    meta_income_statement_history_quarterly = (
        await meta.get_income_statement_history_quarterly()
    )

    meta_balance_sheet_history = await meta.get_balance_sheet_history()

    meta_balance_sheet_history_quarterly = (
        await meta.get_balance_sheet_history_quarterly()
    )

    meta_cashflow_statement_history = await meta.get_cashflow_statement_history()

    meta_cashflow_statement_history_quarterly = (
        await meta.get_cashflow_statement_history_quarterly()
    )

    meta_esg_scores = await meta.get_esg_scores()

    meta_price = await meta.get_price()

    meta_default_key_statistics = await meta.get_default_key_statistics()

    meta_financial_data = await meta.get_financial_data()

    meta_calendar_events = await meta.get_calendar_events()

    meta_sec_filings = await meta.get_sec_filings()

    meta_upgrade_downgrade_history = await meta.get_upgrade_downgrade_history()

    meta_institution_ownership = await meta.get_institution_ownership()

    meta_fund_ownership = await meta.get_fund_ownership()

    meta_major_direct_holders = await meta.get_major_direct_holders()

    meta_major_holders_breakdown = await meta.get_major_holders_breakdown()

    meta_insider_transactions = await meta.get_insider_transactions()

    meta_insider_holders = await meta.get_insider_holders()

    meta_net_share_purchase_activity = await meta.get_net_share_purchase_activity()

    meta_earnings = await meta.get_earnings()

    meta_earnings_history = await meta.get_earnings_history()

    meta_earnings_trend = await meta.get_earnings_trend()

    meta_industry_trend = await meta.get_industry_trend()

    meta_index_trend = await meta.get_index_trend()

    meta_sector_trend = await meta.get_sector_trend()

    meta_recommendation_trend = await meta.get_recommendation_trend()

    meta_page_views = await meta.get_page_views()

    meta_get_income_statement = await meta.get_income_statement(frequency='trailing')

    meta_get_balance_sheet = await meta.get_balance_sheet(
        frequency='annual',
        period1=datetime(2020, 1, 1).timestamp(),
        period2=datetime.now().timestamp(),
    )

    meta_get_cash_flow = await meta.get_cash_flow(frequency='quarterly')

    meta_options = await meta.get_options()

    meta_search = await meta.get_search()

    meta_recommendations = await meta.get_recommendations()

    meta_insights = await meta.get_insights()

if __name__ == '__main__':
    asyncio.run(main())
