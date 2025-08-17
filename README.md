# YFAS - Yahoo Finance ~~Async~~ Stonks

### TODO
- [ ] (Sync) client
- ~~[ ] AsyncClient - get crumb only once~~
    - crumb set as attribute in the constructor: TypeError: __init__() should return None, not 'coroutine'
    - crumb cached_property: RuntimeError: cannot reuse already awaited coroutine
    - fetch crumb via synchronous session - not possible session (cookies) and crumb have to 1:1 (otherwise HTTP401)
- ~~[ ] modules as enum~~ - Module.QUOTE_TYPE.value usage is meh
- [ ] fetch multiple tickers at once?

https://github.com/ranaroussi/yfinance

https://github.com/pasdam/yahoo-finance-openapi/blob/main/query2.yml
https://github.com/pasdam/yahoo-finance-openapi/blob/main/query1.yml

_QUERY1_URL_ = 'https://query1.finance.yahoo.com'
_BASE_URL_ = 'https://query2.finance.yahoo.com'
_ROOT_URL_ = 'https://finance.yahoo.com'

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

fundamentals_keys = {
    'financials': ["TaxEffectOfUnusualItems", "TaxRateForCalcs", "NormalizedEBITDA", "NormalizedDilutedEPS",
                   "NormalizedBasicEPS", "TotalUnusualItems", "TotalUnusualItemsExcludingGoodwill",
                   "NetIncomeFromContinuingOperationNetMinorityInterest", "ReconciledDepreciation",
                   "ReconciledCostOfRevenue", "EBITDA", "EBIT", "NetInterestIncome", "InterestExpense",
                   "InterestIncome", "ContinuingAndDiscontinuedDilutedEPS", "ContinuingAndDiscontinuedBasicEPS",
                   "NormalizedIncome", "NetIncomeFromContinuingAndDiscontinuedOperation", "TotalExpenses",
                   "RentExpenseSupplemental", "ReportedNormalizedDilutedEPS", "ReportedNormalizedBasicEPS",
                   "TotalOperatingIncomeAsReported", "DividendPerShare", "DilutedAverageShares", "BasicAverageShares",
                   "DilutedEPS", "DilutedEPSOtherGainsLosses", "TaxLossCarryforwardDilutedEPS",
                   "DilutedAccountingChange", "DilutedExtraordinary", "DilutedDiscontinuousOperations",
                   "DilutedContinuousOperations", "BasicEPS", "BasicEPSOtherGainsLosses", "TaxLossCarryforwardBasicEPS",
                   "BasicAccountingChange", "BasicExtraordinary", "BasicDiscontinuousOperations",
                   "BasicContinuousOperations", "DilutedNIAvailtoComStockholders", "AverageDilutionEarnings",
                   "NetIncomeCommonStockholders", "OtherunderPreferredStockDividend", "PreferredStockDividends",
                   "NetIncome", "MinorityInterests", "NetIncomeIncludingNoncontrollingInterests",
                   "NetIncomeFromTaxLossCarryforward", "NetIncomeExtraordinary", "NetIncomeDiscontinuousOperations",
                   "NetIncomeContinuousOperations", "EarningsFromEquityInterestNetOfTax", "TaxProvision",
                   "PretaxIncome", "OtherIncomeExpense", "OtherNonOperatingIncomeExpenses", "SpecialIncomeCharges",
                   "GainOnSaleOfPPE", "GainOnSaleOfBusiness", "OtherSpecialCharges", "WriteOff",
                   "ImpairmentOfCapitalAssets", "RestructuringAndMergernAcquisition", "SecuritiesAmortization",
                   "EarningsFromEquityInterest", "GainOnSaleOfSecurity", "NetNonOperatingInterestIncomeExpense",
                   "TotalOtherFinanceCost", "InterestExpenseNonOperating", "InterestIncomeNonOperating",
                   "OperatingIncome", "OperatingExpense", "OtherOperatingExpenses", "OtherTaxes",
                   "ProvisionForDoubtfulAccounts", "DepreciationAmortizationDepletionIncomeStatement",
                   "DepletionIncomeStatement", "DepreciationAndAmortizationInIncomeStatement", "Amortization",
                   "AmortizationOfIntangiblesIncomeStatement", "DepreciationIncomeStatement", "ResearchAndDevelopment",
                   "SellingGeneralAndAdministration", "SellingAndMarketingExpense", "GeneralAndAdministrativeExpense",
                   "OtherGandA", "InsuranceAndClaims", "RentAndLandingFees", "SalariesAndWages", "GrossProfit",
                   "CostOfRevenue", "TotalRevenue", "ExciseTaxes", "OperatingRevenue", "LossAdjustmentExpense",
                   "NetPolicyholderBenefitsAndClaims", "PolicyholderBenefitsGross", "PolicyholderBenefitsCeded",
                   "OccupancyAndEquipment", "ProfessionalExpenseAndContractServicesExpense", "OtherNonInterestExpense"],
    'balance-sheet': ["TreasurySharesNumber", "PreferredSharesNumber", "OrdinarySharesNumber", "ShareIssued", "NetDebt",
                      "TotalDebt", "TangibleBookValue", "InvestedCapital", "WorkingCapital", "NetTangibleAssets",
                      "CapitalLeaseObligations", "CommonStockEquity", "PreferredStockEquity", "TotalCapitalization",
                      "TotalEquityGrossMinorityInterest", "MinorityInterest", "StockholdersEquity",
                      "OtherEquityInterest", "GainsLossesNotAffectingRetainedEarnings", "OtherEquityAdjustments",
                      "FixedAssetsRevaluationReserve", "ForeignCurrencyTranslationAdjustments",
                      "MinimumPensionLiabilities", "UnrealizedGainLoss", "TreasuryStock", "RetainedEarnings",
                      "AdditionalPaidInCapital", "CapitalStock", "OtherCapitalStock", "CommonStock", "PreferredStock",
                      "TotalPartnershipCapital", "GeneralPartnershipCapital", "LimitedPartnershipCapital",
                      "TotalLiabilitiesNetMinorityInterest", "TotalNonCurrentLiabilitiesNetMinorityInterest",
                      "OtherNonCurrentLiabilities", "LiabilitiesHeldforSaleNonCurrent", "RestrictedCommonStock",
                      "PreferredSecuritiesOutsideStockEquity", "DerivativeProductLiabilities", "EmployeeBenefits",
                      "NonCurrentPensionAndOtherPostretirementBenefitPlans", "NonCurrentAccruedExpenses",
                      "DuetoRelatedPartiesNonCurrent", "TradeandOtherPayablesNonCurrent",
                      "NonCurrentDeferredLiabilities", "NonCurrentDeferredRevenue",
                      "NonCurrentDeferredTaxesLiabilities", "LongTermDebtAndCapitalLeaseObligation",
                      "LongTermCapitalLeaseObligation", "LongTermDebt", "LongTermProvisions", "CurrentLiabilities",
                      "OtherCurrentLiabilities", "CurrentDeferredLiabilities", "CurrentDeferredRevenue",
                      "CurrentDeferredTaxesLiabilities", "CurrentDebtAndCapitalLeaseObligation",
                      "CurrentCapitalLeaseObligation", "CurrentDebt", "OtherCurrentBorrowings", "LineOfCredit",
                      "CommercialPaper", "CurrentNotesPayable", "PensionandOtherPostRetirementBenefitPlansCurrent",
                      "CurrentProvisions", "PayablesAndAccruedExpenses", "CurrentAccruedExpenses", "InterestPayable",
                      "Payables", "OtherPayable", "DuetoRelatedPartiesCurrent", "DividendsPayable", "TotalTaxPayable",
                      "IncomeTaxPayable", "AccountsPayable", "TotalAssets", "TotalNonCurrentAssets",
                      "OtherNonCurrentAssets", "DefinedPensionBenefit", "NonCurrentPrepaidAssets",
                      "NonCurrentDeferredAssets", "NonCurrentDeferredTaxesAssets", "DuefromRelatedPartiesNonCurrent",
                      "NonCurrentNoteReceivables", "NonCurrentAccountsReceivable", "FinancialAssets",
                      "InvestmentsAndAdvances", "OtherInvestments", "InvestmentinFinancialAssets",
                      "HeldToMaturitySecurities", "AvailableForSaleSecurities",
                      "FinancialAssetsDesignatedasFairValueThroughProfitorLossTotal", "TradingSecurities",
                      "LongTermEquityInvestment", "InvestmentsinJointVenturesatCost",
                      "InvestmentsInOtherVenturesUnderEquityMethod", "InvestmentsinAssociatesatCost",
                      "InvestmentsinSubsidiariesatCost", "InvestmentProperties", "GoodwillAndOtherIntangibleAssets",
                      "OtherIntangibleAssets", "Goodwill", "NetPPE", "AccumulatedDepreciation", "GrossPPE", "Leases",
                      "ConstructionInProgress", "OtherProperties", "MachineryFurnitureEquipment",
                      "BuildingsAndImprovements", "LandAndImprovements", "Properties", "CurrentAssets",
                      "OtherCurrentAssets", "HedgingAssetsCurrent", "AssetsHeldForSaleCurrent", "CurrentDeferredAssets",
                      "CurrentDeferredTaxesAssets", "RestrictedCash", "PrepaidAssets", "Inventory",
                      "InventoriesAdjustmentsAllowances", "OtherInventories", "FinishedGoods", "WorkInProcess",
                      "RawMaterials", "Receivables", "ReceivablesAdjustmentsAllowances", "OtherReceivables",
                      "DuefromRelatedPartiesCurrent", "TaxesReceivable", "AccruedInterestReceivable", "NotesReceivable",
                      "LoansReceivable", "AccountsReceivable", "AllowanceForDoubtfulAccountsReceivable",
                      "GrossAccountsReceivable", "CashCashEquivalentsAndShortTermInvestments",
                      "OtherShortTermInvestments", "CashAndCashEquivalents", "CashEquivalents", "CashFinancial",
                      "CashCashEquivalentsAndFederalFundsSold"],
    'cash-flow': ["ForeignSales", "DomesticSales", "AdjustedGeographySegmentData", "FreeCashFlow",
                  "RepurchaseOfCapitalStock", "RepaymentOfDebt", "IssuanceOfDebt", "IssuanceOfCapitalStock",
                  "CapitalExpenditure", "InterestPaidSupplementalData", "IncomeTaxPaidSupplementalData",
                  "EndCashPosition", "OtherCashAdjustmentOutsideChangeinCash", "BeginningCashPosition",
                  "EffectOfExchangeRateChanges", "ChangesInCash", "OtherCashAdjustmentInsideChangeinCash",
                  "CashFlowFromDiscontinuedOperation", "FinancingCashFlow", "CashFromDiscontinuedFinancingActivities",
                  "CashFlowFromContinuingFinancingActivities", "NetOtherFinancingCharges", "InterestPaidCFF",
                  "ProceedsFromStockOptionExercised", "CashDividendsPaid", "PreferredStockDividendPaid",
                  "CommonStockDividendPaid", "NetPreferredStockIssuance", "PreferredStockPayments",
                  "PreferredStockIssuance", "NetCommonStockIssuance", "CommonStockPayments", "CommonStockIssuance",
                  "NetIssuancePaymentsOfDebt", "NetShortTermDebtIssuance", "ShortTermDebtPayments",
                  "ShortTermDebtIssuance", "NetLongTermDebtIssuance", "LongTermDebtPayments", "LongTermDebtIssuance",
                  "InvestingCashFlow", "CashFromDiscontinuedInvestingActivities",
                  "CashFlowFromContinuingInvestingActivities", "NetOtherInvestingChanges", "InterestReceivedCFI",
                  "DividendsReceivedCFI", "NetInvestmentPurchaseAndSale", "SaleOfInvestment", "PurchaseOfInvestment",
                  "NetInvestmentPropertiesPurchaseAndSale", "SaleOfInvestmentProperties",
                  "PurchaseOfInvestmentProperties", "NetBusinessPurchaseAndSale", "SaleOfBusiness",
                  "PurchaseOfBusiness", "NetIntangiblesPurchaseAndSale", "SaleOfIntangibles", "PurchaseOfIntangibles",
                  "NetPPEPurchaseAndSale", "SaleOfPPE", "PurchaseOfPPE", "CapitalExpenditureReported",
                  "OperatingCashFlow", "CashFromDiscontinuedOperatingActivities",
                  "CashFlowFromContinuingOperatingActivities", "TaxesRefundPaid", "InterestReceivedCFO",
                  "InterestPaidCFO", "DividendReceivedCFO", "DividendPaidCFO", "ChangeInWorkingCapital",
                  "ChangeInOtherWorkingCapital", "ChangeInOtherCurrentLiabilities", "ChangeInOtherCurrentAssets",
                  "ChangeInPayablesAndAccruedExpense", "ChangeInAccruedExpense", "ChangeInInterestPayable",
                  "ChangeInPayable", "ChangeInDividendPayable", "ChangeInAccountPayable", "ChangeInTaxPayable",
                  "ChangeInIncomeTaxPayable", "ChangeInPrepaidAssets", "ChangeInInventory", "ChangeInReceivables",
                  "ChangesInAccountReceivables", "OtherNonCashItems", "ExcessTaxBenefitFromStockBasedCompensation",
                  "StockBasedCompensation", "UnrealizedGainLossOnInvestmentSecurities", "ProvisionandWriteOffofAssets",
                  "AssetImpairmentCharge", "AmortizationOfSecurities", "DeferredTax", "DeferredIncomeTax",
                  "DepreciationAmortizationDepletion", "Depletion", "DepreciationAndAmortization",
                  "AmortizationCashFlow", "AmortizationOfIntangibles", "Depreciation", "OperatingGainsLosses",
                  "PensionAndEmployeeBenefitExpense", "EarningsLossesFromEquityInvestments",
                  "GainLossOnInvestmentSecurities", "NetForeignCurrencyExchangeGainLoss", "GainLossOnSaleOfPPE",
                  "GainLossOnSaleOfBusiness", "NetIncomeFromContinuingOperations",
                  "CashFlowsfromusedinOperatingActivitiesDirect", "TaxesRefundPaidDirect", "InterestReceivedDirect",
                  "InterestPaidDirect", "DividendsReceivedDirect", "DividendsPaidDirect", "ClassesofCashPayments",
                  "OtherCashPaymentsfromOperatingActivities", "PaymentsonBehalfofEmployees",
                  "PaymentstoSuppliersforGoodsandServices", "ClassesofCashReceiptsfromOperatingActivities",
                  "OtherCashReceiptsfromOperatingActivities", "ReceiptsfromGovernmentGrants", "ReceiptsfromCustomers"]}


earnings_estimates
growth_estimates
revenue_estimates

price_targets

upgrades_downgrades

options
    url = f"{_BASE_URL_}/v7/finance/options/{self.ticker}"
    https://query2.finance.yahoo.com/v7/finance/options/META?crumb=ipmS.n8I6Bi

news

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
            - esgScores # Environmental, social, and governance (ESG) scores, sustainability and ethical performance of companies
            - price # current prices
            - defaultKeyStatistics # KPIs (PE, enterprise value, EPS, EBITA, and more)
            - financialData # Financial KPIs (revenue, gross margins, operating cash flow, free cash flow, and more)
            - calendarEvents # future earnings date
            - secFilings # SEC filings, such as 10K and 10Q reports
            - upgradeDowngradeHistory # upgrades and downgrades that analysts have given a company's stock
            - institutionOwnership # institutional ownership, holders and shares outstanding
            - fundOwnership # mutual fund ownership, holders and shares outstanding
            - majorDirectHolders
            - majorHoldersBreakdown
            - insiderTransactions # insider transactions, such as the number of shares bought and sold by company executives
            - insiderHolders # insider holders, such as the number of shares held by company executives
            - netSharePurchaseActivity # net share purchase activity, such as the number of shares bought and sold by company executives
            - earnings # earnings history
            - earningsHistory
            - earningsTrend
            - industryTrend
            - indexTrend
            - sectorTrend
            - recommendationTrend
            - futuresChain

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
