from __future__ import annotations
from typing import List, Optional, Union
from requests import Response
from spgci_qa.api_client import get_data
from spgci_qa.utilities import list_to_filter
from pandas import DataFrame, Series
from datetime import date, datetime
import pandas as pd


class Biofuels:
    _endpoint = "api/v1/"
    _reference_endpoint = "reference/v1/"
    _tbl_biofuel_short_term_forecast_endpoint = "/short-term-forecast"
    _tbl_biofuel_long_term_forecast_endpoint = "/long-term-forecast"
    _tbl_biofuel_assets_capacities_endpoint = "/assets-capacities"
    _tbl_biofuel_aviation_fuel_transaction_tracker_endpoint = (
        "/aviation-fuel-transaction"
    )
    _tbl_biofuel_bunker_transaction_tracker_endpoint = "/bunker_transaction_tracker"
    _tbl_biofuel_feedstock_transaction_tracker_endpoint = (
        "/feedstock_transaction_tracker"
    )

    def get_short_term_forecast(
        self,
        *,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        reporting_region: Optional[Union[list[str], Series[str], str]] = None,
        partner_region: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
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


        Parameters
        ----------

         commodity: Optional[Union[list[str], Series[str], str]]
             The name of an economic good, usually a resource, being traded in the derivatives markets., by default None
         reporting_region: Optional[Union[list[str], Series[str], str]]
             The geographic region for which the report or model output is reported., by default None
         partner_region: Optional[Union[list[str], Series[str], str]]
             The name of the geographic region representing the other side of the model scenario transaction, such as import or export region. , by default None
         concept: Optional[Union[list[str], Series[str], str]]
             The logical grouping or classification of related data elements and entities that are relevant to a particular subject or topic., by default None
         frequency: Optional[Union[list[str], Series[str], str]]
             The indicator of how often the data is refreshed or collected., by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Numeric value used to convert between units of measure of different fuel types., by default None
         currency: Optional[Union[list[str], Series[str], str]]
             A code representing a standard unit of value of a country or region., by default None
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
             The date on which the historical data ends and the forecast data begins., by default None
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
        filter_params.append(list_to_filter("reportingRegion", reporting_region))
        filter_params.append(list_to_filter("partnerRegion", partner_region))
        filter_params.append(list_to_filter("concept", concept))
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
            path=f"/analytics/biofuels/v1/short-term-forecast",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_long_term_forecast(
        self,
        *,
        stream: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        reporting_region: Optional[Union[list[str], Series[str], str]] = None,
        coverage: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        actual_concept: Optional[Union[list[str], Series[str], str]] = None,
        classification: Optional[Union[list[str], Series[str], str]] = None,
        frequency: Optional[Union[list[str], Series[str], str]] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        currency: Optional[Union[list[str], Series[str], str]] = None,
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


        Parameters
        ----------

         stream: Optional[Union[list[str], Series[str], str]]
             The name of an economic good, usually a resource, being traded in the derivatives markets., by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             The name of an economic good, usually a resource, being traded in the derivatives markets., by default None
         region: Optional[Union[list[str], Series[str], str]]
             The name of the geographic region. , by default None
         reporting_region: Optional[Union[list[str], Series[str], str]]
             The geographic region for which the report or model output is reported., by default None
         coverage: Optional[Union[list[str], Series[str], str]]
             The logical grouping or classification of related data elements and entities that are relevant to a particular subject or topic., by default None
         concept: Optional[Union[list[str], Series[str], str]]
             The logical grouping or classification of related data elements and entities that are relevant to a particular subject or topic., by default None
         actual_concept: Optional[Union[list[str], Series[str], str]]
             The logical grouping or classification of related data elements and entities that are relevant to a particular subject or topic., by default None
         classification: Optional[Union[list[str], Series[str], str]]
             The logical grouping or classification of related data elements and entities that are relevant to a particular subject or topic., by default None
         frequency: Optional[Union[list[str], Series[str], str]]
             The indicator of how often the data is refreshed or collected., by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Numeric value used to convert between units of measure of different fuel types., by default None
         currency: Optional[Union[list[str], Series[str], str]]
             A code representing a standard unit of value of a country or region., by default None
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
        filter_params.append(list_to_filter("stream", stream))
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("reportingRegion", reporting_region))
        filter_params.append(list_to_filter("coverage", coverage))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("actualConcept", actual_concept))
        filter_params.append(list_to_filter("classification", classification))
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
            path=f"/analytics/biofuels/v1/long-term-forecast",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_assets_capacities(
        self,
        *,
        industry: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        country: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        asset_capactiy_status: Optional[Union[list[str], Series[str], str]] = None,
        owner_operator: Optional[Union[list[str], Series[str], str]] = None,
        location: Optional[Union[list[str], Series[str], str]] = None,
        production_capacities: Optional[Union[list[str], Series[str], str]] = None,
        feedstocks: Optional[Union[list[str], Series[str], str]] = None,
        historical_info: Optional[Union[list[str], Series[str], str]] = None,
        capital_expenditures: Optional[Union[list[str], Series[str], str]] = None,
        source_id: Optional[Union[list[str], Series[str], str]] = None,
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


        Parameters
        ----------

         industry: Optional[Union[list[str], Series[str], str]]
             The classification for group of commodities belong to., by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             The name of an economic good, usually a resource, being traded in the derivatives markets., by default None
         country: Optional[Union[list[str], Series[str], str]]
             The name of the geographic region. , by default None
         region: Optional[Union[list[str], Series[str], str]]
             The geographic region for which the report or model output is reported., by default None
         asset_capactiy_status: Optional[Union[list[str], Series[str], str]]
             The logical grouping or classification of related data elements and entities that are relevant to a particular subject or topic., by default None
         owner_operator: Optional[Union[list[str], Series[str], str]]
             The logical grouping or classification of related data elements and entities that are relevant to a particular subject or topic., by default None
         location: Optional[Union[list[str], Series[str], str]]
             The logical grouping or classification of related data elements and entities that are relevant to a particular subject or topic., by default None
         production_capacities: Optional[Union[list[str], Series[str], str]]
             The logical grouping or classification of related data elements and entities that are relevant to a particular subject or topic., by default None
         feedstocks: Optional[Union[list[str], Series[str], str]]
             The indicator of how often the data is refreshed or collected., by default None
         historical_info: Optional[Union[list[str], Series[str], str]]
             Numeric value used to convert between units of measure of different fuel types., by default None
         capital_expenditures: Optional[Union[list[str], Series[str], str]]
             A code representing a standard unit of value of a country or region., by default None
         source_id: Optional[Union[list[str], Series[str], str]]
             A code representing a standard unit of value of a country or region., by default None
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
        filter_params.append(list_to_filter("industry", industry))
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(
            list_to_filter("assetCapactiyStatus", asset_capactiy_status)
        )
        filter_params.append(list_to_filter("ownerOperator", owner_operator))
        filter_params.append(list_to_filter("location", location))
        filter_params.append(
            list_to_filter("productionCapacities", production_capacities)
        )
        filter_params.append(list_to_filter("feedstocks", feedstocks))
        filter_params.append(list_to_filter("historicalInfo", historical_info))
        filter_params.append(
            list_to_filter("capitalExpenditures", capital_expenditures)
        )
        filter_params.append(list_to_filter("sourceId", source_id))
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
            path=f"/analytics/biofuels/v1/assets-capacities",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_aviation_fuel_transaction(
        self,
        *,
        seller: Optional[Union[list[str], Series[str], str]] = None,
        buyer: Optional[Union[list[str], Series[str], str]] = None,
        agreement_type: Optional[Union[list[str], Series[str], str]] = None,
        announcement_period: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        technology: Optional[Union[list[str], Series[str], str]] = None,
        offtake_start_year: Optional[Union[list[str], Series[str], str]] = None,
        offtake_duration: Optional[Union[list[str], Series[str], str]] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        offtake_yearly_value: Optional[Union[list[str], Series[str], str]] = None,
        offtake_total_value: Optional[Union[list[str], Series[str], str]] = None,
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


        Parameters
        ----------

         seller: Optional[Union[list[str], Series[str], str]]
             The name of seller., by default None
         buyer: Optional[Union[list[str], Series[str], str]]
             The name of buyer., by default None
         agreement_type: Optional[Union[list[str], Series[str], str]]
             The type of agreement., by default None
         announcement_period: Optional[Union[list[str], Series[str], str]]
             The transaction was announced., by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             The name of an economic good, usually a resource, being traded in the derivatives markets., by default None
         technology: Optional[Union[list[str], Series[str], str]]
             The type of technology involved., by default None
         offtake_start_year: Optional[Union[list[str], Series[str], str]]
             Transaction start year., by default None
         offtake_duration: Optional[Union[list[str], Series[str], str]]
             The transaction duration., by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Numeric value used to convert between units of measure of different fuel types., by default None
         offtake_yearly_value: Optional[Union[list[str], Series[str], str]]
             The offtake Yearly value., by default None
         offtake_total_value: Optional[Union[list[str], Series[str], str]]
             The offtake Total value., by default None
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
        filter_params.append(list_to_filter("seller", seller))
        filter_params.append(list_to_filter("buyer", buyer))
        filter_params.append(list_to_filter("agreementType", agreement_type))
        filter_params.append(list_to_filter("announcementPeriod", announcement_period))
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("technology", technology))
        filter_params.append(list_to_filter("offtakeStartYear", offtake_start_year))
        filter_params.append(list_to_filter("offtakeDuration", offtake_duration))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("offtakeYearlyValue", offtake_yearly_value))
        filter_params.append(list_to_filter("offtakeTotalValue", offtake_total_value))
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
            path=f"/analytics/biofuels/v1/aviation-fuel-transaction",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_bunker_transaction_tracker(
        self,
        *,
        port: Optional[Union[list[str], Series[str], str]] = None,
        port_market: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        seller: Optional[Union[list[str], Series[str], str]] = None,
        buyer: Optional[Union[list[str], Series[str], str]] = None,
        agreement_type: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        currency: Optional[Union[list[str], Series[str], str]] = None,
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


        Parameters
        ----------

         port: Optional[Union[list[str], Series[str], str]]
             The name of Port., by default None
         port_market: Optional[Union[list[str], Series[str], str]]
             The market for Port., by default None
         region: Optional[Union[list[str], Series[str], str]]
             The geographic region for which the report or model output is reported., by default None
         seller: Optional[Union[list[str], Series[str], str]]
             The name of seller., by default None
         buyer: Optional[Union[list[str], Series[str], str]]
             The name of buyer., by default None
         agreement_type: Optional[Union[list[str], Series[str], str]]
             The type of agreement., by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             The name of an economic good, usually a resource, being traded in the derivatives markets., by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Numeric value used to convert between units of measure of different fuel types., by default None
         currency: Optional[Union[list[str], Series[str], str]]
             A code representing a standard unit of value of a country or region., by default None
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
        filter_params.append(list_to_filter("port", port))
        filter_params.append(list_to_filter("portMarket", port_market))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("seller", seller))
        filter_params.append(list_to_filter("buyer", buyer))
        filter_params.append(list_to_filter("agreementType", agreement_type))
        filter_params.append(list_to_filter("commodity", commodity))
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
            path=f"/analytics/biofuels/v1/bunker_transaction_tracker",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_feedstock_transaction_tracker(
        self,
        *,
        upstream_company: Optional[Union[list[str], Series[str], str]] = None,
        upstream_company_region: Optional[Union[list[str], Series[str], str]] = None,
        upstream_company_sector: Optional[Union[list[str], Series[str], str]] = None,
        downstream_company: Optional[Union[list[str], Series[str], str]] = None,
        downstream_company_region: Optional[Union[list[str], Series[str], str]] = None,
        downstream_company_sector: Optional[Union[list[str], Series[str], str]] = None,
        commodity_group: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        generation_type: Optional[Union[list[str], Series[str], str]] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        currency: Optional[Union[list[str], Series[str], str]] = None,
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


        Parameters
        ----------

         upstream_company: Optional[Union[list[str], Series[str], str]]
             The name of upstrream company., by default None
         upstream_company_region: Optional[Union[list[str], Series[str], str]]
             The region of upstrream company., by default None
         upstream_company_sector: Optional[Union[list[str], Series[str], str]]
             The Sector of upstrream company., by default None
         downstream_company: Optional[Union[list[str], Series[str], str]]
             The name of upstrream company., by default None
         downstream_company_region: Optional[Union[list[str], Series[str], str]]
             The region of downstream company., by default None
         downstream_company_sector: Optional[Union[list[str], Series[str], str]]
             The Sector of downstream company., by default None
         commodity_group: Optional[Union[list[str], Series[str], str]]
             The Commodity Group., by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             The name of an economic good, usually a resource, being traded in the derivatives markets., by default None
         generation_type: Optional[Union[list[str], Series[str], str]]
             The type of generation., by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Numeric value used to convert between units of measure of different fuel types., by default None
         currency: Optional[Union[list[str], Series[str], str]]
             A code representing a standard unit of value of a country or region., by default None
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
        filter_params.append(list_to_filter("upstreamCompany", upstream_company))
        filter_params.append(
            list_to_filter("upstreamCompanyRegion", upstream_company_region)
        )
        filter_params.append(
            list_to_filter("upstreamCompanySector", upstream_company_sector)
        )
        filter_params.append(list_to_filter("downstreamCompany", downstream_company))
        filter_params.append(
            list_to_filter("downstreamCompanyRegion", downstream_company_region)
        )
        filter_params.append(
            list_to_filter("downstreamCompanySector", downstream_company_sector)
        )
        filter_params.append(list_to_filter("commodityGroup", commodity_group))
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("generationType", generation_type))
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
            path=f"/analytics/biofuels/v1/feedstock_transaction_tracker",
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
