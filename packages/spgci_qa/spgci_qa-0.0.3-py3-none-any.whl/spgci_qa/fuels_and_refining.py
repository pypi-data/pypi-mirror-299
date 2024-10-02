from __future__ import annotations
from typing import List, Optional, Union
from requests import Response
from spgci_qa.api_client import get_data
from spgci_qa.utilities import list_to_filter
from pandas import DataFrame, Series
from datetime import date, datetime
import pandas as pd


class Fuels_and_refining:
    _endpoint = "api/v1/"
    _reference_endpoint = "reference/v1/"
    _tbl_arbflow_refined_product_arbitrage_endpoint = "/arbflow/arbitrage"
    _tbl_refinery_production_endpoint = "/refinery-production"
    _tbl_refinery_utilization_rate_endpoint = "/refinery-utilization-rate"
    _tbl_refinery_runs_endpoint = "/refinery-runs"
    _tbl_oil_inventory_endpoint = "/oil-inventory"

    def get_arbflow_arbitrage(
        self,
        *,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        report_for_date: Optional[date] = None,
        report_for_date_lt: Optional[date] = None,
        report_for_date_lte: Optional[date] = None,
        report_for_date_gt: Optional[date] = None,
        report_for_date_gte: Optional[date] = None,
        from_region: Optional[Union[list[str], Series[str], str]] = None,
        to_region: Optional[Union[list[str], Series[str], str]] = None,
        currency: Optional[Union[list[str], Series[str], str]] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        frequency: Optional[Union[list[str], Series[str], str]] = None,
        vintage_date: Optional[date] = None,
        vintage_date_lt: Optional[date] = None,
        vintage_date_lte: Optional[date] = None,
        vintage_date_gt: Optional[date] = None,
        vintage_date_gte: Optional[date] = None,
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
             Commodity Name - The name of basic good, raw material, or primary OMD product that can be bought, sold and traded., by default None
         concept: Optional[Union[list[str], Series[str], str]]
             Subject Area Type - The type of category or domain of information describing the subject of the data being reported., by default None
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
         from_region: Optional[Union[list[str], Series[str], str]]
             From Region Name - The geographic region for which the report or model output is reported., by default None
         to_region: Optional[Union[list[str], Series[str], str]]
             To Region Name - The geographic region for which the report or model output is reported., by default None
         currency: Optional[Union[list[str], Series[str], str]]
             Currency, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Commodity Unit of Measure - The unit or units in which the value of the commodity is measured., by default None
         frequency: Optional[Union[list[str], Series[str], str]]
             Dataset Frequency - The indicator of how often the data is refreshed or collected., by default None
         vintage_date: Optional[date], optional
             Vintage Date - The date for which the record applies within the data set., by default None
         vintage_date_gt: Optional[date], optional
             filter by '' vintage_date > x '', by default None
         vintage_date_gte: Optional[date], optional
             filter by vintage_date, by default None
         vintage_date_lt: Optional[date], optional
             filter by vintage_date, by default None
         vintage_date_lte: Optional[date], optional
             filter by vintage_date, by default None
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
        filter_params.append(list_to_filter("reportForDate", report_for_date))
        if report_for_date_gt is not None:
            filter_params.append(f'reportForDate > "{report_for_date_gt}"')
        if report_for_date_gte is not None:
            filter_params.append(f'reportForDate >= "{report_for_date_gte}"')
        if report_for_date_lt is not None:
            filter_params.append(f'reportForDate < "{report_for_date_lt}"')
        if report_for_date_lte is not None:
            filter_params.append(f'reportForDate <= "{report_for_date_lte}"')
        filter_params.append(list_to_filter("fromRegion", from_region))
        filter_params.append(list_to_filter("toRegion", to_region))
        filter_params.append(list_to_filter("currency", currency))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("frequency", frequency))
        filter_params.append(list_to_filter("vintageDate", vintage_date))
        if vintage_date_gt is not None:
            filter_params.append(f'vintageDate > "{vintage_date_gt}"')
        if vintage_date_gte is not None:
            filter_params.append(f'vintageDate >= "{vintage_date_gte}"')
        if vintage_date_lt is not None:
            filter_params.append(f'vintageDate < "{vintage_date_lt}"')
        if vintage_date_lte is not None:
            filter_params.append(f'vintageDate <= "{vintage_date_lte}"')
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
            path=f"/analytics/fuels-refining/v1/arbflow/arbitrage",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_refinery_production(
        self,
        *,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        outlook_horizon: Optional[Union[list[str], Series[str], str]] = None,
        zone: Optional[Union[list[str], Series[str], str]] = None,
        state: Optional[Union[list[str], Series[str], str]] = None,
        from_region: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        country: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        frequency: Optional[Union[list[str], Series[str], str]] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        vintage_date: Optional[date] = None,
        vintage_date_lt: Optional[date] = None,
        vintage_date_lte: Optional[date] = None,
        vintage_date_gt: Optional[date] = None,
        vintage_date_gte: Optional[date] = None,
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
        Refinery oil production forecast.

        Parameters
        ----------

         commodity: Optional[Union[list[str], Series[str], str]]
             The name of an economic good, usually a resource, being traded in the derivatives markets., by default None
         outlook_horizon: Optional[Union[list[str], Series[str], str]]
             The outlook type specifies the time frame for the forecast., by default None
         zone: Optional[Union[list[str], Series[str], str]]
             , by default None
         state: Optional[Union[list[str], Series[str], str]]
             The name of the state or province where the refinery is located., by default None
         from_region: Optional[Union[list[str], Series[str], str]]
             The name of an area, country division, or the world with characteristics defined by either physical boundaries or human-defined borders., by default None
         region: Optional[Union[list[str], Series[str], str]]
             The name of an area, country division, or the world with characteristics defined by either physical boundaries or human-defined borders., by default None
         country: Optional[Union[list[str], Series[str], str]]
             The name of the country where the refinery is located., by default None
         concept: Optional[Union[list[str], Series[str], str]]
             The logical grouping or classification of related data elements and entities that are relevant to a particular subject or topic., by default None
         frequency: Optional[Union[list[str], Series[str], str]]
             The indicator of how often the data is refreshed or collected., by default None
         uom: Optional[Union[list[str], Series[str], str]]
             A standardized system used to measure quantity, length, weight, time, value, speed, weather conditions, power, and others., by default None
         vintage_date: Optional[date], optional
             The date when the forecast is issued., by default None
         vintage_date_gt: Optional[date], optional
             filter by '' vintage_date > x '', by default None
         vintage_date_gte: Optional[date], optional
             filter by vintage_date, by default None
         vintage_date_lt: Optional[date], optional
             filter by vintage_date, by default None
         vintage_date_lte: Optional[date], optional
             filter by vintage_date, by default None
         report_for_date: Optional[date], optional
             The date for which the record applies within the data table, this can be a historical or forecast date., by default None
         report_for_date_gt: Optional[date], optional
             filter by '' report_for_date > x '', by default None
         report_for_date_gte: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lt: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lte: Optional[date], optional
             filter by report_for_date, by default None
         historical_edge_date: Optional[date], optional
             The month and year when historical data ends and the refinery production forecast begins., by default None
         historical_edge_date_gt: Optional[date], optional
             filter by '' historical_edge_date > x '', by default None
         historical_edge_date_gte: Optional[date], optional
             filter by historical_edge_date, by default None
         historical_edge_date_lt: Optional[date], optional
             filter by historical_edge_date, by default None
         historical_edge_date_lte: Optional[date], optional
             filter by historical_edge_date, by default None
         modified_date: Optional[datetime], optional
             The date and time when a particular record was last updated or modified., by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             For point in time data, indicator if this record is currently an active record., by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("outlookHorizon", outlook_horizon))
        filter_params.append(list_to_filter("zone", zone))
        filter_params.append(list_to_filter("state", state))
        filter_params.append(list_to_filter("fromRegion", from_region))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("frequency", frequency))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("vintageDate", vintage_date))
        if vintage_date_gt is not None:
            filter_params.append(f'vintageDate > "{vintage_date_gt}"')
        if vintage_date_gte is not None:
            filter_params.append(f'vintageDate >= "{vintage_date_gte}"')
        if vintage_date_lt is not None:
            filter_params.append(f'vintageDate < "{vintage_date_lt}"')
        if vintage_date_lte is not None:
            filter_params.append(f'vintageDate <= "{vintage_date_lte}"')
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
            path=f"/analytics/fuels-refining/v1/refinery-production",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_refinery_utilization_rate(
        self,
        *,
        outlook_horizon: Optional[Union[list[str], Series[str], str]] = None,
        zone: Optional[Union[list[str], Series[str], str]] = None,
        state: Optional[Union[list[str], Series[str], str]] = None,
        from_region: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        country: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        frequency: Optional[Union[list[str], Series[str], str]] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        vintage_date: Optional[date] = None,
        vintage_date_lt: Optional[date] = None,
        vintage_date_lte: Optional[date] = None,
        vintage_date_gt: Optional[date] = None,
        vintage_date_gte: Optional[date] = None,
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
        Refinery unit oil capacity processing.

        Parameters
        ----------

         outlook_horizon: Optional[Union[list[str], Series[str], str]]
             The outlook type specifies the time frame for the forecast., by default None
         zone: Optional[Union[list[str], Series[str], str]]
             , by default None
         state: Optional[Union[list[str], Series[str], str]]
             The name of the state or province where the refinery is located., by default None
         from_region: Optional[Union[list[str], Series[str], str]]
             The name of an area, country division, or the world with characteristics defined by either physical boundaries or human-defined borders., by default None
         region: Optional[Union[list[str], Series[str], str]]
             The name of an area, country division, or the world with characteristics defined by either physical boundaries or human-defined borders., by default None
         country: Optional[Union[list[str], Series[str], str]]
             The name of the country where the refinery is located., by default None
         concept: Optional[Union[list[str], Series[str], str]]
             The logical grouping or classification of related data elements and entities that are relevant to a particular subject or topic., by default None
         frequency: Optional[Union[list[str], Series[str], str]]
             The indicator of how often the data is refreshed or collected., by default None
         uom: Optional[Union[list[str], Series[str], str]]
             A standardized system used to measure quantity, length, weight, time, value, speed, weather conditions, power, and others., by default None
         vintage_date: Optional[date], optional
             The date when the forecast is issued., by default None
         vintage_date_gt: Optional[date], optional
             filter by '' vintage_date > x '', by default None
         vintage_date_gte: Optional[date], optional
             filter by vintage_date, by default None
         vintage_date_lt: Optional[date], optional
             filter by vintage_date, by default None
         vintage_date_lte: Optional[date], optional
             filter by vintage_date, by default None
         report_for_date: Optional[date], optional
             The date for which the record applies within the data table, this can be a historical or forecast date., by default None
         report_for_date_gt: Optional[date], optional
             filter by '' report_for_date > x '', by default None
         report_for_date_gte: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lt: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lte: Optional[date], optional
             filter by report_for_date, by default None
         modified_date: Optional[datetime], optional
             The date and time when a particular record was last updated or modified., by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             For point in time data, indicator if this record is currently an active record., by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("outlookHorizon", outlook_horizon))
        filter_params.append(list_to_filter("zone", zone))
        filter_params.append(list_to_filter("state", state))
        filter_params.append(list_to_filter("fromRegion", from_region))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("frequency", frequency))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("vintageDate", vintage_date))
        if vintage_date_gt is not None:
            filter_params.append(f'vintageDate > "{vintage_date_gt}"')
        if vintage_date_gte is not None:
            filter_params.append(f'vintageDate >= "{vintage_date_gte}"')
        if vintage_date_lt is not None:
            filter_params.append(f'vintageDate < "{vintage_date_lt}"')
        if vintage_date_lte is not None:
            filter_params.append(f'vintageDate <= "{vintage_date_lte}"')
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
            path=f"/analytics/fuels-refining/v1/refinery-utilization-rate",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_refinery_runs(
        self,
        *,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        outlook_horizon: Optional[Union[list[str], Series[str], str]] = None,
        zone: Optional[Union[list[str], Series[str], str]] = None,
        state: Optional[Union[list[str], Series[str], str]] = None,
        from_region: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        country: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        frequency: Optional[Union[list[str], Series[str], str]] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        vintage_date: Optional[date] = None,
        vintage_date_lt: Optional[date] = None,
        vintage_date_lte: Optional[date] = None,
        vintage_date_gt: Optional[date] = None,
        vintage_date_gte: Optional[date] = None,
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
        Refinery crude runs forecast.

        Parameters
        ----------

         commodity: Optional[Union[list[str], Series[str], str]]
             The name of an economic good, usually a resource, being traded in the derivatives markets., by default None
         outlook_horizon: Optional[Union[list[str], Series[str], str]]
             The outlook type specifies the time frame for the forecast., by default None
         zone: Optional[Union[list[str], Series[str], str]]
             , by default None
         state: Optional[Union[list[str], Series[str], str]]
             The name of the state or province where the refinery is located., by default None
         from_region: Optional[Union[list[str], Series[str], str]]
             The name of an area, country division, or the world with characteristics defined by either physical boundaries or human-defined borders., by default None
         region: Optional[Union[list[str], Series[str], str]]
             The name of an area, country division, or the world with characteristics defined by either physical boundaries or human-defined borders., by default None
         country: Optional[Union[list[str], Series[str], str]]
             The name of the country where the refinery is located., by default None
         concept: Optional[Union[list[str], Series[str], str]]
             The logical grouping or classification of related data elements and entities that are relevant to a particular subject or topic., by default None
         frequency: Optional[Union[list[str], Series[str], str]]
             The indicator of how often the data is refreshed or collected., by default None
         uom: Optional[Union[list[str], Series[str], str]]
             A standardized system used to measure quantity, length, weight, time, value, speed, weather conditions, power, and others., by default None
         vintage_date: Optional[date], optional
             The date when the forecast is issued., by default None
         vintage_date_gt: Optional[date], optional
             filter by '' vintage_date > x '', by default None
         vintage_date_gte: Optional[date], optional
             filter by vintage_date, by default None
         vintage_date_lt: Optional[date], optional
             filter by vintage_date, by default None
         vintage_date_lte: Optional[date], optional
             filter by vintage_date, by default None
         report_for_date: Optional[date], optional
             The date for which the record applies within the data table, this can be a historical or forecast date., by default None
         report_for_date_gt: Optional[date], optional
             filter by '' report_for_date > x '', by default None
         report_for_date_gte: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lt: Optional[date], optional
             filter by report_for_date, by default None
         report_for_date_lte: Optional[date], optional
             filter by report_for_date, by default None
         modified_date: Optional[datetime], optional
             The date and time when a particular record was last updated or modified., by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             For point in time data, indicator if this record is currently an active record., by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("outlookHorizon", outlook_horizon))
        filter_params.append(list_to_filter("zone", zone))
        filter_params.append(list_to_filter("state", state))
        filter_params.append(list_to_filter("fromRegion", from_region))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("frequency", frequency))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("vintageDate", vintage_date))
        if vintage_date_gt is not None:
            filter_params.append(f'vintageDate > "{vintage_date_gt}"')
        if vintage_date_gte is not None:
            filter_params.append(f'vintageDate >= "{vintage_date_gte}"')
        if vintage_date_lt is not None:
            filter_params.append(f'vintageDate < "{vintage_date_lt}"')
        if vintage_date_lte is not None:
            filter_params.append(f'vintageDate <= "{vintage_date_lte}"')
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
            path=f"/analytics/fuels-refining/v1/refinery-runs",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_oil_inventory(
        self,
        *,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        geography: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        frequency: Optional[Union[list[str], Series[str], str]] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        vintage_date: Optional[date] = None,
        vintage_date_lt: Optional[date] = None,
        vintage_date_lte: Optional[date] = None,
        vintage_date_gt: Optional[date] = None,
        vintage_date_gte: Optional[date] = None,
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
             Commodity Name - The name of basic good, raw material, or primary OMD product that can be bought, sold and traded., by default None
         geography: Optional[Union[list[str], Series[str], str]]
             Geography - The geographic region for which the report or model output is reported., by default None
         concept: Optional[Union[list[str], Series[str], str]]
             Subject Area Type - The type of category or domain of information describing the subject of the data being reported., by default None
         frequency: Optional[Union[list[str], Series[str], str]]
             Dataset Frequency - The indicator of how often the data is refreshed or collected., by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Commodity Unit of Measure - The unit or units in which the value of the commodity is measured., by default None
         vintage_date: Optional[date], optional
             Vintage Date - The date for which the record applies within the data set., by default None
         vintage_date_gt: Optional[date], optional
             filter by '' vintage_date > x '', by default None
         vintage_date_gte: Optional[date], optional
             filter by vintage_date, by default None
         vintage_date_lt: Optional[date], optional
             filter by vintage_date, by default None
         vintage_date_lte: Optional[date], optional
             filter by vintage_date, by default None
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
             Historical Edge Date - The date and time when a particular record was last updated or modified in history, by default None
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
        filter_params.append(list_to_filter("geography", geography))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("frequency", frequency))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("vintageDate", vintage_date))
        if vintage_date_gt is not None:
            filter_params.append(f'vintageDate > "{vintage_date_gt}"')
        if vintage_date_gte is not None:
            filter_params.append(f'vintageDate >= "{vintage_date_gte}"')
        if vintage_date_lt is not None:
            filter_params.append(f'vintageDate < "{vintage_date_lt}"')
        if vintage_date_lte is not None:
            filter_params.append(f'vintageDate <= "{vintage_date_lte}"')
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
            path=f"/analytics/fuels-refining/v1/oil-inventory",
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

        if "vintageDate" in df.columns:
            df["vintageDate"] = pd.to_datetime(df["vintageDate"])  # type: ignore

        if "modifiedDate" in df.columns:
            df["modifiedDate"] = pd.to_datetime(df["modifiedDate"])  # type: ignore

        if "historicalEdgeDate" in df.columns:
            df["historicalEdgeDate"] = pd.to_datetime(df["historicalEdgeDate"])  # type: ignore
        return df
