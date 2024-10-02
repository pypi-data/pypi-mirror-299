from __future__ import annotations
from typing import List, Optional, Union
from requests import Response
from spgci_qa.api_client import get_data
from spgci_qa.utilities import list_to_filter
from pandas import DataFrame, Series
from datetime import date, datetime
import pandas as pd


class Chemicals_supply_demand:
    _endpoint = "api/v1/"
    _reference_endpoint = "reference/v1/"
    _capacity_w_names_v_endpoint = "/capacity"
    _production_w_names_v_endpoint = "/production"
    _capacity_utilization_w_names_v_endpoint = "/capacity-utilization"
    _demand_by_derivative_or_application_w_names_rest_v_endpoint = (
        "/demand-by-derivative"
    )
    _demand_by_end_use_w_names_rest_v_endpoint = "/demand-by-end-use"
    _trade_w_names_v_endpoint = "/trade"
    _inventory_change_w_names_v_endpoint = "/inventory-change"
    _total_supply_with_names_v_endpoint = "/total-supply"
    _total_demand_with_names_v_endpoint = "/total-demand"

    def get_capacity(
        self,
        *,
        forecast_period: Optional[Union[list[str], Series[str], str]] = None,
        scenario_id: Optional[int] = None,
        scenario_id_lt: Optional[int] = None,
        scenario_id_lte: Optional[int] = None,
        scenario_id_gt: Optional[int] = None,
        scenario_id_gte: Optional[int] = None,
        scenario_description: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        production_route: Optional[Union[list[str], Series[str], str]] = None,
        country: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        date: Optional[date] = None,
        date_lt: Optional[date] = None,
        date_lte: Optional[date] = None,
        date_gt: Optional[date] = None,
        date_gte: Optional[date] = None,
        value: Optional[str] = None,
        value_lt: Optional[str] = None,
        value_lte: Optional[str] = None,
        value_gt: Optional[str] = None,
        value_gte: Optional[str] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        data_type: Optional[Union[list[str], Series[str], str]] = None,
        valid_to: Optional[date] = None,
        valid_to_lt: Optional[date] = None,
        valid_to_lte: Optional[date] = None,
        valid_to_gt: Optional[date] = None,
        valid_to_gte: Optional[date] = None,
        valid_from: Optional[date] = None,
        valid_from_lt: Optional[date] = None,
        valid_from_lte: Optional[date] = None,
        valid_from_gt: Optional[date] = None,
        valid_from_gte: Optional[date] = None,
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
        Country-level capacity data by production route for a product

        Parameters
        ----------

         forecast_period: Optional[Union[list[str], Series[str], str]]
             Long term or short term, by default None
         scenario_id: Optional[int], optional
             Scenario ID, by default None
         scenario_id_gt: Optional[int], optional
             filter by '' scenario_id > x '', by default None
         scenario_id_gte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lt: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_description: Optional[Union[list[str], Series[str], str]]
             Scenario Description, by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             Name for Product (chemical commodity), by default None
         production_route: Optional[Union[list[str], Series[str], str]]
             Name for Production Route, by default None
         country: Optional[Union[list[str], Series[str], str]]
             Name for Country (geography), by default None
         region: Optional[Union[list[str], Series[str], str]]
             Name for Region (geography), by default None
         concept: Optional[Union[list[str], Series[str], str]]
             Concept that describes what the dataset is, by default None
         date: Optional[date], optional
             Date, by default None
         date_gt: Optional[date], optional
             filter by '' date > x '', by default None
         date_gte: Optional[date], optional
             filter by date, by default None
         date_lt: Optional[date], optional
             filter by date, by default None
         date_lte: Optional[date], optional
             filter by date, by default None
         value: Optional[str], optional
             Data Value, by default None
         value_gt: Optional[str], optional
             filter by '' value > x '', by default None
         value_gte: Optional[str], optional
             filter by value, by default None
         value_lt: Optional[str], optional
             filter by value, by default None
         value_lte: Optional[str], optional
             filter by value, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Name for Unit of Measure (volume), by default None
         data_type: Optional[Union[list[str], Series[str], str]]
             Data Type (history or forecast), by default None
         valid_to: Optional[date], optional
             End Date of Record Validity, by default None
         valid_to_gt: Optional[date], optional
             filter by '' valid_to > x '', by default None
         valid_to_gte: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lt: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lte: Optional[date], optional
             filter by valid_to, by default None
         valid_from: Optional[date], optional
             As of date for when the data is updated, by default None
         valid_from_gt: Optional[date], optional
             filter by '' valid_from > x '', by default None
         valid_from_gte: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lt: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lte: Optional[date], optional
             filter by valid_from, by default None
         modified_date: Optional[datetime], optional
             Date when the data is last modified, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             If the record is active, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("forecast_period", forecast_period))
        filter_params.append(list_to_filter("scenario_id", scenario_id))
        if scenario_id_gt is not None:
            filter_params.append(f'scenario_id > "{scenario_id_gt}"')
        if scenario_id_gte is not None:
            filter_params.append(f'scenario_id >= "{scenario_id_gte}"')
        if scenario_id_lt is not None:
            filter_params.append(f'scenario_id < "{scenario_id_lt}"')
        if scenario_id_lte is not None:
            filter_params.append(f'scenario_id <= "{scenario_id_lte}"')
        filter_params.append(
            list_to_filter("scenario_description", scenario_description)
        )
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("production_route", production_route))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("date", date))
        if date_gt is not None:
            filter_params.append(f'date > "{date_gt}"')
        if date_gte is not None:
            filter_params.append(f'date >= "{date_gte}"')
        if date_lt is not None:
            filter_params.append(f'date < "{date_lt}"')
        if date_lte is not None:
            filter_params.append(f'date <= "{date_lte}"')
        filter_params.append(list_to_filter("value", value))
        if value_gt is not None:
            filter_params.append(f'value > "{value_gt}"')
        if value_gte is not None:
            filter_params.append(f'value >= "{value_gte}"')
        if value_lt is not None:
            filter_params.append(f'value < "{value_lt}"')
        if value_lte is not None:
            filter_params.append(f'value <= "{value_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("data_type", data_type))
        filter_params.append(list_to_filter("valid_to", valid_to))
        if valid_to_gt is not None:
            filter_params.append(f'valid_to > "{valid_to_gt}"')
        if valid_to_gte is not None:
            filter_params.append(f'valid_to >= "{valid_to_gte}"')
        if valid_to_lt is not None:
            filter_params.append(f'valid_to < "{valid_to_lt}"')
        if valid_to_lte is not None:
            filter_params.append(f'valid_to <= "{valid_to_lte}"')
        filter_params.append(list_to_filter("valid_from", valid_from))
        if valid_from_gt is not None:
            filter_params.append(f'valid_from > "{valid_from_gt}"')
        if valid_from_gte is not None:
            filter_params.append(f'valid_from >= "{valid_from_gte}"')
        if valid_from_lt is not None:
            filter_params.append(f'valid_from < "{valid_from_lt}"')
        if valid_from_lte is not None:
            filter_params.append(f'valid_from <= "{valid_from_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')
        filter_params.append(list_to_filter("is_active", is_active))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/v1/chemicals/capacity",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_production(
        self,
        *,
        forecast_period: Optional[Union[list[str], Series[str], str]] = None,
        scenario_id: Optional[int] = None,
        scenario_id_lt: Optional[int] = None,
        scenario_id_lte: Optional[int] = None,
        scenario_id_gt: Optional[int] = None,
        scenario_id_gte: Optional[int] = None,
        scenario_description: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        production_route: Optional[Union[list[str], Series[str], str]] = None,
        country: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        date: Optional[date] = None,
        date_lt: Optional[date] = None,
        date_lte: Optional[date] = None,
        date_gt: Optional[date] = None,
        date_gte: Optional[date] = None,
        value: Optional[str] = None,
        value_lt: Optional[str] = None,
        value_lte: Optional[str] = None,
        value_gt: Optional[str] = None,
        value_gte: Optional[str] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        data_type: Optional[Union[list[str], Series[str], str]] = None,
        valid_to: Optional[date] = None,
        valid_to_lt: Optional[date] = None,
        valid_to_lte: Optional[date] = None,
        valid_to_gt: Optional[date] = None,
        valid_to_gte: Optional[date] = None,
        valid_from: Optional[date] = None,
        valid_from_lt: Optional[date] = None,
        valid_from_lte: Optional[date] = None,
        valid_from_gt: Optional[date] = None,
        valid_from_gte: Optional[date] = None,
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
        Country-level production data by production route for a product

        Parameters
        ----------

         forecast_period: Optional[Union[list[str], Series[str], str]]
             Long term or short term, by default None
         scenario_id: Optional[int], optional
             Scenario ID, by default None
         scenario_id_gt: Optional[int], optional
             filter by '' scenario_id > x '', by default None
         scenario_id_gte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lt: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_description: Optional[Union[list[str], Series[str], str]]
             Scenario Description, by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             Name for Product (chemical commodity), by default None
         production_route: Optional[Union[list[str], Series[str], str]]
             Name for Production Route, by default None
         country: Optional[Union[list[str], Series[str], str]]
             Name for Country (geography), by default None
         region: Optional[Union[list[str], Series[str], str]]
             Name for Region (geography), by default None
         concept: Optional[Union[list[str], Series[str], str]]
             Concept that describes what the dataset is, by default None
         date: Optional[date], optional
             Date, by default None
         date_gt: Optional[date], optional
             filter by '' date > x '', by default None
         date_gte: Optional[date], optional
             filter by date, by default None
         date_lt: Optional[date], optional
             filter by date, by default None
         date_lte: Optional[date], optional
             filter by date, by default None
         value: Optional[str], optional
             Data Value, by default None
         value_gt: Optional[str], optional
             filter by '' value > x '', by default None
         value_gte: Optional[str], optional
             filter by value, by default None
         value_lt: Optional[str], optional
             filter by value, by default None
         value_lte: Optional[str], optional
             filter by value, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Name for Unit of Measure (volume), by default None
         data_type: Optional[Union[list[str], Series[str], str]]
             Data Type (history or forecast), by default None
         valid_to: Optional[date], optional
             End Date of Record Validity, by default None
         valid_to_gt: Optional[date], optional
             filter by '' valid_to > x '', by default None
         valid_to_gte: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lt: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lte: Optional[date], optional
             filter by valid_to, by default None
         valid_from: Optional[date], optional
             As of date for when the data is updated, by default None
         valid_from_gt: Optional[date], optional
             filter by '' valid_from > x '', by default None
         valid_from_gte: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lt: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lte: Optional[date], optional
             filter by valid_from, by default None
         modified_date: Optional[datetime], optional
             Date when the data is last modified, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             If the record is active, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("forecast_period", forecast_period))
        filter_params.append(list_to_filter("scenario_id", scenario_id))
        if scenario_id_gt is not None:
            filter_params.append(f'scenario_id > "{scenario_id_gt}"')
        if scenario_id_gte is not None:
            filter_params.append(f'scenario_id >= "{scenario_id_gte}"')
        if scenario_id_lt is not None:
            filter_params.append(f'scenario_id < "{scenario_id_lt}"')
        if scenario_id_lte is not None:
            filter_params.append(f'scenario_id <= "{scenario_id_lte}"')
        filter_params.append(
            list_to_filter("scenario_description", scenario_description)
        )
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("production_route", production_route))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("date", date))
        if date_gt is not None:
            filter_params.append(f'date > "{date_gt}"')
        if date_gte is not None:
            filter_params.append(f'date >= "{date_gte}"')
        if date_lt is not None:
            filter_params.append(f'date < "{date_lt}"')
        if date_lte is not None:
            filter_params.append(f'date <= "{date_lte}"')
        filter_params.append(list_to_filter("value", value))
        if value_gt is not None:
            filter_params.append(f'value > "{value_gt}"')
        if value_gte is not None:
            filter_params.append(f'value >= "{value_gte}"')
        if value_lt is not None:
            filter_params.append(f'value < "{value_lt}"')
        if value_lte is not None:
            filter_params.append(f'value <= "{value_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("data_type", data_type))
        filter_params.append(list_to_filter("valid_to", valid_to))
        if valid_to_gt is not None:
            filter_params.append(f'valid_to > "{valid_to_gt}"')
        if valid_to_gte is not None:
            filter_params.append(f'valid_to >= "{valid_to_gte}"')
        if valid_to_lt is not None:
            filter_params.append(f'valid_to < "{valid_to_lt}"')
        if valid_to_lte is not None:
            filter_params.append(f'valid_to <= "{valid_to_lte}"')
        filter_params.append(list_to_filter("valid_from", valid_from))
        if valid_from_gt is not None:
            filter_params.append(f'valid_from > "{valid_from_gt}"')
        if valid_from_gte is not None:
            filter_params.append(f'valid_from >= "{valid_from_gte}"')
        if valid_from_lt is not None:
            filter_params.append(f'valid_from < "{valid_from_lt}"')
        if valid_from_lte is not None:
            filter_params.append(f'valid_from <= "{valid_from_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')
        filter_params.append(list_to_filter("is_active", is_active))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/v1/chemicals/production",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_capacity_utilization(
        self,
        *,
        forecast_period: Optional[Union[list[str], Series[str], str]] = None,
        scenario_id: Optional[int] = None,
        scenario_id_lt: Optional[int] = None,
        scenario_id_lte: Optional[int] = None,
        scenario_id_gt: Optional[int] = None,
        scenario_id_gte: Optional[int] = None,
        scenario_description: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        production_route: Optional[Union[list[str], Series[str], str]] = None,
        country: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        date: Optional[date] = None,
        date_lt: Optional[date] = None,
        date_lte: Optional[date] = None,
        date_gt: Optional[date] = None,
        date_gte: Optional[date] = None,
        value: Optional[str] = None,
        value_lt: Optional[str] = None,
        value_lte: Optional[str] = None,
        value_gt: Optional[str] = None,
        value_gte: Optional[str] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        data_type: Optional[Union[list[str], Series[str], str]] = None,
        valid_to: Optional[date] = None,
        valid_to_lt: Optional[date] = None,
        valid_to_lte: Optional[date] = None,
        valid_to_gt: Optional[date] = None,
        valid_to_gte: Optional[date] = None,
        valid_from: Optional[date] = None,
        valid_from_lt: Optional[date] = None,
        valid_from_lte: Optional[date] = None,
        valid_from_gt: Optional[date] = None,
        valid_from_gte: Optional[date] = None,
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
        Capacity Utilization data for a product

        Parameters
        ----------

         forecast_period: Optional[Union[list[str], Series[str], str]]
             Long term or short term, by default None
         scenario_id: Optional[int], optional
             Scenario ID, by default None
         scenario_id_gt: Optional[int], optional
             filter by '' scenario_id > x '', by default None
         scenario_id_gte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lt: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_description: Optional[Union[list[str], Series[str], str]]
             Scenario Description, by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             Name for Product (chemical commodity), by default None
         production_route: Optional[Union[list[str], Series[str], str]]
             Name for Production Route, by default None
         country: Optional[Union[list[str], Series[str], str]]
             Name for Country (geography), by default None
         region: Optional[Union[list[str], Series[str], str]]
             Name for Region (geography), by default None
         concept: Optional[Union[list[str], Series[str], str]]
             Concept that describes what the dataset is, by default None
         date: Optional[date], optional
             Date, by default None
         date_gt: Optional[date], optional
             filter by '' date > x '', by default None
         date_gte: Optional[date], optional
             filter by date, by default None
         date_lt: Optional[date], optional
             filter by date, by default None
         date_lte: Optional[date], optional
             filter by date, by default None
         value: Optional[str], optional
             Data Value, by default None
         value_gt: Optional[str], optional
             filter by '' value > x '', by default None
         value_gte: Optional[str], optional
             filter by value, by default None
         value_lt: Optional[str], optional
             filter by value, by default None
         value_lte: Optional[str], optional
             filter by value, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Name for Unit of Measure (volume), by default None
         data_type: Optional[Union[list[str], Series[str], str]]
             Data Type (history or forecast), by default None
         valid_to: Optional[date], optional
             End Date of Record Validity, by default None
         valid_to_gt: Optional[date], optional
             filter by '' valid_to > x '', by default None
         valid_to_gte: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lt: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lte: Optional[date], optional
             filter by valid_to, by default None
         valid_from: Optional[date], optional
             As of date for when the data is updated, by default None
         valid_from_gt: Optional[date], optional
             filter by '' valid_from > x '', by default None
         valid_from_gte: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lt: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lte: Optional[date], optional
             filter by valid_from, by default None
         modified_date: Optional[datetime], optional
             Date when the data is last modified, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             If the record is active, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("forecast_period", forecast_period))
        filter_params.append(list_to_filter("scenario_id", scenario_id))
        if scenario_id_gt is not None:
            filter_params.append(f'scenario_id > "{scenario_id_gt}"')
        if scenario_id_gte is not None:
            filter_params.append(f'scenario_id >= "{scenario_id_gte}"')
        if scenario_id_lt is not None:
            filter_params.append(f'scenario_id < "{scenario_id_lt}"')
        if scenario_id_lte is not None:
            filter_params.append(f'scenario_id <= "{scenario_id_lte}"')
        filter_params.append(
            list_to_filter("scenario_description", scenario_description)
        )
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("production_route", production_route))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("date", date))
        if date_gt is not None:
            filter_params.append(f'date > "{date_gt}"')
        if date_gte is not None:
            filter_params.append(f'date >= "{date_gte}"')
        if date_lt is not None:
            filter_params.append(f'date < "{date_lt}"')
        if date_lte is not None:
            filter_params.append(f'date <= "{date_lte}"')
        filter_params.append(list_to_filter("value", value))
        if value_gt is not None:
            filter_params.append(f'value > "{value_gt}"')
        if value_gte is not None:
            filter_params.append(f'value >= "{value_gte}"')
        if value_lt is not None:
            filter_params.append(f'value < "{value_lt}"')
        if value_lte is not None:
            filter_params.append(f'value <= "{value_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("data_type", data_type))
        filter_params.append(list_to_filter("valid_to", valid_to))
        if valid_to_gt is not None:
            filter_params.append(f'valid_to > "{valid_to_gt}"')
        if valid_to_gte is not None:
            filter_params.append(f'valid_to >= "{valid_to_gte}"')
        if valid_to_lt is not None:
            filter_params.append(f'valid_to < "{valid_to_lt}"')
        if valid_to_lte is not None:
            filter_params.append(f'valid_to <= "{valid_to_lte}"')
        filter_params.append(list_to_filter("valid_from", valid_from))
        if valid_from_gt is not None:
            filter_params.append(f'valid_from > "{valid_from_gt}"')
        if valid_from_gte is not None:
            filter_params.append(f'valid_from >= "{valid_from_gte}"')
        if valid_from_lt is not None:
            filter_params.append(f'valid_from < "{valid_from_lt}"')
        if valid_from_lte is not None:
            filter_params.append(f'valid_from <= "{valid_from_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')
        filter_params.append(list_to_filter("is_active", is_active))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/v1/chemicals/capacity-utilization",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_demand_by_derivative(
        self,
        *,
        forecast_period: Optional[Union[list[str], Series[str], str]] = None,
        scenario_id: Optional[int] = None,
        scenario_id_lt: Optional[int] = None,
        scenario_id_lte: Optional[int] = None,
        scenario_id_gt: Optional[int] = None,
        scenario_id_gte: Optional[int] = None,
        scenario_description: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        country: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        date: Optional[date] = None,
        date_lt: Optional[date] = None,
        date_lte: Optional[date] = None,
        date_gt: Optional[date] = None,
        date_gte: Optional[date] = None,
        value: Optional[str] = None,
        value_lt: Optional[str] = None,
        value_lte: Optional[str] = None,
        value_gt: Optional[str] = None,
        value_gte: Optional[str] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        data_type: Optional[Union[list[str], Series[str], str]] = None,
        valid_to: Optional[date] = None,
        valid_to_lt: Optional[date] = None,
        valid_to_lte: Optional[date] = None,
        valid_to_gt: Optional[date] = None,
        valid_to_gte: Optional[date] = None,
        valid_from: Optional[date] = None,
        valid_from_lt: Optional[date] = None,
        valid_from_lte: Optional[date] = None,
        valid_from_gt: Optional[date] = None,
        valid_from_gte: Optional[date] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        is_active: Optional[Union[list[str], Series[str], str]] = None,
        application: Optional[Union[list[str], Series[str], str]] = None,
        derivative_product: Optional[Union[list[str], Series[str], str]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Country-level demand data for a product categorized by derivative or specific application

        Parameters
        ----------

         forecast_period: Optional[Union[list[str], Series[str], str]]
             Long term or short term, by default None
         scenario_id: Optional[int], optional
             Scenario ID, by default None
         scenario_id_gt: Optional[int], optional
             filter by '' scenario_id > x '', by default None
         scenario_id_gte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lt: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_description: Optional[Union[list[str], Series[str], str]]
             Scenario Description, by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             Name for Product (chemical commodity), by default None
         country: Optional[Union[list[str], Series[str], str]]
             Name for Country (geography), by default None
         region: Optional[Union[list[str], Series[str], str]]
             Name for Region (geography), by default None
         concept: Optional[Union[list[str], Series[str], str]]
             Concept that describes what the dataset is, by default None
         date: Optional[date], optional
             Date, by default None
         date_gt: Optional[date], optional
             filter by '' date > x '', by default None
         date_gte: Optional[date], optional
             filter by date, by default None
         date_lt: Optional[date], optional
             filter by date, by default None
         date_lte: Optional[date], optional
             filter by date, by default None
         value: Optional[str], optional
             Data Value, by default None
         value_gt: Optional[str], optional
             filter by '' value > x '', by default None
         value_gte: Optional[str], optional
             filter by value, by default None
         value_lt: Optional[str], optional
             filter by value, by default None
         value_lte: Optional[str], optional
             filter by value, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Name for Unit of Measure (volume), by default None
         data_type: Optional[Union[list[str], Series[str], str]]
             Data Type (history or forecast), by default None
         valid_to: Optional[date], optional
             End Date of Record Validity, by default None
         valid_to_gt: Optional[date], optional
             filter by '' valid_to > x '', by default None
         valid_to_gte: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lt: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lte: Optional[date], optional
             filter by valid_to, by default None
         valid_from: Optional[date], optional
             As of date for when the data is updated, by default None
         valid_from_gt: Optional[date], optional
             filter by '' valid_from > x '', by default None
         valid_from_gte: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lt: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lte: Optional[date], optional
             filter by valid_from, by default None
         modified_date: Optional[datetime], optional
             Date when the data is last modified, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             If the record is active, by default None
         application: Optional[Union[list[str], Series[str], str]]
             Product(chemical commodity) Application, by default None
         derivative_product: Optional[Union[list[str], Series[str], str]]
             Derivative Product (chemical commodity), by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("forecast_period", forecast_period))
        filter_params.append(list_to_filter("scenario_id", scenario_id))
        if scenario_id_gt is not None:
            filter_params.append(f'scenario_id > "{scenario_id_gt}"')
        if scenario_id_gte is not None:
            filter_params.append(f'scenario_id >= "{scenario_id_gte}"')
        if scenario_id_lt is not None:
            filter_params.append(f'scenario_id < "{scenario_id_lt}"')
        if scenario_id_lte is not None:
            filter_params.append(f'scenario_id <= "{scenario_id_lte}"')
        filter_params.append(
            list_to_filter("scenario_description", scenario_description)
        )
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("date", date))
        if date_gt is not None:
            filter_params.append(f'date > "{date_gt}"')
        if date_gte is not None:
            filter_params.append(f'date >= "{date_gte}"')
        if date_lt is not None:
            filter_params.append(f'date < "{date_lt}"')
        if date_lte is not None:
            filter_params.append(f'date <= "{date_lte}"')
        filter_params.append(list_to_filter("value", value))
        if value_gt is not None:
            filter_params.append(f'value > "{value_gt}"')
        if value_gte is not None:
            filter_params.append(f'value >= "{value_gte}"')
        if value_lt is not None:
            filter_params.append(f'value < "{value_lt}"')
        if value_lte is not None:
            filter_params.append(f'value <= "{value_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("data_type", data_type))
        filter_params.append(list_to_filter("valid_to", valid_to))
        if valid_to_gt is not None:
            filter_params.append(f'valid_to > "{valid_to_gt}"')
        if valid_to_gte is not None:
            filter_params.append(f'valid_to >= "{valid_to_gte}"')
        if valid_to_lt is not None:
            filter_params.append(f'valid_to < "{valid_to_lt}"')
        if valid_to_lte is not None:
            filter_params.append(f'valid_to <= "{valid_to_lte}"')
        filter_params.append(list_to_filter("valid_from", valid_from))
        if valid_from_gt is not None:
            filter_params.append(f'valid_from > "{valid_from_gt}"')
        if valid_from_gte is not None:
            filter_params.append(f'valid_from >= "{valid_from_gte}"')
        if valid_from_lt is not None:
            filter_params.append(f'valid_from < "{valid_from_lt}"')
        if valid_from_lte is not None:
            filter_params.append(f'valid_from <= "{valid_from_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')
        filter_params.append(list_to_filter("is_active", is_active))
        filter_params.append(list_to_filter("application", application))
        filter_params.append(list_to_filter("derivative_product", derivative_product))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/v1/chemicals/demand-by-derivative",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_demand_by_end_use(
        self,
        *,
        forecast_period: Optional[Union[list[str], Series[str], str]] = None,
        scenario_id: Optional[int] = None,
        scenario_id_lt: Optional[int] = None,
        scenario_id_lte: Optional[int] = None,
        scenario_id_gt: Optional[int] = None,
        scenario_id_gte: Optional[int] = None,
        scenario_description: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        country: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        date: Optional[date] = None,
        date_lt: Optional[date] = None,
        date_lte: Optional[date] = None,
        date_gt: Optional[date] = None,
        date_gte: Optional[date] = None,
        value: Optional[str] = None,
        value_lt: Optional[str] = None,
        value_lte: Optional[str] = None,
        value_gt: Optional[str] = None,
        value_gte: Optional[str] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        data_type: Optional[Union[list[str], Series[str], str]] = None,
        valid_to: Optional[date] = None,
        valid_to_lt: Optional[date] = None,
        valid_to_lte: Optional[date] = None,
        valid_to_gt: Optional[date] = None,
        valid_to_gte: Optional[date] = None,
        valid_from: Optional[date] = None,
        valid_from_lt: Optional[date] = None,
        valid_from_lte: Optional[date] = None,
        valid_from_gt: Optional[date] = None,
        valid_from_gte: Optional[date] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        is_active: Optional[Union[list[str], Series[str], str]] = None,
        end_use: Optional[Union[list[str], Series[str], str]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Country-level demand data for a product categorized by end use

        Parameters
        ----------

         forecast_period: Optional[Union[list[str], Series[str], str]]
             Long term or short term, by default None
         scenario_id: Optional[int], optional
             Scenario ID, by default None
         scenario_id_gt: Optional[int], optional
             filter by '' scenario_id > x '', by default None
         scenario_id_gte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lt: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_description: Optional[Union[list[str], Series[str], str]]
             Scenario Description, by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             Name for Product (chemical commodity), by default None
         country: Optional[Union[list[str], Series[str], str]]
             Name for Country (geography), by default None
         region: Optional[Union[list[str], Series[str], str]]
             Name for Region (geography), by default None
         concept: Optional[Union[list[str], Series[str], str]]
             Concept that describes what the dataset is, by default None
         date: Optional[date], optional
             Date, by default None
         date_gt: Optional[date], optional
             filter by '' date > x '', by default None
         date_gte: Optional[date], optional
             filter by date, by default None
         date_lt: Optional[date], optional
             filter by date, by default None
         date_lte: Optional[date], optional
             filter by date, by default None
         value: Optional[str], optional
             Data Value, by default None
         value_gt: Optional[str], optional
             filter by '' value > x '', by default None
         value_gte: Optional[str], optional
             filter by value, by default None
         value_lt: Optional[str], optional
             filter by value, by default None
         value_lte: Optional[str], optional
             filter by value, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Name for Unit of Measure (volume), by default None
         data_type: Optional[Union[list[str], Series[str], str]]
             Data Type (history or forecast), by default None
         valid_to: Optional[date], optional
             End Date of Record Validity, by default None
         valid_to_gt: Optional[date], optional
             filter by '' valid_to > x '', by default None
         valid_to_gte: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lt: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lte: Optional[date], optional
             filter by valid_to, by default None
         valid_from: Optional[date], optional
             As of date for when the data is updated, by default None
         valid_from_gt: Optional[date], optional
             filter by '' valid_from > x '', by default None
         valid_from_gte: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lt: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lte: Optional[date], optional
             filter by valid_from, by default None
         modified_date: Optional[datetime], optional
             Date when the data is last modified, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             If the record is active, by default None
         end_use: Optional[Union[list[str], Series[str], str]]
             Product (chemical commodity) End Use, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("forecast_period", forecast_period))
        filter_params.append(list_to_filter("scenario_id", scenario_id))
        if scenario_id_gt is not None:
            filter_params.append(f'scenario_id > "{scenario_id_gt}"')
        if scenario_id_gte is not None:
            filter_params.append(f'scenario_id >= "{scenario_id_gte}"')
        if scenario_id_lt is not None:
            filter_params.append(f'scenario_id < "{scenario_id_lt}"')
        if scenario_id_lte is not None:
            filter_params.append(f'scenario_id <= "{scenario_id_lte}"')
        filter_params.append(
            list_to_filter("scenario_description", scenario_description)
        )
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("date", date))
        if date_gt is not None:
            filter_params.append(f'date > "{date_gt}"')
        if date_gte is not None:
            filter_params.append(f'date >= "{date_gte}"')
        if date_lt is not None:
            filter_params.append(f'date < "{date_lt}"')
        if date_lte is not None:
            filter_params.append(f'date <= "{date_lte}"')
        filter_params.append(list_to_filter("value", value))
        if value_gt is not None:
            filter_params.append(f'value > "{value_gt}"')
        if value_gte is not None:
            filter_params.append(f'value >= "{value_gte}"')
        if value_lt is not None:
            filter_params.append(f'value < "{value_lt}"')
        if value_lte is not None:
            filter_params.append(f'value <= "{value_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("data_type", data_type))
        filter_params.append(list_to_filter("valid_to", valid_to))
        if valid_to_gt is not None:
            filter_params.append(f'valid_to > "{valid_to_gt}"')
        if valid_to_gte is not None:
            filter_params.append(f'valid_to >= "{valid_to_gte}"')
        if valid_to_lt is not None:
            filter_params.append(f'valid_to < "{valid_to_lt}"')
        if valid_to_lte is not None:
            filter_params.append(f'valid_to <= "{valid_to_lte}"')
        filter_params.append(list_to_filter("valid_from", valid_from))
        if valid_from_gt is not None:
            filter_params.append(f'valid_from > "{valid_from_gt}"')
        if valid_from_gte is not None:
            filter_params.append(f'valid_from >= "{valid_from_gte}"')
        if valid_from_lt is not None:
            filter_params.append(f'valid_from < "{valid_from_lt}"')
        if valid_from_lte is not None:
            filter_params.append(f'valid_from <= "{valid_from_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')
        filter_params.append(list_to_filter("is_active", is_active))
        filter_params.append(list_to_filter("end_use", end_use))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/v1/chemicals/demand-by-end-use",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_trade(
        self,
        *,
        forecast_period: Optional[Union[list[str], Series[str], str]] = None,
        scenario_id: Optional[int] = None,
        scenario_id_lt: Optional[int] = None,
        scenario_id_lte: Optional[int] = None,
        scenario_id_gt: Optional[int] = None,
        scenario_id_gte: Optional[int] = None,
        scenario_description: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        country: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        date: Optional[date] = None,
        date_lt: Optional[date] = None,
        date_lte: Optional[date] = None,
        date_gt: Optional[date] = None,
        date_gte: Optional[date] = None,
        value: Optional[str] = None,
        value_lt: Optional[str] = None,
        value_lte: Optional[str] = None,
        value_gt: Optional[str] = None,
        value_gte: Optional[str] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        data_type: Optional[Union[list[str], Series[str], str]] = None,
        valid_to: Optional[date] = None,
        valid_to_lt: Optional[date] = None,
        valid_to_lte: Optional[date] = None,
        valid_to_gt: Optional[date] = None,
        valid_to_gte: Optional[date] = None,
        valid_from: Optional[date] = None,
        valid_from_lt: Optional[date] = None,
        valid_from_lte: Optional[date] = None,
        valid_from_gt: Optional[date] = None,
        valid_from_gte: Optional[date] = None,
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
        Country-level trade (import, export and net trade) for a product

        Parameters
        ----------

         forecast_period: Optional[Union[list[str], Series[str], str]]
             Long term or short term, by default None
         scenario_id: Optional[int], optional
             Scenario ID, by default None
         scenario_id_gt: Optional[int], optional
             filter by '' scenario_id > x '', by default None
         scenario_id_gte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lt: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_description: Optional[Union[list[str], Series[str], str]]
             Scenario Description, by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             Name for Product (chemical commodity), by default None
         country: Optional[Union[list[str], Series[str], str]]
             Name for Country (geography), by default None
         region: Optional[Union[list[str], Series[str], str]]
             Name for Region (geography), by default None
         concept: Optional[Union[list[str], Series[str], str]]
             Concept that describes what the dataset is, by default None
         date: Optional[date], optional
             Date, by default None
         date_gt: Optional[date], optional
             filter by '' date > x '', by default None
         date_gte: Optional[date], optional
             filter by date, by default None
         date_lt: Optional[date], optional
             filter by date, by default None
         date_lte: Optional[date], optional
             filter by date, by default None
         value: Optional[str], optional
             Data Value, by default None
         value_gt: Optional[str], optional
             filter by '' value > x '', by default None
         value_gte: Optional[str], optional
             filter by value, by default None
         value_lt: Optional[str], optional
             filter by value, by default None
         value_lte: Optional[str], optional
             filter by value, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Name for Unit of Measure (volume), by default None
         data_type: Optional[Union[list[str], Series[str], str]]
             Data Type (history or forecast), by default None
         valid_to: Optional[date], optional
             End Date of Record Validity, by default None
         valid_to_gt: Optional[date], optional
             filter by '' valid_to > x '', by default None
         valid_to_gte: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lt: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lte: Optional[date], optional
             filter by valid_to, by default None
         valid_from: Optional[date], optional
             As of date for when the data is updated, by default None
         valid_from_gt: Optional[date], optional
             filter by '' valid_from > x '', by default None
         valid_from_gte: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lt: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lte: Optional[date], optional
             filter by valid_from, by default None
         modified_date: Optional[datetime], optional
             Date when the data is last modified, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             If the record is active, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("forecast_period", forecast_period))
        filter_params.append(list_to_filter("scenario_id", scenario_id))
        if scenario_id_gt is not None:
            filter_params.append(f'scenario_id > "{scenario_id_gt}"')
        if scenario_id_gte is not None:
            filter_params.append(f'scenario_id >= "{scenario_id_gte}"')
        if scenario_id_lt is not None:
            filter_params.append(f'scenario_id < "{scenario_id_lt}"')
        if scenario_id_lte is not None:
            filter_params.append(f'scenario_id <= "{scenario_id_lte}"')
        filter_params.append(
            list_to_filter("scenario_description", scenario_description)
        )
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("date", date))
        if date_gt is not None:
            filter_params.append(f'date > "{date_gt}"')
        if date_gte is not None:
            filter_params.append(f'date >= "{date_gte}"')
        if date_lt is not None:
            filter_params.append(f'date < "{date_lt}"')
        if date_lte is not None:
            filter_params.append(f'date <= "{date_lte}"')
        filter_params.append(list_to_filter("value", value))
        if value_gt is not None:
            filter_params.append(f'value > "{value_gt}"')
        if value_gte is not None:
            filter_params.append(f'value >= "{value_gte}"')
        if value_lt is not None:
            filter_params.append(f'value < "{value_lt}"')
        if value_lte is not None:
            filter_params.append(f'value <= "{value_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("data_type", data_type))
        filter_params.append(list_to_filter("valid_to", valid_to))
        if valid_to_gt is not None:
            filter_params.append(f'valid_to > "{valid_to_gt}"')
        if valid_to_gte is not None:
            filter_params.append(f'valid_to >= "{valid_to_gte}"')
        if valid_to_lt is not None:
            filter_params.append(f'valid_to < "{valid_to_lt}"')
        if valid_to_lte is not None:
            filter_params.append(f'valid_to <= "{valid_to_lte}"')
        filter_params.append(list_to_filter("valid_from", valid_from))
        if valid_from_gt is not None:
            filter_params.append(f'valid_from > "{valid_from_gt}"')
        if valid_from_gte is not None:
            filter_params.append(f'valid_from >= "{valid_from_gte}"')
        if valid_from_lt is not None:
            filter_params.append(f'valid_from < "{valid_from_lt}"')
        if valid_from_lte is not None:
            filter_params.append(f'valid_from <= "{valid_from_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')
        filter_params.append(list_to_filter("is_active", is_active))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/v1/chemicals/trade",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_inventory_change(
        self,
        *,
        forecast_period: Optional[Union[list[str], Series[str], str]] = None,
        scenario_id: Optional[int] = None,
        scenario_id_lt: Optional[int] = None,
        scenario_id_lte: Optional[int] = None,
        scenario_id_gt: Optional[int] = None,
        scenario_id_gte: Optional[int] = None,
        scenario_description: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        country: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        date: Optional[date] = None,
        date_lt: Optional[date] = None,
        date_lte: Optional[date] = None,
        date_gt: Optional[date] = None,
        date_gte: Optional[date] = None,
        value: Optional[str] = None,
        value_lt: Optional[str] = None,
        value_lte: Optional[str] = None,
        value_gt: Optional[str] = None,
        value_gte: Optional[str] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        data_type: Optional[Union[list[str], Series[str], str]] = None,
        valid_to: Optional[date] = None,
        valid_to_lt: Optional[date] = None,
        valid_to_lte: Optional[date] = None,
        valid_to_gt: Optional[date] = None,
        valid_to_gte: Optional[date] = None,
        valid_from: Optional[date] = None,
        valid_from_lt: Optional[date] = None,
        valid_from_lte: Optional[date] = None,
        valid_from_gt: Optional[date] = None,
        valid_from_gte: Optional[date] = None,
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
        Country-level inventory change data

        Parameters
        ----------

         forecast_period: Optional[Union[list[str], Series[str], str]]
             Long term or short term, by default None
         scenario_id: Optional[int], optional
             Scenario ID, by default None
         scenario_id_gt: Optional[int], optional
             filter by '' scenario_id > x '', by default None
         scenario_id_gte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lt: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_description: Optional[Union[list[str], Series[str], str]]
             Scenario Description, by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             Name for Product (chemical commodity), by default None
         country: Optional[Union[list[str], Series[str], str]]
             Name for Country (geography), by default None
         region: Optional[Union[list[str], Series[str], str]]
             Name for Region (geography), by default None
         concept: Optional[Union[list[str], Series[str], str]]
             Concept that describes what the dataset is, by default None
         date: Optional[date], optional
             Date, by default None
         date_gt: Optional[date], optional
             filter by '' date > x '', by default None
         date_gte: Optional[date], optional
             filter by date, by default None
         date_lt: Optional[date], optional
             filter by date, by default None
         date_lte: Optional[date], optional
             filter by date, by default None
         value: Optional[str], optional
             Data Value, by default None
         value_gt: Optional[str], optional
             filter by '' value > x '', by default None
         value_gte: Optional[str], optional
             filter by value, by default None
         value_lt: Optional[str], optional
             filter by value, by default None
         value_lte: Optional[str], optional
             filter by value, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Name for Unit of Measure (volume), by default None
         data_type: Optional[Union[list[str], Series[str], str]]
             Data Type (history or forecast), by default None
         valid_to: Optional[date], optional
             End Date of Record Validity, by default None
         valid_to_gt: Optional[date], optional
             filter by '' valid_to > x '', by default None
         valid_to_gte: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lt: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lte: Optional[date], optional
             filter by valid_to, by default None
         valid_from: Optional[date], optional
             As of date for when the data is updated, by default None
         valid_from_gt: Optional[date], optional
             filter by '' valid_from > x '', by default None
         valid_from_gte: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lt: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lte: Optional[date], optional
             filter by valid_from, by default None
         modified_date: Optional[datetime], optional
             Date when the data is last modified, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             If the record is active, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("forecast_period", forecast_period))
        filter_params.append(list_to_filter("scenario_id", scenario_id))
        if scenario_id_gt is not None:
            filter_params.append(f'scenario_id > "{scenario_id_gt}"')
        if scenario_id_gte is not None:
            filter_params.append(f'scenario_id >= "{scenario_id_gte}"')
        if scenario_id_lt is not None:
            filter_params.append(f'scenario_id < "{scenario_id_lt}"')
        if scenario_id_lte is not None:
            filter_params.append(f'scenario_id <= "{scenario_id_lte}"')
        filter_params.append(
            list_to_filter("scenario_description", scenario_description)
        )
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("date", date))
        if date_gt is not None:
            filter_params.append(f'date > "{date_gt}"')
        if date_gte is not None:
            filter_params.append(f'date >= "{date_gte}"')
        if date_lt is not None:
            filter_params.append(f'date < "{date_lt}"')
        if date_lte is not None:
            filter_params.append(f'date <= "{date_lte}"')
        filter_params.append(list_to_filter("value", value))
        if value_gt is not None:
            filter_params.append(f'value > "{value_gt}"')
        if value_gte is not None:
            filter_params.append(f'value >= "{value_gte}"')
        if value_lt is not None:
            filter_params.append(f'value < "{value_lt}"')
        if value_lte is not None:
            filter_params.append(f'value <= "{value_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("data_type", data_type))
        filter_params.append(list_to_filter("valid_to", valid_to))
        if valid_to_gt is not None:
            filter_params.append(f'valid_to > "{valid_to_gt}"')
        if valid_to_gte is not None:
            filter_params.append(f'valid_to >= "{valid_to_gte}"')
        if valid_to_lt is not None:
            filter_params.append(f'valid_to < "{valid_to_lt}"')
        if valid_to_lte is not None:
            filter_params.append(f'valid_to <= "{valid_to_lte}"')
        filter_params.append(list_to_filter("valid_from", valid_from))
        if valid_from_gt is not None:
            filter_params.append(f'valid_from > "{valid_from_gt}"')
        if valid_from_gte is not None:
            filter_params.append(f'valid_from >= "{valid_from_gte}"')
        if valid_from_lt is not None:
            filter_params.append(f'valid_from < "{valid_from_lt}"')
        if valid_from_lte is not None:
            filter_params.append(f'valid_from <= "{valid_from_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')
        filter_params.append(list_to_filter("is_active", is_active))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/v1/chemicals/inventory-change",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_total_supply(
        self,
        *,
        forecast_period: Optional[Union[list[str], Series[str], str]] = None,
        scenario_id: Optional[int] = None,
        scenario_id_lt: Optional[int] = None,
        scenario_id_lte: Optional[int] = None,
        scenario_id_gt: Optional[int] = None,
        scenario_id_gte: Optional[int] = None,
        scenario_description: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        country: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        date: Optional[date] = None,
        date_lt: Optional[date] = None,
        date_lte: Optional[date] = None,
        date_gt: Optional[date] = None,
        date_gte: Optional[date] = None,
        value: Optional[str] = None,
        value_lt: Optional[str] = None,
        value_lte: Optional[str] = None,
        value_gt: Optional[str] = None,
        value_gte: Optional[str] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        data_type: Optional[Union[list[str], Series[str], str]] = None,
        valid_to: Optional[date] = None,
        valid_to_lt: Optional[date] = None,
        valid_to_lte: Optional[date] = None,
        valid_to_gt: Optional[date] = None,
        valid_to_gte: Optional[date] = None,
        valid_from: Optional[date] = None,
        valid_from_lt: Optional[date] = None,
        valid_from_lte: Optional[date] = None,
        valid_from_gt: Optional[date] = None,
        valid_from_gte: Optional[date] = None,
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
        Country-level total supply data for a product

        Parameters
        ----------

         forecast_period: Optional[Union[list[str], Series[str], str]]
             Long term or short term, by default None
         scenario_id: Optional[int], optional
             Scenario ID, by default None
         scenario_id_gt: Optional[int], optional
             filter by '' scenario_id > x '', by default None
         scenario_id_gte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lt: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_description: Optional[Union[list[str], Series[str], str]]
             Scenario Description, by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             Name for Product (chemical commodity), by default None
         country: Optional[Union[list[str], Series[str], str]]
             Name for Country (geography), by default None
         region: Optional[Union[list[str], Series[str], str]]
             Name for Region (geography), by default None
         concept: Optional[Union[list[str], Series[str], str]]
             Concept that describes what the dataset is, by default None
         date: Optional[date], optional
             Date, by default None
         date_gt: Optional[date], optional
             filter by '' date > x '', by default None
         date_gte: Optional[date], optional
             filter by date, by default None
         date_lt: Optional[date], optional
             filter by date, by default None
         date_lte: Optional[date], optional
             filter by date, by default None
         value: Optional[str], optional
             Data Value, by default None
         value_gt: Optional[str], optional
             filter by '' value > x '', by default None
         value_gte: Optional[str], optional
             filter by value, by default None
         value_lt: Optional[str], optional
             filter by value, by default None
         value_lte: Optional[str], optional
             filter by value, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Name for Unit of Measure (volume), by default None
         data_type: Optional[Union[list[str], Series[str], str]]
             Data Type (history or forecast), by default None
         valid_to: Optional[date], optional
             End Date of Record Validity, by default None
         valid_to_gt: Optional[date], optional
             filter by '' valid_to > x '', by default None
         valid_to_gte: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lt: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lte: Optional[date], optional
             filter by valid_to, by default None
         valid_from: Optional[date], optional
             As of date for when the data is updated, by default None
         valid_from_gt: Optional[date], optional
             filter by '' valid_from > x '', by default None
         valid_from_gte: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lt: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lte: Optional[date], optional
             filter by valid_from, by default None
         modified_date: Optional[datetime], optional
             Date when the data is last modified, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             If the record is active, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("forecast_period", forecast_period))
        filter_params.append(list_to_filter("scenario_id", scenario_id))
        if scenario_id_gt is not None:
            filter_params.append(f'scenario_id > "{scenario_id_gt}"')
        if scenario_id_gte is not None:
            filter_params.append(f'scenario_id >= "{scenario_id_gte}"')
        if scenario_id_lt is not None:
            filter_params.append(f'scenario_id < "{scenario_id_lt}"')
        if scenario_id_lte is not None:
            filter_params.append(f'scenario_id <= "{scenario_id_lte}"')
        filter_params.append(
            list_to_filter("scenario_description", scenario_description)
        )
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("date", date))
        if date_gt is not None:
            filter_params.append(f'date > "{date_gt}"')
        if date_gte is not None:
            filter_params.append(f'date >= "{date_gte}"')
        if date_lt is not None:
            filter_params.append(f'date < "{date_lt}"')
        if date_lte is not None:
            filter_params.append(f'date <= "{date_lte}"')
        filter_params.append(list_to_filter("value", value))
        if value_gt is not None:
            filter_params.append(f'value > "{value_gt}"')
        if value_gte is not None:
            filter_params.append(f'value >= "{value_gte}"')
        if value_lt is not None:
            filter_params.append(f'value < "{value_lt}"')
        if value_lte is not None:
            filter_params.append(f'value <= "{value_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("data_type", data_type))
        filter_params.append(list_to_filter("valid_to", valid_to))
        if valid_to_gt is not None:
            filter_params.append(f'valid_to > "{valid_to_gt}"')
        if valid_to_gte is not None:
            filter_params.append(f'valid_to >= "{valid_to_gte}"')
        if valid_to_lt is not None:
            filter_params.append(f'valid_to < "{valid_to_lt}"')
        if valid_to_lte is not None:
            filter_params.append(f'valid_to <= "{valid_to_lte}"')
        filter_params.append(list_to_filter("valid_from", valid_from))
        if valid_from_gt is not None:
            filter_params.append(f'valid_from > "{valid_from_gt}"')
        if valid_from_gte is not None:
            filter_params.append(f'valid_from >= "{valid_from_gte}"')
        if valid_from_lt is not None:
            filter_params.append(f'valid_from < "{valid_from_lt}"')
        if valid_from_lte is not None:
            filter_params.append(f'valid_from <= "{valid_from_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')
        filter_params.append(list_to_filter("is_active", is_active))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/v1/chemicals/total-supply",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_total_demand(
        self,
        *,
        forecast_period: Optional[Union[list[str], Series[str], str]] = None,
        scenario_id: Optional[int] = None,
        scenario_id_lt: Optional[int] = None,
        scenario_id_lte: Optional[int] = None,
        scenario_id_gt: Optional[int] = None,
        scenario_id_gte: Optional[int] = None,
        scenario_description: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        country: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        date: Optional[date] = None,
        date_lt: Optional[date] = None,
        date_lte: Optional[date] = None,
        date_gt: Optional[date] = None,
        date_gte: Optional[date] = None,
        value: Optional[str] = None,
        value_lt: Optional[str] = None,
        value_lte: Optional[str] = None,
        value_gt: Optional[str] = None,
        value_gte: Optional[str] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        data_type: Optional[Union[list[str], Series[str], str]] = None,
        valid_to: Optional[date] = None,
        valid_to_lt: Optional[date] = None,
        valid_to_lte: Optional[date] = None,
        valid_to_gt: Optional[date] = None,
        valid_to_gte: Optional[date] = None,
        valid_from: Optional[date] = None,
        valid_from_lt: Optional[date] = None,
        valid_from_lte: Optional[date] = None,
        valid_from_gt: Optional[date] = None,
        valid_from_gte: Optional[date] = None,
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
        Country-level total demand data for a product

        Parameters
        ----------

         forecast_period: Optional[Union[list[str], Series[str], str]]
             Long term or short term, by default None
         scenario_id: Optional[int], optional
             Scenario ID, by default None
         scenario_id_gt: Optional[int], optional
             filter by '' scenario_id > x '', by default None
         scenario_id_gte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lt: Optional[int], optional
             filter by scenario_id, by default None
         scenario_id_lte: Optional[int], optional
             filter by scenario_id, by default None
         scenario_description: Optional[Union[list[str], Series[str], str]]
             Scenario Description, by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             Name for Product (chemical commodity), by default None
         country: Optional[Union[list[str], Series[str], str]]
             Name for Country (geography), by default None
         region: Optional[Union[list[str], Series[str], str]]
             Name for Region (geography), by default None
         concept: Optional[Union[list[str], Series[str], str]]
             Concept that describes what the dataset is, by default None
         date: Optional[date], optional
             Date, by default None
         date_gt: Optional[date], optional
             filter by '' date > x '', by default None
         date_gte: Optional[date], optional
             filter by date, by default None
         date_lt: Optional[date], optional
             filter by date, by default None
         date_lte: Optional[date], optional
             filter by date, by default None
         value: Optional[str], optional
             Data Value, by default None
         value_gt: Optional[str], optional
             filter by '' value > x '', by default None
         value_gte: Optional[str], optional
             filter by value, by default None
         value_lt: Optional[str], optional
             filter by value, by default None
         value_lte: Optional[str], optional
             filter by value, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Name for Unit of Measure (volume), by default None
         data_type: Optional[Union[list[str], Series[str], str]]
             Data Type (history or forecast), by default None
         valid_to: Optional[date], optional
             End Date of Record Validity, by default None
         valid_to_gt: Optional[date], optional
             filter by '' valid_to > x '', by default None
         valid_to_gte: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lt: Optional[date], optional
             filter by valid_to, by default None
         valid_to_lte: Optional[date], optional
             filter by valid_to, by default None
         valid_from: Optional[date], optional
             As of date for when the data is updated, by default None
         valid_from_gt: Optional[date], optional
             filter by '' valid_from > x '', by default None
         valid_from_gte: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lt: Optional[date], optional
             filter by valid_from, by default None
         valid_from_lte: Optional[date], optional
             filter by valid_from, by default None
         modified_date: Optional[datetime], optional
             Date when the data is last modified, by default None
         modified_date_gt: Optional[datetime], optional
             filter by '' modified_date > x '', by default None
         modified_date_gte: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lt: Optional[datetime], optional
             filter by modified_date, by default None
         modified_date_lte: Optional[datetime], optional
             filter by modified_date, by default None
         is_active: Optional[Union[list[str], Series[str], str]]
             If the record is active, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("forecast_period", forecast_period))
        filter_params.append(list_to_filter("scenario_id", scenario_id))
        if scenario_id_gt is not None:
            filter_params.append(f'scenario_id > "{scenario_id_gt}"')
        if scenario_id_gte is not None:
            filter_params.append(f'scenario_id >= "{scenario_id_gte}"')
        if scenario_id_lt is not None:
            filter_params.append(f'scenario_id < "{scenario_id_lt}"')
        if scenario_id_lte is not None:
            filter_params.append(f'scenario_id <= "{scenario_id_lte}"')
        filter_params.append(
            list_to_filter("scenario_description", scenario_description)
        )
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("date", date))
        if date_gt is not None:
            filter_params.append(f'date > "{date_gt}"')
        if date_gte is not None:
            filter_params.append(f'date >= "{date_gte}"')
        if date_lt is not None:
            filter_params.append(f'date < "{date_lt}"')
        if date_lte is not None:
            filter_params.append(f'date <= "{date_lte}"')
        filter_params.append(list_to_filter("value", value))
        if value_gt is not None:
            filter_params.append(f'value > "{value_gt}"')
        if value_gte is not None:
            filter_params.append(f'value >= "{value_gte}"')
        if value_lt is not None:
            filter_params.append(f'value < "{value_lt}"')
        if value_lte is not None:
            filter_params.append(f'value <= "{value_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("data_type", data_type))
        filter_params.append(list_to_filter("valid_to", valid_to))
        if valid_to_gt is not None:
            filter_params.append(f'valid_to > "{valid_to_gt}"')
        if valid_to_gte is not None:
            filter_params.append(f'valid_to >= "{valid_to_gte}"')
        if valid_to_lt is not None:
            filter_params.append(f'valid_to < "{valid_to_lt}"')
        if valid_to_lte is not None:
            filter_params.append(f'valid_to <= "{valid_to_lte}"')
        filter_params.append(list_to_filter("valid_from", valid_from))
        if valid_from_gt is not None:
            filter_params.append(f'valid_from > "{valid_from_gt}"')
        if valid_from_gte is not None:
            filter_params.append(f'valid_from >= "{valid_from_gte}"')
        if valid_from_lt is not None:
            filter_params.append(f'valid_from < "{valid_from_lt}"')
        if valid_from_lte is not None:
            filter_params.append(f'valid_from <= "{valid_from_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')
        filter_params.append(list_to_filter("is_active", is_active))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/v1/chemicals/total-demand",
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

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])  # type: ignore

        if "valid_to" in df.columns:
            df["valid_to"] = pd.to_datetime(df["valid_to"])  # type: ignore

        if "valid_from" in df.columns:
            df["valid_from"] = pd.to_datetime(df["valid_from"])  # type: ignore

        if "modifiedDate" in df.columns:
            df["modifiedDate"] = pd.to_datetime(df["modifiedDate"])  # type: ignore
        return df
