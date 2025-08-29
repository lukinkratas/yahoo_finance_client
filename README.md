# YFAS - Yahoo Finance ~~Async~~ Stonks

### TODO
- [ ] create postman collection from findings - yfinance urls + openapi spec
- [ ] create test within the postman collection
- [ ] compare to the bruno collection
- [ ] (Sync) client
- ~~[ ] AsyncClient - get crumb only once~~
    - crumb set as attribute in the constructor: TypeError: __init__() should return None, not 'coroutine'
    - crumb cached_property: RuntimeError: cannot reuse already awaited coroutine
    - fetch crumb via synchronous session - not possible session (cookies) and crumb have to 1:1 (otherwise HTTP401)
- ~~[ ] modules as enum~~ - Module.QUOTE_TYPE.value usage is meh
- [ ] fetch multiple tickers at once?
- [ ] news

# yfinance
https://github.com/ranaroussi/yfinance

# open api
https://github.com/pasdam/yahoo-finance-openapi/blob/main/query2.yml
https://github.com/pasdam/yahoo-finance-openapi/blob/main/query1.yml

# yahoo-finance-api-collection
https://github.com/Scarvy/yahoo-finance-api-collection

# URLs
_QUERY1_URL_ = 'https://query1.finance.yahoo.com'
_BASE_URL_ = 'https://query2.finance.yahoo.com'
_ROOT_URL_ = 'https://finance.yahoo.com'

# CRUMB 
https://query1.finance.yahoo.com/v1/test/getcrumb
https://query2.finance.yahoo.com/v1/test/getcrumb

history:
    url = f"{_BASE_URL_}/v8/finance/chart/{self.ticker}"
    # single symbol
    https://query2.finance.yahoo.com/v8/finance/chart/META?range=1mo&interval=1d
    # only close price
    https://query2.finance.yahoo.com/v8/finance/spark?symbols=META,AAPL&range=1mo&interval=1d
    # only close price
    https://query2.finance.yahoo.com/v7/finance/spark?symbols=META,AAPL&range=1mo&interval=1d
    # no price info
    https://query2.finance.yahoo.com/v7/finance/quote?symbols=META,AAPL&crumb=ipmS.n8I6Bi

info:
    _QUOTE_SUMMARY_URL_ = f"{_BASE_URL_}/v10/finance/quoteSummary/"
    modules = ['financialData', 'quoteType', 'defaultKeyStatistics', 'assetProfile', 'summaryDetail']
    params_dict = {"modules": modules, "corsDomain": "finance.yahoo.com", "symbol": self._symbol, "formatted": "false"}

    https://query2.finance.yahoo.com/v10/finance/quoteSummary/META?modules=financialData,quoteType,defaultKeyStatistics,assetProfile,summaryDetail&formatted=false&crumb=ipmS.n8I6Bi

income_stmt
balance_sheet
cash_flow
    timescale_translation = {"yearly": "annual", "quarterly": "quarterly", "trailing": "trailing"}
    timescale = timescale_translation[timescale]

    # Step 2: construct url:
    ts_url_base = f"https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{self._symbol}?symbol={self._symbol}"
    url = ts_url_base + "&type=" + ",".join([timescale + k for k in keys])
    # Yahoo returns maximum 4 years or 5 quarters, regardless of start_dt:
    start_ts = datetime.datetime(2016, 12, 31).timestamp()
    start_ts = datetime.today.timestamp()
    end = pd.Timestamp.utcnow().ceil("D")
    url += f"&period1={int(start_st)}&period2={int(end.timestamp())}"

    https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/META?symbol=META&type=quarterlyEBIT&period1=1483138800&period2=1755475200

    https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/META?symbol=META&type=quarterlyEBIT,annualEBIT,trailingEBIT&period1=1483138800&period2=1755475200

earnings_estimates
growth_estimates
revenue_estimates

price_targets

upgrades_downgrades

options
    url = f"{_BASE_URL_}/v7/finance/options/{self.ticker}"
    https://query2.finance.yahoo.com/v7/finance/options/META?crumb=ipmS.n8I6Bi

news
    count = 10
    tab = "news"
    tab_queryrefs = {
        "all": "newsAll",
        "news": "latestNews",
        "press releases": "pressRelease",
    }

    query_ref = tab_queryrefs.get(tab.lower())
    
    query_ref = "latestNews"

    url = f"{_ROOT_URL_}/xhr/ncp?queryRef={query_ref}&serviceKey=ncp_fin"
    payload = {"serviceConfig": {"snippetCount": count, "s": ["AAPL"]}}
    data = self._data.post(url, body=payload)

    data = data.json()

    news = data.get("data", {}).get("tickerStream", {}).get("stream", [])

    return [article for article in news if not article.get('ad', [])]

summary:
    https://query2.finance.yahoo.com
    _QUOTE_SUMMARY_URL_ = f"{_BASE_URL_}/v10/finance/quoteSummary/"
    modules = ','.join(["quoteType", "summaryProfile", "topHoldings", "fundProfile"])
    params_dict = {"modules": modules, "corsDomain": "finance.yahoo.com", "symbol": self._symbol, "formatted": "false"}
    result = self._data.get_raw_json(_QUOTE_SUMMARY_URL_+self._symbol, params=params_dict)

    https://query2.finance.yahoo.com/v10/finance/quoteSummary/META?modules=quoteType,summaryProfile,topHoldings,fundProfile&corsDomain=finance.yahoo.com&symbol=META&formatted=false&crumb=ipmS.n8I6Bi

    modules:
        default:
            - calendarEvents
            - defaultKeyStatistics
            - details
            - earnings
            - esgScores
            - summaryProfile
        enum:
            - [x] details - does not work for stonks
            - [x] fundProfile - does not work for stonks
            - [x] quoteType
            - [x] assetProfile # summaryProfile + company officers
            - [x] summaryProfile # contains general information about the company
            - [x] summaryDetail # prices + volume + market cap + etc
            - [x] incomeStatementHistory - not use via finance/quoteSummary, finance/timeseries is much better
            - [x] incomeStatementHistoryQuarterly - not use via finance/quoteSummary, finance/timeseries is much better
            - [x] balanceSheetHistory - not use via finance/quoteSummary, finance/timeseries is much better
            - [x] balanceSheetHistoryQuarterly - not use via finance/quoteSummary, finance/timeseries is much better
            - [x] cashflowStatementHistory - not use via finance/quoteSummary, finance/timeseries is much better
            - [x] cashflowStatementHistoryQuarterly - not use via finance/quoteSummary, finance/timeseries is much better
            - [x] esgScores # Environmental, social, and governance (ESG) scores, sustainability and ethical performance of companies
            - price # current prices
            - defaultKeyStatistics # KPIs (PE, enterprise value, EPS, EBITA, and more)
            - financialData # Financial KPIs (revenue, gross margins, operating cash flow, free cash flow, and more)
            - [x] calendarEvents # future earnings date
            - [x] secFilings # SEC filings, such as 10K and 10Q reports
            - [x] upgradeDowngradeHistory # upgrades and downgrades that analysts have given a company's stock
            - [x] institutionOwnership # institutional ownership, holders and shares outstanding
            - [x] fundOwnership # mutual fund ownership, holders and shares outstanding
            - [x] majorDirectHolders
            - [x] majorHoldersBreakdown
            - [x] insiderTransactions # insider transactions, such as the number of shares bought and sold by company executives
            - [x] insiderHolders # insider holders, such as the number of shares held by company executives
            - [x] netSharePurchaseActivity # net share purchase activity, such as the number of shares bought and sold by company executives
            - [x] earnings # earnings history
            - [x] earningsHistory
            - [x] earningsTrend
            - [x] industryTrend
            - [x] indexTrend
            - [x] sectorTrend
            - [x] recommendationTrend
            - [x] futuresChain

holders:
    _QUOTE_SUMMARY_URL_ = f"{_BASE_URL_}/v10/finance/quoteSummary"
    class Holders:
    _SCRAPE_URL_ = 'https://finance.yahoo.com/quote'
    https://query2.finance.yahoo.com/v10/finance/quoteSummary/META

ticker:
    url = f"{_BASE_URL_}/v7/finance/options/{self.ticker}"
    https://query2.finance.yahoo.com/v7/finance/options/META

sector:
    self._query_url: str = f'{_QUERY_URL_}/sectors/{self._key}'

industry:
    self._query_url = f'{_QUERY_URL_}/industries/{self._key}'

fundamentals:
    ts_url_base = f"https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{self._symbol…
    url = ts_url_base + "&type=" + ",".join([timescale + k for k in keys])
    url += f"&period1={int(start_dt.timestamp())}&period2={int(end.timestamp())}"
    json_str = self._data.cache_get(url=url).text

analysis:
    result = self._data.get_raw_json(_QUOTE_SUMMARY_URL_ + f"/{self._symbol}", params=params_dict)

ALL_MODULES = details,fundProfile,quoteType,assetProfile,summaryProfile,summaryDetail,incomeStatementHistory,incomeStatementHistoryQuarterly,balanceSheetHistory,balanceSheetHistoryQuarterly,cashflowStatementHistory,cashflowStatementHistoryQuarterly,esgScores,price,defaultKeyStatistics,financialData,calendarEvents,secFilings,upgradeDowngradeHistory,institutionOwnership,fundOwnership,majorDirectHolders,majorHoldersBreakdown,insiderTransactions,insiderHolders,netSharePurchaseActivity,earnings,earningsHistory,earningsTrend,industryTrend,indexTrend,sectorTrend,recommendationTrend,futuresChain,pageViews,topHoldings,fundPerformance

INCOME_STMT_TYPES = annualTaxEffectOfUnusualItems,annualTaxRateForCalcs,annualNormalizedEBITDA,annualNormalizedDilutedEPS,annualNormalizedBasicEPS,annualTotalUnusualItems,annualTotalUnusualItemsExcludingGoodwill,annualNetIncomeFromContinuingOperationNetMinorityInterest,annualReconciledDepreciation,annualReconciledCostOfRevenue,annualEBITDA,annualEBIT,annualNetInterestIncome,annualInterestExpense,annualInterestIncome,annualContinuingAndDiscontinuedDilutedEPS,annualContinuingAndDiscontinuedBasicEPS,annualNormalizedIncome,annualNetIncomeFromContinuingAndDiscontinuedOperation,annualTotalExpenses,annualRentExpenseSupplemental,annualReportedNormalizedDilutedEPS,annualReportedNormalizedBasicEPS,annualTotalOperatingIncomeAsReported,annualDividendPerShare,annualDilutedAverageShares,annualBasicAverageShares,annualDilutedEPS,annualDilutedEPSOtherGainsLosses,annualTaxLossCarryforwardDilutedEPS,annualDilutedAccountingChange,DilutedExtraordinary,annualDilutedDiscontinuousOperations,annualDilutedContinuousOperations,annualBasicEPS,annualBasicEPSOtherGainsLosses,annualTaxLossCarryforwardBasicEPS,annualBasicAccountingChange,annualBasicExtraordinary,annualBasicDiscontinuousOperations,annualBasicContinuousOperations,annualDilutedNIAvailtoComStockholders,annualAverageDilutionEarnings,annualNetIncomeCommonStockholders,annualOtherunderPreferredStockDividend,annualPreferredStockDividends,annualNetIncome,annualMinorityInterests,annualNetIncomeIncludingNoncontrollingInterests,annualNetIncomeFromTaxLossCarryforward,annualNetIncomeExtraordinary,annualNetIncomeDiscontinuousOperations,annualNetIncomeContinuousOperations,annualEarningsFromEquityInterestNetOfTax,annualTaxProvision,annualPretaxIncome,annualOtherIncomeExpense,annualOtherNonOperatingIncomeExpenses,annualSpecialIncomeCharges,annualGainOnSaleOfPPE,annualGainOnSaleOfBusiness,annualOtherSpecialCharges,annualWriteOff,annualImpairmentOfCapitalAssets,annualRestructuringAndMergernAcquisition,annualSecuritiesAmortization,annualEarningsFromEquityInterest,annualGainOnSaleOfSecurity,annualNetNonOperatingInterestIncomeExpense,annualTotalOtherFinanceCost,annualInterestExpenseNonOperating,annualInterestIncomeNonOperating,annualOperatingIncome,annualOperatingExpense,annualOtherOperatingExpenses,annualOtherTaxes,annualProvisionForDoubtfulAccounts,annualDepreciationAmortizationDepletionIncomeStatement,annualDepletionIncomeStatement,DepreciationAndAmortizationInIncomeStatement,annualAmortization,annualAmortizationOfIntangiblesIncomeStatement,annualDepreciationIncomeStatement,annualResearchAndDevelopment,annualSellingGeneralAndAdministration,annualSellingAndMarketingExpense,annualGeneralAndAdministrativeExpense,annualOtherGandA,annualInsuranceAndClaims,annualRentAndLandingFees,annualSalariesAndWages,annualGrossProfit,annualCostOfRevenue,annualTotalRevenue,annualExciseTaxes,annualOperatingRevenue,annualLossAdjustmentExpense,annualNetPolicyholderBenefitsAndClaims,annualPolicyholderBenefitsGross,annualPolicyholderBenefitsCeded,annualOccupancyAndEquipment,annualProfessionalExpenseAndContractServicesExpense,OtherNonInterestExpense

BALANCE_SHEET_TYPE = annualTreasurySharesNumber,annualPreferredSharesNumber,annualOrdinarySharesNumber' annualShareIssued,annualNetDebt,annualTotalDebt,annualTangibleBookValue,annualInvestedCapital,annualWorkingCapital,annualNetTangibleAssets,annualCapitalLeaseObligations,annualCommonStockEquity,annualPreferredStockEquity,annualTotalCapitalization,annualTotalEquityGrossMinorityInterest,annualMinorityInterest,annualStockholdersEquity,annualOtherEquityInterest,annualGainsLossesNotAffectingRetainedEarnings,annualOtherEquityAdjustments,annualFixedAssetsRevaluationReserve,annualForeignCurrencyTranslationAdjustments,annualMinimumPensionLiabilities,annualUnrealizedGainLoss,annualTreasuryStock,annualRetainedEarnings,annualAdditionalPaidInCapital,annualCapitalStock,annualOtherCapitalStock,annualCommonStock,annualPreferredStock,annualTotalPartnershipCapital,annualGeneralPartnershipCapital,annualLimitedPartnershipCapital,annualTotalLiabilitiesNetMinorityInterest,annualTotalNonCurrentLiabilitiesNetMinorityInterest,annualOtherNonCurrentLiabilities,annualLiabilitiesHeldforSaleNonCurrent,annualRestrictedCommonStock,annualPreferredSecuritiesOutsideStockEquity,annualDerivativeProductLiabilities,annualEmployeeBenefits,annualNonCurrentPensionAndOtherPostretirementBenefitPlans,annualNonCurrentAccruedExpenses,annualDuetoRelatedPartiesNonCurrent,annualTradeandOtherPayablesNonCurrent,annualNonCurrentDeferredLiabilities,annualNonCurrentDeferredRevenue,annualNonCurrentDeferredTaxesLiabilities,annualLongTermDebtAndCapitalLeaseObligation,annualLongTermCapitalLeaseObligation,annualLongTermDebt,annualLongTermProvisions,annualCurrentLiabilities,annualOtherCurrentLiabilities,annualCurrentDeferredLiabilities,annualCurrentDeferredRevenue,annualCurrentDeferredTaxesLiabilities,annualCurrentDebtAndCapitalLeaseObligation,annualCurrentCapitalLeaseObligation,annualCurrentDebt,annualOtherCurrentBorrowings,annualLineOfCredit,annualCommercialPaper,annualCurrentNotesPayable,annualPensionandOtherPostRetirementBenefitPlansCurrent,annualCurrentProvisions,annualPayablesAndAccruedExpenses,annualCurrentAccruedExpenses,annualInterestPayable,annualPayables,annualOtherPayable,annualDuetoRelatedPartiesCurrent,annualDividendsPayable,annualTotalTaxPayable,annualIncomeTaxPayable,annualAccountsPayable,annualTotalAssets,annualTotalNonCurrentAssets,annualOtherNonCurrentAssets,annualDefinedPensionBenefit,annualNonCurrentPrepaidAssets,annualNonCurrentDeferredAssets,annualNonCurrentDeferredTaxesAssets,annualDuefromRelatedPartiesNonCurrent,annualNonCurrentNoteReceivables,annualNonCurrentAccountsReceivable,annualFinancialAssets,annualInvestmentsAndAdvances,annualOtherInvestments,annualInvestmentinFinancialAssets,annualHeldToMaturitySecurities,annualAvailableForSaleSecurities,annualFinancialAssetsDesignatedasFairValueThroughProfitorLossTotal,annualTradingSecurities,annualLongTermEquityInvestment,annualInvestmentsinJointVenturesatCost,annualInvestmentsInOtherVenturesUnderEquityMethod,annualInvestmentsinAssociatesatCost,annualInvestmentsinSubsidiariesatCost,annualInvestmentProperties,annualGoodwillAndOtherIntangibleAssets,annualOtherIntangibleAssets,annualGoodwill,annualNetPPE,annualAccumulatedDepreciation,annualGrossPPE,annualLeases,annualConstructionInProgress,annualOtherProperties,annualMachineryFurnitureEquipment,annualBuildingsAndImprovements,annualLandAndImprovements,annualProperties,annualCurrentAssets,annualOtherCurrentAssets,annualHedgingAssetsCurrent,annualAssetsHeldForSaleCurrent,annualCurrentDeferredAssets,annualCurrentDeferredTaxesAssets,annualRestrictedCash,annualPrepaidAssets,annualInventory,annualInventoriesAdjustmentsAllowances,annualOtherInventories,annualFinishedGoods,annualWorkInProcess,annualRawMaterials,annualReceivables,annualReceivablesAdjustmentsAllowances,annualOtherReceivables,annualDuefromRelatedPartiesCurrent,annualTaxesReceivable,annualAccruedInterestReceivable,annualNotesReceivable,annualLoansReceivable,annualAccountsReceivable,annualAllowanceForDoubtfulAccountsReceivable,annualGrossAccountsReceivable,annualCashCashEquivalentsAndShortTermInvestments,annualOtherShortTermInvestments,annualCashAndCashEquivalents,annualCashEquivalents,annualCashFinancial,annualCashCashEquivalentsAndFederalFundsSold

CASH_FLOW_TYPES = annualForeignSales,annualDomesticSales,annualAdjustedGeographySegmentData,annualFreeCashFlow,annualRepurchaseOfCapitalStock,annualRepaymentOfDebt,annualIssuanceOfDebt,annualIssuanceOfCapitalStock,annualCapitalExpenditure,annualInterestPaidSupplementalData,annualIncomeTaxPaidSupplementalData,annualEndCashPosition,annualOtherCashAdjustmentOutsideChangeinCash,annualBeginningCashPosition,annualEffectOfExchangeRateChanges,annualChangesInCash,annualOtherCashAdjustmentInsideChangeinCash,annualCashFlowFromDiscontinuedOperation,annualFinancingCashFlow,annualCashFromDiscontinuedFinancingActivities,annualCashFlowFromContinuingFinancingActivities,annualNetOtherFinancingCharges,annualInterestPaidCFF,annualProceedsFromStockOptionExercised,annualCashDividendsPaid,annualPreferredStockDividendPaid,annualCommonStockDividendPaid,annualNetPreferredStockIssuance,annualPreferredStockPayments,annualPreferredStockIssuance,annualNetCommonStockIssuance,annualCommonStockPayments,annualCommonStockIssuance,annualNetIssuancePaymentsOfDebt,annualNetShortTermDebtIssuance,annualShortTermDebtPayments,annualShortTermDebtIssuance,annualNetLongTermDebtIssuance,annualLongTermDebtPayments,annualLongTermDebtIssuance,annualInvestingCashFlow,annualCashFromDiscontinuedInvestingActivities,annualCashFlowFromContinuingInvestingActivities,annualNetOtherInvestingChanges,annualInterestReceivedCFI,annualDividendsReceivedCFI,annualNetInvestmentPurchaseAndSale,annualSaleOfInvestment,annualPurchaseOfInvestment,annualNetInvestmentPropertiesPurchaseAndSale,annualSaleOfInvestmentProperties,annualPurchaseOfInvestmentProperties,annualNetBusinessPurchaseAndSale,annualSaleOfBusiness,annualPurchaseOfBusiness,annualNetIntangiblesPurchaseAndSale,annualSaleOfIntangibles,annualPurchaseOfIntangibles,annualNetPPEPurchaseAndSale,annualSaleOfPPE,annualPurchaseOfPPE,annualCapitalExpenditureReported,annualOperatingCashFlow,annualCashFromDiscontinuedOperatingActivities,annualCashFlowFromContinuingOperatingActivities,annualTaxesRefundPaid,annualInterestReceivedCFO,annualInterestPaidCFO,annualDividendReceivedCFO,annualDividendPaidCFO,annualChangeInWorkingCapital,annualChangeInOtherWorkingCapital,annualChangeInOtherCurrentLiabilities,annualChangeInOtherCurrentAssets,annualChangeInPayablesAndAccruedExpense,annualChangeInAccruedExpense,annualChangeInInterestPayable,annualChangeInPayable,annualChangeInDividendPayable,annualChangeInAccountPayable,annualChangeInTaxPayable,annualChangeInIncomeTaxPayable,annualChangeInPrepaidAssets,annualChangeInInventory,annualChangeInReceivables,annualChangesInAccountReceivables,annualOtherNonCashItems,annualExcessTaxBenefitFromStockBasedCompensation,annualStockBasedCompensation,annualUnrealizedGainLossOnInvestmentSecurities,annualProvisionandWriteOffofAssets,annualAssetImpairmentCharge,annualAmortizationOfSecurities,annualDeferredTax,annualDeferredIncomeTax,annualDepreciationAmortizationDepletion,annualDepletion,annualDepreciationAndAmortization,annualAmortizationCashFlow,annualAmortizationOfIntangibles,annualDepreciation,annualOperatingGainsLosses,annualPensionAndEmployeeBenefitExpense,annualEarningsLossesFromEquityInvestments,annualGainLossOnInvestmentSecurities,annualNetForeignCurrencyExchangeGainLoss,annualGainLossOnSaleOfPPE,annualGainLossOnSaleOfBusiness,annualNetIncomeFromContinuingOperations,annualCashFlowsfromusedinOperatingActivitiesDirect,annualTaxesRefundPaidDirect,annualInterestReceivedDirect,annualInterestPaidDirect,annualDividendsReceivedDirect,annualDividendsPaidDirect,annualClassesofCashPayments,annualOtherCashPaymentsfromOperatingActivities,annualPaymentsonBehalfofEmployees,annualPaymentstoSuppliersforGoodsandServices,annualClassesofCashReceiptsfromOperatingActivities,annualOtherCashReceiptsfromOperatingActivities,annualReceiptsfromGovernmentGrants,annualReceiptsfromCustomers
