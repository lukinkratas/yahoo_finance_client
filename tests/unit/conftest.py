import json
import pathlib
from typing import Any

import pytest

FIXTURES_PATH = pathlib.Path(__file__).resolve().parent.joinpath('fixtures')


@pytest.fixture
def mock_chart_json() -> dict[str, Any]:
    """Mock chart response json with data for META, 1y, 1d."""
    return json.loads(FIXTURES_PATH.joinpath('chart.json').read_text())


@pytest.fixture
def mock_quote_json() -> dict[str, Any]:
    """Mock get_quote response json with data for META."""
    return json.loads(FIXTURES_PATH.joinpath('quotes.json').read_text())


@pytest.fixture
def mock_search_json() -> dict[str, Any]:
    """Mock search response json with data for META."""
    return json.loads(FIXTURES_PATH.joinpath('search.json').read_text())


@pytest.fixture
def mock_options_json() -> dict[str, Any]:
    """Mock options response json with data for META."""
    return json.loads(FIXTURES_PATH.joinpath('options.json').read_text())


@pytest.fixture
def mock_recommendations_json() -> dict[str, Any]:
    """Mock recommendations response json with data for META."""
    return json.loads(FIXTURES_PATH.joinpath('recommendations.json').read_text())


@pytest.fixture
def mock_insights_json() -> dict[str, Any]:
    """Mock insights response json with data for META."""
    return json.loads(FIXTURES_PATH.joinpath('insights.json').read_text())


@pytest.fixture
def mock_market_summaries_json() -> dict[str, Any]:
    """Mock market summaries response."""
    return json.loads(FIXTURES_PATH.joinpath('market_summaries.json').read_text())


@pytest.fixture
def mock_trending_json() -> dict[str, Any]:
    """Mock trending response json."""
    return json.loads(FIXTURES_PATH.joinpath('trending.json').read_text())


@pytest.fixture
def mock_currencies_json() -> dict[str, Any]:
    """Mock currencies response json."""
    return json.loads(FIXTURES_PATH.joinpath('currencies.json').read_text())


@pytest.fixture
def mock_quote_summary_all_modules_json() -> dict[str, Any]:
    """Mock quote_summary respons json with all modules data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_all_modules.json').read_text())


@pytest.fixture
def mock_timeseries_income_statement_json() -> dict[str, Any]:
    """Mock timeseries response json with annual income statement data for META."""
    return json.loads(FIXTURES_PATH.joinpath('ts_income_statement.json').read_text())


@pytest.fixture
def mock_timeseries_balance_sheet_json() -> dict[str, Any]:
    """Mock timeseries response json with annual balance sheet data for META."""
    return json.loads(FIXTURES_PATH.joinpath('ts_balance_sheet.json').read_text())


@pytest.fixture
def mock_timeseries_cash_flow_json() -> dict[str, Any]:
    """Mock timeseries response json with annual cash flow data for META."""
    return json.loads(FIXTURES_PATH.joinpath('ts_cash_flow.json').read_text())


@pytest.fixture
def mock_asset_profile_json() -> dict[str, Any]:
    """Mock quote summary response json with asset profile data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_asset_profile.json').read_text())


@pytest.fixture
def mock_quote_type_json() -> dict[str, Any]:
    return json.loads(FIXTURES_PATH.joinpath('qs_quote_type.json').read_text())


@pytest.fixture
def mock_summary_profile_json() -> dict[str, Any]:
    return json.loads(FIXTURES_PATH.joinpath('qs_summary_profile.json').read_text())


@pytest.fixture
def mock_summary_detail_json() -> dict[str, Any]:
    return json.loads(FIXTURES_PATH.joinpath('qs_summary_detail.json').read_text())


@pytest.fixture
def mock_income_statement_history_json() -> dict[str, Any]:
    return json.loads(
        FIXTURES_PATH.joinpath('qs_income_statement_history.json').read_text()
    )


@pytest.fixture
def mock_income_statement_history_quarterly_json() -> dict[str, Any]:
    return json.loads(
        FIXTURES_PATH.joinpath('qs_income_statement_history_quarterly.json').read_text()
    )


@pytest.fixture
def mock_balance_sheet_history_json() -> dict[str, Any]:
    return json.loads(
        FIXTURES_PATH.joinpath('qs_balance_sheet_history.json').read_text()
    )


@pytest.fixture
def mock_balance_sheet_history_quarterly_json() -> dict[str, Any]:
    return json.loads(
        FIXTURES_PATH.joinpath('qs_balance_sheet_history_quarterly.json').read_text()
    )


@pytest.fixture
def mock_cashflow_statement_history_json() -> dict[str, Any]:
    return json.loads(
        FIXTURES_PATH.joinpath('qs_cashflow_statement_history.json').read_text()
    )


@pytest.fixture
def mock_cashflow_statement_history_quarterly_json() -> dict[str, Any]:
    return json.loads(
        FIXTURES_PATH.joinpath(
            'qs_cashflow_statement_history_quarterly.json'
        ).read_text()
    )


@pytest.fixture
def mock_esg_scores_json() -> dict[str, Any]:
    return json.loads(FIXTURES_PATH.joinpath('qs_esg_scores.json').read_text())


@pytest.fixture
def mock_price_json() -> dict[str, Any]:
    return json.loads(FIXTURES_PATH.joinpath('qs_price.json').read_text())


@pytest.fixture
def mock_default_key_statistics_json() -> dict[str, Any]:
    return json.loads(
        FIXTURES_PATH.joinpath('qs_default_key_statistics.json').read_text()
    )


@pytest.fixture
def mock_financial_data_json() -> dict[str, Any]:
    return json.loads(FIXTURES_PATH.joinpath('qs_financial_data.json').read_text())


@pytest.fixture
def mock_calendar_events_json() -> dict[str, Any]:
    return json.loads(FIXTURES_PATH.joinpath('qs_calendar_events.json').read_text())


@pytest.fixture
def mock_sec_filings_json() -> dict[str, Any]:
    return json.loads(FIXTURES_PATH.joinpath('qs_sec_filings.json').read_text())


@pytest.fixture
def mock_upgrade_downgrade_history_json() -> dict[str, Any]:
    return json.loads(
        FIXTURES_PATH.joinpath('qs_upgrade_downgrade_history.json').read_text()
    )


@pytest.fixture
def mock_institution_ownership_json() -> dict[str, Any]:
    return json.loads(
        FIXTURES_PATH.joinpath('qs_institution_ownership.json').read_text()
    )


@pytest.fixture
def mock_fund_ownership_json() -> dict[str, Any]:
    return json.loads(FIXTURES_PATH.joinpath('qs_fund_ownership.json').read_text())


@pytest.fixture
def mock_major_direct_holders_json() -> dict[str, Any]:
    return json.loads(
        FIXTURES_PATH.joinpath('qs_major_direct_holders.json').read_text()
    )


@pytest.fixture
def mock_major_holders_breakdown_json() -> dict[str, Any]:
    return json.loads(
        FIXTURES_PATH.joinpath('qs_major_holders_breakdown.json').read_text()
    )


@pytest.fixture
def mock_insider_transactions_json() -> dict[str, Any]:
    return json.loads(
        FIXTURES_PATH.joinpath('qs_insider_transactions.json').read_text()
    )


@pytest.fixture
def mock_insider_holders_json() -> dict[str, Any]:
    return json.loads(FIXTURES_PATH.joinpath('qs_insider_holders.json').read_text())


@pytest.fixture
def mock_net_share_purchase_activity_json() -> dict[str, Any]:
    return json.loads(
        FIXTURES_PATH.joinpath('qs_net_share_purchase_activity.json').read_text()
    )


@pytest.fixture
def mock_earnings_json() -> dict[str, Any]:
    return json.loads(FIXTURES_PATH.joinpath('qs_earnings.json').read_text())


@pytest.fixture
def mock_earnings_history_json() -> dict[str, Any]:
    return json.loads(FIXTURES_PATH.joinpath('qs_earnings_history.json').read_text())


@pytest.fixture
def mock_earnings_trend_json() -> dict[str, Any]:
    return json.loads(FIXTURES_PATH.joinpath('qs_earnings_trend.json').read_text())


@pytest.fixture
def mock_industry_trend_json() -> dict[str, Any]:
    return json.loads(FIXTURES_PATH.joinpath('qs_industry_trend.json').read_text())


@pytest.fixture
def mock_index_trend_json() -> dict[str, Any]:
    return json.loads(FIXTURES_PATH.joinpath('qs_index_trend.json').read_text())


@pytest.fixture
def mock_sector_trend_json() -> dict[str, Any]:
    return json.loads(FIXTURES_PATH.joinpath('qs_sector_trend.json').read_text())


@pytest.fixture
def mock_recommendation_trend_json() -> dict[str, Any]:
    return json.loads(
        FIXTURES_PATH.joinpath('qs_recommendation_trend.json').read_text()
    )


@pytest.fixture
def mock_page_views_json() -> dict[str, Any]:
    return json.loads(FIXTURES_PATH.joinpath('qs_page_views.json').read_text())
