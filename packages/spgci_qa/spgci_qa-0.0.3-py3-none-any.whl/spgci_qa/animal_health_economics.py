from __future__ import annotations
from typing import List, Optional, Union
from requests import Response
from spgci_qa.api_client import get_data
from spgci_qa.utilities import list_to_filter
from pandas import DataFrame, Series
from datetime import date, datetime
import pandas as pd


class Animal_health_economics:
    _endpoint = "api/v1/"
    _reference_endpoint = "reference/v1/"
    _tbl_animal_health_animal_population_endpoint = "/animal-population"
    _tbl_animal_health_livestock_fundamentals_endpoint = "/livestock-fundamentals"
    _tbl_animal_health_industry_data_endpoint = "/industry-data"
    _tbl_animal_health_macroeconomy_endpoint = "/macroeconomy"
    _tbl_animal_health_product_market_data_endpoint = "/product-market-data"
    _tbl_animal_health_economics_company_financials_endpoint = "/company-financials"

    def get_animal_population(
        self,
        *,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        reporting_region: Optional[Union[list[str], Series[str], str]] = None,
        frequency: Optional[Union[list[str], Series[str], str]] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        currency: Optional[Union[list[str], Series[str], str]] = None,
        report_for_date: Optional[date] = None,
        report_for_date_lt: Optional[date] = None,
        report_for_date_lte: Optional[date] = None,
        report_for_date_gt: Optional[date] = None,
        report_for_date_gte: Optional[date] = None,
        historical_edge_date: Optional[date] = None,
        historical_edge_date_lt: Optional[date] = None,
        historical_edge_date_lte: Optional[date] = None,
        historical_edge_date_gt: Optional[date] = None,
        historical_edge_date_gte: Optional[date] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        is_active: Optional[Union[list[str], Series[str], str]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        API provides forecast data

        Parameters
        ----------

         commodity: Optional[Union[list[str], Series[str], str]]
             Commodity Name - The name of basic good, raw material, or primary animal health product that can be bought, sold and traded., by default None
         reporting_region: Optional[Union[list[str], Series[str], str]]
             Reporting Region Name - The geographic region for which the report or model output is reported., by default None
         frequency: Optional[Union[list[str], Series[str], str]]
             Dataset Frequency - The indicator of how often the data is refreshed or collected., by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Commodity Unit of Measure - The unit or units in which the value of the commodity is measured., by default None
         currency: Optional[Union[list[str], Series[str], str]]
             Currency, by default None
         report_for_date: Optional[date], optional
             Report For Date - The date for which the record applies within the data table, this can be a historical or forecast date., by default None
         report_for_date_gt: Optional[date], optional
             filter by '' report_for_date > x '', by default None
         report_for_date_gte: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lt: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lte: Optional[date], optional
             filter by report_for_date, by default None
         historical_edge_date: Optional[date], optional
             Historical Edge Date - The date and time when a particular record was last updated or modified in hostory, by default None
         historical_edge_date_gt: Optional[date], optional
             filter by '' historical_edge_date > x '', by default None
         historical_edge_date_gte: Optional[date], optional
             filter by historical_edge_date, by default None
         historical_edge_date_lt: Optional[date], optional
             filter by historical_edge_date, by default None
         historical_edge_date_lte: Optional[date], optional
             filter by historical_edge_date, by default None
         modified_date: Optional[datetime], optional
             Last Modified Date - The date and time when a particular record was last updated or modified., by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             An indicator if the data is active., by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("reportingRegion", reporting_region))
        filter_params.append(list_to_filter("frequency", frequency))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("currency", currency))
        filter_params.append(list_to_filter("reportForDate", report_for_date))
        if report_for_date_gt is not None:
            filter_params.append(f'reportForDate > "{report_for_date_gt}"')
        if report_for_date_gte is not None:
            filter_params.append(f'reportForDate >= "{report_for_date_gte}"')
        if report_for_date_lt is not None:
            filter_params.append(f'reportForDate < "{report_for_date_lt}"')
        if report_for_date_lte is not None:
            filter_params.append(f'reportForDate <= "{report_for_date_lte}"')
        filter_params.append(list_to_filter("historicalEdgeDate", historical_edge_date))
        if historical_edge_date_gt is not None:
            filter_params.append(f'historicalEdgeDate > "{historical_edge_date_gt}"')
        if historical_edge_date_gte is not None:
            filter_params.append(f'historicalEdgeDate >= "{historical_edge_date_gte}"')
        if historical_edge_date_lt is not None:
            filter_params.append(f'historicalEdgeDate < "{historical_edge_date_lt}"')
        if historical_edge_date_lte is not None:
            filter_params.append(f'historicalEdgeDate <= "{historical_edge_date_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')
        filter_params.append(list_to_filter("isActive", is_active))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/animal-health/v1/animal-population",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_livestock_fundamentals(
        self,
        *,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        reporting_region: Optional[Union[list[str], Series[str], str]] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        frequency: Optional[Union[list[str], Series[str], str]] = None,
        report_for_date: Optional[date] = None,
        report_for_date_lt: Optional[date] = None,
        report_for_date_lte: Optional[date] = None,
        report_for_date_gt: Optional[date] = None,
        report_for_date_gte: Optional[date] = None,
        historical_edge_date: Optional[date] = None,
        historical_edge_date_lt: Optional[date] = None,
        historical_edge_date_lte: Optional[date] = None,
        historical_edge_date_gt: Optional[date] = None,
        historical_edge_date_gte: Optional[date] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        is_active: Optional[Union[list[str], Series[str], str]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        API provides forecast data

        Parameters
        ----------

         commodity: Optional[Union[list[str], Series[str], str]]
             Commodity Name - The name of basic good, raw material, or primary animal health product that can be bought, sold and traded., by default None
         concept: Optional[Union[list[str], Series[str], str]]
             Subject Area Type - The type of category or domain of information describing the subject of the data being reported., by default None
         reporting_region: Optional[Union[list[str], Series[str], str]]
             Reporting Region Name - The geographic region for which the report or model output is reported., by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Commodity Unit of Measure - The unit or units in which the value of the commodity is measured., by default None
         frequency: Optional[Union[list[str], Series[str], str]]
             Dataset Frequency - The indicator of how often the data is refreshed or collected., by default None
         report_for_date: Optional[date], optional
             Report For Date - The date for which the record applies within the data table, this can be a historical or forecast date., by default None
         report_for_date_gt: Optional[date], optional
             filter by '' report_for_date > x '', by default None
         report_for_date_gte: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lt: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lte: Optional[date], optional
             filter by report_for_date, by default None
         historical_edge_date: Optional[date], optional
             Historical Edge Date - The date and time when a particular record was last updated or modified in hostory, by default None
         historical_edge_date_gt: Optional[date], optional
             filter by '' historical_edge_date > x '', by default None
         historical_edge_date_gte: Optional[date], optional
             filter by historical_edge_date, by default None
         historical_edge_date_lt: Optional[date], optional
             filter by historical_edge_date, by default None
         historical_edge_date_lte: Optional[date], optional
             filter by historical_edge_date, by default None
         modified_date: Optional[datetime], optional
             Last Modified Date - The date and time when a particular record was last updated or modified., by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             An indicator if the data is active., by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("reportingRegion", reporting_region))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("frequency", frequency))
        filter_params.append(list_to_filter("reportForDate", report_for_date))
        if report_for_date_gt is not None:
            filter_params.append(f'reportForDate > "{report_for_date_gt}"')
        if report_for_date_gte is not None:
            filter_params.append(f'reportForDate >= "{report_for_date_gte}"')
        if report_for_date_lt is not None:
            filter_params.append(f'reportForDate < "{report_for_date_lt}"')
        if report_for_date_lte is not None:
            filter_params.append(f'reportForDate <= "{report_for_date_lte}"')
        filter_params.append(list_to_filter("historicalEdgeDate", historical_edge_date))
        if historical_edge_date_gt is not None:
            filter_params.append(f'historicalEdgeDate > "{historical_edge_date_gt}"')
        if historical_edge_date_gte is not None:
            filter_params.append(f'historicalEdgeDate >= "{historical_edge_date_gte}"')
        if historical_edge_date_lt is not None:
            filter_params.append(f'historicalEdgeDate < "{historical_edge_date_lt}"')
        if historical_edge_date_lte is not None:
            filter_params.append(f'historicalEdgeDate <= "{historical_edge_date_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')
        filter_params.append(list_to_filter("isActive", is_active))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/animal-health/v1/livestock-fundamentals",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_industry_data(
        self,
        *,
        commodity_group: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        reporting_region: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        frequency: Optional[Union[list[str], Series[str], str]] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        report_for_date: Optional[date] = None,
        report_for_date_lt: Optional[date] = None,
        report_for_date_lte: Optional[date] = None,
        report_for_date_gt: Optional[date] = None,
        report_for_date_gte: Optional[date] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        is_active: Optional[Union[list[str], Series[str], str]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        API provides forecast data

        Parameters
        ----------

         commodity_group: Optional[Union[list[str], Series[str], str]]
             Commodity Group Name - The name of basic good, raw material, or primary animal health product that can be bought, sold and traded., by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             Commodity Name - The name of basic good, raw material, or primary animal health product that can be bought, sold and traded., by default None
         reporting_region: Optional[Union[list[str], Series[str], str]]
             Reporting Region Name - The geographic region for which the report or model output is reported., by default None
         concept: Optional[Union[list[str], Series[str], str]]
             Subject Area Type - The type of category or domain of information describing the subject of the data being reported., by default None
         frequency: Optional[Union[list[str], Series[str], str]]
             Dataset Frequency - The indicator of how often the data is refreshed or collected., by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Commodity Unit of Measure - The unit or units in which the value of the commodity is measured., by default None
         report_for_date: Optional[date], optional
             Report For Date - The date for which the record applies within the data table, this can be a historical or forecast date., by default None
         report_for_date_gt: Optional[date], optional
             filter by '' report_for_date > x '', by default None
         report_for_date_gte: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lt: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lte: Optional[date], optional
             filter by report_for_date, by default None
         modified_date: Optional[datetime], optional
             Last Modified Date - The date and time when a particular record was last updated or modified., by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             An indicator if the data is active., by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("commodityGroup", commodity_group))
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("reportingRegion", reporting_region))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("frequency", frequency))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("reportForDate", report_for_date))
        if report_for_date_gt is not None:
            filter_params.append(f'reportForDate > "{report_for_date_gt}"')
        if report_for_date_gte is not None:
            filter_params.append(f'reportForDate >= "{report_for_date_gte}"')
        if report_for_date_lt is not None:
            filter_params.append(f'reportForDate < "{report_for_date_lt}"')
        if report_for_date_lte is not None:
            filter_params.append(f'reportForDate <= "{report_for_date_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')
        filter_params.append(list_to_filter("isActive", is_active))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/animal-health/v1/industry-data",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_macroeconomy(
        self,
        *,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        reporting_region: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        frequency: Optional[Union[list[str], Series[str], str]] = None,
        report_for_date: Optional[date] = None,
        report_for_date_lt: Optional[date] = None,
        report_for_date_lte: Optional[date] = None,
        report_for_date_gt: Optional[date] = None,
        report_for_date_gte: Optional[date] = None,
        historical_edge_date: Optional[date] = None,
        historical_edge_date_lt: Optional[date] = None,
        historical_edge_date_lte: Optional[date] = None,
        historical_edge_date_gt: Optional[date] = None,
        historical_edge_date_gte: Optional[date] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        is_active: Optional[Union[list[str], Series[str], str]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        API provides forecast data

        Parameters
        ----------

         commodity: Optional[Union[list[str], Series[str], str]]
             Commodity Name - The name of basic good, raw material, or primary animal health product that can be bought, sold and traded., by default None
         reporting_region: Optional[Union[list[str], Series[str], str]]
             Reporting Region Name - The geographic region for which the report or model output is reported., by default None
         concept: Optional[Union[list[str], Series[str], str]]
             Subject Area Type - The type of category or domain of information describing the subject of the data being reported., by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Commodity Unit of Measure - The unit or units in which the value of the commodity is measured., by default None
         frequency: Optional[Union[list[str], Series[str], str]]
             Dataset Frequency - The indicator of how often the data is refreshed or collected., by default None
         report_for_date: Optional[date], optional
             Report For Date - The date for which the record applies within the data table, this can be a historical or forecast date., by default None
         report_for_date_gt: Optional[date], optional
             filter by '' report_for_date > x '', by default None
         report_for_date_gte: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lt: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lte: Optional[date], optional
             filter by report_for_date, by default None
         historical_edge_date: Optional[date], optional
             Historical Edge Date - The date and time when a particular record was last updated or modified in hostory, by default None
         historical_edge_date_gt: Optional[date], optional
             filter by '' historical_edge_date > x '', by default None
         historical_edge_date_gte: Optional[date], optional
             filter by historical_edge_date, by default None
         historical_edge_date_lt: Optional[date], optional
             filter by historical_edge_date, by default None
         historical_edge_date_lte: Optional[date], optional
             filter by historical_edge_date, by default None
         modified_date: Optional[datetime], optional
             Last Modified Date - The date and time when a particular record was last updated or modified., by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             An indicator if the data is active., by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("reportingRegion", reporting_region))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("frequency", frequency))
        filter_params.append(list_to_filter("reportForDate", report_for_date))
        if report_for_date_gt is not None:
            filter_params.append(f'reportForDate > "{report_for_date_gt}"')
        if report_for_date_gte is not None:
            filter_params.append(f'reportForDate >= "{report_for_date_gte}"')
        if report_for_date_lt is not None:
            filter_params.append(f'reportForDate < "{report_for_date_lt}"')
        if report_for_date_lte is not None:
            filter_params.append(f'reportForDate <= "{report_for_date_lte}"')
        filter_params.append(list_to_filter("historicalEdgeDate", historical_edge_date))
        if historical_edge_date_gt is not None:
            filter_params.append(f'historicalEdgeDate > "{historical_edge_date_gt}"')
        if historical_edge_date_gte is not None:
            filter_params.append(f'historicalEdgeDate >= "{historical_edge_date_gte}"')
        if historical_edge_date_lt is not None:
            filter_params.append(f'historicalEdgeDate < "{historical_edge_date_lt}"')
        if historical_edge_date_lte is not None:
            filter_params.append(f'historicalEdgeDate <= "{historical_edge_date_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')
        filter_params.append(list_to_filter("isActive", is_active))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/animal-health/v1/macroeconomy",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_product_market_data(
        self,
        *,
        commodity_group: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        sub_commodity: Optional[Union[list[str], Series[str], str]] = None,
        region_categorization: Optional[Union[list[str], Series[str], str]] = None,
        sub_region_categorization: Optional[Union[list[str], Series[str], str]] = None,
        reporting_region: Optional[Union[list[str], Series[str], str]] = None,
        medical_condition: Optional[Union[list[str], Series[str], str]] = None,
        medical_treatment_group: Optional[Union[list[str], Series[str], str]] = None,
        medical_treatment: Optional[Union[list[str], Series[str], str]] = None,
        medical_sub_treatment: Optional[Union[list[str], Series[str], str]] = None,
        medication_type: Optional[Union[list[str], Series[str], str]] = None,
        frequency: Optional[Union[list[str], Series[str], str]] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        report_for_date: Optional[date] = None,
        report_for_date_lt: Optional[date] = None,
        report_for_date_lte: Optional[date] = None,
        report_for_date_gt: Optional[date] = None,
        report_for_date_gte: Optional[date] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        is_active: Optional[Union[list[str], Series[str], str]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        API provides forecast data

        Parameters
        ----------

         commodity_group: Optional[Union[list[str], Series[str], str]]
             Commodity Name - The name of basic good, raw material, or primary animal health product that can be bought, sold and traded., by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             Commodity Name - The name of basic good, raw material, or primary animal health product that can be bought, sold and traded., by default None
         sub_commodity: Optional[Union[list[str], Series[str], str]]
             Commodity Name - The name of basic good, raw material, or primary animal health product that can be bought, sold and traded., by default None
         region_categorization: Optional[Union[list[str], Series[str], str]]
             Reporting Region Name - The geographic region for which the report or model output is reported., by default None
         sub_region_categorization: Optional[Union[list[str], Series[str], str]]
             Reporting Region Name - The geographic region for which the report or model output is reported., by default None
         reporting_region: Optional[Union[list[str], Series[str], str]]
             Reporting Region Name - The geographic region for which the report or model output is reported., by default None
         medical_condition: Optional[Union[list[str], Series[str], str]]
             Subject Area Type - The type of category or domain of information describing the subject of the data being reported., by default None
         medical_treatment_group: Optional[Union[list[str], Series[str], str]]
             Subject Area Type - The type of category or domain of information describing the subject of the data being reported., by default None
         medical_treatment: Optional[Union[list[str], Series[str], str]]
             Subject Area Type - The type of category or domain of information describing the subject of the data being reported., by default None
         medical_sub_treatment: Optional[Union[list[str], Series[str], str]]
             Subject Area Type - The type of category or domain of information describing the subject of the data being reported., by default None
         medication_type: Optional[Union[list[str], Series[str], str]]
             Subject Area Type - The type of category or domain of information describing the subject of the data being reported., by default None
         frequency: Optional[Union[list[str], Series[str], str]]
             Dataset Frequency - The indicator of how often the data is refreshed or collected., by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Commodity Unit of Measure - The unit or units in which the value of the commodity is measured., by default None
         report_for_date: Optional[date], optional
             Report For Date - The date for which the record applies within the data table, this can be a historical or forecast date., by default None
         report_for_date_gt: Optional[date], optional
             filter by '' report_for_date > x '', by default None
         report_for_date_gte: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lt: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lte: Optional[date], optional
             filter by report_for_date, by default None
         modified_date: Optional[datetime], optional
             Last Modified Date - The date and time when a particular record was last updated or modified., by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             An indicator if the data is active., by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("commodityGroup", commodity_group))
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("subCommodity", sub_commodity))
        filter_params.append(
            list_to_filter("regionCategorization", region_categorization)
        )
        filter_params.append(
            list_to_filter("subRegionCategorization", sub_region_categorization)
        )
        filter_params.append(list_to_filter("reportingRegion", reporting_region))
        filter_params.append(list_to_filter("medicalCondition", medical_condition))
        filter_params.append(
            list_to_filter("medicalTreatmentGroup", medical_treatment_group)
        )
        filter_params.append(list_to_filter("medicalTreatment", medical_treatment))
        filter_params.append(
            list_to_filter("medicalSubTreatment", medical_sub_treatment)
        )
        filter_params.append(list_to_filter("medicationType", medication_type))
        filter_params.append(list_to_filter("frequency", frequency))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("reportForDate", report_for_date))
        if report_for_date_gt is not None:
            filter_params.append(f'reportForDate > "{report_for_date_gt}"')
        if report_for_date_gte is not None:
            filter_params.append(f'reportForDate >= "{report_for_date_gte}"')
        if report_for_date_lt is not None:
            filter_params.append(f'reportForDate < "{report_for_date_lt}"')
        if report_for_date_lte is not None:
            filter_params.append(f'reportForDate <= "{report_for_date_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')
        filter_params.append(list_to_filter("isActive", is_active))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/animal-health/v1/product-market-data",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_company_financials(
        self,
        *,
        company: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        category: Optional[Union[list[str], Series[str], str]] = None,
        sub_category: Optional[Union[list[str], Series[str], str]] = None,
        report_for_year: Optional[Union[list[int], Series[int], int]] = None,
        report_for_date: Optional[date] = None,
        report_for_date_lt: Optional[date] = None,
        report_for_date_lte: Optional[date] = None,
        report_for_date_gt: Optional[date] = None,
        report_for_date_gte: Optional[date] = None,
        local_currency_unit: Optional[Union[list[str], Series[str], str]] = None,
        local_currency_sales: Optional[str] = None,
        local_currency_sales_lt: Optional[str] = None,
        local_currency_sales_lte: Optional[str] = None,
        local_currency_sales_gt: Optional[str] = None,
        local_currency_sales_gte: Optional[str] = None,
        local_currency_growth_rate_percentage: Optional[str] = None,
        local_currency_growth_rate_percentage_lt: Optional[str] = None,
        local_currency_growth_rate_percentage_lte: Optional[str] = None,
        local_currency_growth_rate_percentage_gt: Optional[str] = None,
        local_currency_growth_rate_percentage_gte: Optional[str] = None,
        usd_currency_unit: Optional[Union[list[str], Series[str], str]] = None,
        usd_currency_sales: Optional[str] = None,
        usd_currency_sales_lt: Optional[str] = None,
        usd_currency_sales_lte: Optional[str] = None,
        usd_currency_sales_gt: Optional[str] = None,
        usd_currency_sales_gte: Optional[str] = None,
        usd_growth_rate_percentage: Optional[str] = None,
        usd_growth_rate_percentage_lt: Optional[str] = None,
        usd_growth_rate_percentage_lte: Optional[str] = None,
        usd_growth_rate_percentage_gt: Optional[str] = None,
        usd_growth_rate_percentage_gte: Optional[str] = None,
        average_annual_conversion_rate: Optional[str] = None,
        average_annual_conversion_rate_lt: Optional[str] = None,
        average_annual_conversion_rate_lte: Optional[str] = None,
        average_annual_conversion_rate_gt: Optional[str] = None,
        average_annual_conversion_rate_gte: Optional[str] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        is_active: Optional[Union[list[str], Series[str], str]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        API provides forecast data

        Parameters
        ----------

         company: Optional[Union[list[str], Series[str], str]]
             Identify the connecting business or company name., by default None
         concept: Optional[Union[list[str], Series[str], str]]
             Subject Area Type - The type of category or domain of information describing the subject of the data being reported., by default None
         category: Optional[Union[list[str], Series[str], str]]
             Commodity Name - The name of basic good, raw material, or primary animal health product that can be bought, sold and traded., by default None
         sub_category: Optional[Union[list[str], Series[str], str]]
             Commodity Name - The name of basic good, raw material, or primary animal health product that can be bought, sold and traded., by default None
         report_for_year: Optional[Union[list[int], Series[int], int]]
             The year for which the record applies within the data table, this can be a historical or forecast date., by default None
         report_for_date: Optional[date], optional
             Report For Date - The date for which the record applies within the data table, this can be a historical or forecast date., by default None
         report_for_date_gt: Optional[date], optional
             filter by '' report_for_date > x '', by default None
         report_for_date_gte: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lt: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lte: Optional[date], optional
             filter by report_for_date, by default None
         local_currency_unit: Optional[Union[list[str], Series[str], str]]
             Local Currency Unit., by default None
         local_currency_sales: Optional[str], optional
             Sales in Local Currency., by default None
         local_currency_sales_gt: Optional[str], optional
             filter by '' local_currency_sales > x '', by default None
         local_currency_sales_gte: Optional[str], optional
             filter by local_currency_sales, by default None
         local_currency_sales_lt: Optional[str], optional
             filter by local_currency_sales, by default None
         local_currency_sales_lte: Optional[str], optional
             filter by local_currency_sales, by default None
         local_currency_growth_rate_percentage: Optional[str], optional
             Subject Area Type - The type of category or domain of information describing the subject of the data being reported., by default None
         local_currency_growth_rate_percentage_gt: Optional[str], optional
             filter by '' local_currency_growth_rate_percentage > x '', by default None
         local_currency_growth_rate_percentage_gte: Optional[str], optional
             filter by local_currency_growth_rate_percentage, by default None
         local_currency_growth_rate_percentage_lt: Optional[str], optional
             filter by local_currency_growth_rate_percentage, by default None
         local_currency_growth_rate_percentage_lte: Optional[str], optional
             filter by local_currency_growth_rate_percentage, by default None
         usd_currency_unit: Optional[Union[list[str], Series[str], str]]
             USD Currency Unit., by default None
         usd_currency_sales: Optional[str], optional
             Sales in Local Currency., by default None
         usd_currency_sales_gt: Optional[str], optional
             filter by '' usd_currency_sales > x '', by default None
         usd_currency_sales_gte: Optional[str], optional
             filter by usd_currency_sales, by default None
         usd_currency_sales_lt: Optional[str], optional
             filter by usd_currency_sales, by default None
         usd_currency_sales_lte: Optional[str], optional
             filter by usd_currency_sales, by default None
         usd_growth_rate_percentage: Optional[str], optional
             Subject Area Type - The type of category or domain of information describing the subject of the data being reported., by default None
         usd_growth_rate_percentage_gt: Optional[str], optional
             filter by '' usd_growth_rate_percentage > x '', by default None
         usd_growth_rate_percentage_gte: Optional[str], optional
             filter by usd_growth_rate_percentage, by default None
         usd_growth_rate_percentage_lt: Optional[str], optional
             filter by usd_growth_rate_percentage, by default None
         usd_growth_rate_percentage_lte: Optional[str], optional
             filter by usd_growth_rate_percentage, by default None
         average_annual_conversion_rate: Optional[str], optional
             Subject Area Type - The type of category or domain of information describing the subject of the data being reported., by default None
         average_annual_conversion_rate_gt: Optional[str], optional
             filter by '' average_annual_conversion_rate > x '', by default None
         average_annual_conversion_rate_gte: Optional[str], optional
             filter by average_annual_conversion_rate, by default None
         average_annual_conversion_rate_lt: Optional[str], optional
             filter by average_annual_conversion_rate, by default None
         average_annual_conversion_rate_lte: Optional[str], optional
             filter by average_annual_conversion_rate, by default None
         modified_date: Optional[datetime], optional
             Last Modified Date - The date and time when a particular record was last updated or modified., by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             An indicator if the data is active., by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("company", company))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("category", category))
        filter_params.append(list_to_filter("subCategory", sub_category))
        filter_params.append(list_to_filter("reportForYear", report_for_year))
        filter_params.append(list_to_filter("reportForDate", report_for_date))
        if report_for_date_gt is not None:
            filter_params.append(f'reportForDate > "{report_for_date_gt}"')
        if report_for_date_gte is not None:
            filter_params.append(f'reportForDate >= "{report_for_date_gte}"')
        if report_for_date_lt is not None:
            filter_params.append(f'reportForDate < "{report_for_date_lt}"')
        if report_for_date_lte is not None:
            filter_params.append(f'reportForDate <= "{report_for_date_lte}"')
        filter_params.append(list_to_filter("localCurrencyUnit", local_currency_unit))
        filter_params.append(list_to_filter("localCurrencySales", local_currency_sales))
        if local_currency_sales_gt is not None:
            filter_params.append(f'localCurrencySales > "{local_currency_sales_gt}"')
        if local_currency_sales_gte is not None:
            filter_params.append(f'localCurrencySales >= "{local_currency_sales_gte}"')
        if local_currency_sales_lt is not None:
            filter_params.append(f'localCurrencySales < "{local_currency_sales_lt}"')
        if local_currency_sales_lte is not None:
            filter_params.append(f'localCurrencySales <= "{local_currency_sales_lte}"')
        filter_params.append(
            list_to_filter(
                "localCurrencyGrowthRatePercentage",
                local_currency_growth_rate_percentage,
            )
        )
        if local_currency_growth_rate_percentage_gt is not None:
            filter_params.append(
                f'localCurrencyGrowthRatePercentage > "{local_currency_growth_rate_percentage_gt}"'
            )
        if local_currency_growth_rate_percentage_gte is not None:
            filter_params.append(
                f'localCurrencyGrowthRatePercentage >= "{local_currency_growth_rate_percentage_gte}"'
            )
        if local_currency_growth_rate_percentage_lt is not None:
            filter_params.append(
                f'localCurrencyGrowthRatePercentage < "{local_currency_growth_rate_percentage_lt}"'
            )
        if local_currency_growth_rate_percentage_lte is not None:
            filter_params.append(
                f'localCurrencyGrowthRatePercentage <= "{local_currency_growth_rate_percentage_lte}"'
            )
        filter_params.append(list_to_filter("usdCurrencyUnit", usd_currency_unit))
        filter_params.append(list_to_filter("usdCurrencySales", usd_currency_sales))
        if usd_currency_sales_gt is not None:
            filter_params.append(f'usdCurrencySales > "{usd_currency_sales_gt}"')
        if usd_currency_sales_gte is not None:
            filter_params.append(f'usdCurrencySales >= "{usd_currency_sales_gte}"')
        if usd_currency_sales_lt is not None:
            filter_params.append(f'usdCurrencySales < "{usd_currency_sales_lt}"')
        if usd_currency_sales_lte is not None:
            filter_params.append(f'usdCurrencySales <= "{usd_currency_sales_lte}"')
        filter_params.append(
            list_to_filter("usdGrowthRatePercentage", usd_growth_rate_percentage)
        )
        if usd_growth_rate_percentage_gt is not None:
            filter_params.append(
                f'usdGrowthRatePercentage > "{usd_growth_rate_percentage_gt}"'
            )
        if usd_growth_rate_percentage_gte is not None:
            filter_params.append(
                f'usdGrowthRatePercentage >= "{usd_growth_rate_percentage_gte}"'
            )
        if usd_growth_rate_percentage_lt is not None:
            filter_params.append(
                f'usdGrowthRatePercentage < "{usd_growth_rate_percentage_lt}"'
            )
        if usd_growth_rate_percentage_lte is not None:
            filter_params.append(
                f'usdGrowthRatePercentage <= "{usd_growth_rate_percentage_lte}"'
            )
        filter_params.append(
            list_to_filter(
                "averageAnnualConversionRate", average_annual_conversion_rate
            )
        )
        if average_annual_conversion_rate_gt is not None:
            filter_params.append(
                f'averageAnnualConversionRate > "{average_annual_conversion_rate_gt}"'
            )
        if average_annual_conversion_rate_gte is not None:
            filter_params.append(
                f'averageAnnualConversionRate >= "{average_annual_conversion_rate_gte}"'
            )
        if average_annual_conversion_rate_lt is not None:
            filter_params.append(
                f'averageAnnualConversionRate < "{average_annual_conversion_rate_lt}"'
            )
        if average_annual_conversion_rate_lte is not None:
            filter_params.append(
                f'averageAnnualConversionRate <= "{average_annual_conversion_rate_lte}"'
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
        filter_params.append(list_to_filter("isActive", is_active))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/animal-health/v1/company-financials",
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

        if "reportForDate" in df.columns:
            df["reportForDate"] = pd.to_datetime(df["reportForDate"])  # type: ignore

        if "historicalEdgeDate" in df.columns:
            df["historicalEdgeDate"] = pd.to_datetime(df["historicalEdgeDate"])  # type: ignore

        if "modifiedDate" in df.columns:
            df["modifiedDate"] = pd.to_datetime(df["modifiedDate"])  # type: ignore
        return df
