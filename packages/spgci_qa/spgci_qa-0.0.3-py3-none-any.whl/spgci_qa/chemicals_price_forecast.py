from __future__ import annotations
from typing import List, Optional, Union
from requests import Response
from spgci_qa.api_client import get_data
from spgci_qa.utilities import list_to_filter
from pandas import DataFrame, Series
from datetime import date, datetime
import pandas as pd


class Chemicals_price_forecast:
    _endpoint = "api/v1/"
    _reference_endpoint = "reference/v1/"
    _price_forecast_lt_api_endpoint = "/long-term-prices"
    _price_forecast_st_api_endpoint = "/short-term-prices"

    def get_long_term_prices(
        self,
        *,
        scenario_id: Optional[int] = None,
        scenario_id_lt: Optional[int] = None,
        scenario_id_lte: Optional[int] = None,
        scenario_id_gt: Optional[int] = None,
        scenario_id_gte: Optional[int] = None,
        scenario_description: Optional[Union[list[str], Series[str], str]] = None,
        series_description: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        commodity_grade: Optional[Union[list[str], Series[str], str]] = None,
        associated_platts_symbol: Optional[Union[list[str], Series[str], str]] = None,
        delivery_region: Optional[Union[list[str], Series[str], str]] = None,
        shipping_terms: Optional[Union[list[str], Series[str], str]] = None,
        currency: Optional[Union[list[str], Series[str], str]] = None,
        contract_type: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        data_type: Optional[Union[list[str], Series[str], str]] = None,
        value: Optional[float] = None,
        value_lt: Optional[float] = None,
        value_lte: Optional[float] = None,
        value_gt: Optional[float] = None,
        value_gte: Optional[float] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        publish_date: Optional[datetime] = None,
        publish_date_lt: Optional[datetime] = None,
        publish_date_lte: Optional[datetime] = None,
        publish_date_gt: Optional[datetime] = None,
        publish_date_gte: Optional[datetime] = None,
        year: Optional[int] = None,
        year_lt: Optional[int] = None,
        year_lte: Optional[int] = None,
        year_gt: Optional[int] = None,
        year_gte: Optional[int] = None,
        valid_to: Optional[datetime] = None,
        valid_to_lt: Optional[datetime] = None,
        valid_to_lte: Optional[datetime] = None,
        valid_to_gt: Optional[datetime] = None,
        valid_to_gte: Optional[datetime] = None,
        valid_from: Optional[datetime] = None,
        valid_from_lt: Optional[datetime] = None,
        valid_from_lte: Optional[datetime] = None,
        valid_from_gt: Optional[datetime] = None,
        valid_from_gte: Optional[datetime] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        is_active: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Long-term price and margin forecasts

        Parameters
        ----------

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
         series_description: Optional[Union[list[str], Series[str], str]]
             Price Series Description, by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             Name for Product (chemical commodity), by default None
         commodity_grade: Optional[Union[list[str], Series[str], str]]
             Commodity Grade, by default None
         associated_platts_symbol: Optional[Union[list[str], Series[str], str]]
             Associated Platts Symbol, by default None
         delivery_region: Optional[Union[list[str], Series[str], str]]
             Delivery Region, by default None
         shipping_terms: Optional[Union[list[str], Series[str], str]]
             Shipping Terms, by default None
         currency: Optional[Union[list[str], Series[str], str]]
             Currency, by default None
         contract_type: Optional[Union[list[str], Series[str], str]]
             Contract Type, by default None
         concept: Optional[Union[list[str], Series[str], str]]
             Concept that describes what the dataset is, by default None
         data_type: Optional[Union[list[str], Series[str], str]]
             Data Type (history or forecast), by default None
         value: Optional[float], optional
             Data Value, by default None
         value_gt: Optional[float], optional
             filter by '' value > x '', by default None
         value_gte: Optional[float], optional
             filter by value, by default None
         value_lt: Optional[float], optional
             filter by value, by default None
         value_lte: Optional[float], optional
             filter by value, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Name for Unit of Measure (volume), by default None
         publish_date: Optional[datetime], optional
             Publish Date, by default None
         publish_date_gt: Optional[datetime], optional
             filter by '' publish_date > x '', by default None
         publish_date_gte: Optional[datetime], optional
             filter by publish_date, by default None
         publish_date_lt: Optional[datetime], optional
             filter by publish_date, by default None
         publish_date_lte: Optional[datetime], optional
             filter by publish_date, by default None
         year: Optional[int], optional
             year, by default None
         year_gt: Optional[int], optional
             filter by '' year > x '', by default None
         year_gte: Optional[int], optional
             filter by year, by default None
         year_lt: Optional[int], optional
             filter by year, by default None
         year_lte: Optional[int], optional
             filter by year, by default None
         valid_to: Optional[datetime], optional
             End Date of Record Validity, by default None
         valid_to_gt: Optional[datetime], optional
             filter by '' valid_to > x '', by default None
         valid_to_gte: Optional[datetime], optional
             filter by valid_to, by default None
         valid_to_lt: Optional[datetime], optional
             filter by valid_to, by default None
         valid_to_lte: Optional[datetime], optional
             filter by valid_to, by default None
         valid_from: Optional[datetime], optional
             As of date for when the data is updated, by default None
         valid_from_gt: Optional[datetime], optional
             filter by '' valid_from > x '', by default None
         valid_from_gte: Optional[datetime], optional
             filter by valid_from, by default None
         valid_from_lt: Optional[datetime], optional
             filter by valid_from, by default None
         valid_from_lte: Optional[datetime], optional
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
         region: Optional[Union[list[str], Series[str], str]]
             Name for Region (geography), by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
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
        filter_params.append(list_to_filter("series_description", series_description))
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("commodity_grade", commodity_grade))
        filter_params.append(
            list_to_filter("associated_platts_symbol", associated_platts_symbol)
        )
        filter_params.append(list_to_filter("delivery_region", delivery_region))
        filter_params.append(list_to_filter("shipping_terms", shipping_terms))
        filter_params.append(list_to_filter("currency", currency))
        filter_params.append(list_to_filter("contract_type", contract_type))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("dataType", data_type))
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
        filter_params.append(list_to_filter("publish_date", publish_date))
        if publish_date_gt is not None:
            filter_params.append(f'publish_date > "{publish_date_gt}"')
        if publish_date_gte is not None:
            filter_params.append(f'publish_date >= "{publish_date_gte}"')
        if publish_date_lt is not None:
            filter_params.append(f'publish_date < "{publish_date_lt}"')
        if publish_date_lte is not None:
            filter_params.append(f'publish_date <= "{publish_date_lte}"')
        filter_params.append(list_to_filter("year", year))
        if year_gt is not None:
            filter_params.append(f'year > "{year_gt}"')
        if year_gte is not None:
            filter_params.append(f'year >= "{year_gte}"')
        if year_lt is not None:
            filter_params.append(f'year < "{year_lt}"')
        if year_lte is not None:
            filter_params.append(f'year <= "{year_lte}"')
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
        filter_params.append(list_to_filter("region", region))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/v1/chemicals/price-forecast/long-term-prices",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_short_term_prices(
        self,
        *,
        scenario_id: Optional[int] = None,
        scenario_id_lt: Optional[int] = None,
        scenario_id_lte: Optional[int] = None,
        scenario_id_gt: Optional[int] = None,
        scenario_id_gte: Optional[int] = None,
        scenario_description: Optional[Union[list[str], Series[str], str]] = None,
        series_description: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        commodity_grade: Optional[Union[list[str], Series[str], str]] = None,
        associated_platts_symbol: Optional[Union[list[str], Series[str], str]] = None,
        delivery_region: Optional[Union[list[str], Series[str], str]] = None,
        shipping_terms: Optional[Union[list[str], Series[str], str]] = None,
        currency: Optional[Union[list[str], Series[str], str]] = None,
        contract_type: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        data_type: Optional[Union[list[str], Series[str], str]] = None,
        value: Optional[float] = None,
        value_lt: Optional[float] = None,
        value_lte: Optional[float] = None,
        value_gt: Optional[float] = None,
        value_gte: Optional[float] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        publish_date: Optional[datetime] = None,
        publish_date_lt: Optional[datetime] = None,
        publish_date_lte: Optional[datetime] = None,
        publish_date_gt: Optional[datetime] = None,
        publish_date_gte: Optional[datetime] = None,
        date: Optional[date] = None,
        date_lt: Optional[date] = None,
        date_lte: Optional[date] = None,
        date_gt: Optional[date] = None,
        date_gte: Optional[date] = None,
        valid_to: Optional[datetime] = None,
        valid_to_lt: Optional[datetime] = None,
        valid_to_lte: Optional[datetime] = None,
        valid_to_gt: Optional[datetime] = None,
        valid_to_gte: Optional[datetime] = None,
        valid_from: Optional[datetime] = None,
        valid_from_lt: Optional[datetime] = None,
        valid_from_lte: Optional[datetime] = None,
        valid_from_gt: Optional[datetime] = None,
        valid_from_gte: Optional[datetime] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        is_active: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Short-term price and margin forecasts

        Parameters
        ----------

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
         series_description: Optional[Union[list[str], Series[str], str]]
             Price Series Description, by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             Name for Product (chemical commodity), by default None
         commodity_grade: Optional[Union[list[str], Series[str], str]]
             Commodity Grade, by default None
         associated_platts_symbol: Optional[Union[list[str], Series[str], str]]
             Associated Platts Symbol, by default None
         delivery_region: Optional[Union[list[str], Series[str], str]]
             Delivery Region, by default None
         shipping_terms: Optional[Union[list[str], Series[str], str]]
             Shipping Terms, by default None
         currency: Optional[Union[list[str], Series[str], str]]
             Currency, by default None
         contract_type: Optional[Union[list[str], Series[str], str]]
             Contract Type, by default None
         concept: Optional[Union[list[str], Series[str], str]]
             Concept that describes what the dataset is, by default None
         data_type: Optional[Union[list[str], Series[str], str]]
             Data Type (history or forecast), by default None
         value: Optional[float], optional
             Data Value, by default None
         value_gt: Optional[float], optional
             filter by '' value > x '', by default None
         value_gte: Optional[float], optional
             filter by value, by default None
         value_lt: Optional[float], optional
             filter by value, by default None
         value_lte: Optional[float], optional
             filter by value, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Name for Unit of Measure (volume), by default None
         publish_date: Optional[datetime], optional
             Publish Date, by default None
         publish_date_gt: Optional[datetime], optional
             filter by '' publish_date > x '', by default None
         publish_date_gte: Optional[datetime], optional
             filter by publish_date, by default None
         publish_date_lt: Optional[datetime], optional
             filter by publish_date, by default None
         publish_date_lte: Optional[datetime], optional
             filter by publish_date, by default None
         date: Optional[date], optional
             year, by default None
         date_gt: Optional[date], optional
             filter by '' date > x '', by default None
         date_gte: Optional[date], optional
             filter by date, by default None
         date_lt: Optional[date], optional
             filter by date, by default None
         date_lte: Optional[date], optional
             filter by date, by default None
         valid_to: Optional[datetime], optional
             End Date of Record Validity, by default None
         valid_to_gt: Optional[datetime], optional
             filter by '' valid_to > x '', by default None
         valid_to_gte: Optional[datetime], optional
             filter by valid_to, by default None
         valid_to_lt: Optional[datetime], optional
             filter by valid_to, by default None
         valid_to_lte: Optional[datetime], optional
             filter by valid_to, by default None
         valid_from: Optional[datetime], optional
             As of date for when the data is updated, by default None
         valid_from_gt: Optional[datetime], optional
             filter by '' valid_from > x '', by default None
         valid_from_gte: Optional[datetime], optional
             filter by valid_from, by default None
         valid_from_lt: Optional[datetime], optional
             filter by valid_from, by default None
         valid_from_lte: Optional[datetime], optional
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
         region: Optional[Union[list[str], Series[str], str]]
             Name for Region (geography), by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
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
        filter_params.append(list_to_filter("series_description", series_description))
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("commodity_grade", commodity_grade))
        filter_params.append(
            list_to_filter("associated_platts_symbol", associated_platts_symbol)
        )
        filter_params.append(list_to_filter("delivery_region", delivery_region))
        filter_params.append(list_to_filter("shipping_terms", shipping_terms))
        filter_params.append(list_to_filter("currency", currency))
        filter_params.append(list_to_filter("contract_type", contract_type))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("dataType", data_type))
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
        filter_params.append(list_to_filter("publish_date", publish_date))
        if publish_date_gt is not None:
            filter_params.append(f'publish_date > "{publish_date_gt}"')
        if publish_date_gte is not None:
            filter_params.append(f'publish_date >= "{publish_date_gte}"')
        if publish_date_lt is not None:
            filter_params.append(f'publish_date < "{publish_date_lt}"')
        if publish_date_lte is not None:
            filter_params.append(f'publish_date <= "{publish_date_lte}"')
        filter_params.append(list_to_filter("date", date))
        if date_gt is not None:
            filter_params.append(f'date > "{date_gt}"')
        if date_gte is not None:
            filter_params.append(f'date >= "{date_gte}"')
        if date_lt is not None:
            filter_params.append(f'date < "{date_lt}"')
        if date_lte is not None:
            filter_params.append(f'date <= "{date_lte}"')
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
        filter_params.append(list_to_filter("region", region))

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/v1/chemicals/price-forecast/short-term-prices",
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

        if "publish_date" in df.columns:
            df["publish_date"] = pd.to_datetime(df["publish_date"])  # type: ignore

        if "valid_to" in df.columns:
            df["valid_to"] = pd.to_datetime(df["valid_to"])  # type: ignore

        if "valid_from" in df.columns:
            df["valid_from"] = pd.to_datetime(df["valid_from"])  # type: ignore

        if "modifiedDate" in df.columns:
            df["modifiedDate"] = pd.to_datetime(df["modifiedDate"])  # type: ignore

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])  # type: ignore

        if "created_date" in df.columns:
            df["created_date"] = pd.to_datetime(df["created_date"])  # type: ignore

        if "modified_date" in df.columns:
            df["modified_date"] = pd.to_datetime(df["modified_date"])  # type: ignore

        if "validFrom" in df.columns:
            df["validFrom"] = pd.to_datetime(df["validFrom"])  # type: ignore

        if "validTo" in df.columns:
            df["validTo"] = pd.to_datetime(df["validTo"])  # type: ignore
        return df
