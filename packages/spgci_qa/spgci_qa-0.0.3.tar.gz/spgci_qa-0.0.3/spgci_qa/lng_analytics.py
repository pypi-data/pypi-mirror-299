from __future__ import annotations
from typing import List, Optional, Union
from requests import Response
from spgci_qa.api_client import get_data
from spgci_qa.utilities import list_to_filter
from pandas import DataFrame, Series
from datetime import date, datetime
import pandas as pd


class Lng_analytics:
    _endpoint = "api/v1/"
    _reference_endpoint = "reference/v1/"
    _forecast_annual_prices_endpoint = "/price/annual-forecast"
    _forecast_monthly_prices_endpoint = "/price/monthly-forecast"
    _historical_bilateral_customs_prices_endpoint = "/price/historical/bilateral-custom"
    _historical_monthly_prices_endpoint = "/price/historical/monthly"
    _liquefaction_economics_endpoint = "/assets-contracts/liquefaction-economics"
    _country_coasts_endpoint = "/assets-contracts/country-coasts"
    _current_liquefaction_endpoint = "/assets-contracts/current-liquefaction"
    _current_regasification_endpoint = "/assets-contracts/current-regasification"
    _liquefaction_projects_endpoint = "/assets-contracts/liquefaction-projects"
    _liquefaction_train_ownership_endpoint = (
        "/assets-contracts/liquefaction-train-ownership"
    )
    _liquefaction_trains_endpoint = "/assets-contracts/liquefaction-trains"
    _offtake_contracts_endpoint = "/assets-contracts/offtake-contracts"
    _regasification_contracts_endpoint = "/assets-contracts/regasification-contracts"
    _regasification_phase_ownership_endpoint = (
        "/assets-contracts/regasification-phase-ownership"
    )
    _regasification_phases_endpoint = "/assets-contracts/regasification-phases"
    _regasification_projects_endpoint = "/assets-contracts/regasification-projects"
    _vessel_endpoint = "/assets-contracts/vessel"
    _offtake_contracts_monthly_estimated_buildout_endpoint = (
        "/assets-contracts/monthly-estimated-buildout/offtake-contracts"
    )
    _liquefaction_capacity_monthly_estimated_buildout_endpoint = (
        "/assets-contracts/monthly-estimated-buildout/liquefaction-capacity"
    )
    _regasification_contract_monthly_estimated_buildout_endpoint = (
        "/assets-contracts/monthly-estimated-buildout/regasification-contracts"
    )
    _regasification_capacity_monthly_estimated_buildout_endpoint = (
        "/assets-contracts/monthly-estimated-buildout/regasification-capacity"
    )
    _feedstock_profiles_endpoint = "/assets-contracts/feedstock"

    def get_price_annual_forecast(
        self,
        *,
        year: Optional[int] = None,
        year_lt: Optional[int] = None,
        year_lte: Optional[int] = None,
        year_gt: Optional[int] = None,
        year_gte: Optional[int] = None,
        price_marker_name: Optional[Union[list[str], Series[str], str]] = None,
        price_marker_uom: Optional[Union[list[str], Series[str], str]] = None,
        price_marker_currency: Optional[Union[list[str], Series[str], str]] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Price forecast for select gas and LNG price marker. Annual figures in US dollar per million British thermal units

        Parameters
        ----------

         year: Optional[int], optional
             The date for which the price forecast is provided, by default None
         year_gt: Optional[int], optional
             filter by '' year > x '', by default None
         year_gte: Optional[int], optional
             filter by year, by default None
         year_lt: Optional[int], optional
             filter by year, by default None
         year_lte: Optional[int], optional
             filter by year, by default None
         price_marker_name: Optional[Union[list[str], Series[str], str]]
             The name of the price marker, by default None
         price_marker_uom: Optional[Union[list[str], Series[str], str]]
             The unit of measure for a given price for the indicated time period, by default None
         price_marker_currency: Optional[Union[list[str], Series[str], str]]
             The currency for a given price for the indicated time period, by default None
         modified_date: Optional[datetime], optional
             Forecast annual prices record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("year", year))
        if year_gt is not None:
            filter_params.append(f'year > "{year_gt}"')
        if year_gte is not None:
            filter_params.append(f'year >= "{year_gte}"')
        if year_lt is not None:
            filter_params.append(f'year < "{year_lt}"')
        if year_lte is not None:
            filter_params.append(f'year <= "{year_lte}"')
        filter_params.append(list_to_filter("priceMarkerName", price_marker_name))
        filter_params.append(list_to_filter("priceMarkerUom", price_marker_uom))
        filter_params.append(
            list_to_filter("priceMarkerCurrency", price_marker_currency)
        )
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/price/annual-forecast",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_price_monthly_forecast(
        self,
        *,
        date: Optional[date] = None,
        date_lt: Optional[date] = None,
        date_lte: Optional[date] = None,
        date_gt: Optional[date] = None,
        date_gte: Optional[date] = None,
        price_marker_name: Optional[Union[list[str], Series[str], str]] = None,
        price_marker_uom: Optional[Union[list[str], Series[str], str]] = None,
        price_marker_currency: Optional[Union[list[str], Series[str], str]] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Price forecast for select gas and LNG price markers for next few years. Monthly figures in US dollar per million British thermal units

        Parameters
        ----------

         date: Optional[date], optional
             The date for which the price forecast is provided, by default None
         date_gt: Optional[date], optional
             filter by '' date > x '', by default None
         date_gte: Optional[date], optional
             filter by date, by default None
         date_lt: Optional[date], optional
             filter by date, by default None
         date_lte: Optional[date], optional
             filter by date, by default None
         price_marker_name: Optional[Union[list[str], Series[str], str]]
             The name of the price marker, by default None
         price_marker_uom: Optional[Union[list[str], Series[str], str]]
             The unit of measure for a given price for the indicated time period, by default None
         price_marker_currency: Optional[Union[list[str], Series[str], str]]
             The currency for a given price for the indicated time period, by default None
         modified_date: Optional[datetime], optional
             Forecast monthly prices record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("date", date))
        if date_gt is not None:
            filter_params.append(f'date > "{date_gt}"')
        if date_gte is not None:
            filter_params.append(f'date >= "{date_gte}"')
        if date_lt is not None:
            filter_params.append(f'date < "{date_lt}"')
        if date_lte is not None:
            filter_params.append(f'date <= "{date_lte}"')
        filter_params.append(list_to_filter("priceMarkerName", price_marker_name))
        filter_params.append(list_to_filter("priceMarkerUom", price_marker_uom))
        filter_params.append(
            list_to_filter("priceMarkerCurrency", price_marker_currency)
        )
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/price/monthly-forecast",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_price_historical_bilateral_custom(
        self,
        *,
        month: Optional[date] = None,
        month_lt: Optional[date] = None,
        month_lte: Optional[date] = None,
        month_gt: Optional[date] = None,
        month_gte: Optional[date] = None,
        import_market: Optional[Union[list[str], Series[str], str]] = None,
        supply_source: Optional[Union[list[str], Series[str], str]] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        currency: Optional[Union[list[str], Series[str], str]] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Historical bilateral prices of select markets and their LNG supply sources. The data is primarily sourced from customs reporting agencies

        Parameters
        ----------

         month: Optional[date], optional
             The month for which the price data is recorded, by default None
         month_gt: Optional[date], optional
             filter by '' month > x '', by default None
         month_gte: Optional[date], optional
             filter by month, by default None
         month_lt: Optional[date], optional
             filter by month, by default None
         month_lte: Optional[date], optional
             filter by month, by default None
         import_market: Optional[Union[list[str], Series[str], str]]
             The market or country where the LNG is being imported, by default None
         supply_source: Optional[Union[list[str], Series[str], str]]
             The source or country from which the LNG is being supplied, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             The unit of measure for a given price for the indicated time period, by default None
         currency: Optional[Union[list[str], Series[str], str]]
             The currency for a given price for the indicated time period, by default None
         modified_date: Optional[datetime], optional
             Historical bilateral customs prices record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("month", month))
        if month_gt is not None:
            filter_params.append(f'month > "{month_gt}"')
        if month_gte is not None:
            filter_params.append(f'month >= "{month_gte}"')
        if month_lt is not None:
            filter_params.append(f'month < "{month_lt}"')
        if month_lte is not None:
            filter_params.append(f'month <= "{month_lte}"')
        filter_params.append(list_to_filter("importMarket", import_market))
        filter_params.append(list_to_filter("supplySource", supply_source))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("currency", currency))
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/price/historical/bilateral-custom",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_price_historical_monthly(
        self,
        *,
        date: Optional[date] = None,
        date_lt: Optional[date] = None,
        date_lte: Optional[date] = None,
        date_gt: Optional[date] = None,
        date_gte: Optional[date] = None,
        price_marker_name: Optional[Union[list[str], Series[str], str]] = None,
        price_marker_uom: Optional[Union[list[str], Series[str], str]] = None,
        price_marker_currency: Optional[Union[list[str], Series[str], str]] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Historical prices for several gas and LNG price markers. Monthly figures in US dollar per million British thermal units

        Parameters
        ----------

         date: Optional[date], optional
             The date for which the price data is recorded, by default None
         date_gt: Optional[date], optional
             filter by '' date > x '', by default None
         date_gte: Optional[date], optional
             filter by date, by default None
         date_lt: Optional[date], optional
             filter by date, by default None
         date_lte: Optional[date], optional
             filter by date, by default None
         price_marker_name: Optional[Union[list[str], Series[str], str]]
             The name of the price marker, by default None
         price_marker_uom: Optional[Union[list[str], Series[str], str]]
             The unit of measure for a given price for the indicated time period, by default None
         price_marker_currency: Optional[Union[list[str], Series[str], str]]
             The currency for a given price for the indicated time period, by default None
         modified_date: Optional[datetime], optional
             Historical monthly prices record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("date", date))
        if date_gt is not None:
            filter_params.append(f'date > "{date_gt}"')
        if date_gte is not None:
            filter_params.append(f'date >= "{date_gte}"')
        if date_lt is not None:
            filter_params.append(f'date < "{date_lt}"')
        if date_lte is not None:
            filter_params.append(f'date <= "{date_lte}"')
        filter_params.append(list_to_filter("priceMarkerName", price_marker_name))
        filter_params.append(list_to_filter("priceMarkerUom", price_marker_uom))
        filter_params.append(
            list_to_filter("priceMarkerCurrency", price_marker_currency)
        )
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/price/historical/monthly",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_liquefaction_economics(
        self,
        *,
        economic_group: Optional[Union[list[str], Series[str], str]] = None,
        liquefaction_project: Optional[Union[list[str], Series[str], str]] = None,
        supply_market: Optional[Union[list[str], Series[str], str]] = None,
        start_year: Optional[int] = None,
        start_year_lt: Optional[int] = None,
        start_year_lte: Optional[int] = None,
        start_year_gt: Optional[int] = None,
        start_year_gte: Optional[int] = None,
        capital_recovered: Optional[Union[list[str], Series[str], str]] = None,
        midstream_discount_rate: Optional[Union[list[str], Series[str], str]] = None,
        upstream_discount_rate: Optional[Union[list[str], Series[str], str]] = None,
        upstream_pricing_scenario: Optional[Union[list[str], Series[str], str]] = None,
        liquefaction_capacity: Optional[float] = None,
        liquefaction_capacity_lt: Optional[float] = None,
        liquefaction_capacity_lte: Optional[float] = None,
        liquefaction_capacity_gt: Optional[float] = None,
        liquefaction_capacity_gte: Optional[float] = None,
        economics_category: Optional[Union[list[str], Series[str], str]] = None,
        economics_category_uom: Optional[Union[list[str], Series[str], str]] = None,
        economics_category_currency: Optional[
            Union[list[str], Series[str], str]
        ] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Table of project breakeven costs for upstream, pipeline, and liquefaction segments. Costs are estimated for various rates of returns and oil price scenarios

        Parameters
        ----------

         economic_group: Optional[Union[list[str], Series[str], str]]
             Classification of the project based on economic characteristics, by default None
         liquefaction_project: Optional[Union[list[str], Series[str], str]]
             Name of the specific liquefaction project, by default None
         supply_market: Optional[Union[list[str], Series[str], str]]
             The market from which the feedstock is sourced, by default None
         start_year: Optional[int], optional
             Year of project start-up, by default None
         start_year_gt: Optional[int], optional
             filter by '' start_year > x '', by default None
         start_year_gte: Optional[int], optional
             filter by start_year, by default None
         start_year_lt: Optional[int], optional
             filter by start_year, by default None
         start_year_lte: Optional[int], optional
             filter by start_year, by default None
         capital_recovered: Optional[Union[list[str], Series[str], str]]
             Yes or no whether all capital is recovered, by default None
         midstream_discount_rate: Optional[Union[list[str], Series[str], str]]
             Discount rate applied to midstream cash flows, by default None
         upstream_discount_rate: Optional[Union[list[str], Series[str], str]]
             Discount rate applied to upstream cash flows, by default None
         upstream_pricing_scenario: Optional[Union[list[str], Series[str], str]]
             The name of the category defining the upstream modeling scenario, by default None
         liquefaction_capacity: Optional[float], optional
             Annual liquefaction capacity, by default None
         liquefaction_capacity_gt: Optional[float], optional
             filter by '' liquefaction_capacity > x '', by default None
         liquefaction_capacity_gte: Optional[float], optional
             filter by liquefaction_capacity, by default None
         liquefaction_capacity_lt: Optional[float], optional
             filter by liquefaction_capacity, by default None
         liquefaction_capacity_lte: Optional[float], optional
             filter by liquefaction_capacity, by default None
         economics_category: Optional[Union[list[str], Series[str], str]]
             The name of the cost component in liquefaction project economic analysis, by default None
         economics_category_uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure of the cost for the specific component of liquefaction project economic analysis, by default None
         economics_category_currency: Optional[Union[list[str], Series[str], str]]
             Currency of the cost for the specific component of liquefaction project economic analysis, by default None
         modified_date: Optional[datetime], optional
             Liquefaction Economics record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("economicGroup", economic_group))
        filter_params.append(
            list_to_filter("liquefactionProject", liquefaction_project)
        )
        filter_params.append(list_to_filter("supplyMarket", supply_market))
        filter_params.append(list_to_filter("startYear", start_year))
        if start_year_gt is not None:
            filter_params.append(f'startYear > "{start_year_gt}"')
        if start_year_gte is not None:
            filter_params.append(f'startYear >= "{start_year_gte}"')
        if start_year_lt is not None:
            filter_params.append(f'startYear < "{start_year_lt}"')
        if start_year_lte is not None:
            filter_params.append(f'startYear <= "{start_year_lte}"')
        filter_params.append(list_to_filter("capitalRecovered", capital_recovered))
        filter_params.append(
            list_to_filter("midstreamDiscountRate", midstream_discount_rate)
        )
        filter_params.append(
            list_to_filter("upstreamDiscountRate", upstream_discount_rate)
        )
        filter_params.append(
            list_to_filter("upstreamPricingScenario", upstream_pricing_scenario)
        )
        filter_params.append(
            list_to_filter("liquefactionCapacity", liquefaction_capacity)
        )
        if liquefaction_capacity_gt is not None:
            filter_params.append(f'liquefactionCapacity > "{liquefaction_capacity_gt}"')
        if liquefaction_capacity_gte is not None:
            filter_params.append(
                f'liquefactionCapacity >= "{liquefaction_capacity_gte}"'
            )
        if liquefaction_capacity_lt is not None:
            filter_params.append(f'liquefactionCapacity < "{liquefaction_capacity_lt}"')
        if liquefaction_capacity_lte is not None:
            filter_params.append(
                f'liquefactionCapacity <= "{liquefaction_capacity_lte}"'
            )
        filter_params.append(list_to_filter("economicsCategory", economics_category))
        filter_params.append(
            list_to_filter("economicsCategoryUom", economics_category_uom)
        )
        filter_params.append(
            list_to_filter("economicsCategoryCurrency", economics_category_currency)
        )
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/liquefaction-economics",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_country_coasts(
        self,
        *,
        country_coast: Optional[Union[list[str], Series[str], str]] = None,
        country: Optional[Union[list[str], Series[str], str]] = None,
        basin: Optional[Union[list[str], Series[str], str]] = None,
        region_export: Optional[Union[list[str], Series[str], str]] = None,
        region_import: Optional[Union[list[str], Series[str], str]] = None,
        region_cross_basin_import: Optional[Union[list[str], Series[str], str]] = None,
        region_general: Optional[Union[list[str], Series[str], str]] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Provides information on the countries and coasts as well as their geographic regions. This is used for classification purposes

        Parameters
        ----------

         country_coast: Optional[Union[list[str], Series[str], str]]
             Specific coast and country identity, by default None
         country: Optional[Union[list[str], Series[str], str]]
             Name of the country associated with the coast, by default None
         basin: Optional[Union[list[str], Series[str], str]]
             The geographic basin where the country coast is located, by default None
         region_export: Optional[Union[list[str], Series[str], str]]
             Regional classification for export country coasts, by default None
         region_import: Optional[Union[list[str], Series[str], str]]
             Regional classification for import country coasts, by default None
         region_cross_basin_import: Optional[Union[list[str], Series[str], str]]
             Cross-basin trade regional classification for different country coasts, by default None
         region_general: Optional[Union[list[str], Series[str], str]]
             General regional classification for country coasts, by default None
         modified_date: Optional[datetime], optional
             Country coasts record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("countryCoast", country_coast))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("basin", basin))
        filter_params.append(list_to_filter("regionExport", region_export))
        filter_params.append(list_to_filter("regionImport", region_import))
        filter_params.append(
            list_to_filter("regionCrossBasinImport", region_cross_basin_import)
        )
        filter_params.append(list_to_filter("regionGeneral", region_general))
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/country-coasts",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_current_liquefaction(
        self,
        *,
        supply_project: Optional[Union[list[str], Series[str], str]] = None,
        export_country: Optional[Union[list[str], Series[str], str]] = None,
        export_basin: Optional[Union[list[str], Series[str], str]] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Table of regional classifications for liquefaction projects. This is a support table that can be used to create relationships between other tables

        Parameters
        ----------

         supply_project: Optional[Union[list[str], Series[str], str]]
             Name of the LNG supply project, by default None
         export_country: Optional[Union[list[str], Series[str], str]]
             Country where the supply project is located, by default None
         export_basin: Optional[Union[list[str], Series[str], str]]
             The geographic basin where the supply project is located, by default None
         modified_date: Optional[datetime], optional
             Current liuquefaction record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("supplyProject", supply_project))
        filter_params.append(list_to_filter("exportCountry", export_country))
        filter_params.append(list_to_filter("exportBasin", export_basin))
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/current-liquefaction",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_current_regasification(
        self,
        *,
        import_port: Optional[Union[list[str], Series[str], str]] = None,
        import_country: Optional[Union[list[str], Series[str], str]] = None,
        import_basin: Optional[Union[list[str], Series[str], str]] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Table of regional classifications for regasification phases. This is a support table that can be used to create relationships between other tables

        Parameters
        ----------

         import_port: Optional[Union[list[str], Series[str], str]]
             Name of existing (or soon-to-be-existing) regasification terminal, by default None
         import_country: Optional[Union[list[str], Series[str], str]]
             Country where the regasification port is located, by default None
         import_basin: Optional[Union[list[str], Series[str], str]]
             Geological basin associated with the import location, by default None
         modified_date: Optional[datetime], optional
             Current regaisification record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("importPort", import_port))
        filter_params.append(list_to_filter("importCountry", import_country))
        filter_params.append(list_to_filter("importBasin", import_basin))
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/current-regasification",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_liquefaction_projects(
        self,
        *,
        liquefaction_project: Optional[Union[list[str], Series[str], str]] = None,
        country_coast: Optional[Union[list[str], Series[str], str]] = None,
        supply_market: Optional[Union[list[str], Series[str], str]] = None,
        supply_basin: Optional[Union[list[str], Series[str], str]] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        List of liquefaction projects with their IDs and associated country coasts

        Parameters
        ----------

         liquefaction_project: Optional[Union[list[str], Series[str], str]]
             Name of the liquefaction project, by default None
         country_coast: Optional[Union[list[str], Series[str], str]]
             Country and coast identity where the project is located, by default None
         supply_market: Optional[Union[list[str], Series[str], str]]
             Market where the liquefaction project is located, by default None
         supply_basin: Optional[Union[list[str], Series[str], str]]
             Geographic basin where the liquefaction project is located, by default None
         modified_date: Optional[datetime], optional
             Liquefication projects record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(
            list_to_filter("liquefactionProject", liquefaction_project)
        )
        filter_params.append(list_to_filter("countryCoast", country_coast))
        filter_params.append(list_to_filter("supplyMarket", supply_market))
        filter_params.append(list_to_filter("supplyBasin", supply_basin))
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/liquefaction-projects",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_liquefaction_train_ownership(
        self,
        *,
        liquefaction_train: Optional[Union[list[str], Series[str], str]] = None,
        shareholder: Optional[Union[list[str], Series[str], str]] = None,
        share: Optional[float] = None,
        share_lt: Optional[float] = None,
        share_lte: Optional[float] = None,
        share_gt: Optional[float] = None,
        share_gte: Optional[float] = None,
        created_date: Optional[datetime] = None,
        created_date_lt: Optional[datetime] = None,
        created_date_lte: Optional[datetime] = None,
        created_date_gt: Optional[datetime] = None,
        created_date_gte: Optional[datetime] = None,
        shareholder_modified_date: Optional[datetime] = None,
        shareholder_modified_date_lt: Optional[datetime] = None,
        shareholder_modified_date_lte: Optional[datetime] = None,
        shareholder_modified_date_gt: Optional[datetime] = None,
        shareholder_modified_date_gte: Optional[datetime] = None,
        share_modified_date: Optional[datetime] = None,
        share_modified_date_lt: Optional[datetime] = None,
        share_modified_date_lte: Optional[datetime] = None,
        share_modified_date_gt: Optional[datetime] = None,
        share_modified_date_gte: Optional[datetime] = None,
        ownership_start_date: Optional[datetime] = None,
        ownership_start_date_lt: Optional[datetime] = None,
        ownership_start_date_lte: Optional[datetime] = None,
        ownership_start_date_gt: Optional[datetime] = None,
        ownership_start_date_gte: Optional[datetime] = None,
        ownership_end_date: Optional[datetime] = None,
        ownership_end_date_lt: Optional[datetime] = None,
        ownership_end_date_lte: Optional[datetime] = None,
        ownership_end_date_gt: Optional[datetime] = None,
        ownership_end_date_gte: Optional[datetime] = None,
        current_owner: Optional[Union[list[str], Series[str], str]] = None,
        country_coast: Optional[Union[list[str], Series[str], str]] = None,
        supply_market: Optional[Union[list[str], Series[str], str]] = None,
        liquefaction_project: Optional[Union[list[str], Series[str], str]] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Provides information on the ownership of liquefaction trains over time

        Parameters
        ----------

         liquefaction_train: Optional[Union[list[str], Series[str], str]]
             Name of the liquefaction train, by default None
         shareholder: Optional[Union[list[str], Series[str], str]]
             Company holding ownership in the liquefaction train, by default None
         share: Optional[float], optional
             Percentage of ownership held by the shareholder, by default None
         share_gt: Optional[float], optional
             filter by '' share > x '', by default None
         share_gte: Optional[float], optional
             filter by share, by default None
         share_lt: Optional[float], optional
             filter by share, by default None
         share_lte: Optional[float], optional
             filter by share, by default None
         created_date: Optional[datetime], optional
             Date when the ownership record was created, by default None
         created_date_gt: Optional[datetime], optional
             filter by '' created_date > x '', by default None
         created_date_gte: Optional[datetime], optional
             filter by created_date, by default None
         created_date_lt: Optional[datetime], optional
             filter by created_date, by default None
         created_date_lte: Optional[datetime], optional
             filter by created_date, by default None
         shareholder_modified_date: Optional[datetime], optional
             Date of last modification to shareholder information, by default None
         shareholder_modified_date_gt: Optional[datetime], optional
             filter by '' shareholder_modified_date > x '', by default None
         shareholder_modified_date_gte: Optional[datetime], optional
             filter by shareholder_modified_date, by default None
         shareholder_modified_date_lt: Optional[datetime], optional
             filter by shareholder_modified_date, by default None
         shareholder_modified_date_lte: Optional[datetime], optional
             filter by shareholder_modified_date, by default None
         share_modified_date: Optional[datetime], optional
             Date of last change to the ownership share, by default None
         share_modified_date_gt: Optional[datetime], optional
             filter by '' share_modified_date > x '', by default None
         share_modified_date_gte: Optional[datetime], optional
             filter by share_modified_date, by default None
         share_modified_date_lt: Optional[datetime], optional
             filter by share_modified_date, by default None
         share_modified_date_lte: Optional[datetime], optional
             filter by share_modified_date, by default None
         ownership_start_date: Optional[datetime], optional
             Date when the ownership began, by default None
         ownership_start_date_gt: Optional[datetime], optional
             filter by '' ownership_start_date > x '', by default None
         ownership_start_date_gte: Optional[datetime], optional
             filter by ownership_start_date, by default None
         ownership_start_date_lt: Optional[datetime], optional
             filter by ownership_start_date, by default None
         ownership_start_date_lte: Optional[datetime], optional
             filter by ownership_start_date, by default None
         ownership_end_date: Optional[datetime], optional
             Date when the ownership ended, if applicable, by default None
         ownership_end_date_gt: Optional[datetime], optional
             filter by '' ownership_end_date > x '', by default None
         ownership_end_date_gte: Optional[datetime], optional
             filter by ownership_end_date, by default None
         ownership_end_date_lt: Optional[datetime], optional
             filter by ownership_end_date, by default None
         ownership_end_date_lte: Optional[datetime], optional
             filter by ownership_end_date, by default None
         current_owner: Optional[Union[list[str], Series[str], str]]
             Indicates if the shareholder is a current owner, by default None
         country_coast: Optional[Union[list[str], Series[str], str]]
             Country and coast identity associated with the liquefaction train, by default None
         supply_market: Optional[Union[list[str], Series[str], str]]
             Market where the liquefaction train is located, by default None
         liquefaction_project: Optional[Union[list[str], Series[str], str]]
             The project to which the train belongs, by default None
         modified_date: Optional[datetime], optional
             Liquefaction train ownership record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("liquefactionTrain", liquefaction_train))
        filter_params.append(list_to_filter("shareholder", shareholder))
        filter_params.append(list_to_filter("share", share))
        if share_gt is not None:
            filter_params.append(f'share > "{share_gt}"')
        if share_gte is not None:
            filter_params.append(f'share >= "{share_gte}"')
        if share_lt is not None:
            filter_params.append(f'share < "{share_lt}"')
        if share_lte is not None:
            filter_params.append(f'share <= "{share_lte}"')
        filter_params.append(list_to_filter("createdDate", created_date))
        if created_date_gt is not None:
            filter_params.append(f'createdDate > "{created_date_gt}"')
        if created_date_gte is not None:
            filter_params.append(f'createdDate >= "{created_date_gte}"')
        if created_date_lt is not None:
            filter_params.append(f'createdDate < "{created_date_lt}"')
        if created_date_lte is not None:
            filter_params.append(f'createdDate <= "{created_date_lte}"')
        filter_params.append(
            list_to_filter("shareholderModifiedDate", shareholder_modified_date)
        )
        if shareholder_modified_date_gt is not None:
            filter_params.append(
                f'shareholderModifiedDate > "{shareholder_modified_date_gt}"'
            )
        if shareholder_modified_date_gte is not None:
            filter_params.append(
                f'shareholderModifiedDate >= "{shareholder_modified_date_gte}"'
            )
        if shareholder_modified_date_lt is not None:
            filter_params.append(
                f'shareholderModifiedDate < "{shareholder_modified_date_lt}"'
            )
        if shareholder_modified_date_lte is not None:
            filter_params.append(
                f'shareholderModifiedDate <= "{shareholder_modified_date_lte}"'
            )
        filter_params.append(list_to_filter("shareModifiedDate", share_modified_date))
        if share_modified_date_gt is not None:
            filter_params.append(f'shareModifiedDate > "{share_modified_date_gt}"')
        if share_modified_date_gte is not None:
            filter_params.append(f'shareModifiedDate >= "{share_modified_date_gte}"')
        if share_modified_date_lt is not None:
            filter_params.append(f'shareModifiedDate < "{share_modified_date_lt}"')
        if share_modified_date_lte is not None:
            filter_params.append(f'shareModifiedDate <= "{share_modified_date_lte}"')
        filter_params.append(list_to_filter("ownershipStartDate", ownership_start_date))
        if ownership_start_date_gt is not None:
            filter_params.append(f'ownershipStartDate > "{ownership_start_date_gt}"')
        if ownership_start_date_gte is not None:
            filter_params.append(f'ownershipStartDate >= "{ownership_start_date_gte}"')
        if ownership_start_date_lt is not None:
            filter_params.append(f'ownershipStartDate < "{ownership_start_date_lt}"')
        if ownership_start_date_lte is not None:
            filter_params.append(f'ownershipStartDate <= "{ownership_start_date_lte}"')
        filter_params.append(list_to_filter("ownershipEndDate", ownership_end_date))
        if ownership_end_date_gt is not None:
            filter_params.append(f'ownershipEndDate > "{ownership_end_date_gt}"')
        if ownership_end_date_gte is not None:
            filter_params.append(f'ownershipEndDate >= "{ownership_end_date_gte}"')
        if ownership_end_date_lt is not None:
            filter_params.append(f'ownershipEndDate < "{ownership_end_date_lt}"')
        if ownership_end_date_lte is not None:
            filter_params.append(f'ownershipEndDate <= "{ownership_end_date_lte}"')
        filter_params.append(list_to_filter("currentOwner", current_owner))
        filter_params.append(list_to_filter("countryCoast", country_coast))
        filter_params.append(list_to_filter("supplyMarket", supply_market))
        filter_params.append(
            list_to_filter("liquefactionProject", liquefaction_project)
        )
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/liquefaction-train-ownership",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_liquefaction_trains(
        self,
        *,
        liquefaction_train: Optional[Union[list[str], Series[str], str]] = None,
        liquefaction_project: Optional[Union[list[str], Series[str], str]] = None,
        train_status: Optional[Union[list[str], Series[str], str]] = None,
        announced_start_date: Optional[datetime] = None,
        announced_start_date_lt: Optional[datetime] = None,
        announced_start_date_lte: Optional[datetime] = None,
        announced_start_date_gt: Optional[datetime] = None,
        announced_start_date_gte: Optional[datetime] = None,
        estimated_start_date: Optional[datetime] = None,
        estimated_start_date_lt: Optional[datetime] = None,
        estimated_start_date_lte: Optional[datetime] = None,
        estimated_start_date_gt: Optional[datetime] = None,
        estimated_start_date_gte: Optional[datetime] = None,
        offline_date: Optional[datetime] = None,
        offline_date_lt: Optional[datetime] = None,
        offline_date_lte: Optional[datetime] = None,
        offline_date_gt: Optional[datetime] = None,
        offline_date_gte: Optional[datetime] = None,
        green_brownfield: Optional[Union[list[str], Series[str], str]] = None,
        liquefaction_technology: Optional[Union[list[str], Series[str], str]] = None,
        created_date: Optional[datetime] = None,
        created_date_lt: Optional[datetime] = None,
        created_date_lte: Optional[datetime] = None,
        created_date_gt: Optional[datetime] = None,
        created_date_gte: Optional[datetime] = None,
        status_modified_date: Optional[datetime] = None,
        status_modified_date_lt: Optional[datetime] = None,
        status_modified_date_lte: Optional[datetime] = None,
        status_modified_date_gt: Optional[datetime] = None,
        status_modified_date_gte: Optional[datetime] = None,
        capacity_modified_date: Optional[datetime] = None,
        capacity_modified_date_lt: Optional[datetime] = None,
        capacity_modified_date_lte: Optional[datetime] = None,
        capacity_modified_date_gt: Optional[datetime] = None,
        capacity_modified_date_gte: Optional[datetime] = None,
        announced_start_date_modified_date: Optional[datetime] = None,
        announced_start_date_modified_date_lt: Optional[datetime] = None,
        announced_start_date_modified_date_lte: Optional[datetime] = None,
        announced_start_date_modified_date_gt: Optional[datetime] = None,
        announced_start_date_modified_date_gte: Optional[datetime] = None,
        estimated_start_date_modified_date: Optional[datetime] = None,
        estimated_start_date_modified_date_lt: Optional[datetime] = None,
        estimated_start_date_modified_date_lte: Optional[datetime] = None,
        estimated_start_date_modified_date_gt: Optional[datetime] = None,
        estimated_start_date_modified_date_gte: Optional[datetime] = None,
        announced_start_date_at_final_investment_decision: Optional[datetime] = None,
        announced_start_date_at_final_investment_decision_lt: Optional[datetime] = None,
        announced_start_date_at_final_investment_decision_lte: Optional[
            datetime
        ] = None,
        announced_start_date_at_final_investment_decision_gt: Optional[datetime] = None,
        announced_start_date_at_final_investment_decision_gte: Optional[
            datetime
        ] = None,
        latest_announced_final_investment_decision_date: Optional[datetime] = None,
        latest_announced_final_investment_decision_date_lt: Optional[datetime] = None,
        latest_announced_final_investment_decision_date_lte: Optional[datetime] = None,
        latest_announced_final_investment_decision_date_gt: Optional[datetime] = None,
        latest_announced_final_investment_decision_date_gte: Optional[datetime] = None,
        estimated_first_cargo_date: Optional[datetime] = None,
        estimated_first_cargo_date_lt: Optional[datetime] = None,
        estimated_first_cargo_date_lte: Optional[datetime] = None,
        estimated_first_cargo_date_gt: Optional[datetime] = None,
        estimated_first_cargo_date_gte: Optional[datetime] = None,
        risk_factor_feedstock_availability: Optional[int] = None,
        risk_factor_feedstock_availability_lt: Optional[int] = None,
        risk_factor_feedstock_availability_lte: Optional[int] = None,
        risk_factor_feedstock_availability_gt: Optional[int] = None,
        risk_factor_feedstock_availability_gte: Optional[int] = None,
        risk_factor_politics_and_geopolitics: Optional[int] = None,
        risk_factor_politics_and_geopolitics_lt: Optional[int] = None,
        risk_factor_politics_and_geopolitics_lte: Optional[int] = None,
        risk_factor_politics_and_geopolitics_gt: Optional[int] = None,
        risk_factor_politics_and_geopolitics_gte: Optional[int] = None,
        risk_factor_environmental_regulation: Optional[int] = None,
        risk_factor_environmental_regulation_lt: Optional[int] = None,
        risk_factor_environmental_regulation_lte: Optional[int] = None,
        risk_factor_environmental_regulation_gt: Optional[int] = None,
        risk_factor_environmental_regulation_gte: Optional[int] = None,
        risk_factor_domestic_gas_needs: Optional[int] = None,
        risk_factor_domestic_gas_needs_lt: Optional[int] = None,
        risk_factor_domestic_gas_needs_lte: Optional[int] = None,
        risk_factor_domestic_gas_needs_gt: Optional[int] = None,
        risk_factor_domestic_gas_needs_gte: Optional[int] = None,
        risk_factor_partner_priorities: Optional[int] = None,
        risk_factor_partner_priorities_lt: Optional[int] = None,
        risk_factor_partner_priorities_lte: Optional[int] = None,
        risk_factor_partner_priorities_gt: Optional[int] = None,
        risk_factor_partner_priorities_gte: Optional[int] = None,
        risk_factor_project_economics: Optional[int] = None,
        risk_factor_project_economics_lt: Optional[int] = None,
        risk_factor_project_economics_lte: Optional[int] = None,
        risk_factor_project_economics_gt: Optional[int] = None,
        risk_factor_project_economics_gte: Optional[int] = None,
        risk_factor_ability_to_execute: Optional[int] = None,
        risk_factor_ability_to_execute_lt: Optional[int] = None,
        risk_factor_ability_to_execute_lte: Optional[int] = None,
        risk_factor_ability_to_execute_gt: Optional[int] = None,
        risk_factor_ability_to_execute_gte: Optional[int] = None,
        risk_factor_contracts: Optional[int] = None,
        risk_factor_contracts_lt: Optional[int] = None,
        risk_factor_contracts_lte: Optional[int] = None,
        risk_factor_contracts_gt: Optional[int] = None,
        risk_factor_contracts_gte: Optional[int] = None,
        risk_factor_overall: Optional[int] = None,
        risk_factor_overall_lt: Optional[int] = None,
        risk_factor_overall_lte: Optional[int] = None,
        risk_factor_overall_gt: Optional[int] = None,
        risk_factor_overall_gte: Optional[int] = None,
        estimated_final_investment_decision_date: Optional[datetime] = None,
        estimated_final_investment_decision_date_lt: Optional[datetime] = None,
        estimated_final_investment_decision_date_lte: Optional[datetime] = None,
        estimated_final_investment_decision_date_gt: Optional[datetime] = None,
        estimated_final_investment_decision_date_gte: Optional[datetime] = None,
        number_of_trains: Optional[int] = None,
        number_of_trains_lt: Optional[int] = None,
        number_of_trains_lte: Optional[int] = None,
        number_of_trains_gt: Optional[int] = None,
        number_of_trains_gte: Optional[int] = None,
        flng_charterer: Optional[Union[list[str], Series[str], str]] = None,
        project_type: Optional[Union[list[str], Series[str], str]] = None,
        liquefaction_train_feature: Optional[Union[list[str], Series[str], str]] = None,
        liquefaction_train_feature_uom: Optional[
            Union[list[str], Series[str], str]
        ] = None,
        liquefaction_train_feature_currency: Optional[
            Union[list[str], Series[str], str]
        ] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        List of all existing, under construction, and future liquefaction projects as well as their attributes

        Parameters
        ----------

         liquefaction_train: Optional[Union[list[str], Series[str], str]]
             Name of the individual liquefaction unit, by default None
         liquefaction_project: Optional[Union[list[str], Series[str], str]]
             Associated liquefaction project, by default None
         train_status: Optional[Union[list[str], Series[str], str]]
             Current operational status of the train, by default None
         announced_start_date: Optional[datetime], optional
             Publicly declared start date, by default None
         announced_start_date_gt: Optional[datetime], optional
             filter by '' announced_start_date > x '', by default None
         announced_start_date_gte: Optional[datetime], optional
             filter by announced_start_date, by default None
         announced_start_date_lt: Optional[datetime], optional
             filter by announced_start_date, by default None
         announced_start_date_lte: Optional[datetime], optional
             filter by announced_start_date, by default None
         estimated_start_date: Optional[datetime], optional
             Our projected date for commercial operations to begin, by default None
         estimated_start_date_gt: Optional[datetime], optional
             filter by '' estimated_start_date > x '', by default None
         estimated_start_date_gte: Optional[datetime], optional
             filter by estimated_start_date, by default None
         estimated_start_date_lt: Optional[datetime], optional
             filter by estimated_start_date, by default None
         estimated_start_date_lte: Optional[datetime], optional
             filter by estimated_start_date, by default None
         offline_date: Optional[datetime], optional
             Date when the train went offline, if applicable, by default None
         offline_date_gt: Optional[datetime], optional
             filter by '' offline_date > x '', by default None
         offline_date_gte: Optional[datetime], optional
             filter by offline_date, by default None
         offline_date_lt: Optional[datetime], optional
             filter by offline_date, by default None
         offline_date_lte: Optional[datetime], optional
             filter by offline_date, by default None
         green_brownfield: Optional[Union[list[str], Series[str], str]]
             Classification as a new (greenfield) or upgraded (brownfield) project, by default None
         liquefaction_technology: Optional[Union[list[str], Series[str], str]]
             Technology used for liquefaction, by default None
         created_date: Optional[datetime], optional
             Date when the train record was created, by default None
         created_date_gt: Optional[datetime], optional
             filter by '' created_date > x '', by default None
         created_date_gte: Optional[datetime], optional
             filter by created_date, by default None
         created_date_lt: Optional[datetime], optional
             filter by created_date, by default None
         created_date_lte: Optional[datetime], optional
             filter by created_date, by default None
         status_modified_date: Optional[datetime], optional
             Date when the train's status was last updated, by default None
         status_modified_date_gt: Optional[datetime], optional
             filter by '' status_modified_date > x '', by default None
         status_modified_date_gte: Optional[datetime], optional
             filter by status_modified_date, by default None
         status_modified_date_lt: Optional[datetime], optional
             filter by status_modified_date, by default None
         status_modified_date_lte: Optional[datetime], optional
             filter by status_modified_date, by default None
         capacity_modified_date: Optional[datetime], optional
             Date when the train's capacity information was last updated, by default None
         capacity_modified_date_gt: Optional[datetime], optional
             filter by '' capacity_modified_date > x '', by default None
         capacity_modified_date_gte: Optional[datetime], optional
             filter by capacity_modified_date, by default None
         capacity_modified_date_lt: Optional[datetime], optional
             filter by capacity_modified_date, by default None
         capacity_modified_date_lte: Optional[datetime], optional
             filter by capacity_modified_date, by default None
         announced_start_date_modified_date: Optional[datetime], optional
             Date when the announced start date was last updated, by default None
         announced_start_date_modified_date_gt: Optional[datetime], optional
             filter by '' announced_start_date_modified_date > x '', by default None
         announced_start_date_modified_date_gte: Optional[datetime], optional
             filter by announced_start_date_modified_date, by default None
         announced_start_date_modified_date_lt: Optional[datetime], optional
             filter by announced_start_date_modified_date, by default None
         announced_start_date_modified_date_lte: Optional[datetime], optional
             filter by announced_start_date_modified_date, by default None
         estimated_start_date_modified_date: Optional[datetime], optional
             Date when the estimated start date was last updated, by default None
         estimated_start_date_modified_date_gt: Optional[datetime], optional
             filter by '' estimated_start_date_modified_date > x '', by default None
         estimated_start_date_modified_date_gte: Optional[datetime], optional
             filter by estimated_start_date_modified_date, by default None
         estimated_start_date_modified_date_lt: Optional[datetime], optional
             filter by estimated_start_date_modified_date, by default None
         estimated_start_date_modified_date_lte: Optional[datetime], optional
             filter by estimated_start_date_modified_date, by default None
         announced_start_date_at_final_investment_decision: Optional[datetime], optional
             Start date announced at the time of the final investment decision, by default None
         announced_start_date_at_final_investment_decision_gt: Optional[datetime], optional
             filter by '' announced_start_date_at_final_investment_decision > x '', by default None
         announced_start_date_at_final_investment_decision_gte: Optional[datetime], optional
             filter by announced_start_date_at_final_investment_decision, by default None
         announced_start_date_at_final_investment_decision_lt: Optional[datetime], optional
             filter by announced_start_date_at_final_investment_decision, by default None
         announced_start_date_at_final_investment_decision_lte: Optional[datetime], optional
             filter by announced_start_date_at_final_investment_decision, by default None
         latest_announced_final_investment_decision_date: Optional[datetime], optional
             Most recent final investment decision date, by default None
         latest_announced_final_investment_decision_date_gt: Optional[datetime], optional
             filter by '' latest_announced_final_investment_decision_date > x '', by default None
         latest_announced_final_investment_decision_date_gte: Optional[datetime], optional
             filter by latest_announced_final_investment_decision_date, by default None
         latest_announced_final_investment_decision_date_lt: Optional[datetime], optional
             filter by latest_announced_final_investment_decision_date, by default None
         latest_announced_final_investment_decision_date_lte: Optional[datetime], optional
             filter by latest_announced_final_investment_decision_date, by default None
         estimated_first_cargo_date: Optional[datetime], optional
             Projected date for the first shipment of LNG, by default None
         estimated_first_cargo_date_gt: Optional[datetime], optional
             filter by '' estimated_first_cargo_date > x '', by default None
         estimated_first_cargo_date_gte: Optional[datetime], optional
             filter by estimated_first_cargo_date, by default None
         estimated_first_cargo_date_lt: Optional[datetime], optional
             filter by estimated_first_cargo_date, by default None
         estimated_first_cargo_date_lte: Optional[datetime], optional
             filter by estimated_first_cargo_date, by default None
         risk_factor_feedstock_availability: Optional[int], optional
             Various risks associated with feedstock availability, by default None
         risk_factor_feedstock_availability_gt: Optional[int], optional
             filter by '' risk_factor_feedstock_availability > x '', by default None
         risk_factor_feedstock_availability_gte: Optional[int], optional
             filter by risk_factor_feedstock_availability, by default None
         risk_factor_feedstock_availability_lt: Optional[int], optional
             filter by risk_factor_feedstock_availability, by default None
         risk_factor_feedstock_availability_lte: Optional[int], optional
             filter by risk_factor_feedstock_availability, by default None
         risk_factor_politics_and_geopolitics: Optional[int], optional
             Various risks associated with politics, by default None
         risk_factor_politics_and_geopolitics_gt: Optional[int], optional
             filter by '' risk_factor_politics_and_geopolitics > x '', by default None
         risk_factor_politics_and_geopolitics_gte: Optional[int], optional
             filter by risk_factor_politics_and_geopolitics, by default None
         risk_factor_politics_and_geopolitics_lt: Optional[int], optional
             filter by risk_factor_politics_and_geopolitics, by default None
         risk_factor_politics_and_geopolitics_lte: Optional[int], optional
             filter by risk_factor_politics_and_geopolitics, by default None
         risk_factor_environmental_regulation: Optional[int], optional
             Various risks associated with environmental regulation, by default None
         risk_factor_environmental_regulation_gt: Optional[int], optional
             filter by '' risk_factor_environmental_regulation > x '', by default None
         risk_factor_environmental_regulation_gte: Optional[int], optional
             filter by risk_factor_environmental_regulation, by default None
         risk_factor_environmental_regulation_lt: Optional[int], optional
             filter by risk_factor_environmental_regulation, by default None
         risk_factor_environmental_regulation_lte: Optional[int], optional
             filter by risk_factor_environmental_regulation, by default None
         risk_factor_domestic_gas_needs: Optional[int], optional
             Various risks associated with domestic gas needs, by default None
         risk_factor_domestic_gas_needs_gt: Optional[int], optional
             filter by '' risk_factor_domestic_gas_needs > x '', by default None
         risk_factor_domestic_gas_needs_gte: Optional[int], optional
             filter by risk_factor_domestic_gas_needs, by default None
         risk_factor_domestic_gas_needs_lt: Optional[int], optional
             filter by risk_factor_domestic_gas_needs, by default None
         risk_factor_domestic_gas_needs_lte: Optional[int], optional
             filter by risk_factor_domestic_gas_needs, by default None
         risk_factor_partner_priorities: Optional[int], optional
             Various risks associated with partner priorities, by default None
         risk_factor_partner_priorities_gt: Optional[int], optional
             filter by '' risk_factor_partner_priorities > x '', by default None
         risk_factor_partner_priorities_gte: Optional[int], optional
             filter by risk_factor_partner_priorities, by default None
         risk_factor_partner_priorities_lt: Optional[int], optional
             filter by risk_factor_partner_priorities, by default None
         risk_factor_partner_priorities_lte: Optional[int], optional
             filter by risk_factor_partner_priorities, by default None
         risk_factor_project_economics: Optional[int], optional
             Various risks associated with project economics, by default None
         risk_factor_project_economics_gt: Optional[int], optional
             filter by '' risk_factor_project_economics > x '', by default None
         risk_factor_project_economics_gte: Optional[int], optional
             filter by risk_factor_project_economics, by default None
         risk_factor_project_economics_lt: Optional[int], optional
             filter by risk_factor_project_economics, by default None
         risk_factor_project_economics_lte: Optional[int], optional
             filter by risk_factor_project_economics, by default None
         risk_factor_ability_to_execute: Optional[int], optional
             Various risks associated with execution ability, by default None
         risk_factor_ability_to_execute_gt: Optional[int], optional
             filter by '' risk_factor_ability_to_execute > x '', by default None
         risk_factor_ability_to_execute_gte: Optional[int], optional
             filter by risk_factor_ability_to_execute, by default None
         risk_factor_ability_to_execute_lt: Optional[int], optional
             filter by risk_factor_ability_to_execute, by default None
         risk_factor_ability_to_execute_lte: Optional[int], optional
             filter by risk_factor_ability_to_execute, by default None
         risk_factor_contracts: Optional[int], optional
             Various risks associated with contracts, by default None
         risk_factor_contracts_gt: Optional[int], optional
             filter by '' risk_factor_contracts > x '', by default None
         risk_factor_contracts_gte: Optional[int], optional
             filter by risk_factor_contracts, by default None
         risk_factor_contracts_lt: Optional[int], optional
             filter by risk_factor_contracts, by default None
         risk_factor_contracts_lte: Optional[int], optional
             filter by risk_factor_contracts, by default None
         risk_factor_overall: Optional[int], optional
             Various risks associated with overall project risk, by default None
         risk_factor_overall_gt: Optional[int], optional
             filter by '' risk_factor_overall > x '', by default None
         risk_factor_overall_gte: Optional[int], optional
             filter by risk_factor_overall, by default None
         risk_factor_overall_lt: Optional[int], optional
             filter by risk_factor_overall, by default None
         risk_factor_overall_lte: Optional[int], optional
             filter by risk_factor_overall, by default None
         estimated_final_investment_decision_date: Optional[datetime], optional
             Projected date for the final investment decision, by default None
         estimated_final_investment_decision_date_gt: Optional[datetime], optional
             filter by '' estimated_final_investment_decision_date > x '', by default None
         estimated_final_investment_decision_date_gte: Optional[datetime], optional
             filter by estimated_final_investment_decision_date, by default None
         estimated_final_investment_decision_date_lt: Optional[datetime], optional
             filter by estimated_final_investment_decision_date, by default None
         estimated_final_investment_decision_date_lte: Optional[datetime], optional
             filter by estimated_final_investment_decision_date, by default None
         number_of_trains: Optional[int], optional
             Total number of liquefaction trains for each record, by default None
         number_of_trains_gt: Optional[int], optional
             filter by '' number_of_trains > x '', by default None
         number_of_trains_gte: Optional[int], optional
             filter by number_of_trains, by default None
         number_of_trains_lt: Optional[int], optional
             filter by number_of_trains, by default None
         number_of_trains_lte: Optional[int], optional
             filter by number_of_trains, by default None
         flng_charterer: Optional[Union[list[str], Series[str], str]]
             Entity chartering any floating LNG facilities, by default None
         project_type: Optional[Union[list[str], Series[str], str]]
             Classification of the project type (e.g., onshore, offshore, floating), by default None
         liquefaction_train_feature: Optional[Union[list[str], Series[str], str]]
             Types of features of liquefaction trains ranging from capacity to storage to capital expenditure (capex) to other facility-specific characteristics, by default None
         liquefaction_train_feature_uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure of the corresponding liquefaction train feature, by default None
         liquefaction_train_feature_currency: Optional[Union[list[str], Series[str], str]]
             Currency of the corresponding liquefaction train feature, by default None
         modified_date: Optional[datetime], optional
             Liquefaction Trains record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("liquefactionTrain", liquefaction_train))
        filter_params.append(
            list_to_filter("liquefactionProject", liquefaction_project)
        )
        filter_params.append(list_to_filter("trainStatus", train_status))
        filter_params.append(list_to_filter("announcedStartDate", announced_start_date))
        if announced_start_date_gt is not None:
            filter_params.append(f'announcedStartDate > "{announced_start_date_gt}"')
        if announced_start_date_gte is not None:
            filter_params.append(f'announcedStartDate >= "{announced_start_date_gte}"')
        if announced_start_date_lt is not None:
            filter_params.append(f'announcedStartDate < "{announced_start_date_lt}"')
        if announced_start_date_lte is not None:
            filter_params.append(f'announcedStartDate <= "{announced_start_date_lte}"')
        filter_params.append(list_to_filter("estimatedStartDate", estimated_start_date))
        if estimated_start_date_gt is not None:
            filter_params.append(f'estimatedStartDate > "{estimated_start_date_gt}"')
        if estimated_start_date_gte is not None:
            filter_params.append(f'estimatedStartDate >= "{estimated_start_date_gte}"')
        if estimated_start_date_lt is not None:
            filter_params.append(f'estimatedStartDate < "{estimated_start_date_lt}"')
        if estimated_start_date_lte is not None:
            filter_params.append(f'estimatedStartDate <= "{estimated_start_date_lte}"')
        filter_params.append(list_to_filter("offlineDate", offline_date))
        if offline_date_gt is not None:
            filter_params.append(f'offlineDate > "{offline_date_gt}"')
        if offline_date_gte is not None:
            filter_params.append(f'offlineDate >= "{offline_date_gte}"')
        if offline_date_lt is not None:
            filter_params.append(f'offlineDate < "{offline_date_lt}"')
        if offline_date_lte is not None:
            filter_params.append(f'offlineDate <= "{offline_date_lte}"')
        filter_params.append(list_to_filter("greenBrownfield", green_brownfield))
        filter_params.append(
            list_to_filter("liquefactionTechnology", liquefaction_technology)
        )
        filter_params.append(list_to_filter("createdDate", created_date))
        if created_date_gt is not None:
            filter_params.append(f'createdDate > "{created_date_gt}"')
        if created_date_gte is not None:
            filter_params.append(f'createdDate >= "{created_date_gte}"')
        if created_date_lt is not None:
            filter_params.append(f'createdDate < "{created_date_lt}"')
        if created_date_lte is not None:
            filter_params.append(f'createdDate <= "{created_date_lte}"')
        filter_params.append(list_to_filter("statusModifiedDate", status_modified_date))
        if status_modified_date_gt is not None:
            filter_params.append(f'statusModifiedDate > "{status_modified_date_gt}"')
        if status_modified_date_gte is not None:
            filter_params.append(f'statusModifiedDate >= "{status_modified_date_gte}"')
        if status_modified_date_lt is not None:
            filter_params.append(f'statusModifiedDate < "{status_modified_date_lt}"')
        if status_modified_date_lte is not None:
            filter_params.append(f'statusModifiedDate <= "{status_modified_date_lte}"')
        filter_params.append(
            list_to_filter("capacityModifiedDate", capacity_modified_date)
        )
        if capacity_modified_date_gt is not None:
            filter_params.append(
                f'capacityModifiedDate > "{capacity_modified_date_gt}"'
            )
        if capacity_modified_date_gte is not None:
            filter_params.append(
                f'capacityModifiedDate >= "{capacity_modified_date_gte}"'
            )
        if capacity_modified_date_lt is not None:
            filter_params.append(
                f'capacityModifiedDate < "{capacity_modified_date_lt}"'
            )
        if capacity_modified_date_lte is not None:
            filter_params.append(
                f'capacityModifiedDate <= "{capacity_modified_date_lte}"'
            )
        filter_params.append(
            list_to_filter(
                "announcedStartDateModifiedDate", announced_start_date_modified_date
            )
        )
        if announced_start_date_modified_date_gt is not None:
            filter_params.append(
                f'announcedStartDateModifiedDate > "{announced_start_date_modified_date_gt}"'
            )
        if announced_start_date_modified_date_gte is not None:
            filter_params.append(
                f'announcedStartDateModifiedDate >= "{announced_start_date_modified_date_gte}"'
            )
        if announced_start_date_modified_date_lt is not None:
            filter_params.append(
                f'announcedStartDateModifiedDate < "{announced_start_date_modified_date_lt}"'
            )
        if announced_start_date_modified_date_lte is not None:
            filter_params.append(
                f'announcedStartDateModifiedDate <= "{announced_start_date_modified_date_lte}"'
            )
        filter_params.append(
            list_to_filter(
                "estimatedStartDateModifiedDate", estimated_start_date_modified_date
            )
        )
        if estimated_start_date_modified_date_gt is not None:
            filter_params.append(
                f'estimatedStartDateModifiedDate > "{estimated_start_date_modified_date_gt}"'
            )
        if estimated_start_date_modified_date_gte is not None:
            filter_params.append(
                f'estimatedStartDateModifiedDate >= "{estimated_start_date_modified_date_gte}"'
            )
        if estimated_start_date_modified_date_lt is not None:
            filter_params.append(
                f'estimatedStartDateModifiedDate < "{estimated_start_date_modified_date_lt}"'
            )
        if estimated_start_date_modified_date_lte is not None:
            filter_params.append(
                f'estimatedStartDateModifiedDate <= "{estimated_start_date_modified_date_lte}"'
            )
        filter_params.append(
            list_to_filter(
                "announcedStartDateAtFinalInvestmentDecision",
                announced_start_date_at_final_investment_decision,
            )
        )
        if announced_start_date_at_final_investment_decision_gt is not None:
            filter_params.append(
                f'announcedStartDateAtFinalInvestmentDecision > "{announced_start_date_at_final_investment_decision_gt}"'
            )
        if announced_start_date_at_final_investment_decision_gte is not None:
            filter_params.append(
                f'announcedStartDateAtFinalInvestmentDecision >= "{announced_start_date_at_final_investment_decision_gte}"'
            )
        if announced_start_date_at_final_investment_decision_lt is not None:
            filter_params.append(
                f'announcedStartDateAtFinalInvestmentDecision < "{announced_start_date_at_final_investment_decision_lt}"'
            )
        if announced_start_date_at_final_investment_decision_lte is not None:
            filter_params.append(
                f'announcedStartDateAtFinalInvestmentDecision <= "{announced_start_date_at_final_investment_decision_lte}"'
            )
        filter_params.append(
            list_to_filter(
                "latestAnnouncedFinalInvestmentDecisionDate",
                latest_announced_final_investment_decision_date,
            )
        )
        if latest_announced_final_investment_decision_date_gt is not None:
            filter_params.append(
                f'latestAnnouncedFinalInvestmentDecisionDate > "{latest_announced_final_investment_decision_date_gt}"'
            )
        if latest_announced_final_investment_decision_date_gte is not None:
            filter_params.append(
                f'latestAnnouncedFinalInvestmentDecisionDate >= "{latest_announced_final_investment_decision_date_gte}"'
            )
        if latest_announced_final_investment_decision_date_lt is not None:
            filter_params.append(
                f'latestAnnouncedFinalInvestmentDecisionDate < "{latest_announced_final_investment_decision_date_lt}"'
            )
        if latest_announced_final_investment_decision_date_lte is not None:
            filter_params.append(
                f'latestAnnouncedFinalInvestmentDecisionDate <= "{latest_announced_final_investment_decision_date_lte}"'
            )
        filter_params.append(
            list_to_filter("estimatedFirstCargoDate", estimated_first_cargo_date)
        )
        if estimated_first_cargo_date_gt is not None:
            filter_params.append(
                f'estimatedFirstCargoDate > "{estimated_first_cargo_date_gt}"'
            )
        if estimated_first_cargo_date_gte is not None:
            filter_params.append(
                f'estimatedFirstCargoDate >= "{estimated_first_cargo_date_gte}"'
            )
        if estimated_first_cargo_date_lt is not None:
            filter_params.append(
                f'estimatedFirstCargoDate < "{estimated_first_cargo_date_lt}"'
            )
        if estimated_first_cargo_date_lte is not None:
            filter_params.append(
                f'estimatedFirstCargoDate <= "{estimated_first_cargo_date_lte}"'
            )
        filter_params.append(
            list_to_filter(
                "riskFactorFeedstockAvailability", risk_factor_feedstock_availability
            )
        )
        if risk_factor_feedstock_availability_gt is not None:
            filter_params.append(
                f'riskFactorFeedstockAvailability > "{risk_factor_feedstock_availability_gt}"'
            )
        if risk_factor_feedstock_availability_gte is not None:
            filter_params.append(
                f'riskFactorFeedstockAvailability >= "{risk_factor_feedstock_availability_gte}"'
            )
        if risk_factor_feedstock_availability_lt is not None:
            filter_params.append(
                f'riskFactorFeedstockAvailability < "{risk_factor_feedstock_availability_lt}"'
            )
        if risk_factor_feedstock_availability_lte is not None:
            filter_params.append(
                f'riskFactorFeedstockAvailability <= "{risk_factor_feedstock_availability_lte}"'
            )
        filter_params.append(
            list_to_filter(
                "riskFactorPoliticsAndGeopolitics", risk_factor_politics_and_geopolitics
            )
        )
        if risk_factor_politics_and_geopolitics_gt is not None:
            filter_params.append(
                f'riskFactorPoliticsAndGeopolitics > "{risk_factor_politics_and_geopolitics_gt}"'
            )
        if risk_factor_politics_and_geopolitics_gte is not None:
            filter_params.append(
                f'riskFactorPoliticsAndGeopolitics >= "{risk_factor_politics_and_geopolitics_gte}"'
            )
        if risk_factor_politics_and_geopolitics_lt is not None:
            filter_params.append(
                f'riskFactorPoliticsAndGeopolitics < "{risk_factor_politics_and_geopolitics_lt}"'
            )
        if risk_factor_politics_and_geopolitics_lte is not None:
            filter_params.append(
                f'riskFactorPoliticsAndGeopolitics <= "{risk_factor_politics_and_geopolitics_lte}"'
            )
        filter_params.append(
            list_to_filter(
                "riskFactorEnvironmentalRegulation",
                risk_factor_environmental_regulation,
            )
        )
        if risk_factor_environmental_regulation_gt is not None:
            filter_params.append(
                f'riskFactorEnvironmentalRegulation > "{risk_factor_environmental_regulation_gt}"'
            )
        if risk_factor_environmental_regulation_gte is not None:
            filter_params.append(
                f'riskFactorEnvironmentalRegulation >= "{risk_factor_environmental_regulation_gte}"'
            )
        if risk_factor_environmental_regulation_lt is not None:
            filter_params.append(
                f'riskFactorEnvironmentalRegulation < "{risk_factor_environmental_regulation_lt}"'
            )
        if risk_factor_environmental_regulation_lte is not None:
            filter_params.append(
                f'riskFactorEnvironmentalRegulation <= "{risk_factor_environmental_regulation_lte}"'
            )
        filter_params.append(
            list_to_filter("riskFactorDomesticGasNeeds", risk_factor_domestic_gas_needs)
        )
        if risk_factor_domestic_gas_needs_gt is not None:
            filter_params.append(
                f'riskFactorDomesticGasNeeds > "{risk_factor_domestic_gas_needs_gt}"'
            )
        if risk_factor_domestic_gas_needs_gte is not None:
            filter_params.append(
                f'riskFactorDomesticGasNeeds >= "{risk_factor_domestic_gas_needs_gte}"'
            )
        if risk_factor_domestic_gas_needs_lt is not None:
            filter_params.append(
                f'riskFactorDomesticGasNeeds < "{risk_factor_domestic_gas_needs_lt}"'
            )
        if risk_factor_domestic_gas_needs_lte is not None:
            filter_params.append(
                f'riskFactorDomesticGasNeeds <= "{risk_factor_domestic_gas_needs_lte}"'
            )
        filter_params.append(
            list_to_filter(
                "riskFactorPartnerPriorities", risk_factor_partner_priorities
            )
        )
        if risk_factor_partner_priorities_gt is not None:
            filter_params.append(
                f'riskFactorPartnerPriorities > "{risk_factor_partner_priorities_gt}"'
            )
        if risk_factor_partner_priorities_gte is not None:
            filter_params.append(
                f'riskFactorPartnerPriorities >= "{risk_factor_partner_priorities_gte}"'
            )
        if risk_factor_partner_priorities_lt is not None:
            filter_params.append(
                f'riskFactorPartnerPriorities < "{risk_factor_partner_priorities_lt}"'
            )
        if risk_factor_partner_priorities_lte is not None:
            filter_params.append(
                f'riskFactorPartnerPriorities <= "{risk_factor_partner_priorities_lte}"'
            )
        filter_params.append(
            list_to_filter("riskFactorProjectEconomics", risk_factor_project_economics)
        )
        if risk_factor_project_economics_gt is not None:
            filter_params.append(
                f'riskFactorProjectEconomics > "{risk_factor_project_economics_gt}"'
            )
        if risk_factor_project_economics_gte is not None:
            filter_params.append(
                f'riskFactorProjectEconomics >= "{risk_factor_project_economics_gte}"'
            )
        if risk_factor_project_economics_lt is not None:
            filter_params.append(
                f'riskFactorProjectEconomics < "{risk_factor_project_economics_lt}"'
            )
        if risk_factor_project_economics_lte is not None:
            filter_params.append(
                f'riskFactorProjectEconomics <= "{risk_factor_project_economics_lte}"'
            )
        filter_params.append(
            list_to_filter("riskFactorAbilityToExecute", risk_factor_ability_to_execute)
        )
        if risk_factor_ability_to_execute_gt is not None:
            filter_params.append(
                f'riskFactorAbilityToExecute > "{risk_factor_ability_to_execute_gt}"'
            )
        if risk_factor_ability_to_execute_gte is not None:
            filter_params.append(
                f'riskFactorAbilityToExecute >= "{risk_factor_ability_to_execute_gte}"'
            )
        if risk_factor_ability_to_execute_lt is not None:
            filter_params.append(
                f'riskFactorAbilityToExecute < "{risk_factor_ability_to_execute_lt}"'
            )
        if risk_factor_ability_to_execute_lte is not None:
            filter_params.append(
                f'riskFactorAbilityToExecute <= "{risk_factor_ability_to_execute_lte}"'
            )
        filter_params.append(
            list_to_filter("riskFactorContracts", risk_factor_contracts)
        )
        if risk_factor_contracts_gt is not None:
            filter_params.append(f'riskFactorContracts > "{risk_factor_contracts_gt}"')
        if risk_factor_contracts_gte is not None:
            filter_params.append(
                f'riskFactorContracts >= "{risk_factor_contracts_gte}"'
            )
        if risk_factor_contracts_lt is not None:
            filter_params.append(f'riskFactorContracts < "{risk_factor_contracts_lt}"')
        if risk_factor_contracts_lte is not None:
            filter_params.append(
                f'riskFactorContracts <= "{risk_factor_contracts_lte}"'
            )
        filter_params.append(list_to_filter("riskFactorOverall", risk_factor_overall))
        if risk_factor_overall_gt is not None:
            filter_params.append(f'riskFactorOverall > "{risk_factor_overall_gt}"')
        if risk_factor_overall_gte is not None:
            filter_params.append(f'riskFactorOverall >= "{risk_factor_overall_gte}"')
        if risk_factor_overall_lt is not None:
            filter_params.append(f'riskFactorOverall < "{risk_factor_overall_lt}"')
        if risk_factor_overall_lte is not None:
            filter_params.append(f'riskFactorOverall <= "{risk_factor_overall_lte}"')
        filter_params.append(
            list_to_filter(
                "estimatedFinalInvestmentDecisionDate",
                estimated_final_investment_decision_date,
            )
        )
        if estimated_final_investment_decision_date_gt is not None:
            filter_params.append(
                f'estimatedFinalInvestmentDecisionDate > "{estimated_final_investment_decision_date_gt}"'
            )
        if estimated_final_investment_decision_date_gte is not None:
            filter_params.append(
                f'estimatedFinalInvestmentDecisionDate >= "{estimated_final_investment_decision_date_gte}"'
            )
        if estimated_final_investment_decision_date_lt is not None:
            filter_params.append(
                f'estimatedFinalInvestmentDecisionDate < "{estimated_final_investment_decision_date_lt}"'
            )
        if estimated_final_investment_decision_date_lte is not None:
            filter_params.append(
                f'estimatedFinalInvestmentDecisionDate <= "{estimated_final_investment_decision_date_lte}"'
            )
        filter_params.append(list_to_filter("numberOfTrains", number_of_trains))
        if number_of_trains_gt is not None:
            filter_params.append(f'numberOfTrains > "{number_of_trains_gt}"')
        if number_of_trains_gte is not None:
            filter_params.append(f'numberOfTrains >= "{number_of_trains_gte}"')
        if number_of_trains_lt is not None:
            filter_params.append(f'numberOfTrains < "{number_of_trains_lt}"')
        if number_of_trains_lte is not None:
            filter_params.append(f'numberOfTrains <= "{number_of_trains_lte}"')
        filter_params.append(list_to_filter("flngCharterer", flng_charterer))
        filter_params.append(list_to_filter("projectType", project_type))
        filter_params.append(
            list_to_filter("liquefactionTrainFeature", liquefaction_train_feature)
        )
        filter_params.append(
            list_to_filter(
                "liquefactionTrainFeatureUom", liquefaction_train_feature_uom
            )
        )
        filter_params.append(
            list_to_filter(
                "liquefactionTrainFeatureCurrency", liquefaction_train_feature_currency
            )
        )
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/liquefaction-trains",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_offtake_contracts(
        self,
        *,
        liquefaction_project: Optional[Union[list[str], Series[str], str]] = None,
        contract_group: Optional[Union[list[str], Series[str], str]] = None,
        exporter: Optional[Union[list[str], Series[str], str]] = None,
        buyer: Optional[Union[list[str], Series[str], str]] = None,
        assumed_destination: Optional[Union[list[str], Series[str], str]] = None,
        original_signing_date: Optional[datetime] = None,
        original_signing_date_lt: Optional[datetime] = None,
        original_signing_date_lte: Optional[datetime] = None,
        original_signing_date_gt: Optional[datetime] = None,
        original_signing_date_gte: Optional[datetime] = None,
        latest_contract_revision_date: Optional[
            Union[list[str], Series[str], str]
        ] = None,
        announced_start_date: Optional[datetime] = None,
        announced_start_date_lt: Optional[datetime] = None,
        announced_start_date_lte: Optional[datetime] = None,
        announced_start_date_gt: Optional[datetime] = None,
        announced_start_date_gte: Optional[datetime] = None,
        preliminary_signing_date: Optional[datetime] = None,
        preliminary_signing_date_lt: Optional[datetime] = None,
        preliminary_signing_date_lte: Optional[datetime] = None,
        preliminary_signing_date_gt: Optional[datetime] = None,
        preliminary_signing_date_gte: Optional[datetime] = None,
        length_years: Optional[float] = None,
        length_years_lt: Optional[float] = None,
        length_years_lte: Optional[float] = None,
        length_years_gt: Optional[float] = None,
        length_years_gte: Optional[float] = None,
        contract_model_type: Optional[Union[list[str], Series[str], str]] = None,
        percentage_of_train: Optional[float] = None,
        percentage_of_train_lt: Optional[float] = None,
        percentage_of_train_lte: Optional[float] = None,
        percentage_of_train_gt: Optional[float] = None,
        percentage_of_train_gte: Optional[float] = None,
        destination_flexibility: Optional[Union[list[str], Series[str], str]] = None,
        contract_status: Optional[Union[list[str], Series[str], str]] = None,
        shipping_terms: Optional[Union[list[str], Series[str], str]] = None,
        contract_price_linkage_type: Optional[
            Union[list[str], Series[str], str]
        ] = None,
        contract_price_slope: Optional[float] = None,
        contract_price_slope_lt: Optional[float] = None,
        contract_price_slope_lte: Optional[float] = None,
        contract_price_slope_gt: Optional[float] = None,
        contract_price_slope_gte: Optional[float] = None,
        contract_price_linkage: Optional[Union[list[str], Series[str], str]] = None,
        fid_enabling: Optional[Union[list[str], Series[str], str]] = None,
        green_or_brownfield: Optional[Union[list[str], Series[str], str]] = None,
        created_date: Optional[datetime] = None,
        created_date_lt: Optional[datetime] = None,
        created_date_lte: Optional[datetime] = None,
        created_date_gt: Optional[datetime] = None,
        created_date_gte: Optional[datetime] = None,
        buyer_modified_date: Optional[datetime] = None,
        buyer_modified_date_lt: Optional[datetime] = None,
        buyer_modified_date_lte: Optional[datetime] = None,
        buyer_modified_date_gt: Optional[datetime] = None,
        buyer_modified_date_gte: Optional[datetime] = None,
        announced_start_modified_date: Optional[datetime] = None,
        announced_start_modified_date_lt: Optional[datetime] = None,
        announced_start_modified_date_lte: Optional[datetime] = None,
        announced_start_modified_date_gt: Optional[datetime] = None,
        announced_start_modified_date_gte: Optional[datetime] = None,
        length_modified_date: Optional[datetime] = None,
        length_modified_date_lt: Optional[datetime] = None,
        length_modified_date_lte: Optional[datetime] = None,
        length_modified_date_gt: Optional[datetime] = None,
        length_modified_date_gte: Optional[datetime] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        published_volume_modified_date: Optional[datetime] = None,
        published_volume_modified_date_lt: Optional[datetime] = None,
        published_volume_modified_date_lte: Optional[datetime] = None,
        published_volume_modified_date_gt: Optional[datetime] = None,
        published_volume_modified_date_gte: Optional[datetime] = None,
        estimated_buildout_modified_date: Optional[datetime] = None,
        estimated_buildout_modified_date_lt: Optional[datetime] = None,
        estimated_buildout_modified_date_lte: Optional[datetime] = None,
        estimated_buildout_modified_date_gt: Optional[datetime] = None,
        estimated_buildout_modified_date_gte: Optional[datetime] = None,
        contract_volume_type: Optional[Union[list[str], Series[str], str]] = None,
        contract_volume_uom: Optional[Union[list[str], Series[str], str]] = None,
        supply_market: Optional[Union[list[str], Series[str], str]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        List of all announced and observed offtake contract relationships for liquefaction projects and company portfolios as well as their attributes

        Parameters
        ----------

         liquefaction_project: Optional[Union[list[str], Series[str], str]]
             Name of the associated liquefaction project, by default None
         contract_group: Optional[Union[list[str], Series[str], str]]
             Group or consortium involved in the contract, by default None
         exporter: Optional[Union[list[str], Series[str], str]]
             Entity responsible for exporting the LNG, by default None
         buyer: Optional[Union[list[str], Series[str], str]]
             Entity purchasing the LNG, by default None
         assumed_destination: Optional[Union[list[str], Series[str], str]]
             Expected delivery location for the LNG, by default None
         original_signing_date: Optional[datetime], optional
             Date when the contract was first signed, by default None
         original_signing_date_gt: Optional[datetime], optional
             filter by '' original_signing_date > x '', by default None
         original_signing_date_gte: Optional[datetime], optional
             filter by original_signing_date, by default None
         original_signing_date_lt: Optional[datetime], optional
             filter by original_signing_date, by default None
         original_signing_date_lte: Optional[datetime], optional
             filter by original_signing_date, by default None
         latest_contract_revision_date: Optional[Union[list[str], Series[str], str]]
             Date of the most recent contract amendment, by default None
         announced_start_date: Optional[datetime], optional
             Publicly declared start date of the contract, by default None
         announced_start_date_gt: Optional[datetime], optional
             filter by '' announced_start_date > x '', by default None
         announced_start_date_gte: Optional[datetime], optional
             filter by announced_start_date, by default None
         announced_start_date_lt: Optional[datetime], optional
             filter by announced_start_date, by default None
         announced_start_date_lte: Optional[datetime], optional
             filter by announced_start_date, by default None
         preliminary_signing_date: Optional[datetime], optional
             Date when the contract was preliminarily signed, by default None
         preliminary_signing_date_gt: Optional[datetime], optional
             filter by '' preliminary_signing_date > x '', by default None
         preliminary_signing_date_gte: Optional[datetime], optional
             filter by preliminary_signing_date, by default None
         preliminary_signing_date_lt: Optional[datetime], optional
             filter by preliminary_signing_date, by default None
         preliminary_signing_date_lte: Optional[datetime], optional
             filter by preliminary_signing_date, by default None
         length_years: Optional[float], optional
             Duration of the contract in years, by default None
         length_years_gt: Optional[float], optional
             filter by '' length_years > x '', by default None
         length_years_gte: Optional[float], optional
             filter by length_years, by default None
         length_years_lt: Optional[float], optional
             filter by length_years, by default None
         length_years_lte: Optional[float], optional
             filter by length_years, by default None
         contract_model_type: Optional[Union[list[str], Series[str], str]]
             Type of contract model used, by default None
         percentage_of_train: Optional[float], optional
             Share of the liquefaction train's capacity allocated to the contract, by default None
         percentage_of_train_gt: Optional[float], optional
             filter by '' percentage_of_train > x '', by default None
         percentage_of_train_gte: Optional[float], optional
             filter by percentage_of_train, by default None
         percentage_of_train_lt: Optional[float], optional
             filter by percentage_of_train, by default None
         percentage_of_train_lte: Optional[float], optional
             filter by percentage_of_train, by default None
         destination_flexibility: Optional[Union[list[str], Series[str], str]]
             Designation if the offtake contract is destination-fixed or is flexible, by default None
         contract_status: Optional[Union[list[str], Series[str], str]]
             Current status of the contract, by default None
         shipping_terms: Optional[Union[list[str], Series[str], str]]
             Terms related to the transportation of LNG, by default None
         contract_price_linkage_type: Optional[Union[list[str], Series[str], str]]
             Identifies the general commodity that the pricing formula is applied to, by default None
         contract_price_slope: Optional[float], optional
             Slope of the price formula in the contract, by default None
         contract_price_slope_gt: Optional[float], optional
             filter by '' contract_price_slope > x '', by default None
         contract_price_slope_gte: Optional[float], optional
             filter by contract_price_slope, by default None
         contract_price_slope_lt: Optional[float], optional
             filter by contract_price_slope, by default None
         contract_price_slope_lte: Optional[float], optional
             filter by contract_price_slope, by default None
         contract_price_linkage: Optional[Union[list[str], Series[str], str]]
             Identifies the specific price marker that the pricing formula is applied to, by default None
         fid_enabling: Optional[Union[list[str], Series[str], str]]
             Indicates if the contract enables the final investment decision, by default None
         green_or_brownfield: Optional[Union[list[str], Series[str], str]]
             Indicates if the project is a new development (greenfield) or an upgrade (brownfield), by default None
         created_date: Optional[datetime], optional
             Date when the contract record was created, by default None
         created_date_gt: Optional[datetime], optional
             filter by '' created_date > x '', by default None
         created_date_gte: Optional[datetime], optional
             filter by created_date, by default None
         created_date_lt: Optional[datetime], optional
             filter by created_date, by default None
         created_date_lte: Optional[datetime], optional
             filter by created_date, by default None
         buyer_modified_date: Optional[datetime], optional
             Date when the buyer information was last updated, by default None
         buyer_modified_date_gt: Optional[datetime], optional
             filter by '' buyer_modified_date > x '', by default None
         buyer_modified_date_gte: Optional[datetime], optional
             filter by buyer_modified_date, by default None
         buyer_modified_date_lt: Optional[datetime], optional
             filter by buyer_modified_date, by default None
         buyer_modified_date_lte: Optional[datetime], optional
             filter by buyer_modified_date, by default None
         announced_start_modified_date: Optional[datetime], optional
             Date when the announced start date was last updated, by default None
         announced_start_modified_date_gt: Optional[datetime], optional
             filter by '' announced_start_modified_date > x '', by default None
         announced_start_modified_date_gte: Optional[datetime], optional
             filter by announced_start_modified_date, by default None
         announced_start_modified_date_lt: Optional[datetime], optional
             filter by announced_start_modified_date, by default None
         announced_start_modified_date_lte: Optional[datetime], optional
             filter by announced_start_modified_date, by default None
         length_modified_date: Optional[datetime], optional
             Date when the contract length was last updated, by default None
         length_modified_date_gt: Optional[datetime], optional
             filter by '' length_modified_date > x '', by default None
         length_modified_date_gte: Optional[datetime], optional
             filter by length_modified_date, by default None
         length_modified_date_lt: Optional[datetime], optional
             filter by length_modified_date, by default None
         length_modified_date_lte: Optional[datetime], optional
             filter by length_modified_date, by default None
         modified_date: Optional[datetime], optional
             Date when the contract was last modified, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         published_volume_modified_date: Optional[datetime], optional
             Date when the published volume was last updated, by default None
         published_volume_modified_date_gt: Optional[datetime], optional
             filter by '' published_volume_modified_date > x '', by default None
         published_volume_modified_date_gte: Optional[datetime], optional
             filter by published_volume_modified_date, by default None
         published_volume_modified_date_lt: Optional[datetime], optional
             filter by published_volume_modified_date, by default None
         published_volume_modified_date_lte: Optional[datetime], optional
             filter by published_volume_modified_date, by default None
         estimated_buildout_modified_date: Optional[datetime], optional
             Date when the estimated buildout was last updated, by default None
         estimated_buildout_modified_date_gt: Optional[datetime], optional
             filter by '' estimated_buildout_modified_date > x '', by default None
         estimated_buildout_modified_date_gte: Optional[datetime], optional
             filter by estimated_buildout_modified_date, by default None
         estimated_buildout_modified_date_lt: Optional[datetime], optional
             filter by estimated_buildout_modified_date, by default None
         estimated_buildout_modified_date_lte: Optional[datetime], optional
             filter by estimated_buildout_modified_date, by default None
         contract_volume_type: Optional[Union[list[str], Series[str], str]]
             Type of contract volume information, by default None
         contract_volume_uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure of the contract volume, by default None
         supply_market: Optional[Union[list[str], Series[str], str]]
             Market supplying the LNG for the contract, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(
            list_to_filter("liquefactionProject", liquefaction_project)
        )
        filter_params.append(list_to_filter("contractGroup", contract_group))
        filter_params.append(list_to_filter("exporter", exporter))
        filter_params.append(list_to_filter("buyer", buyer))
        filter_params.append(list_to_filter("assumedDestination", assumed_destination))
        filter_params.append(
            list_to_filter("originalSigningDate", original_signing_date)
        )
        if original_signing_date_gt is not None:
            filter_params.append(f'originalSigningDate > "{original_signing_date_gt}"')
        if original_signing_date_gte is not None:
            filter_params.append(
                f'originalSigningDate >= "{original_signing_date_gte}"'
            )
        if original_signing_date_lt is not None:
            filter_params.append(f'originalSigningDate < "{original_signing_date_lt}"')
        if original_signing_date_lte is not None:
            filter_params.append(
                f'originalSigningDate <= "{original_signing_date_lte}"'
            )
        filter_params.append(
            list_to_filter("latestContractRevisionDate", latest_contract_revision_date)
        )
        filter_params.append(list_to_filter("announcedStartDate", announced_start_date))
        if announced_start_date_gt is not None:
            filter_params.append(f'announcedStartDate > "{announced_start_date_gt}"')
        if announced_start_date_gte is not None:
            filter_params.append(f'announcedStartDate >= "{announced_start_date_gte}"')
        if announced_start_date_lt is not None:
            filter_params.append(f'announcedStartDate < "{announced_start_date_lt}"')
        if announced_start_date_lte is not None:
            filter_params.append(f'announcedStartDate <= "{announced_start_date_lte}"')
        filter_params.append(
            list_to_filter("preliminarySigningDate", preliminary_signing_date)
        )
        if preliminary_signing_date_gt is not None:
            filter_params.append(
                f'preliminarySigningDate > "{preliminary_signing_date_gt}"'
            )
        if preliminary_signing_date_gte is not None:
            filter_params.append(
                f'preliminarySigningDate >= "{preliminary_signing_date_gte}"'
            )
        if preliminary_signing_date_lt is not None:
            filter_params.append(
                f'preliminarySigningDate < "{preliminary_signing_date_lt}"'
            )
        if preliminary_signing_date_lte is not None:
            filter_params.append(
                f'preliminarySigningDate <= "{preliminary_signing_date_lte}"'
            )
        filter_params.append(list_to_filter("lengthYears", length_years))
        if length_years_gt is not None:
            filter_params.append(f'lengthYears > "{length_years_gt}"')
        if length_years_gte is not None:
            filter_params.append(f'lengthYears >= "{length_years_gte}"')
        if length_years_lt is not None:
            filter_params.append(f'lengthYears < "{length_years_lt}"')
        if length_years_lte is not None:
            filter_params.append(f'lengthYears <= "{length_years_lte}"')
        filter_params.append(list_to_filter("contractModelType", contract_model_type))
        filter_params.append(list_to_filter("percentageOfTrain", percentage_of_train))
        if percentage_of_train_gt is not None:
            filter_params.append(f'percentageOfTrain > "{percentage_of_train_gt}"')
        if percentage_of_train_gte is not None:
            filter_params.append(f'percentageOfTrain >= "{percentage_of_train_gte}"')
        if percentage_of_train_lt is not None:
            filter_params.append(f'percentageOfTrain < "{percentage_of_train_lt}"')
        if percentage_of_train_lte is not None:
            filter_params.append(f'percentageOfTrain <= "{percentage_of_train_lte}"')
        filter_params.append(
            list_to_filter("destinationFlexibility", destination_flexibility)
        )
        filter_params.append(list_to_filter("contractStatus", contract_status))
        filter_params.append(list_to_filter("shippingTerms", shipping_terms))
        filter_params.append(
            list_to_filter("contractPriceLinkageType", contract_price_linkage_type)
        )
        filter_params.append(list_to_filter("contractPriceSlope", contract_price_slope))
        if contract_price_slope_gt is not None:
            filter_params.append(f'contractPriceSlope > "{contract_price_slope_gt}"')
        if contract_price_slope_gte is not None:
            filter_params.append(f'contractPriceSlope >= "{contract_price_slope_gte}"')
        if contract_price_slope_lt is not None:
            filter_params.append(f'contractPriceSlope < "{contract_price_slope_lt}"')
        if contract_price_slope_lte is not None:
            filter_params.append(f'contractPriceSlope <= "{contract_price_slope_lte}"')
        filter_params.append(
            list_to_filter("contractPriceLinkage", contract_price_linkage)
        )
        filter_params.append(list_to_filter("fidEnabling", fid_enabling))
        filter_params.append(list_to_filter("greenOrBrownfield", green_or_brownfield))
        filter_params.append(list_to_filter("createdDate", created_date))
        if created_date_gt is not None:
            filter_params.append(f'createdDate > "{created_date_gt}"')
        if created_date_gte is not None:
            filter_params.append(f'createdDate >= "{created_date_gte}"')
        if created_date_lt is not None:
            filter_params.append(f'createdDate < "{created_date_lt}"')
        if created_date_lte is not None:
            filter_params.append(f'createdDate <= "{created_date_lte}"')
        filter_params.append(list_to_filter("buyerModifiedDate", buyer_modified_date))
        if buyer_modified_date_gt is not None:
            filter_params.append(f'buyerModifiedDate > "{buyer_modified_date_gt}"')
        if buyer_modified_date_gte is not None:
            filter_params.append(f'buyerModifiedDate >= "{buyer_modified_date_gte}"')
        if buyer_modified_date_lt is not None:
            filter_params.append(f'buyerModifiedDate < "{buyer_modified_date_lt}"')
        if buyer_modified_date_lte is not None:
            filter_params.append(f'buyerModifiedDate <= "{buyer_modified_date_lte}"')
        filter_params.append(
            list_to_filter("announcedStartModifiedDate", announced_start_modified_date)
        )
        if announced_start_modified_date_gt is not None:
            filter_params.append(
                f'announcedStartModifiedDate > "{announced_start_modified_date_gt}"'
            )
        if announced_start_modified_date_gte is not None:
            filter_params.append(
                f'announcedStartModifiedDate >= "{announced_start_modified_date_gte}"'
            )
        if announced_start_modified_date_lt is not None:
            filter_params.append(
                f'announcedStartModifiedDate < "{announced_start_modified_date_lt}"'
            )
        if announced_start_modified_date_lte is not None:
            filter_params.append(
                f'announcedStartModifiedDate <= "{announced_start_modified_date_lte}"'
            )
        filter_params.append(list_to_filter("lengthModifiedDate", length_modified_date))
        if length_modified_date_gt is not None:
            filter_params.append(f'lengthModifiedDate > "{length_modified_date_gt}"')
        if length_modified_date_gte is not None:
            filter_params.append(f'lengthModifiedDate >= "{length_modified_date_gte}"')
        if length_modified_date_lt is not None:
            filter_params.append(f'lengthModifiedDate < "{length_modified_date_lt}"')
        if length_modified_date_lte is not None:
            filter_params.append(f'lengthModifiedDate <= "{length_modified_date_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')
        filter_params.append(
            list_to_filter(
                "publishedVolumeModifiedDate", published_volume_modified_date
            )
        )
        if published_volume_modified_date_gt is not None:
            filter_params.append(
                f'publishedVolumeModifiedDate > "{published_volume_modified_date_gt}"'
            )
        if published_volume_modified_date_gte is not None:
            filter_params.append(
                f'publishedVolumeModifiedDate >= "{published_volume_modified_date_gte}"'
            )
        if published_volume_modified_date_lt is not None:
            filter_params.append(
                f'publishedVolumeModifiedDate < "{published_volume_modified_date_lt}"'
            )
        if published_volume_modified_date_lte is not None:
            filter_params.append(
                f'publishedVolumeModifiedDate <= "{published_volume_modified_date_lte}"'
            )
        filter_params.append(
            list_to_filter(
                "estimatedBuildoutModifiedDate", estimated_buildout_modified_date
            )
        )
        if estimated_buildout_modified_date_gt is not None:
            filter_params.append(
                f'estimatedBuildoutModifiedDate > "{estimated_buildout_modified_date_gt}"'
            )
        if estimated_buildout_modified_date_gte is not None:
            filter_params.append(
                f'estimatedBuildoutModifiedDate >= "{estimated_buildout_modified_date_gte}"'
            )
        if estimated_buildout_modified_date_lt is not None:
            filter_params.append(
                f'estimatedBuildoutModifiedDate < "{estimated_buildout_modified_date_lt}"'
            )
        if estimated_buildout_modified_date_lte is not None:
            filter_params.append(
                f'estimatedBuildoutModifiedDate <= "{estimated_buildout_modified_date_lte}"'
            )
        filter_params.append(list_to_filter("contractVolumeType", contract_volume_type))
        filter_params.append(list_to_filter("contractVolumeUom", contract_volume_uom))
        filter_params.append(list_to_filter("supplyMarket", supply_market))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/offtake-contracts",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_regasification_contracts(
        self,
        *,
        regasification_phase: Optional[Union[list[str], Series[str], str]] = None,
        regasification_project: Optional[Union[list[str], Series[str], str]] = None,
        capacity_owner: Optional[Union[list[str], Series[str], str]] = None,
        contract_type: Optional[Union[list[str], Series[str], str]] = None,
        contract_length_years: Optional[float] = None,
        contract_length_years_lt: Optional[float] = None,
        contract_length_years_lte: Optional[float] = None,
        contract_length_years_gt: Optional[float] = None,
        contract_length_years_gte: Optional[float] = None,
        contract_start_date: Optional[datetime] = None,
        contract_start_date_lt: Optional[datetime] = None,
        contract_start_date_lte: Optional[datetime] = None,
        contract_start_date_gt: Optional[datetime] = None,
        contract_start_date_gte: Optional[datetime] = None,
        created_date: Optional[datetime] = None,
        created_date_lt: Optional[datetime] = None,
        created_date_lte: Optional[datetime] = None,
        created_date_gt: Optional[datetime] = None,
        created_date_gte: Optional[datetime] = None,
        capacity_modified_date: Optional[datetime] = None,
        capacity_modified_date_lt: Optional[datetime] = None,
        capacity_modified_date_lte: Optional[datetime] = None,
        capacity_modified_date_gt: Optional[datetime] = None,
        capacity_modified_date_gte: Optional[datetime] = None,
        start_modified_date: Optional[datetime] = None,
        start_modified_date_lt: Optional[datetime] = None,
        start_modified_date_lte: Optional[datetime] = None,
        start_modified_date_gt: Optional[datetime] = None,
        start_modified_date_gte: Optional[datetime] = None,
        capacity_owner_modified_date: Optional[datetime] = None,
        capacity_owner_modified_date_lt: Optional[datetime] = None,
        capacity_owner_modified_date_lte: Optional[datetime] = None,
        capacity_owner_modified_date_gt: Optional[datetime] = None,
        capacity_owner_modified_date_gte: Optional[datetime] = None,
        type_modified_date: Optional[datetime] = None,
        type_modified_date_lt: Optional[datetime] = None,
        type_modified_date_lte: Optional[datetime] = None,
        type_modified_date_gt: Optional[datetime] = None,
        type_modified_date_gte: Optional[datetime] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        List of all announced and observed capacity contract relationships for regasification phases as well as their attributes

        Parameters
        ----------

         regasification_phase: Optional[Union[list[str], Series[str], str]]
             Regasification phase associated with the contract, by default None
         regasification_project: Optional[Union[list[str], Series[str], str]]
             Name of the regasification project, by default None
         capacity_owner: Optional[Union[list[str], Series[str], str]]
             Entity or company that owns the regasification capacity, by default None
         contract_type: Optional[Union[list[str], Series[str], str]]
             Type of regasification contract, by default None
         contract_length_years: Optional[float], optional
             Length of the contract in years, by default None
         contract_length_years_gt: Optional[float], optional
             filter by '' contract_length_years > x '', by default None
         contract_length_years_gte: Optional[float], optional
             filter by contract_length_years, by default None
         contract_length_years_lt: Optional[float], optional
             filter by contract_length_years, by default None
         contract_length_years_lte: Optional[float], optional
             filter by contract_length_years, by default None
         contract_start_date: Optional[datetime], optional
             Start date of the contract, by default None
         contract_start_date_gt: Optional[datetime], optional
             filter by '' contract_start_date > x '', by default None
         contract_start_date_gte: Optional[datetime], optional
             filter by contract_start_date, by default None
         contract_start_date_lt: Optional[datetime], optional
             filter by contract_start_date, by default None
         contract_start_date_lte: Optional[datetime], optional
             filter by contract_start_date, by default None
         created_date: Optional[datetime], optional
             Date when the contract was created, by default None
         created_date_gt: Optional[datetime], optional
             filter by '' created_date > x '', by default None
         created_date_gte: Optional[datetime], optional
             filter by created_date, by default None
         created_date_lt: Optional[datetime], optional
             filter by created_date, by default None
         created_date_lte: Optional[datetime], optional
             filter by created_date, by default None
         capacity_modified_date: Optional[datetime], optional
             Date when the capacity rights were modified, by default None
         capacity_modified_date_gt: Optional[datetime], optional
             filter by '' capacity_modified_date > x '', by default None
         capacity_modified_date_gte: Optional[datetime], optional
             filter by capacity_modified_date, by default None
         capacity_modified_date_lt: Optional[datetime], optional
             filter by capacity_modified_date, by default None
         capacity_modified_date_lte: Optional[datetime], optional
             filter by capacity_modified_date, by default None
         start_modified_date: Optional[datetime], optional
             Date when the contract start date was modified, by default None
         start_modified_date_gt: Optional[datetime], optional
             filter by '' start_modified_date > x '', by default None
         start_modified_date_gte: Optional[datetime], optional
             filter by start_modified_date, by default None
         start_modified_date_lt: Optional[datetime], optional
             filter by start_modified_date, by default None
         start_modified_date_lte: Optional[datetime], optional
             filter by start_modified_date, by default None
         capacity_owner_modified_date: Optional[datetime], optional
             Date when the capacity owner was modified, by default None
         capacity_owner_modified_date_gt: Optional[datetime], optional
             filter by '' capacity_owner_modified_date > x '', by default None
         capacity_owner_modified_date_gte: Optional[datetime], optional
             filter by capacity_owner_modified_date, by default None
         capacity_owner_modified_date_lt: Optional[datetime], optional
             filter by capacity_owner_modified_date, by default None
         capacity_owner_modified_date_lte: Optional[datetime], optional
             filter by capacity_owner_modified_date, by default None
         type_modified_date: Optional[datetime], optional
             Date when the contract type was modified, by default None
         type_modified_date_gt: Optional[datetime], optional
             filter by '' type_modified_date > x '', by default None
         type_modified_date_gte: Optional[datetime], optional
             filter by type_modified_date, by default None
         type_modified_date_lt: Optional[datetime], optional
             filter by type_modified_date, by default None
         type_modified_date_lte: Optional[datetime], optional
             filter by type_modified_date, by default None
         modified_date: Optional[datetime], optional
             Regasification contracts record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(
            list_to_filter("regasificationPhase", regasification_phase)
        )
        filter_params.append(
            list_to_filter("regasificationProject", regasification_project)
        )
        filter_params.append(list_to_filter("capacityOwner", capacity_owner))
        filter_params.append(list_to_filter("contractType", contract_type))
        filter_params.append(
            list_to_filter("contractLengthYears", contract_length_years)
        )
        if contract_length_years_gt is not None:
            filter_params.append(f'contractLengthYears > "{contract_length_years_gt}"')
        if contract_length_years_gte is not None:
            filter_params.append(
                f'contractLengthYears >= "{contract_length_years_gte}"'
            )
        if contract_length_years_lt is not None:
            filter_params.append(f'contractLengthYears < "{contract_length_years_lt}"')
        if contract_length_years_lte is not None:
            filter_params.append(
                f'contractLengthYears <= "{contract_length_years_lte}"'
            )
        filter_params.append(list_to_filter("contractStartDate", contract_start_date))
        if contract_start_date_gt is not None:
            filter_params.append(f'contractStartDate > "{contract_start_date_gt}"')
        if contract_start_date_gte is not None:
            filter_params.append(f'contractStartDate >= "{contract_start_date_gte}"')
        if contract_start_date_lt is not None:
            filter_params.append(f'contractStartDate < "{contract_start_date_lt}"')
        if contract_start_date_lte is not None:
            filter_params.append(f'contractStartDate <= "{contract_start_date_lte}"')
        filter_params.append(list_to_filter("createdDate", created_date))
        if created_date_gt is not None:
            filter_params.append(f'createdDate > "{created_date_gt}"')
        if created_date_gte is not None:
            filter_params.append(f'createdDate >= "{created_date_gte}"')
        if created_date_lt is not None:
            filter_params.append(f'createdDate < "{created_date_lt}"')
        if created_date_lte is not None:
            filter_params.append(f'createdDate <= "{created_date_lte}"')
        filter_params.append(
            list_to_filter("capacityModifiedDate", capacity_modified_date)
        )
        if capacity_modified_date_gt is not None:
            filter_params.append(
                f'capacityModifiedDate > "{capacity_modified_date_gt}"'
            )
        if capacity_modified_date_gte is not None:
            filter_params.append(
                f'capacityModifiedDate >= "{capacity_modified_date_gte}"'
            )
        if capacity_modified_date_lt is not None:
            filter_params.append(
                f'capacityModifiedDate < "{capacity_modified_date_lt}"'
            )
        if capacity_modified_date_lte is not None:
            filter_params.append(
                f'capacityModifiedDate <= "{capacity_modified_date_lte}"'
            )
        filter_params.append(list_to_filter("startModifiedDate", start_modified_date))
        if start_modified_date_gt is not None:
            filter_params.append(f'startModifiedDate > "{start_modified_date_gt}"')
        if start_modified_date_gte is not None:
            filter_params.append(f'startModifiedDate >= "{start_modified_date_gte}"')
        if start_modified_date_lt is not None:
            filter_params.append(f'startModifiedDate < "{start_modified_date_lt}"')
        if start_modified_date_lte is not None:
            filter_params.append(f'startModifiedDate <= "{start_modified_date_lte}"')
        filter_params.append(
            list_to_filter("capacityOwnerModifiedDate", capacity_owner_modified_date)
        )
        if capacity_owner_modified_date_gt is not None:
            filter_params.append(
                f'capacityOwnerModifiedDate > "{capacity_owner_modified_date_gt}"'
            )
        if capacity_owner_modified_date_gte is not None:
            filter_params.append(
                f'capacityOwnerModifiedDate >= "{capacity_owner_modified_date_gte}"'
            )
        if capacity_owner_modified_date_lt is not None:
            filter_params.append(
                f'capacityOwnerModifiedDate < "{capacity_owner_modified_date_lt}"'
            )
        if capacity_owner_modified_date_lte is not None:
            filter_params.append(
                f'capacityOwnerModifiedDate <= "{capacity_owner_modified_date_lte}"'
            )
        filter_params.append(list_to_filter("typeModifiedDate", type_modified_date))
        if type_modified_date_gt is not None:
            filter_params.append(f'typeModifiedDate > "{type_modified_date_gt}"')
        if type_modified_date_gte is not None:
            filter_params.append(f'typeModifiedDate >= "{type_modified_date_gte}"')
        if type_modified_date_lt is not None:
            filter_params.append(f'typeModifiedDate < "{type_modified_date_lt}"')
        if type_modified_date_lte is not None:
            filter_params.append(f'typeModifiedDate <= "{type_modified_date_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/regasification-contracts",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_regasification_phase_ownership(
        self,
        *,
        regasification_phase: Optional[Union[list[str], Series[str], str]] = None,
        shareholder: Optional[Union[list[str], Series[str], str]] = None,
        created_date: Optional[datetime] = None,
        created_date_lt: Optional[datetime] = None,
        created_date_lte: Optional[datetime] = None,
        created_date_gt: Optional[datetime] = None,
        created_date_gte: Optional[datetime] = None,
        shareholder_modified_date: Optional[datetime] = None,
        shareholder_modified_date_lt: Optional[datetime] = None,
        shareholder_modified_date_lte: Optional[datetime] = None,
        shareholder_modified_date_gt: Optional[datetime] = None,
        shareholder_modified_date_gte: Optional[datetime] = None,
        share_modified_date: Optional[datetime] = None,
        share_modified_date_lt: Optional[datetime] = None,
        share_modified_date_lte: Optional[datetime] = None,
        share_modified_date_gt: Optional[datetime] = None,
        share_modified_date_gte: Optional[datetime] = None,
        ownership_start_date: Optional[datetime] = None,
        ownership_start_date_lt: Optional[datetime] = None,
        ownership_start_date_lte: Optional[datetime] = None,
        ownership_start_date_gt: Optional[datetime] = None,
        ownership_start_date_gte: Optional[datetime] = None,
        ownership_end_date: Optional[datetime] = None,
        ownership_end_date_lt: Optional[datetime] = None,
        ownership_end_date_lte: Optional[datetime] = None,
        ownership_end_date_gt: Optional[datetime] = None,
        ownership_end_date_gte: Optional[datetime] = None,
        current_owner: Optional[Union[list[str], Series[str], str]] = None,
        country_coast: Optional[Union[list[str], Series[str], str]] = None,
        import_market: Optional[Union[list[str], Series[str], str]] = None,
        regasification_project: Optional[Union[list[str], Series[str], str]] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Provides information on the ownership of regasification phases over time

        Parameters
        ----------

         regasification_phase: Optional[Union[list[str], Series[str], str]]
             Phase of the regasification project, by default None
         shareholder: Optional[Union[list[str], Series[str], str]]
             Entity or company that holds ownership in the regasification phase, by default None
         created_date: Optional[datetime], optional
             Date when the ownership record was created, by default None
         created_date_gt: Optional[datetime], optional
             filter by '' created_date > x '', by default None
         created_date_gte: Optional[datetime], optional
             filter by created_date, by default None
         created_date_lt: Optional[datetime], optional
             filter by created_date, by default None
         created_date_lte: Optional[datetime], optional
             filter by created_date, by default None
         shareholder_modified_date: Optional[datetime], optional
             Date when the shareholder information was modified, by default None
         shareholder_modified_date_gt: Optional[datetime], optional
             filter by '' shareholder_modified_date > x '', by default None
         shareholder_modified_date_gte: Optional[datetime], optional
             filter by shareholder_modified_date, by default None
         shareholder_modified_date_lt: Optional[datetime], optional
             filter by shareholder_modified_date, by default None
         shareholder_modified_date_lte: Optional[datetime], optional
             filter by shareholder_modified_date, by default None
         share_modified_date: Optional[datetime], optional
             Date when the ownership share was modified, by default None
         share_modified_date_gt: Optional[datetime], optional
             filter by '' share_modified_date > x '', by default None
         share_modified_date_gte: Optional[datetime], optional
             filter by share_modified_date, by default None
         share_modified_date_lt: Optional[datetime], optional
             filter by share_modified_date, by default None
         share_modified_date_lte: Optional[datetime], optional
             filter by share_modified_date, by default None
         ownership_start_date: Optional[datetime], optional
             Start date of the ownership, by default None
         ownership_start_date_gt: Optional[datetime], optional
             filter by '' ownership_start_date > x '', by default None
         ownership_start_date_gte: Optional[datetime], optional
             filter by ownership_start_date, by default None
         ownership_start_date_lt: Optional[datetime], optional
             filter by ownership_start_date, by default None
         ownership_start_date_lte: Optional[datetime], optional
             filter by ownership_start_date, by default None
         ownership_end_date: Optional[datetime], optional
             End date of the ownership, by default None
         ownership_end_date_gt: Optional[datetime], optional
             filter by '' ownership_end_date > x '', by default None
         ownership_end_date_gte: Optional[datetime], optional
             filter by ownership_end_date, by default None
         ownership_end_date_lt: Optional[datetime], optional
             filter by ownership_end_date, by default None
         ownership_end_date_lte: Optional[datetime], optional
             filter by ownership_end_date, by default None
         current_owner: Optional[Union[list[str], Series[str], str]]
             Current owner of the regasification phase, by default None
         country_coast: Optional[Union[list[str], Series[str], str]]
             Country coast associated with the regasification phase, by default None
         import_market: Optional[Union[list[str], Series[str], str]]
             Market where the regasification project is located, by default None
         regasification_project: Optional[Union[list[str], Series[str], str]]
             Name of the regasification project associated with the phase, by default None
         modified_date: Optional[datetime], optional
             Regasificaion phase ownership record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(
            list_to_filter("regasificationPhase", regasification_phase)
        )
        filter_params.append(list_to_filter("shareholder", shareholder))
        filter_params.append(list_to_filter("createdDate", created_date))
        if created_date_gt is not None:
            filter_params.append(f'createdDate > "{created_date_gt}"')
        if created_date_gte is not None:
            filter_params.append(f'createdDate >= "{created_date_gte}"')
        if created_date_lt is not None:
            filter_params.append(f'createdDate < "{created_date_lt}"')
        if created_date_lte is not None:
            filter_params.append(f'createdDate <= "{created_date_lte}"')
        filter_params.append(
            list_to_filter("shareholderModifiedDate", shareholder_modified_date)
        )
        if shareholder_modified_date_gt is not None:
            filter_params.append(
                f'shareholderModifiedDate > "{shareholder_modified_date_gt}"'
            )
        if shareholder_modified_date_gte is not None:
            filter_params.append(
                f'shareholderModifiedDate >= "{shareholder_modified_date_gte}"'
            )
        if shareholder_modified_date_lt is not None:
            filter_params.append(
                f'shareholderModifiedDate < "{shareholder_modified_date_lt}"'
            )
        if shareholder_modified_date_lte is not None:
            filter_params.append(
                f'shareholderModifiedDate <= "{shareholder_modified_date_lte}"'
            )
        filter_params.append(list_to_filter("shareModifiedDate", share_modified_date))
        if share_modified_date_gt is not None:
            filter_params.append(f'shareModifiedDate > "{share_modified_date_gt}"')
        if share_modified_date_gte is not None:
            filter_params.append(f'shareModifiedDate >= "{share_modified_date_gte}"')
        if share_modified_date_lt is not None:
            filter_params.append(f'shareModifiedDate < "{share_modified_date_lt}"')
        if share_modified_date_lte is not None:
            filter_params.append(f'shareModifiedDate <= "{share_modified_date_lte}"')
        filter_params.append(list_to_filter("ownershipStartDate", ownership_start_date))
        if ownership_start_date_gt is not None:
            filter_params.append(f'ownershipStartDate > "{ownership_start_date_gt}"')
        if ownership_start_date_gte is not None:
            filter_params.append(f'ownershipStartDate >= "{ownership_start_date_gte}"')
        if ownership_start_date_lt is not None:
            filter_params.append(f'ownershipStartDate < "{ownership_start_date_lt}"')
        if ownership_start_date_lte is not None:
            filter_params.append(f'ownershipStartDate <= "{ownership_start_date_lte}"')
        filter_params.append(list_to_filter("ownershipEndDate", ownership_end_date))
        if ownership_end_date_gt is not None:
            filter_params.append(f'ownershipEndDate > "{ownership_end_date_gt}"')
        if ownership_end_date_gte is not None:
            filter_params.append(f'ownershipEndDate >= "{ownership_end_date_gte}"')
        if ownership_end_date_lt is not None:
            filter_params.append(f'ownershipEndDate < "{ownership_end_date_lt}"')
        if ownership_end_date_lte is not None:
            filter_params.append(f'ownershipEndDate <= "{ownership_end_date_lte}"')
        filter_params.append(list_to_filter("currentOwner", current_owner))
        filter_params.append(list_to_filter("countryCoast", country_coast))
        filter_params.append(list_to_filter("importMarket", import_market))
        filter_params.append(
            list_to_filter("regasificationProject", regasification_project)
        )
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/regasification-phase-ownership",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_regasification_phases(
        self,
        *,
        regasification_phase: Optional[Union[list[str], Series[str], str]] = None,
        regasification_project: Optional[Union[list[str], Series[str], str]] = None,
        phase_status: Optional[Union[list[str], Series[str], str]] = None,
        announced_start_date: Optional[datetime] = None,
        announced_start_date_lt: Optional[datetime] = None,
        announced_start_date_lte: Optional[datetime] = None,
        announced_start_date_gt: Optional[datetime] = None,
        announced_start_date_gte: Optional[datetime] = None,
        estimated_start_date: Optional[datetime] = None,
        estimated_start_date_lt: Optional[datetime] = None,
        estimated_start_date_lte: Optional[datetime] = None,
        estimated_start_date_gt: Optional[datetime] = None,
        estimated_start_date_gte: Optional[datetime] = None,
        feed_contractor: Optional[Union[list[str], Series[str], str]] = None,
        epc_contractor: Optional[Union[list[str], Series[str], str]] = None,
        terminal_type: Optional[Union[list[str], Series[str], str]] = None,
        able_to_reload: Optional[int] = None,
        able_to_reload_lt: Optional[int] = None,
        able_to_reload_lte: Optional[int] = None,
        able_to_reload_gt: Optional[int] = None,
        able_to_reload_gte: Optional[int] = None,
        created_date: Optional[datetime] = None,
        created_date_lt: Optional[datetime] = None,
        created_date_lte: Optional[datetime] = None,
        created_date_gt: Optional[datetime] = None,
        created_date_gte: Optional[datetime] = None,
        status_modified_date: Optional[datetime] = None,
        status_modified_date_lt: Optional[datetime] = None,
        status_modified_date_lte: Optional[datetime] = None,
        status_modified_date_gt: Optional[datetime] = None,
        status_modified_date_gte: Optional[datetime] = None,
        capacity_modified_date: Optional[datetime] = None,
        capacity_modified_date_lt: Optional[datetime] = None,
        capacity_modified_date_lte: Optional[datetime] = None,
        capacity_modified_date_gt: Optional[datetime] = None,
        capacity_modified_date_gte: Optional[datetime] = None,
        announced_start_date_modified_date: Optional[datetime] = None,
        announced_start_date_modified_date_lt: Optional[datetime] = None,
        announced_start_date_modified_date_lte: Optional[datetime] = None,
        announced_start_date_modified_date_gt: Optional[datetime] = None,
        announced_start_date_modified_date_gte: Optional[datetime] = None,
        estimated_start_date_modified_date: Optional[datetime] = None,
        estimated_start_date_modified_date_lt: Optional[datetime] = None,
        estimated_start_date_modified_date_lte: Optional[datetime] = None,
        estimated_start_date_modified_date_gt: Optional[datetime] = None,
        estimated_start_date_modified_date_gte: Optional[datetime] = None,
        date_phase_first_announced: Optional[datetime] = None,
        date_phase_first_announced_lt: Optional[datetime] = None,
        date_phase_first_announced_lte: Optional[datetime] = None,
        date_phase_first_announced_gt: Optional[datetime] = None,
        date_phase_first_announced_gte: Optional[datetime] = None,
        small_scale: Optional[int] = None,
        small_scale_lt: Optional[int] = None,
        small_scale_lte: Optional[int] = None,
        small_scale_gt: Optional[int] = None,
        small_scale_gte: Optional[int] = None,
        regasification_phase_feature: Optional[
            Union[list[str], Series[str], str]
        ] = None,
        regasification_phase_feature_uom: Optional[
            Union[list[str], Series[str], str]
        ] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Provides information on LNG regasification phases

        Parameters
        ----------

         regasification_phase: Optional[Union[list[str], Series[str], str]]
             Name of the regasification phase, by default None
         regasification_project: Optional[Union[list[str], Series[str], str]]
             Name of the regasification project associated with the phase, by default None
         phase_status: Optional[Union[list[str], Series[str], str]]
             Status of the regasification phase, by default None
         announced_start_date: Optional[datetime], optional
             Latest publically announced start date of the regasification phase, by default None
         announced_start_date_gt: Optional[datetime], optional
             filter by '' announced_start_date > x '', by default None
         announced_start_date_gte: Optional[datetime], optional
             filter by announced_start_date, by default None
         announced_start_date_lt: Optional[datetime], optional
             filter by announced_start_date, by default None
         announced_start_date_lte: Optional[datetime], optional
             filter by announced_start_date, by default None
         estimated_start_date: Optional[datetime], optional
             Our estimated start date of the regasification phase, by default None
         estimated_start_date_gt: Optional[datetime], optional
             filter by '' estimated_start_date > x '', by default None
         estimated_start_date_gte: Optional[datetime], optional
             filter by estimated_start_date, by default None
         estimated_start_date_lt: Optional[datetime], optional
             filter by estimated_start_date, by default None
         estimated_start_date_lte: Optional[datetime], optional
             filter by estimated_start_date, by default None
         feed_contractor: Optional[Union[list[str], Series[str], str]]
             Contractor responsible for the front-end engineering and design of the regasification phase, by default None
         epc_contractor: Optional[Union[list[str], Series[str], str]]
             Contractor responsible for the engineering, procurement, and construction of the regasification phase, by default None
         terminal_type: Optional[Union[list[str], Series[str], str]]
             Type of regasification terminal, by default None
         able_to_reload: Optional[int], optional
             Indicates whether the regasification phase is capable of reloading LNG onto ships, by default None
         able_to_reload_gt: Optional[int], optional
             filter by '' able_to_reload > x '', by default None
         able_to_reload_gte: Optional[int], optional
             filter by able_to_reload, by default None
         able_to_reload_lt: Optional[int], optional
             filter by able_to_reload, by default None
         able_to_reload_lte: Optional[int], optional
             filter by able_to_reload, by default None
         created_date: Optional[datetime], optional
             Date when the regasification phase record was created, by default None
         created_date_gt: Optional[datetime], optional
             filter by '' created_date > x '', by default None
         created_date_gte: Optional[datetime], optional
             filter by created_date, by default None
         created_date_lt: Optional[datetime], optional
             filter by created_date, by default None
         created_date_lte: Optional[datetime], optional
             filter by created_date, by default None
         status_modified_date: Optional[datetime], optional
             Date when the phase status was last modified, by default None
         status_modified_date_gt: Optional[datetime], optional
             filter by '' status_modified_date > x '', by default None
         status_modified_date_gte: Optional[datetime], optional
             filter by status_modified_date, by default None
         status_modified_date_lt: Optional[datetime], optional
             filter by status_modified_date, by default None
         status_modified_date_lte: Optional[datetime], optional
             filter by status_modified_date, by default None
         capacity_modified_date: Optional[datetime], optional
             Date when the capacity of the regasification phase was last modified, by default None
         capacity_modified_date_gt: Optional[datetime], optional
             filter by '' capacity_modified_date > x '', by default None
         capacity_modified_date_gte: Optional[datetime], optional
             filter by capacity_modified_date, by default None
         capacity_modified_date_lt: Optional[datetime], optional
             filter by capacity_modified_date, by default None
         capacity_modified_date_lte: Optional[datetime], optional
             filter by capacity_modified_date, by default None
         announced_start_date_modified_date: Optional[datetime], optional
             Date when the announced start date of the regasification phase was last modified, by default None
         announced_start_date_modified_date_gt: Optional[datetime], optional
             filter by '' announced_start_date_modified_date > x '', by default None
         announced_start_date_modified_date_gte: Optional[datetime], optional
             filter by announced_start_date_modified_date, by default None
         announced_start_date_modified_date_lt: Optional[datetime], optional
             filter by announced_start_date_modified_date, by default None
         announced_start_date_modified_date_lte: Optional[datetime], optional
             filter by announced_start_date_modified_date, by default None
         estimated_start_date_modified_date: Optional[datetime], optional
             Date when the estimated start date of the regasification phase was last modified, by default None
         estimated_start_date_modified_date_gt: Optional[datetime], optional
             filter by '' estimated_start_date_modified_date > x '', by default None
         estimated_start_date_modified_date_gte: Optional[datetime], optional
             filter by estimated_start_date_modified_date, by default None
         estimated_start_date_modified_date_lt: Optional[datetime], optional
             filter by estimated_start_date_modified_date, by default None
         estimated_start_date_modified_date_lte: Optional[datetime], optional
             filter by estimated_start_date_modified_date, by default None
         date_phase_first_announced: Optional[datetime], optional
             Date when the regasification phase was first announced, by default None
         date_phase_first_announced_gt: Optional[datetime], optional
             filter by '' date_phase_first_announced > x '', by default None
         date_phase_first_announced_gte: Optional[datetime], optional
             filter by date_phase_first_announced, by default None
         date_phase_first_announced_lt: Optional[datetime], optional
             filter by date_phase_first_announced, by default None
         date_phase_first_announced_lte: Optional[datetime], optional
             filter by date_phase_first_announced, by default None
         small_scale: Optional[int], optional
             Indicates whether the regasification phase is a small-scale project, by default None
         small_scale_gt: Optional[int], optional
             filter by '' small_scale > x '', by default None
         small_scale_gte: Optional[int], optional
             filter by small_scale, by default None
         small_scale_lt: Optional[int], optional
             filter by small_scale, by default None
         small_scale_lte: Optional[int], optional
             filter by small_scale, by default None
         regasification_phase_feature: Optional[Union[list[str], Series[str], str]]
             Types of features of regasification phases ranging from capacity to storage and other facility-specific characteristics, by default None
         regasification_phase_feature_uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure of the corresponding regasification phase feature, by default None
         modified_date: Optional[datetime], optional
             Regasification phases record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(
            list_to_filter("regasificationPhase", regasification_phase)
        )
        filter_params.append(
            list_to_filter("regasificationProject", regasification_project)
        )
        filter_params.append(list_to_filter("phaseStatus", phase_status))
        filter_params.append(list_to_filter("announcedStartDate", announced_start_date))
        if announced_start_date_gt is not None:
            filter_params.append(f'announcedStartDate > "{announced_start_date_gt}"')
        if announced_start_date_gte is not None:
            filter_params.append(f'announcedStartDate >= "{announced_start_date_gte}"')
        if announced_start_date_lt is not None:
            filter_params.append(f'announcedStartDate < "{announced_start_date_lt}"')
        if announced_start_date_lte is not None:
            filter_params.append(f'announcedStartDate <= "{announced_start_date_lte}"')
        filter_params.append(list_to_filter("estimatedStartDate", estimated_start_date))
        if estimated_start_date_gt is not None:
            filter_params.append(f'estimatedStartDate > "{estimated_start_date_gt}"')
        if estimated_start_date_gte is not None:
            filter_params.append(f'estimatedStartDate >= "{estimated_start_date_gte}"')
        if estimated_start_date_lt is not None:
            filter_params.append(f'estimatedStartDate < "{estimated_start_date_lt}"')
        if estimated_start_date_lte is not None:
            filter_params.append(f'estimatedStartDate <= "{estimated_start_date_lte}"')
        filter_params.append(list_to_filter("feedContractor", feed_contractor))
        filter_params.append(list_to_filter("epcContractor", epc_contractor))
        filter_params.append(list_to_filter("terminalType", terminal_type))
        filter_params.append(list_to_filter("ableToReload", able_to_reload))
        if able_to_reload_gt is not None:
            filter_params.append(f'ableToReload > "{able_to_reload_gt}"')
        if able_to_reload_gte is not None:
            filter_params.append(f'ableToReload >= "{able_to_reload_gte}"')
        if able_to_reload_lt is not None:
            filter_params.append(f'ableToReload < "{able_to_reload_lt}"')
        if able_to_reload_lte is not None:
            filter_params.append(f'ableToReload <= "{able_to_reload_lte}"')
        filter_params.append(list_to_filter("createdDate", created_date))
        if created_date_gt is not None:
            filter_params.append(f'createdDate > "{created_date_gt}"')
        if created_date_gte is not None:
            filter_params.append(f'createdDate >= "{created_date_gte}"')
        if created_date_lt is not None:
            filter_params.append(f'createdDate < "{created_date_lt}"')
        if created_date_lte is not None:
            filter_params.append(f'createdDate <= "{created_date_lte}"')
        filter_params.append(list_to_filter("statusModifiedDate", status_modified_date))
        if status_modified_date_gt is not None:
            filter_params.append(f'statusModifiedDate > "{status_modified_date_gt}"')
        if status_modified_date_gte is not None:
            filter_params.append(f'statusModifiedDate >= "{status_modified_date_gte}"')
        if status_modified_date_lt is not None:
            filter_params.append(f'statusModifiedDate < "{status_modified_date_lt}"')
        if status_modified_date_lte is not None:
            filter_params.append(f'statusModifiedDate <= "{status_modified_date_lte}"')
        filter_params.append(
            list_to_filter("capacityModifiedDate", capacity_modified_date)
        )
        if capacity_modified_date_gt is not None:
            filter_params.append(
                f'capacityModifiedDate > "{capacity_modified_date_gt}"'
            )
        if capacity_modified_date_gte is not None:
            filter_params.append(
                f'capacityModifiedDate >= "{capacity_modified_date_gte}"'
            )
        if capacity_modified_date_lt is not None:
            filter_params.append(
                f'capacityModifiedDate < "{capacity_modified_date_lt}"'
            )
        if capacity_modified_date_lte is not None:
            filter_params.append(
                f'capacityModifiedDate <= "{capacity_modified_date_lte}"'
            )
        filter_params.append(
            list_to_filter(
                "announcedStartDateModifiedDate", announced_start_date_modified_date
            )
        )
        if announced_start_date_modified_date_gt is not None:
            filter_params.append(
                f'announcedStartDateModifiedDate > "{announced_start_date_modified_date_gt}"'
            )
        if announced_start_date_modified_date_gte is not None:
            filter_params.append(
                f'announcedStartDateModifiedDate >= "{announced_start_date_modified_date_gte}"'
            )
        if announced_start_date_modified_date_lt is not None:
            filter_params.append(
                f'announcedStartDateModifiedDate < "{announced_start_date_modified_date_lt}"'
            )
        if announced_start_date_modified_date_lte is not None:
            filter_params.append(
                f'announcedStartDateModifiedDate <= "{announced_start_date_modified_date_lte}"'
            )
        filter_params.append(
            list_to_filter(
                "estimatedStartDateModifiedDate", estimated_start_date_modified_date
            )
        )
        if estimated_start_date_modified_date_gt is not None:
            filter_params.append(
                f'estimatedStartDateModifiedDate > "{estimated_start_date_modified_date_gt}"'
            )
        if estimated_start_date_modified_date_gte is not None:
            filter_params.append(
                f'estimatedStartDateModifiedDate >= "{estimated_start_date_modified_date_gte}"'
            )
        if estimated_start_date_modified_date_lt is not None:
            filter_params.append(
                f'estimatedStartDateModifiedDate < "{estimated_start_date_modified_date_lt}"'
            )
        if estimated_start_date_modified_date_lte is not None:
            filter_params.append(
                f'estimatedStartDateModifiedDate <= "{estimated_start_date_modified_date_lte}"'
            )
        filter_params.append(
            list_to_filter("datePhaseFirstAnnounced", date_phase_first_announced)
        )
        if date_phase_first_announced_gt is not None:
            filter_params.append(
                f'datePhaseFirstAnnounced > "{date_phase_first_announced_gt}"'
            )
        if date_phase_first_announced_gte is not None:
            filter_params.append(
                f'datePhaseFirstAnnounced >= "{date_phase_first_announced_gte}"'
            )
        if date_phase_first_announced_lt is not None:
            filter_params.append(
                f'datePhaseFirstAnnounced < "{date_phase_first_announced_lt}"'
            )
        if date_phase_first_announced_lte is not None:
            filter_params.append(
                f'datePhaseFirstAnnounced <= "{date_phase_first_announced_lte}"'
            )
        filter_params.append(list_to_filter("smallScale", small_scale))
        if small_scale_gt is not None:
            filter_params.append(f'smallScale > "{small_scale_gt}"')
        if small_scale_gte is not None:
            filter_params.append(f'smallScale >= "{small_scale_gte}"')
        if small_scale_lt is not None:
            filter_params.append(f'smallScale < "{small_scale_lt}"')
        if small_scale_lte is not None:
            filter_params.append(f'smallScale <= "{small_scale_lte}"')
        filter_params.append(
            list_to_filter("regasificationPhaseFeature", regasification_phase_feature)
        )
        filter_params.append(
            list_to_filter(
                "regasificationPhaseFeatureUom", regasification_phase_feature_uom
            )
        )
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/regasification-phases",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_regasification_projects(
        self,
        *,
        regasification_project: Optional[Union[list[str], Series[str], str]] = None,
        country_coast: Optional[Union[list[str], Series[str], str]] = None,
        import_market: Optional[Union[list[str], Series[str], str]] = None,
        import_region: Optional[Union[list[str], Series[str], str]] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        List of regasification projects with their IDs and their associated country coasts

        Parameters
        ----------

         regasification_project: Optional[Union[list[str], Series[str], str]]
             Name of regasification project, by default None
         country_coast: Optional[Union[list[str], Series[str], str]]
             Country coast where the regasification project is located, by default None
         import_market: Optional[Union[list[str], Series[str], str]]
             Market where the regasification project is located, by default None
         import_region: Optional[Union[list[str], Series[str], str]]
             Region where the regasification project is located, by default None
         modified_date: Optional[datetime], optional
             Regasification projects record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(
            list_to_filter("regasificationProject", regasification_project)
        )
        filter_params.append(list_to_filter("countryCoast", country_coast))
        filter_params.append(list_to_filter("importMarket", import_market))
        filter_params.append(list_to_filter("importRegion", import_region))
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/regasification-projects",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_vessel(
        self,
        *,
        imo_number: Optional[int] = None,
        imo_number_lt: Optional[int] = None,
        imo_number_lte: Optional[int] = None,
        imo_number_gt: Optional[int] = None,
        imo_number_gte: Optional[int] = None,
        vessel_name: Optional[Union[list[str], Series[str], str]] = None,
        propulsion_system: Optional[Union[list[str], Series[str], str]] = None,
        vessel_type: Optional[Union[list[str], Series[str], str]] = None,
        charterer: Optional[Union[list[str], Series[str], str]] = None,
        operator: Optional[Union[list[str], Series[str], str]] = None,
        shipowner: Optional[Union[list[str], Series[str], str]] = None,
        shipowner2: Optional[Union[list[str], Series[str], str]] = None,
        shipbuilder: Optional[Union[list[str], Series[str], str]] = None,
        country_of_build: Optional[Union[list[str], Series[str], str]] = None,
        flag: Optional[Union[list[str], Series[str], str]] = None,
        cargo_containment_system: Optional[Union[list[str], Series[str], str]] = None,
        vessel_status: Optional[Union[list[str], Series[str], str]] = None,
        name_currently_in_use: Optional[Union[list[str], Series[str], str]] = None,
        contract_date: Optional[date] = None,
        contract_date_lt: Optional[date] = None,
        contract_date_lte: Optional[date] = None,
        contract_date_gt: Optional[date] = None,
        contract_date_gte: Optional[date] = None,
        delivery_date: Optional[date] = None,
        delivery_date_lt: Optional[date] = None,
        delivery_date_lte: Optional[date] = None,
        delivery_date_gt: Optional[date] = None,
        delivery_date_gte: Optional[date] = None,
        vessel_feature: Optional[Union[list[str], Series[str], str]] = None,
        vessel_feature_uom: Optional[Union[list[str], Series[str], str]] = None,
        vessel_feature_currency: Optional[Union[list[str], Series[str], str]] = None,
        created_date: Optional[datetime] = None,
        created_date_lt: Optional[datetime] = None,
        created_date_lte: Optional[datetime] = None,
        created_date_gt: Optional[datetime] = None,
        created_date_gte: Optional[datetime] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        List of all retired, existing, and future vessels as well as their attributes

        Parameters
        ----------

         imo_number: Optional[int], optional
             International Maritime Organization (IMO) number assigned to the vessel, by default None
         imo_number_gt: Optional[int], optional
             filter by '' imo_number > x '', by default None
         imo_number_gte: Optional[int], optional
             filter by imo_number, by default None
         imo_number_lt: Optional[int], optional
             filter by imo_number, by default None
         imo_number_lte: Optional[int], optional
             filter by imo_number, by default None
         vessel_name: Optional[Union[list[str], Series[str], str]]
             Name of the LNG vessel, by default None
         propulsion_system: Optional[Union[list[str], Series[str], str]]
             Propulsion type of vessel, by default None
         vessel_type: Optional[Union[list[str], Series[str], str]]
             Type or classification of the vessel, by default None
         charterer: Optional[Union[list[str], Series[str], str]]
             Entity or company that charters or leases the vessel, by default None
         operator: Optional[Union[list[str], Series[str], str]]
             Entity or company responsible for operating the vessel, by default None
         shipowner: Optional[Union[list[str], Series[str], str]]
             Primary owner of the vessel, by default None
         shipowner2: Optional[Union[list[str], Series[str], str]]
             Additional owners of the vessel, if applicable, by default None
         shipbuilder: Optional[Union[list[str], Series[str], str]]
             Shipyard or company that constructed the vessel, by default None
         country_of_build: Optional[Union[list[str], Series[str], str]]
             Country where the vessel was built, by default None
         flag: Optional[Union[list[str], Series[str], str]]
             Flag state or country under which the vessel is registered, by default None
         cargo_containment_system: Optional[Union[list[str], Series[str], str]]
             System used for containing the LNG cargo on the vessel, by default None
         vessel_status: Optional[Union[list[str], Series[str], str]]
             Current status of the vessel, by default None
         name_currently_in_use: Optional[Union[list[str], Series[str], str]]
             Yes or no if the identified name is currently in use, by default None
         contract_date: Optional[date], optional
             Date when the vessel contract was signed, by default None
         contract_date_gt: Optional[date], optional
             filter by '' contract_date > x '', by default None
         contract_date_gte: Optional[date], optional
             filter by contract_date, by default None
         contract_date_lt: Optional[date], optional
             filter by contract_date, by default None
         contract_date_lte: Optional[date], optional
             filter by contract_date, by default None
         delivery_date: Optional[date], optional
             Date when the vessel was delivered, by default None
         delivery_date_gt: Optional[date], optional
             filter by '' delivery_date > x '', by default None
         delivery_date_gte: Optional[date], optional
             filter by delivery_date, by default None
         delivery_date_lt: Optional[date], optional
             filter by delivery_date, by default None
         delivery_date_lte: Optional[date], optional
             filter by delivery_date, by default None
         vessel_feature: Optional[Union[list[str], Series[str], str]]
             Types of features of vessels ranging from capacity to cost to other facility-specific characteristics, by default None
         vessel_feature_uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure of the corresponding vessel feature, by default None
         vessel_feature_currency: Optional[Union[list[str], Series[str], str]]
             Currency of the corresponding vessel feature, by default None
         created_date: Optional[datetime], optional
             Date when the vessel record was created, by default None
         created_date_gt: Optional[datetime], optional
             filter by '' created_date > x '', by default None
         created_date_gte: Optional[datetime], optional
             filter by created_date, by default None
         created_date_lt: Optional[datetime], optional
             filter by created_date, by default None
         created_date_lte: Optional[datetime], optional
             filter by created_date, by default None
         modified_date: Optional[datetime], optional
             Vessel record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("imoNumber", imo_number))
        if imo_number_gt is not None:
            filter_params.append(f'imoNumber > "{imo_number_gt}"')
        if imo_number_gte is not None:
            filter_params.append(f'imoNumber >= "{imo_number_gte}"')
        if imo_number_lt is not None:
            filter_params.append(f'imoNumber < "{imo_number_lt}"')
        if imo_number_lte is not None:
            filter_params.append(f'imoNumber <= "{imo_number_lte}"')
        filter_params.append(list_to_filter("vesselName", vessel_name))
        filter_params.append(list_to_filter("propulsionSystem", propulsion_system))
        filter_params.append(list_to_filter("vesselType", vessel_type))
        filter_params.append(list_to_filter("charterer", charterer))
        filter_params.append(list_to_filter("operator", operator))
        filter_params.append(list_to_filter("shipowner", shipowner))
        filter_params.append(list_to_filter("shipowner2", shipowner2))
        filter_params.append(list_to_filter("shipbuilder", shipbuilder))
        filter_params.append(list_to_filter("countryOfBuild", country_of_build))
        filter_params.append(list_to_filter("flag", flag))
        filter_params.append(
            list_to_filter("cargoContainmentSystem", cargo_containment_system)
        )
        filter_params.append(list_to_filter("vesselStatus", vessel_status))
        filter_params.append(
            list_to_filter("nameCurrentlyInUse", name_currently_in_use)
        )
        filter_params.append(list_to_filter("contractDate", contract_date))
        if contract_date_gt is not None:
            filter_params.append(f'contractDate > "{contract_date_gt}"')
        if contract_date_gte is not None:
            filter_params.append(f'contractDate >= "{contract_date_gte}"')
        if contract_date_lt is not None:
            filter_params.append(f'contractDate < "{contract_date_lt}"')
        if contract_date_lte is not None:
            filter_params.append(f'contractDate <= "{contract_date_lte}"')
        filter_params.append(list_to_filter("deliveryDate", delivery_date))
        if delivery_date_gt is not None:
            filter_params.append(f'deliveryDate > "{delivery_date_gt}"')
        if delivery_date_gte is not None:
            filter_params.append(f'deliveryDate >= "{delivery_date_gte}"')
        if delivery_date_lt is not None:
            filter_params.append(f'deliveryDate < "{delivery_date_lt}"')
        if delivery_date_lte is not None:
            filter_params.append(f'deliveryDate <= "{delivery_date_lte}"')
        filter_params.append(list_to_filter("vesselFeature", vessel_feature))
        filter_params.append(list_to_filter("vesselFeatureUom", vessel_feature_uom))
        filter_params.append(
            list_to_filter("vesselFeatureCurrency", vessel_feature_currency)
        )
        filter_params.append(list_to_filter("createdDate", created_date))
        if created_date_gt is not None:
            filter_params.append(f'createdDate > "{created_date_gt}"')
        if created_date_gte is not None:
            filter_params.append(f'createdDate >= "{created_date_gte}"')
        if created_date_lt is not None:
            filter_params.append(f'createdDate < "{created_date_lt}"')
        if created_date_lte is not None:
            filter_params.append(f'createdDate <= "{created_date_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/vessel",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_monthly_estimated_buildout_offtake_contracts(
        self,
        *,
        buildout_month_estimated: Optional[datetime] = None,
        buildout_month_estimated_lt: Optional[datetime] = None,
        buildout_month_estimated_lte: Optional[datetime] = None,
        buildout_month_estimated_gt: Optional[datetime] = None,
        buildout_month_estimated_gte: Optional[datetime] = None,
        created_date_estimated: Optional[datetime] = None,
        created_date_estimated_lt: Optional[datetime] = None,
        created_date_estimated_lte: Optional[datetime] = None,
        created_date_estimated_gt: Optional[datetime] = None,
        created_date_estimated_gte: Optional[datetime] = None,
        modified_date_estimated: Optional[datetime] = None,
        modified_date_estimated_lt: Optional[datetime] = None,
        modified_date_estimated_lte: Optional[datetime] = None,
        modified_date_estimated_gt: Optional[datetime] = None,
        modified_date_estimated_gte: Optional[datetime] = None,
        buyer: Optional[Union[list[str], Series[str], str]] = None,
        exporter: Optional[Union[list[str], Series[str], str]] = None,
        contract_group: Optional[Union[list[str], Series[str], str]] = None,
        supply_market: Optional[Union[list[str], Series[str], str]] = None,
        assumed_destination: Optional[Union[list[str], Series[str], str]] = None,
        contract_type: Optional[Union[list[str], Series[str], str]] = None,
        liquefaction_project: Optional[Union[list[str], Series[str], str]] = None,
        shipping_terms: Optional[Union[list[str], Series[str], str]] = None,
        destination_flexibility: Optional[Union[list[str], Series[str], str]] = None,
        estimated_start_date: Optional[datetime] = None,
        estimated_start_date_lt: Optional[datetime] = None,
        estimated_start_date_lte: Optional[datetime] = None,
        estimated_start_date_gt: Optional[datetime] = None,
        estimated_start_date_gte: Optional[datetime] = None,
        estimated_end_date: Optional[datetime] = None,
        estimated_end_date_lt: Optional[datetime] = None,
        estimated_end_date_lte: Optional[datetime] = None,
        estimated_end_date_gt: Optional[datetime] = None,
        estimated_end_date_gte: Optional[datetime] = None,
        length_years: Optional[float] = None,
        length_years_lt: Optional[float] = None,
        length_years_lte: Optional[float] = None,
        length_years_gt: Optional[float] = None,
        length_years_gte: Optional[float] = None,
        original_signing: Optional[datetime] = None,
        original_signing_lt: Optional[datetime] = None,
        original_signing_lte: Optional[datetime] = None,
        original_signing_gt: Optional[datetime] = None,
        original_signing_gte: Optional[datetime] = None,
        annual_contract_volume: Optional[float] = None,
        annual_contract_volume_lt: Optional[float] = None,
        annual_contract_volume_lte: Optional[float] = None,
        annual_contract_volume_gt: Optional[float] = None,
        annual_contract_volume_gte: Optional[float] = None,
        annual_contract_volume_uom: Optional[Union[list[str], Series[str], str]] = None,
        initial_contract_volume: Optional[float] = None,
        initial_contract_volume_lt: Optional[float] = None,
        initial_contract_volume_lte: Optional[float] = None,
        initial_contract_volume_gt: Optional[float] = None,
        initial_contract_volume_gte: Optional[float] = None,
        initial_contract_volume_uom: Optional[
            Union[list[str], Series[str], str]
        ] = None,
        pricing_linkage: Optional[Union[list[str], Series[str], str]] = None,
        specific_price_link: Optional[Union[list[str], Series[str], str]] = None,
        fid_enabling: Optional[Union[list[str], Series[str], str]] = None,
        green_or_brownfield: Optional[Union[list[str], Series[str], str]] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Provides monthly estimated buildout information on LNG offtake contracts

        Parameters
        ----------

         buildout_month_estimated: Optional[datetime], optional
             Month for which the estimated buildout information is provided, by default None
         buildout_month_estimated_gt: Optional[datetime], optional
             filter by '' buildout_month_estimated > x '', by default None
         buildout_month_estimated_gte: Optional[datetime], optional
             filter by buildout_month_estimated, by default None
         buildout_month_estimated_lt: Optional[datetime], optional
             filter by buildout_month_estimated, by default None
         buildout_month_estimated_lte: Optional[datetime], optional
             filter by buildout_month_estimated, by default None
         created_date_estimated: Optional[datetime], optional
             Date when the estimated buildout information was created, by default None
         created_date_estimated_gt: Optional[datetime], optional
             filter by '' created_date_estimated > x '', by default None
         created_date_estimated_gte: Optional[datetime], optional
             filter by created_date_estimated, by default None
         created_date_estimated_lt: Optional[datetime], optional
             filter by created_date_estimated, by default None
         created_date_estimated_lte: Optional[datetime], optional
             filter by created_date_estimated, by default None
         modified_date_estimated: Optional[datetime], optional
             Date when the estimated buildout information was last modified, by default None
         modified_date_estimated_gt: Optional[datetime], optional
             filter by '' modified_date_estimated > x '', by default None
         modified_date_estimated_gte: Optional[datetime], optional
             filter by modified_date_estimated, by default None
         modified_date_estimated_lt: Optional[datetime], optional
             filter by modified_date_estimated, by default None
         modified_date_estimated_lte: Optional[datetime], optional
             filter by modified_date_estimated, by default None
         buyer: Optional[Union[list[str], Series[str], str]]
             Entity or company purchasing the LNG, by default None
         exporter: Optional[Union[list[str], Series[str], str]]
             Entity or company exporting the LNG, by default None
         contract_group: Optional[Union[list[str], Series[str], str]]
             Group or category to which the contract belongs, by default None
         supply_market: Optional[Union[list[str], Series[str], str]]
             Market where the offtake contract is located, by default None
         assumed_destination: Optional[Union[list[str], Series[str], str]]
             Assumed destination for the LNG, by default None
         contract_type: Optional[Union[list[str], Series[str], str]]
             The status of the capacity contract, by default None
         liquefaction_project: Optional[Union[list[str], Series[str], str]]
             Name or title of the liquefaction project associated with the contract, by default None
         shipping_terms: Optional[Union[list[str], Series[str], str]]
             Terms and conditions related to the shipping of the LNG, by default None
         destination_flexibility: Optional[Union[list[str], Series[str], str]]
             Designation if the offtake contract is destination-fixed or is flexible, by default None
         estimated_start_date: Optional[datetime], optional
             Estimated start date for the offtake contract, by default None
         estimated_start_date_gt: Optional[datetime], optional
             filter by '' estimated_start_date > x '', by default None
         estimated_start_date_gte: Optional[datetime], optional
             filter by estimated_start_date, by default None
         estimated_start_date_lt: Optional[datetime], optional
             filter by estimated_start_date, by default None
         estimated_start_date_lte: Optional[datetime], optional
             filter by estimated_start_date, by default None
         estimated_end_date: Optional[datetime], optional
             Estimated end date for the offtake contract, by default None
         estimated_end_date_gt: Optional[datetime], optional
             filter by '' estimated_end_date > x '', by default None
         estimated_end_date_gte: Optional[datetime], optional
             filter by estimated_end_date, by default None
         estimated_end_date_lt: Optional[datetime], optional
             filter by estimated_end_date, by default None
         estimated_end_date_lte: Optional[datetime], optional
             filter by estimated_end_date, by default None
         length_years: Optional[float], optional
             Duration of the contract in years, by default None
         length_years_gt: Optional[float], optional
             filter by '' length_years > x '', by default None
         length_years_gte: Optional[float], optional
             filter by length_years, by default None
         length_years_lt: Optional[float], optional
             filter by length_years, by default None
         length_years_lte: Optional[float], optional
             filter by length_years, by default None
         original_signing: Optional[datetime], optional
             Date when the contract was originally signed, by default None
         original_signing_gt: Optional[datetime], optional
             filter by '' original_signing > x '', by default None
         original_signing_gte: Optional[datetime], optional
             filter by original_signing, by default None
         original_signing_lt: Optional[datetime], optional
             filter by original_signing, by default None
         original_signing_lte: Optional[datetime], optional
             filter by original_signing, by default None
         annual_contract_volume: Optional[float], optional
             Numeric values of the annual contract quantity for the given offtake contract, by default None
         annual_contract_volume_gt: Optional[float], optional
             filter by '' annual_contract_volume > x '', by default None
         annual_contract_volume_gte: Optional[float], optional
             filter by annual_contract_volume, by default None
         annual_contract_volume_lt: Optional[float], optional
             filter by annual_contract_volume, by default None
         annual_contract_volume_lte: Optional[float], optional
             filter by annual_contract_volume, by default None
         annual_contract_volume_uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure of the annual contract quantity for the given offtake contract, by default None
         initial_contract_volume: Optional[float], optional
             Numeric values of the initial contract quantity for the given offtake contract, by default None
         initial_contract_volume_gt: Optional[float], optional
             filter by '' initial_contract_volume > x '', by default None
         initial_contract_volume_gte: Optional[float], optional
             filter by initial_contract_volume, by default None
         initial_contract_volume_lt: Optional[float], optional
             filter by initial_contract_volume, by default None
         initial_contract_volume_lte: Optional[float], optional
             filter by initial_contract_volume, by default None
         initial_contract_volume_uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure of the initial contract quantity for the given offtake contract, by default None
         pricing_linkage: Optional[Union[list[str], Series[str], str]]
             Determining contract pricing, by default None
         specific_price_link: Optional[Union[list[str], Series[str], str]]
             Prices formula or reference for contract pricing calculation, by default None
         fid_enabling: Optional[Union[list[str], Series[str], str]]
             Category denoting the timing of when the contract was signed relative to the project's FID milestone, by default None
         green_or_brownfield: Optional[Union[list[str], Series[str], str]]
             Whether the contract is associated with a greenfield or brownfield facility or portfolio, by default None
         modified_date: Optional[datetime], optional
             Date when the offtake contract was last modified, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(
            list_to_filter("buildoutMonthEstimated", buildout_month_estimated)
        )
        if buildout_month_estimated_gt is not None:
            filter_params.append(
                f'buildoutMonthEstimated > "{buildout_month_estimated_gt}"'
            )
        if buildout_month_estimated_gte is not None:
            filter_params.append(
                f'buildoutMonthEstimated >= "{buildout_month_estimated_gte}"'
            )
        if buildout_month_estimated_lt is not None:
            filter_params.append(
                f'buildoutMonthEstimated < "{buildout_month_estimated_lt}"'
            )
        if buildout_month_estimated_lte is not None:
            filter_params.append(
                f'buildoutMonthEstimated <= "{buildout_month_estimated_lte}"'
            )
        filter_params.append(
            list_to_filter("createdDateEstimated", created_date_estimated)
        )
        if created_date_estimated_gt is not None:
            filter_params.append(
                f'createdDateEstimated > "{created_date_estimated_gt}"'
            )
        if created_date_estimated_gte is not None:
            filter_params.append(
                f'createdDateEstimated >= "{created_date_estimated_gte}"'
            )
        if created_date_estimated_lt is not None:
            filter_params.append(
                f'createdDateEstimated < "{created_date_estimated_lt}"'
            )
        if created_date_estimated_lte is not None:
            filter_params.append(
                f'createdDateEstimated <= "{created_date_estimated_lte}"'
            )
        filter_params.append(
            list_to_filter("modifiedDateEstimated", modified_date_estimated)
        )
        if modified_date_estimated_gt is not None:
            filter_params.append(
                f'modifiedDateEstimated > "{modified_date_estimated_gt}"'
            )
        if modified_date_estimated_gte is not None:
            filter_params.append(
                f'modifiedDateEstimated >= "{modified_date_estimated_gte}"'
            )
        if modified_date_estimated_lt is not None:
            filter_params.append(
                f'modifiedDateEstimated < "{modified_date_estimated_lt}"'
            )
        if modified_date_estimated_lte is not None:
            filter_params.append(
                f'modifiedDateEstimated <= "{modified_date_estimated_lte}"'
            )
        filter_params.append(list_to_filter("buyer", buyer))
        filter_params.append(list_to_filter("exporter", exporter))
        filter_params.append(list_to_filter("contractGroup", contract_group))
        filter_params.append(list_to_filter("supplyMarket", supply_market))
        filter_params.append(list_to_filter("assumedDestination", assumed_destination))
        filter_params.append(list_to_filter("contractType", contract_type))
        filter_params.append(
            list_to_filter("liquefactionProject", liquefaction_project)
        )
        filter_params.append(list_to_filter("shippingTerms", shipping_terms))
        filter_params.append(
            list_to_filter("destinationFlexibility", destination_flexibility)
        )
        filter_params.append(list_to_filter("estimatedStartDate", estimated_start_date))
        if estimated_start_date_gt is not None:
            filter_params.append(f'estimatedStartDate > "{estimated_start_date_gt}"')
        if estimated_start_date_gte is not None:
            filter_params.append(f'estimatedStartDate >= "{estimated_start_date_gte}"')
        if estimated_start_date_lt is not None:
            filter_params.append(f'estimatedStartDate < "{estimated_start_date_lt}"')
        if estimated_start_date_lte is not None:
            filter_params.append(f'estimatedStartDate <= "{estimated_start_date_lte}"')
        filter_params.append(list_to_filter("estimatedEndDate", estimated_end_date))
        if estimated_end_date_gt is not None:
            filter_params.append(f'estimatedEndDate > "{estimated_end_date_gt}"')
        if estimated_end_date_gte is not None:
            filter_params.append(f'estimatedEndDate >= "{estimated_end_date_gte}"')
        if estimated_end_date_lt is not None:
            filter_params.append(f'estimatedEndDate < "{estimated_end_date_lt}"')
        if estimated_end_date_lte is not None:
            filter_params.append(f'estimatedEndDate <= "{estimated_end_date_lte}"')
        filter_params.append(list_to_filter("lengthYears", length_years))
        if length_years_gt is not None:
            filter_params.append(f'lengthYears > "{length_years_gt}"')
        if length_years_gte is not None:
            filter_params.append(f'lengthYears >= "{length_years_gte}"')
        if length_years_lt is not None:
            filter_params.append(f'lengthYears < "{length_years_lt}"')
        if length_years_lte is not None:
            filter_params.append(f'lengthYears <= "{length_years_lte}"')
        filter_params.append(list_to_filter("originalSigning", original_signing))
        if original_signing_gt is not None:
            filter_params.append(f'originalSigning > "{original_signing_gt}"')
        if original_signing_gte is not None:
            filter_params.append(f'originalSigning >= "{original_signing_gte}"')
        if original_signing_lt is not None:
            filter_params.append(f'originalSigning < "{original_signing_lt}"')
        if original_signing_lte is not None:
            filter_params.append(f'originalSigning <= "{original_signing_lte}"')
        filter_params.append(
            list_to_filter("annualContractVolume", annual_contract_volume)
        )
        if annual_contract_volume_gt is not None:
            filter_params.append(
                f'annualContractVolume > "{annual_contract_volume_gt}"'
            )
        if annual_contract_volume_gte is not None:
            filter_params.append(
                f'annualContractVolume >= "{annual_contract_volume_gte}"'
            )
        if annual_contract_volume_lt is not None:
            filter_params.append(
                f'annualContractVolume < "{annual_contract_volume_lt}"'
            )
        if annual_contract_volume_lte is not None:
            filter_params.append(
                f'annualContractVolume <= "{annual_contract_volume_lte}"'
            )
        filter_params.append(
            list_to_filter("annualContractVolumeUom", annual_contract_volume_uom)
        )
        filter_params.append(
            list_to_filter("initialContractVolume", initial_contract_volume)
        )
        if initial_contract_volume_gt is not None:
            filter_params.append(
                f'initialContractVolume > "{initial_contract_volume_gt}"'
            )
        if initial_contract_volume_gte is not None:
            filter_params.append(
                f'initialContractVolume >= "{initial_contract_volume_gte}"'
            )
        if initial_contract_volume_lt is not None:
            filter_params.append(
                f'initialContractVolume < "{initial_contract_volume_lt}"'
            )
        if initial_contract_volume_lte is not None:
            filter_params.append(
                f'initialContractVolume <= "{initial_contract_volume_lte}"'
            )
        filter_params.append(
            list_to_filter("initialContractVolumeUom", initial_contract_volume_uom)
        )
        filter_params.append(list_to_filter("pricingLinkage", pricing_linkage))
        filter_params.append(list_to_filter("specificPriceLink", specific_price_link))
        filter_params.append(list_to_filter("fidEnabling", fid_enabling))
        filter_params.append(list_to_filter("greenOrBrownfield", green_or_brownfield))
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/monthly-estimated-buildout/offtake-contracts",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_monthly_estimated_buildout_liquefaction_capacity(
        self,
        *,
        buildout_month_estimated: Optional[datetime] = None,
        buildout_month_estimated_lt: Optional[datetime] = None,
        buildout_month_estimated_lte: Optional[datetime] = None,
        buildout_month_estimated_gt: Optional[datetime] = None,
        buildout_month_estimated_gte: Optional[datetime] = None,
        created_date_estimated: Optional[datetime] = None,
        created_date_estimated_lt: Optional[datetime] = None,
        created_date_estimated_lte: Optional[datetime] = None,
        created_date_estimated_gt: Optional[datetime] = None,
        created_date_estimated_gte: Optional[datetime] = None,
        modified_date_estimated: Optional[datetime] = None,
        modified_date_estimated_lt: Optional[datetime] = None,
        modified_date_estimated_lte: Optional[datetime] = None,
        modified_date_estimated_gt: Optional[datetime] = None,
        modified_date_estimated_gte: Optional[datetime] = None,
        buildout_month_announced: Optional[datetime] = None,
        buildout_month_announced_lt: Optional[datetime] = None,
        buildout_month_announced_lte: Optional[datetime] = None,
        buildout_month_announced_gt: Optional[datetime] = None,
        buildout_month_announced_gte: Optional[datetime] = None,
        created_date_announced: Optional[datetime] = None,
        created_date_announced_lt: Optional[datetime] = None,
        created_date_announced_lte: Optional[datetime] = None,
        created_date_announced_gt: Optional[datetime] = None,
        created_date_announced_gte: Optional[datetime] = None,
        modified_date_announced: Optional[datetime] = None,
        modified_date_announced_lt: Optional[datetime] = None,
        modified_date_announced_lte: Optional[datetime] = None,
        modified_date_announced_gt: Optional[datetime] = None,
        modified_date_announced_gte: Optional[datetime] = None,
        liquefaction_train: Optional[Union[list[str], Series[str], str]] = None,
        liquefaction_project: Optional[Union[list[str], Series[str], str]] = None,
        initial_capacity: Optional[float] = None,
        initial_capacity_lt: Optional[float] = None,
        initial_capacity_lte: Optional[float] = None,
        initial_capacity_gt: Optional[float] = None,
        initial_capacity_gte: Optional[float] = None,
        initial_capacity_uom: Optional[Union[list[str], Series[str], str]] = None,
        estimated_start_date: Optional[datetime] = None,
        estimated_start_date_lt: Optional[datetime] = None,
        estimated_start_date_lte: Optional[datetime] = None,
        estimated_start_date_gt: Optional[datetime] = None,
        estimated_start_date_gte: Optional[datetime] = None,
        announced_start_date: Optional[datetime] = None,
        announced_start_date_lt: Optional[datetime] = None,
        announced_start_date_lte: Optional[datetime] = None,
        announced_start_date_gt: Optional[datetime] = None,
        announced_start_date_gte: Optional[datetime] = None,
        train_status: Optional[Union[list[str], Series[str], str]] = None,
        green_brownfield: Optional[Union[list[str], Series[str], str]] = None,
        liquefaction_technology: Optional[Union[list[str], Series[str], str]] = None,
        supply_market: Optional[Union[list[str], Series[str], str]] = None,
        train_operator: Optional[Union[list[str], Series[str], str]] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Provides monthly announced and estimated capacity buildouts for liquefaction trains and their attributes

        Parameters
        ----------

         buildout_month_estimated: Optional[datetime], optional
             Month for which the estimated buildout information is provided, by default None
         buildout_month_estimated_gt: Optional[datetime], optional
             filter by '' buildout_month_estimated > x '', by default None
         buildout_month_estimated_gte: Optional[datetime], optional
             filter by buildout_month_estimated, by default None
         buildout_month_estimated_lt: Optional[datetime], optional
             filter by buildout_month_estimated, by default None
         buildout_month_estimated_lte: Optional[datetime], optional
             filter by buildout_month_estimated, by default None
         created_date_estimated: Optional[datetime], optional
             Date when the estimated buildout information was created, by default None
         created_date_estimated_gt: Optional[datetime], optional
             filter by '' created_date_estimated > x '', by default None
         created_date_estimated_gte: Optional[datetime], optional
             filter by created_date_estimated, by default None
         created_date_estimated_lt: Optional[datetime], optional
             filter by created_date_estimated, by default None
         created_date_estimated_lte: Optional[datetime], optional
             filter by created_date_estimated, by default None
         modified_date_estimated: Optional[datetime], optional
             Date when the estimated buildout information was last modified, by default None
         modified_date_estimated_gt: Optional[datetime], optional
             filter by '' modified_date_estimated > x '', by default None
         modified_date_estimated_gte: Optional[datetime], optional
             filter by modified_date_estimated, by default None
         modified_date_estimated_lt: Optional[datetime], optional
             filter by modified_date_estimated, by default None
         modified_date_estimated_lte: Optional[datetime], optional
             filter by modified_date_estimated, by default None
         buildout_month_announced: Optional[datetime], optional
             Month for which the announced buildout information is provided, by default None
         buildout_month_announced_gt: Optional[datetime], optional
             filter by '' buildout_month_announced > x '', by default None
         buildout_month_announced_gte: Optional[datetime], optional
             filter by buildout_month_announced, by default None
         buildout_month_announced_lt: Optional[datetime], optional
             filter by buildout_month_announced, by default None
         buildout_month_announced_lte: Optional[datetime], optional
             filter by buildout_month_announced, by default None
         created_date_announced: Optional[datetime], optional
             Date when the announced buildout information was created, by default None
         created_date_announced_gt: Optional[datetime], optional
             filter by '' created_date_announced > x '', by default None
         created_date_announced_gte: Optional[datetime], optional
             filter by created_date_announced, by default None
         created_date_announced_lt: Optional[datetime], optional
             filter by created_date_announced, by default None
         created_date_announced_lte: Optional[datetime], optional
             filter by created_date_announced, by default None
         modified_date_announced: Optional[datetime], optional
             Date when the announced buildout information was last modified, by default None
         modified_date_announced_gt: Optional[datetime], optional
             filter by '' modified_date_announced > x '', by default None
         modified_date_announced_gte: Optional[datetime], optional
             filter by modified_date_announced, by default None
         modified_date_announced_lt: Optional[datetime], optional
             filter by modified_date_announced, by default None
         modified_date_announced_lte: Optional[datetime], optional
             filter by modified_date_announced, by default None
         liquefaction_train: Optional[Union[list[str], Series[str], str]]
             Name or identifier of the liquefaction train associated with the buildout information, by default None
         liquefaction_project: Optional[Union[list[str], Series[str], str]]
             Name or title of the liquefaction project associated with the buildout information, by default None
         initial_capacity: Optional[float], optional
             Numeric values of the initial capacity of the liquefaction train, by default None
         initial_capacity_gt: Optional[float], optional
             filter by '' initial_capacity > x '', by default None
         initial_capacity_gte: Optional[float], optional
             filter by initial_capacity, by default None
         initial_capacity_lt: Optional[float], optional
             filter by initial_capacity, by default None
         initial_capacity_lte: Optional[float], optional
             filter by initial_capacity, by default None
         initial_capacity_uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure of the initial capacity of the liquefaction train, by default None
         estimated_start_date: Optional[datetime], optional
             Our estimated start date for the liquefaction train, by default None
         estimated_start_date_gt: Optional[datetime], optional
             filter by '' estimated_start_date > x '', by default None
         estimated_start_date_gte: Optional[datetime], optional
             filter by estimated_start_date, by default None
         estimated_start_date_lt: Optional[datetime], optional
             filter by estimated_start_date, by default None
         estimated_start_date_lte: Optional[datetime], optional
             filter by estimated_start_date, by default None
         announced_start_date: Optional[datetime], optional
             Announced start date for the liquefaction train, by default None
         announced_start_date_gt: Optional[datetime], optional
             filter by '' announced_start_date > x '', by default None
         announced_start_date_gte: Optional[datetime], optional
             filter by announced_start_date, by default None
         announced_start_date_lt: Optional[datetime], optional
             filter by announced_start_date, by default None
         announced_start_date_lte: Optional[datetime], optional
             filter by announced_start_date, by default None
         train_status: Optional[Union[list[str], Series[str], str]]
             Status of the liquefaction train, by default None
         green_brownfield: Optional[Union[list[str], Series[str], str]]
             Indicates whether the liquefaction project is greenfield or brownfield, by default None
         liquefaction_technology: Optional[Union[list[str], Series[str], str]]
             Technology used for liquefaction, by default None
         supply_market: Optional[Union[list[str], Series[str], str]]
             Market where the liquefaction train is located, by default None
         train_operator: Optional[Union[list[str], Series[str], str]]
             Entity or company operating the liquefaction train, by default None
         modified_date: Optional[datetime], optional
             Liquefaction capacity monthly estimated buildout record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(
            list_to_filter("buildoutMonthEstimated", buildout_month_estimated)
        )
        if buildout_month_estimated_gt is not None:
            filter_params.append(
                f'buildoutMonthEstimated > "{buildout_month_estimated_gt}"'
            )
        if buildout_month_estimated_gte is not None:
            filter_params.append(
                f'buildoutMonthEstimated >= "{buildout_month_estimated_gte}"'
            )
        if buildout_month_estimated_lt is not None:
            filter_params.append(
                f'buildoutMonthEstimated < "{buildout_month_estimated_lt}"'
            )
        if buildout_month_estimated_lte is not None:
            filter_params.append(
                f'buildoutMonthEstimated <= "{buildout_month_estimated_lte}"'
            )
        filter_params.append(
            list_to_filter("createdDateEstimated", created_date_estimated)
        )
        if created_date_estimated_gt is not None:
            filter_params.append(
                f'createdDateEstimated > "{created_date_estimated_gt}"'
            )
        if created_date_estimated_gte is not None:
            filter_params.append(
                f'createdDateEstimated >= "{created_date_estimated_gte}"'
            )
        if created_date_estimated_lt is not None:
            filter_params.append(
                f'createdDateEstimated < "{created_date_estimated_lt}"'
            )
        if created_date_estimated_lte is not None:
            filter_params.append(
                f'createdDateEstimated <= "{created_date_estimated_lte}"'
            )
        filter_params.append(
            list_to_filter("modifiedDateEstimated", modified_date_estimated)
        )
        if modified_date_estimated_gt is not None:
            filter_params.append(
                f'modifiedDateEstimated > "{modified_date_estimated_gt}"'
            )
        if modified_date_estimated_gte is not None:
            filter_params.append(
                f'modifiedDateEstimated >= "{modified_date_estimated_gte}"'
            )
        if modified_date_estimated_lt is not None:
            filter_params.append(
                f'modifiedDateEstimated < "{modified_date_estimated_lt}"'
            )
        if modified_date_estimated_lte is not None:
            filter_params.append(
                f'modifiedDateEstimated <= "{modified_date_estimated_lte}"'
            )
        filter_params.append(
            list_to_filter("buildoutMonthAnnounced", buildout_month_announced)
        )
        if buildout_month_announced_gt is not None:
            filter_params.append(
                f'buildoutMonthAnnounced > "{buildout_month_announced_gt}"'
            )
        if buildout_month_announced_gte is not None:
            filter_params.append(
                f'buildoutMonthAnnounced >= "{buildout_month_announced_gte}"'
            )
        if buildout_month_announced_lt is not None:
            filter_params.append(
                f'buildoutMonthAnnounced < "{buildout_month_announced_lt}"'
            )
        if buildout_month_announced_lte is not None:
            filter_params.append(
                f'buildoutMonthAnnounced <= "{buildout_month_announced_lte}"'
            )
        filter_params.append(
            list_to_filter("createdDateAnnounced", created_date_announced)
        )
        if created_date_announced_gt is not None:
            filter_params.append(
                f'createdDateAnnounced > "{created_date_announced_gt}"'
            )
        if created_date_announced_gte is not None:
            filter_params.append(
                f'createdDateAnnounced >= "{created_date_announced_gte}"'
            )
        if created_date_announced_lt is not None:
            filter_params.append(
                f'createdDateAnnounced < "{created_date_announced_lt}"'
            )
        if created_date_announced_lte is not None:
            filter_params.append(
                f'createdDateAnnounced <= "{created_date_announced_lte}"'
            )
        filter_params.append(
            list_to_filter("modifiedDateAnnounced", modified_date_announced)
        )
        if modified_date_announced_gt is not None:
            filter_params.append(
                f'modifiedDateAnnounced > "{modified_date_announced_gt}"'
            )
        if modified_date_announced_gte is not None:
            filter_params.append(
                f'modifiedDateAnnounced >= "{modified_date_announced_gte}"'
            )
        if modified_date_announced_lt is not None:
            filter_params.append(
                f'modifiedDateAnnounced < "{modified_date_announced_lt}"'
            )
        if modified_date_announced_lte is not None:
            filter_params.append(
                f'modifiedDateAnnounced <= "{modified_date_announced_lte}"'
            )
        filter_params.append(list_to_filter("liquefactionTrain", liquefaction_train))
        filter_params.append(
            list_to_filter("liquefactionProject", liquefaction_project)
        )
        filter_params.append(list_to_filter("initialCapacity", initial_capacity))
        if initial_capacity_gt is not None:
            filter_params.append(f'initialCapacity > "{initial_capacity_gt}"')
        if initial_capacity_gte is not None:
            filter_params.append(f'initialCapacity >= "{initial_capacity_gte}"')
        if initial_capacity_lt is not None:
            filter_params.append(f'initialCapacity < "{initial_capacity_lt}"')
        if initial_capacity_lte is not None:
            filter_params.append(f'initialCapacity <= "{initial_capacity_lte}"')
        filter_params.append(list_to_filter("initialCapacityUom", initial_capacity_uom))
        filter_params.append(list_to_filter("estimatedStartDate", estimated_start_date))
        if estimated_start_date_gt is not None:
            filter_params.append(f'estimatedStartDate > "{estimated_start_date_gt}"')
        if estimated_start_date_gte is not None:
            filter_params.append(f'estimatedStartDate >= "{estimated_start_date_gte}"')
        if estimated_start_date_lt is not None:
            filter_params.append(f'estimatedStartDate < "{estimated_start_date_lt}"')
        if estimated_start_date_lte is not None:
            filter_params.append(f'estimatedStartDate <= "{estimated_start_date_lte}"')
        filter_params.append(list_to_filter("announcedStartDate", announced_start_date))
        if announced_start_date_gt is not None:
            filter_params.append(f'announcedStartDate > "{announced_start_date_gt}"')
        if announced_start_date_gte is not None:
            filter_params.append(f'announcedStartDate >= "{announced_start_date_gte}"')
        if announced_start_date_lt is not None:
            filter_params.append(f'announcedStartDate < "{announced_start_date_lt}"')
        if announced_start_date_lte is not None:
            filter_params.append(f'announcedStartDate <= "{announced_start_date_lte}"')
        filter_params.append(list_to_filter("trainStatus", train_status))
        filter_params.append(list_to_filter("greenBrownfield", green_brownfield))
        filter_params.append(
            list_to_filter("liquefactionTechnology", liquefaction_technology)
        )
        filter_params.append(list_to_filter("supplyMarket", supply_market))
        filter_params.append(list_to_filter("trainOperator", train_operator))
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/monthly-estimated-buildout/liquefaction-capacity",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_monthly_estimated_buildout_regasification_contracts(
        self,
        *,
        buildout_month_estimated: Optional[datetime] = None,
        buildout_month_estimated_lt: Optional[datetime] = None,
        buildout_month_estimated_lte: Optional[datetime] = None,
        buildout_month_estimated_gt: Optional[datetime] = None,
        buildout_month_estimated_gte: Optional[datetime] = None,
        created_date_estimated: Optional[datetime] = None,
        created_date_estimated_lt: Optional[datetime] = None,
        created_date_estimated_lte: Optional[datetime] = None,
        created_date_estimated_gt: Optional[datetime] = None,
        created_date_estimated_gte: Optional[datetime] = None,
        modified_date_estimated: Optional[datetime] = None,
        modified_date_estimated_lt: Optional[datetime] = None,
        modified_date_estimated_lte: Optional[datetime] = None,
        modified_date_estimated_gt: Optional[datetime] = None,
        modified_date_estimated_gte: Optional[datetime] = None,
        buildout_month_announced: Optional[datetime] = None,
        buildout_month_announced_lt: Optional[datetime] = None,
        buildout_month_announced_lte: Optional[datetime] = None,
        buildout_month_announced_gt: Optional[datetime] = None,
        buildout_month_announced_gte: Optional[datetime] = None,
        created_date_announced: Optional[datetime] = None,
        created_date_announced_lt: Optional[datetime] = None,
        created_date_announced_lte: Optional[datetime] = None,
        created_date_announced_gt: Optional[datetime] = None,
        created_date_announced_gte: Optional[datetime] = None,
        modified_date_announced: Optional[datetime] = None,
        modified_date_announced_lt: Optional[datetime] = None,
        modified_date_announced_lte: Optional[datetime] = None,
        modified_date_announced_gt: Optional[datetime] = None,
        modified_date_announced_gte: Optional[datetime] = None,
        regasification_phase: Optional[Union[list[str], Series[str], str]] = None,
        regasification_terminal: Optional[Union[list[str], Series[str], str]] = None,
        market: Optional[Union[list[str], Series[str], str]] = None,
        terminal_type: Optional[Union[list[str], Series[str], str]] = None,
        contract_type: Optional[Union[list[str], Series[str], str]] = None,
        capacity_owner: Optional[Union[list[str], Series[str], str]] = None,
        contract_volume: Optional[float] = None,
        contract_volume_lt: Optional[float] = None,
        contract_volume_lte: Optional[float] = None,
        contract_volume_gt: Optional[float] = None,
        contract_volume_gte: Optional[float] = None,
        contract_volume_uom: Optional[Union[list[str], Series[str], str]] = None,
        phase_capacity: Optional[float] = None,
        phase_capacity_lt: Optional[float] = None,
        phase_capacity_lte: Optional[float] = None,
        phase_capacity_gt: Optional[float] = None,
        phase_capacity_gte: Optional[float] = None,
        phase_capacity_uom: Optional[Union[list[str], Series[str], str]] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Provides monthly announced and estimated offtake contract buildouts for liquefaction projects and their attributes

        Parameters
        ----------

         buildout_month_estimated: Optional[datetime], optional
             Month the buildout is estimated to start, by default None
         buildout_month_estimated_gt: Optional[datetime], optional
             filter by '' buildout_month_estimated > x '', by default None
         buildout_month_estimated_gte: Optional[datetime], optional
             filter by buildout_month_estimated, by default None
         buildout_month_estimated_lt: Optional[datetime], optional
             filter by buildout_month_estimated, by default None
         buildout_month_estimated_lte: Optional[datetime], optional
             filter by buildout_month_estimated, by default None
         created_date_estimated: Optional[datetime], optional
             Date when the estimated buildout information was created, by default None
         created_date_estimated_gt: Optional[datetime], optional
             filter by '' created_date_estimated > x '', by default None
         created_date_estimated_gte: Optional[datetime], optional
             filter by created_date_estimated, by default None
         created_date_estimated_lt: Optional[datetime], optional
             filter by created_date_estimated, by default None
         created_date_estimated_lte: Optional[datetime], optional
             filter by created_date_estimated, by default None
         modified_date_estimated: Optional[datetime], optional
             Date when the estimated buildout information was last modified, by default None
         modified_date_estimated_gt: Optional[datetime], optional
             filter by '' modified_date_estimated > x '', by default None
         modified_date_estimated_gte: Optional[datetime], optional
             filter by modified_date_estimated, by default None
         modified_date_estimated_lt: Optional[datetime], optional
             filter by modified_date_estimated, by default None
         modified_date_estimated_lte: Optional[datetime], optional
             filter by modified_date_estimated, by default None
         buildout_month_announced: Optional[datetime], optional
             Month for which the announced buildout information is provided, by default None
         buildout_month_announced_gt: Optional[datetime], optional
             filter by '' buildout_month_announced > x '', by default None
         buildout_month_announced_gte: Optional[datetime], optional
             filter by buildout_month_announced, by default None
         buildout_month_announced_lt: Optional[datetime], optional
             filter by buildout_month_announced, by default None
         buildout_month_announced_lte: Optional[datetime], optional
             filter by buildout_month_announced, by default None
         created_date_announced: Optional[datetime], optional
             Date when the announced buildout information was created, by default None
         created_date_announced_gt: Optional[datetime], optional
             filter by '' created_date_announced > x '', by default None
         created_date_announced_gte: Optional[datetime], optional
             filter by created_date_announced, by default None
         created_date_announced_lt: Optional[datetime], optional
             filter by created_date_announced, by default None
         created_date_announced_lte: Optional[datetime], optional
             filter by created_date_announced, by default None
         modified_date_announced: Optional[datetime], optional
             Date when the announced buildout information was last modified, by default None
         modified_date_announced_gt: Optional[datetime], optional
             filter by '' modified_date_announced > x '', by default None
         modified_date_announced_gte: Optional[datetime], optional
             filter by modified_date_announced, by default None
         modified_date_announced_lt: Optional[datetime], optional
             filter by modified_date_announced, by default None
         modified_date_announced_lte: Optional[datetime], optional
             filter by modified_date_announced, by default None
         regasification_phase: Optional[Union[list[str], Series[str], str]]
             Name of regasification phase the contract is associated with, by default None
         regasification_terminal: Optional[Union[list[str], Series[str], str]]
             Name of regasification terminal the contract is associated with, by default None
         market: Optional[Union[list[str], Series[str], str]]
             Market where the regasification contract is located, by default None
         terminal_type: Optional[Union[list[str], Series[str], str]]
             Offshore or onshore terminal, by default None
         contract_type: Optional[Union[list[str], Series[str], str]]
             The status of the capcity contract, by default None
         capacity_owner: Optional[Union[list[str], Series[str], str]]
             Company of joint venture name that owns the capacity contract, by default None
         contract_volume: Optional[float], optional
             Numeric values of the contract quantity for the given regasification contract, by default None
         contract_volume_gt: Optional[float], optional
             filter by '' contract_volume > x '', by default None
         contract_volume_gte: Optional[float], optional
             filter by contract_volume, by default None
         contract_volume_lt: Optional[float], optional
             filter by contract_volume, by default None
         contract_volume_lte: Optional[float], optional
             filter by contract_volume, by default None
         contract_volume_uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure of the contract quantity for the given regasification contract, by default None
         phase_capacity: Optional[float], optional
             Numeric values of the regasification phase capacity for the corresponding regasification contract, by default None
         phase_capacity_gt: Optional[float], optional
             filter by '' phase_capacity > x '', by default None
         phase_capacity_gte: Optional[float], optional
             filter by phase_capacity, by default None
         phase_capacity_lt: Optional[float], optional
             filter by phase_capacity, by default None
         phase_capacity_lte: Optional[float], optional
             filter by phase_capacity, by default None
         phase_capacity_uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure of the regasification phase capacity for the corresponding regasification contract, by default None
         modified_date: Optional[datetime], optional
             Date when the regasification contract was last modified, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(
            list_to_filter("buildoutMonthEstimated", buildout_month_estimated)
        )
        if buildout_month_estimated_gt is not None:
            filter_params.append(
                f'buildoutMonthEstimated > "{buildout_month_estimated_gt}"'
            )
        if buildout_month_estimated_gte is not None:
            filter_params.append(
                f'buildoutMonthEstimated >= "{buildout_month_estimated_gte}"'
            )
        if buildout_month_estimated_lt is not None:
            filter_params.append(
                f'buildoutMonthEstimated < "{buildout_month_estimated_lt}"'
            )
        if buildout_month_estimated_lte is not None:
            filter_params.append(
                f'buildoutMonthEstimated <= "{buildout_month_estimated_lte}"'
            )
        filter_params.append(
            list_to_filter("createdDateEstimated", created_date_estimated)
        )
        if created_date_estimated_gt is not None:
            filter_params.append(
                f'createdDateEstimated > "{created_date_estimated_gt}"'
            )
        if created_date_estimated_gte is not None:
            filter_params.append(
                f'createdDateEstimated >= "{created_date_estimated_gte}"'
            )
        if created_date_estimated_lt is not None:
            filter_params.append(
                f'createdDateEstimated < "{created_date_estimated_lt}"'
            )
        if created_date_estimated_lte is not None:
            filter_params.append(
                f'createdDateEstimated <= "{created_date_estimated_lte}"'
            )
        filter_params.append(
            list_to_filter("modifiedDateEstimated", modified_date_estimated)
        )
        if modified_date_estimated_gt is not None:
            filter_params.append(
                f'modifiedDateEstimated > "{modified_date_estimated_gt}"'
            )
        if modified_date_estimated_gte is not None:
            filter_params.append(
                f'modifiedDateEstimated >= "{modified_date_estimated_gte}"'
            )
        if modified_date_estimated_lt is not None:
            filter_params.append(
                f'modifiedDateEstimated < "{modified_date_estimated_lt}"'
            )
        if modified_date_estimated_lte is not None:
            filter_params.append(
                f'modifiedDateEstimated <= "{modified_date_estimated_lte}"'
            )
        filter_params.append(
            list_to_filter("buildoutMonthAnnounced", buildout_month_announced)
        )
        if buildout_month_announced_gt is not None:
            filter_params.append(
                f'buildoutMonthAnnounced > "{buildout_month_announced_gt}"'
            )
        if buildout_month_announced_gte is not None:
            filter_params.append(
                f'buildoutMonthAnnounced >= "{buildout_month_announced_gte}"'
            )
        if buildout_month_announced_lt is not None:
            filter_params.append(
                f'buildoutMonthAnnounced < "{buildout_month_announced_lt}"'
            )
        if buildout_month_announced_lte is not None:
            filter_params.append(
                f'buildoutMonthAnnounced <= "{buildout_month_announced_lte}"'
            )
        filter_params.append(
            list_to_filter("createdDateAnnounced", created_date_announced)
        )
        if created_date_announced_gt is not None:
            filter_params.append(
                f'createdDateAnnounced > "{created_date_announced_gt}"'
            )
        if created_date_announced_gte is not None:
            filter_params.append(
                f'createdDateAnnounced >= "{created_date_announced_gte}"'
            )
        if created_date_announced_lt is not None:
            filter_params.append(
                f'createdDateAnnounced < "{created_date_announced_lt}"'
            )
        if created_date_announced_lte is not None:
            filter_params.append(
                f'createdDateAnnounced <= "{created_date_announced_lte}"'
            )
        filter_params.append(
            list_to_filter("modifiedDateAnnounced", modified_date_announced)
        )
        if modified_date_announced_gt is not None:
            filter_params.append(
                f'modifiedDateAnnounced > "{modified_date_announced_gt}"'
            )
        if modified_date_announced_gte is not None:
            filter_params.append(
                f'modifiedDateAnnounced >= "{modified_date_announced_gte}"'
            )
        if modified_date_announced_lt is not None:
            filter_params.append(
                f'modifiedDateAnnounced < "{modified_date_announced_lt}"'
            )
        if modified_date_announced_lte is not None:
            filter_params.append(
                f'modifiedDateAnnounced <= "{modified_date_announced_lte}"'
            )
        filter_params.append(
            list_to_filter("regasificationPhase", regasification_phase)
        )
        filter_params.append(
            list_to_filter("regasificationTerminal", regasification_terminal)
        )
        filter_params.append(list_to_filter("market", market))
        filter_params.append(list_to_filter("terminalType", terminal_type))
        filter_params.append(list_to_filter("contractType", contract_type))
        filter_params.append(list_to_filter("capacityOwner", capacity_owner))
        filter_params.append(list_to_filter("contractVolume", contract_volume))
        if contract_volume_gt is not None:
            filter_params.append(f'contractVolume > "{contract_volume_gt}"')
        if contract_volume_gte is not None:
            filter_params.append(f'contractVolume >= "{contract_volume_gte}"')
        if contract_volume_lt is not None:
            filter_params.append(f'contractVolume < "{contract_volume_lt}"')
        if contract_volume_lte is not None:
            filter_params.append(f'contractVolume <= "{contract_volume_lte}"')
        filter_params.append(list_to_filter("contractVolumeUom", contract_volume_uom))
        filter_params.append(list_to_filter("phaseCapacity", phase_capacity))
        if phase_capacity_gt is not None:
            filter_params.append(f'phaseCapacity > "{phase_capacity_gt}"')
        if phase_capacity_gte is not None:
            filter_params.append(f'phaseCapacity >= "{phase_capacity_gte}"')
        if phase_capacity_lt is not None:
            filter_params.append(f'phaseCapacity < "{phase_capacity_lt}"')
        if phase_capacity_lte is not None:
            filter_params.append(f'phaseCapacity <= "{phase_capacity_lte}"')
        filter_params.append(list_to_filter("phaseCapacityUom", phase_capacity_uom))
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/monthly-estimated-buildout/regasification-contracts",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_monthly_estimated_buildout_regasification_capacity(
        self,
        *,
        buildout_month_estimated: Optional[datetime] = None,
        buildout_month_estimated_lt: Optional[datetime] = None,
        buildout_month_estimated_lte: Optional[datetime] = None,
        buildout_month_estimated_gt: Optional[datetime] = None,
        buildout_month_estimated_gte: Optional[datetime] = None,
        created_date_estimated: Optional[datetime] = None,
        created_date_estimated_lt: Optional[datetime] = None,
        created_date_estimated_lte: Optional[datetime] = None,
        created_date_estimated_gt: Optional[datetime] = None,
        created_date_estimated_gte: Optional[datetime] = None,
        modified_date_estimated: Optional[datetime] = None,
        modified_date_estimated_lt: Optional[datetime] = None,
        modified_date_estimated_lte: Optional[datetime] = None,
        modified_date_estimated_gt: Optional[datetime] = None,
        modified_date_estimated_gte: Optional[datetime] = None,
        buildout_month_announced: Optional[datetime] = None,
        buildout_month_announced_lt: Optional[datetime] = None,
        buildout_month_announced_lte: Optional[datetime] = None,
        buildout_month_announced_gt: Optional[datetime] = None,
        buildout_month_announced_gte: Optional[datetime] = None,
        created_date_announced: Optional[datetime] = None,
        created_date_announced_lt: Optional[datetime] = None,
        created_date_announced_lte: Optional[datetime] = None,
        created_date_announced_gt: Optional[datetime] = None,
        created_date_announced_gte: Optional[datetime] = None,
        modified_date_announced: Optional[datetime] = None,
        modified_date_announced_lt: Optional[datetime] = None,
        modified_date_announced_lte: Optional[datetime] = None,
        modified_date_announced_gt: Optional[datetime] = None,
        modified_date_announced_gte: Optional[datetime] = None,
        regasification_phase: Optional[Union[list[str], Series[str], str]] = None,
        regasification_project: Optional[Union[list[str], Series[str], str]] = None,
        market: Optional[Union[list[str], Series[str], str]] = None,
        phase_status: Optional[Union[list[str], Series[str], str]] = None,
        estimated_start_date: Optional[datetime] = None,
        estimated_start_date_lt: Optional[datetime] = None,
        estimated_start_date_lte: Optional[datetime] = None,
        estimated_start_date_gt: Optional[datetime] = None,
        estimated_start_date_gte: Optional[datetime] = None,
        announced_start_date: Optional[datetime] = None,
        announced_start_date_lt: Optional[datetime] = None,
        announced_start_date_lte: Optional[datetime] = None,
        announced_start_date_gt: Optional[datetime] = None,
        announced_start_date_gte: Optional[datetime] = None,
        initial_capacity: Optional[float] = None,
        initial_capacity_lt: Optional[float] = None,
        initial_capacity_lte: Optional[float] = None,
        initial_capacity_gt: Optional[float] = None,
        initial_capacity_gte: Optional[float] = None,
        initial_capacity_uom: Optional[Union[list[str], Series[str], str]] = None,
        terminal_type_name: Optional[Union[list[str], Series[str], str]] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Provides monthly announced and estimated capacity buildouts for regasification phases and their attributes

        Parameters
        ----------

         buildout_month_estimated: Optional[datetime], optional
             Month in which the estimated buildout of regasification capacity is expected to occur, by default None
         buildout_month_estimated_gt: Optional[datetime], optional
             filter by '' buildout_month_estimated > x '', by default None
         buildout_month_estimated_gte: Optional[datetime], optional
             filter by buildout_month_estimated, by default None
         buildout_month_estimated_lt: Optional[datetime], optional
             filter by buildout_month_estimated, by default None
         buildout_month_estimated_lte: Optional[datetime], optional
             filter by buildout_month_estimated, by default None
         created_date_estimated: Optional[datetime], optional
             Date when the estimated buildout information was created, by default None
         created_date_estimated_gt: Optional[datetime], optional
             filter by '' created_date_estimated > x '', by default None
         created_date_estimated_gte: Optional[datetime], optional
             filter by created_date_estimated, by default None
         created_date_estimated_lt: Optional[datetime], optional
             filter by created_date_estimated, by default None
         created_date_estimated_lte: Optional[datetime], optional
             filter by created_date_estimated, by default None
         modified_date_estimated: Optional[datetime], optional
             Date when the estimated buildout information was last modified, by default None
         modified_date_estimated_gt: Optional[datetime], optional
             filter by '' modified_date_estimated > x '', by default None
         modified_date_estimated_gte: Optional[datetime], optional
             filter by modified_date_estimated, by default None
         modified_date_estimated_lt: Optional[datetime], optional
             filter by modified_date_estimated, by default None
         modified_date_estimated_lte: Optional[datetime], optional
             filter by modified_date_estimated, by default None
         buildout_month_announced: Optional[datetime], optional
             Month for which the announced buildout information is provided, by default None
         buildout_month_announced_gt: Optional[datetime], optional
             filter by '' buildout_month_announced > x '', by default None
         buildout_month_announced_gte: Optional[datetime], optional
             filter by buildout_month_announced, by default None
         buildout_month_announced_lt: Optional[datetime], optional
             filter by buildout_month_announced, by default None
         buildout_month_announced_lte: Optional[datetime], optional
             filter by buildout_month_announced, by default None
         created_date_announced: Optional[datetime], optional
             Date when the announced buildout was created, by default None
         created_date_announced_gt: Optional[datetime], optional
             filter by '' created_date_announced > x '', by default None
         created_date_announced_gte: Optional[datetime], optional
             filter by created_date_announced, by default None
         created_date_announced_lt: Optional[datetime], optional
             filter by created_date_announced, by default None
         created_date_announced_lte: Optional[datetime], optional
             filter by created_date_announced, by default None
         modified_date_announced: Optional[datetime], optional
             Date when the announced buildout was last modified, by default None
         modified_date_announced_gt: Optional[datetime], optional
             filter by '' modified_date_announced > x '', by default None
         modified_date_announced_gte: Optional[datetime], optional
             filter by modified_date_announced, by default None
         modified_date_announced_lt: Optional[datetime], optional
             filter by modified_date_announced, by default None
         modified_date_announced_lte: Optional[datetime], optional
             filter by modified_date_announced, by default None
         regasification_phase: Optional[Union[list[str], Series[str], str]]
             Name of the regasification phase, by default None
         regasification_project: Optional[Union[list[str], Series[str], str]]
             Name of the regasification project associated with the phase, by default None
         market: Optional[Union[list[str], Series[str], str]]
             Market where the regasification phase is located, by default None
         phase_status: Optional[Union[list[str], Series[str], str]]
             Status of the regasification phase, by default None
         estimated_start_date: Optional[datetime], optional
             Our estimated start date for the regasification phase, by default None
         estimated_start_date_gt: Optional[datetime], optional
             filter by '' estimated_start_date > x '', by default None
         estimated_start_date_gte: Optional[datetime], optional
             filter by estimated_start_date, by default None
         estimated_start_date_lt: Optional[datetime], optional
             filter by estimated_start_date, by default None
         estimated_start_date_lte: Optional[datetime], optional
             filter by estimated_start_date, by default None
         announced_start_date: Optional[datetime], optional
             Announced start date for the regasification phase, by default None
         announced_start_date_gt: Optional[datetime], optional
             filter by '' announced_start_date > x '', by default None
         announced_start_date_gte: Optional[datetime], optional
             filter by announced_start_date, by default None
         announced_start_date_lt: Optional[datetime], optional
             filter by announced_start_date, by default None
         announced_start_date_lte: Optional[datetime], optional
             filter by announced_start_date, by default None
         initial_capacity: Optional[float], optional
             Numeric values of the initial capacity of the regasification phase, by default None
         initial_capacity_gt: Optional[float], optional
             filter by '' initial_capacity > x '', by default None
         initial_capacity_gte: Optional[float], optional
             filter by initial_capacity, by default None
         initial_capacity_lt: Optional[float], optional
             filter by initial_capacity, by default None
         initial_capacity_lte: Optional[float], optional
             filter by initial_capacity, by default None
         initial_capacity_uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure of the initial capacity of the regasification phase, by default None
         terminal_type_name: Optional[Union[list[str], Series[str], str]]
             Type of regasification terminal, by default None
         modified_date: Optional[datetime], optional
             Regasification capacity monthly estimated buildout record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(
            list_to_filter("buildoutMonthEstimated", buildout_month_estimated)
        )
        if buildout_month_estimated_gt is not None:
            filter_params.append(
                f'buildoutMonthEstimated > "{buildout_month_estimated_gt}"'
            )
        if buildout_month_estimated_gte is not None:
            filter_params.append(
                f'buildoutMonthEstimated >= "{buildout_month_estimated_gte}"'
            )
        if buildout_month_estimated_lt is not None:
            filter_params.append(
                f'buildoutMonthEstimated < "{buildout_month_estimated_lt}"'
            )
        if buildout_month_estimated_lte is not None:
            filter_params.append(
                f'buildoutMonthEstimated <= "{buildout_month_estimated_lte}"'
            )
        filter_params.append(
            list_to_filter("createdDateEstimated", created_date_estimated)
        )
        if created_date_estimated_gt is not None:
            filter_params.append(
                f'createdDateEstimated > "{created_date_estimated_gt}"'
            )
        if created_date_estimated_gte is not None:
            filter_params.append(
                f'createdDateEstimated >= "{created_date_estimated_gte}"'
            )
        if created_date_estimated_lt is not None:
            filter_params.append(
                f'createdDateEstimated < "{created_date_estimated_lt}"'
            )
        if created_date_estimated_lte is not None:
            filter_params.append(
                f'createdDateEstimated <= "{created_date_estimated_lte}"'
            )
        filter_params.append(
            list_to_filter("modifiedDateEstimated", modified_date_estimated)
        )
        if modified_date_estimated_gt is not None:
            filter_params.append(
                f'modifiedDateEstimated > "{modified_date_estimated_gt}"'
            )
        if modified_date_estimated_gte is not None:
            filter_params.append(
                f'modifiedDateEstimated >= "{modified_date_estimated_gte}"'
            )
        if modified_date_estimated_lt is not None:
            filter_params.append(
                f'modifiedDateEstimated < "{modified_date_estimated_lt}"'
            )
        if modified_date_estimated_lte is not None:
            filter_params.append(
                f'modifiedDateEstimated <= "{modified_date_estimated_lte}"'
            )
        filter_params.append(
            list_to_filter("buildoutMonthAnnounced", buildout_month_announced)
        )
        if buildout_month_announced_gt is not None:
            filter_params.append(
                f'buildoutMonthAnnounced > "{buildout_month_announced_gt}"'
            )
        if buildout_month_announced_gte is not None:
            filter_params.append(
                f'buildoutMonthAnnounced >= "{buildout_month_announced_gte}"'
            )
        if buildout_month_announced_lt is not None:
            filter_params.append(
                f'buildoutMonthAnnounced < "{buildout_month_announced_lt}"'
            )
        if buildout_month_announced_lte is not None:
            filter_params.append(
                f'buildoutMonthAnnounced <= "{buildout_month_announced_lte}"'
            )
        filter_params.append(
            list_to_filter("createdDateAnnounced", created_date_announced)
        )
        if created_date_announced_gt is not None:
            filter_params.append(
                f'createdDateAnnounced > "{created_date_announced_gt}"'
            )
        if created_date_announced_gte is not None:
            filter_params.append(
                f'createdDateAnnounced >= "{created_date_announced_gte}"'
            )
        if created_date_announced_lt is not None:
            filter_params.append(
                f'createdDateAnnounced < "{created_date_announced_lt}"'
            )
        if created_date_announced_lte is not None:
            filter_params.append(
                f'createdDateAnnounced <= "{created_date_announced_lte}"'
            )
        filter_params.append(
            list_to_filter("modifiedDateAnnounced", modified_date_announced)
        )
        if modified_date_announced_gt is not None:
            filter_params.append(
                f'modifiedDateAnnounced > "{modified_date_announced_gt}"'
            )
        if modified_date_announced_gte is not None:
            filter_params.append(
                f'modifiedDateAnnounced >= "{modified_date_announced_gte}"'
            )
        if modified_date_announced_lt is not None:
            filter_params.append(
                f'modifiedDateAnnounced < "{modified_date_announced_lt}"'
            )
        if modified_date_announced_lte is not None:
            filter_params.append(
                f'modifiedDateAnnounced <= "{modified_date_announced_lte}"'
            )
        filter_params.append(
            list_to_filter("regasificationPhase", regasification_phase)
        )
        filter_params.append(
            list_to_filter("regasificationProject", regasification_project)
        )
        filter_params.append(list_to_filter("market", market))
        filter_params.append(list_to_filter("phaseStatus", phase_status))
        filter_params.append(list_to_filter("estimatedStartDate", estimated_start_date))
        if estimated_start_date_gt is not None:
            filter_params.append(f'estimatedStartDate > "{estimated_start_date_gt}"')
        if estimated_start_date_gte is not None:
            filter_params.append(f'estimatedStartDate >= "{estimated_start_date_gte}"')
        if estimated_start_date_lt is not None:
            filter_params.append(f'estimatedStartDate < "{estimated_start_date_lt}"')
        if estimated_start_date_lte is not None:
            filter_params.append(f'estimatedStartDate <= "{estimated_start_date_lte}"')
        filter_params.append(list_to_filter("announcedStartDate", announced_start_date))
        if announced_start_date_gt is not None:
            filter_params.append(f'announcedStartDate > "{announced_start_date_gt}"')
        if announced_start_date_gte is not None:
            filter_params.append(f'announcedStartDate >= "{announced_start_date_gte}"')
        if announced_start_date_lt is not None:
            filter_params.append(f'announcedStartDate < "{announced_start_date_lt}"')
        if announced_start_date_lte is not None:
            filter_params.append(f'announcedStartDate <= "{announced_start_date_lte}"')
        filter_params.append(list_to_filter("initialCapacity", initial_capacity))
        if initial_capacity_gt is not None:
            filter_params.append(f'initialCapacity > "{initial_capacity_gt}"')
        if initial_capacity_gte is not None:
            filter_params.append(f'initialCapacity >= "{initial_capacity_gte}"')
        if initial_capacity_lt is not None:
            filter_params.append(f'initialCapacity < "{initial_capacity_lt}"')
        if initial_capacity_lte is not None:
            filter_params.append(f'initialCapacity <= "{initial_capacity_lte}"')
        filter_params.append(list_to_filter("initialCapacityUom", initial_capacity_uom))
        filter_params.append(list_to_filter("terminalTypeName", terminal_type_name))
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/monthly-estimated-buildout/regasification-capacity",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_contracts_feedstock(
        self,
        *,
        economic_group: Optional[Union[list[str], Series[str], str]] = None,
        liquefaction_project: Optional[Union[list[str], Series[str], str]] = None,
        feedstock_asset: Optional[Union[list[str], Series[str], str]] = None,
        supply_market: Optional[Union[list[str], Series[str], str]] = None,
        year: Optional[int] = None,
        year_lt: Optional[int] = None,
        year_lte: Optional[int] = None,
        year_gt: Optional[int] = None,
        year_gte: Optional[int] = None,
        production_type: Optional[Union[list[str], Series[str], str]] = None,
        production_uom: Optional[Union[list[str], Series[str], str]] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Provides information on LNG feedstock production over time

        Parameters
        ----------

         economic_group: Optional[Union[list[str], Series[str], str]]
             Classification of the project based on economic characteristics, by default None
         liquefaction_project: Optional[Union[list[str], Series[str], str]]
             Name of the specific liquefaction project, by default None
         feedstock_asset: Optional[Union[list[str], Series[str], str]]
             The specific feedstock asset used in the liquefaction process, by default None
         supply_market: Optional[Union[list[str], Series[str], str]]
             The market from which the feedstock is sourced, by default None
         year: Optional[int], optional
             The year to which the data corresponds, by default None
         year_gt: Optional[int], optional
             filter by '' year > x '', by default None
         year_gte: Optional[int], optional
             filter by year, by default None
         year_lt: Optional[int], optional
             filter by year, by default None
         year_lte: Optional[int], optional
             filter by year, by default None
         production_type: Optional[Union[list[str], Series[str], str]]
             The category of production. This includes different commodities as well as the capacity of feedstock gas into the liquefaction project, by default None
         production_uom: Optional[Union[list[str], Series[str], str]]
             The unit of measure of the production rate for a given commidity or capacity rate of the liquefaction project, by default None
         modified_date: Optional[datetime], optional
             Feedstock record latest modified date, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("economicGroup", economic_group))
        filter_params.append(
            list_to_filter("liquefactionProject", liquefaction_project)
        )
        filter_params.append(list_to_filter("feedstockAsset", feedstock_asset))
        filter_params.append(list_to_filter("supplyMarket", supply_market))
        filter_params.append(list_to_filter("year", year))
        if year_gt is not None:
            filter_params.append(f'year > "{year_gt}"')
        if year_gte is not None:
            filter_params.append(f'year >= "{year_gte}"')
        if year_lt is not None:
            filter_params.append(f'year < "{year_lt}"')
        if year_lte is not None:
            filter_params.append(f'year <= "{year_lte}"')
        filter_params.append(list_to_filter("productionType", production_type))
        filter_params.append(list_to_filter("productionUom", production_uom))
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/analytics/assets-contracts/feedstock",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    @staticmethod
    def _convert_to_df(resp: Response) -> pd.DataFrame:
        j = resp.json()
        df = pd.json_normalize(j["results"])  # type: ignore

        if "modifiedDate" in df.columns:
            df["modifiedDate"] = pd.to_datetime(df["modifiedDate"])  # type: ignore

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])  # type: ignore

        if "month" in df.columns:
            df["month"] = pd.to_datetime(df["month"])  # type: ignore

        if "createdDate" in df.columns:
            df["createdDate"] = pd.to_datetime(df["createdDate"])  # type: ignore

        if "shareholderModifiedDate" in df.columns:
            df["shareholderModifiedDate"] = pd.to_datetime(df["shareholderModifiedDate"])  # type: ignore

        if "shareModifiedDate" in df.columns:
            df["shareModifiedDate"] = pd.to_datetime(df["shareModifiedDate"])  # type: ignore

        if "ownershipStartDate" in df.columns:
            df["ownershipStartDate"] = pd.to_datetime(df["ownershipStartDate"])  # type: ignore

        if "ownershipEndDate" in df.columns:
            df["ownershipEndDate"] = pd.to_datetime(df["ownershipEndDate"])  # type: ignore

        if "announcedStartDate" in df.columns:
            df["announcedStartDate"] = pd.to_datetime(df["announcedStartDate"])  # type: ignore

        if "estimatedStartDate" in df.columns:
            df["estimatedStartDate"] = pd.to_datetime(df["estimatedStartDate"])  # type: ignore

        if "capexDate" in df.columns:
            df["capexDate"] = pd.to_datetime(df["capexDate"])  # type: ignore

        if "offlineDate" in df.columns:
            df["offlineDate"] = pd.to_datetime(df["offlineDate"])  # type: ignore

        if "statusModifiedDate" in df.columns:
            df["statusModifiedDate"] = pd.to_datetime(df["statusModifiedDate"])  # type: ignore

        if "capacityModifiedDate" in df.columns:
            df["capacityModifiedDate"] = pd.to_datetime(df["capacityModifiedDate"])  # type: ignore

        if "announcedStartDateModifiedDate" in df.columns:
            df["announcedStartDateModifiedDate"] = pd.to_datetime(df["announcedStartDateModifiedDate"])  # type: ignore

        if "estimatedStartDateModifiedDate" in df.columns:
            df["estimatedStartDateModifiedDate"] = pd.to_datetime(df["estimatedStartDateModifiedDate"])  # type: ignore

        if "announcedStartDateAtFinalInvestmentDecision" in df.columns:
            df["announcedStartDateAtFinalInvestmentDecision"] = pd.to_datetime(df["announcedStartDateAtFinalInvestmentDecision"])  # type: ignore

        if "latestAnnouncedFinalInvestmentDecisionDate" in df.columns:
            df["latestAnnouncedFinalInvestmentDecisionDate"] = pd.to_datetime(df["latestAnnouncedFinalInvestmentDecisionDate"])  # type: ignore

        if "estimatedFirstCargoDate" in df.columns:
            df["estimatedFirstCargoDate"] = pd.to_datetime(df["estimatedFirstCargoDate"])  # type: ignore

        if "estimatedFinalInvestmentDecisionDate" in df.columns:
            df["estimatedFinalInvestmentDecisionDate"] = pd.to_datetime(df["estimatedFinalInvestmentDecisionDate"])  # type: ignore

        if "originalSigningDate" in df.columns:
            df["originalSigningDate"] = pd.to_datetime(df["originalSigningDate"])  # type: ignore

        if "preliminarySigningDate" in df.columns:
            df["preliminarySigningDate"] = pd.to_datetime(df["preliminarySigningDate"])  # type: ignore

        if "contractPriceAsOfDate" in df.columns:
            df["contractPriceAsOfDate"] = pd.to_datetime(df["contractPriceAsOfDate"])  # type: ignore

        if "buyerModifiedDate" in df.columns:
            df["buyerModifiedDate"] = pd.to_datetime(df["buyerModifiedDate"])  # type: ignore

        if "announcedStartModifiedDate" in df.columns:
            df["announcedStartModifiedDate"] = pd.to_datetime(df["announcedStartModifiedDate"])  # type: ignore

        if "lengthModifiedDate" in df.columns:
            df["lengthModifiedDate"] = pd.to_datetime(df["lengthModifiedDate"])  # type: ignore

        if "publishedVolumeModifiedDate" in df.columns:
            df["publishedVolumeModifiedDate"] = pd.to_datetime(df["publishedVolumeModifiedDate"])  # type: ignore

        if "estimatedBuildoutModifiedDate" in df.columns:
            df["estimatedBuildoutModifiedDate"] = pd.to_datetime(df["estimatedBuildoutModifiedDate"])  # type: ignore

        if "contractStartDate" in df.columns:
            df["contractStartDate"] = pd.to_datetime(df["contractStartDate"])  # type: ignore

        if "startModifiedDate" in df.columns:
            df["startModifiedDate"] = pd.to_datetime(df["startModifiedDate"])  # type: ignore

        if "capacityOwnerModifiedDate" in df.columns:
            df["capacityOwnerModifiedDate"] = pd.to_datetime(df["capacityOwnerModifiedDate"])  # type: ignore

        if "typeModifiedDate" in df.columns:
            df["typeModifiedDate"] = pd.to_datetime(df["typeModifiedDate"])  # type: ignore

        if "announcedStartDateOriginal" in df.columns:
            df["announcedStartDateOriginal"] = pd.to_datetime(df["announcedStartDateOriginal"])  # type: ignore

        if "datePhaseFirstAnnounced" in df.columns:
            df["datePhaseFirstAnnounced"] = pd.to_datetime(df["datePhaseFirstAnnounced"])  # type: ignore

        if "contractDate" in df.columns:
            df["contractDate"] = pd.to_datetime(df["contractDate"])  # type: ignore

        if "deliveryDate" in df.columns:
            df["deliveryDate"] = pd.to_datetime(df["deliveryDate"])  # type: ignore

        if "retiredDate" in df.columns:
            df["retiredDate"] = pd.to_datetime(df["retiredDate"])  # type: ignore

        if "buildoutMonthEstimated" in df.columns:
            df["buildoutMonthEstimated"] = pd.to_datetime(df["buildoutMonthEstimated"])  # type: ignore

        if "createdDateEstimated" in df.columns:
            df["createdDateEstimated"] = pd.to_datetime(df["createdDateEstimated"])  # type: ignore

        if "modifiedDateEstimated" in df.columns:
            df["modifiedDateEstimated"] = pd.to_datetime(df["modifiedDateEstimated"])  # type: ignore

        if "estimatedEndDate" in df.columns:
            df["estimatedEndDate"] = pd.to_datetime(df["estimatedEndDate"])  # type: ignore

        if "originalSigning" in df.columns:
            df["originalSigning"] = pd.to_datetime(df["originalSigning"])  # type: ignore

        if "buildoutMonthAnnounced" in df.columns:
            df["buildoutMonthAnnounced"] = pd.to_datetime(df["buildoutMonthAnnounced"])  # type: ignore

        if "createdDateAnnounced" in df.columns:
            df["createdDateAnnounced"] = pd.to_datetime(df["createdDateAnnounced"])  # type: ignore

        if "modifiedDateAnnounced" in df.columns:
            df["modifiedDateAnnounced"] = pd.to_datetime(df["modifiedDateAnnounced"])  # type: ignore
        return df
