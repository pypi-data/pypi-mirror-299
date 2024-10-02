from __future__ import annotations
from typing import List, Optional, Union
from requests import Response
from spgci_qa.api_client import get_data
from spgci_qa.utilities import list_to_filter
from pandas import DataFrame, Series
from datetime import date, datetime
import pandas as pd


class Chemical_outages:
    _endpoint = "api/v1/"
    _reference_endpoint = "reference/v1/"
    _petchem_outages_endpoint = "/"

    def get_data(
        self,
        *,
        unit_name: Optional[Union[list[str], Series[str], str]] = None,
        production_unit_code: Optional[Union[list[str], Series[str], str]] = None,
        alert_status: Optional[Union[list[str], Series[str], str]] = None,
        outage_id: Optional[Union[list[str], Series[str], str]] = None,
        plant_code: Optional[Union[list[str], Series[str], str]] = None,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        country: Optional[Union[list[str], Series[str], str]] = None,
        region: Optional[Union[list[str], Series[str], str]] = None,
        owner: Optional[Union[list[str], Series[str], str]] = None,
        outage_type: Optional[Union[list[str], Series[str], str]] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        capacity: Optional[float] = None,
        capacity_lt: Optional[float] = None,
        capacity_lte: Optional[float] = None,
        capacity_gt: Optional[float] = None,
        capacity_gte: Optional[float] = None,
        capacity_down: Optional[float] = None,
        capacity_down_lt: Optional[float] = None,
        capacity_down_lte: Optional[float] = None,
        capacity_down_gt: Optional[float] = None,
        capacity_down_gte: Optional[float] = None,
        run_rate: Optional[float] = None,
        run_rate_lt: Optional[float] = None,
        run_rate_lte: Optional[float] = None,
        run_rate_gt: Optional[float] = None,
        run_rate_gte: Optional[float] = None,
        modified_date: Optional[datetime] = None,
        modified_date_lt: Optional[datetime] = None,
        modified_date_lte: Optional[datetime] = None,
        modified_date_gt: Optional[datetime] = None,
        modified_date_gte: Optional[datetime] = None,
        start_date: Optional[datetime] = None,
        start_date_lt: Optional[datetime] = None,
        start_date_lte: Optional[datetime] = None,
        start_date_gt: Optional[datetime] = None,
        start_date_gte: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        end_date_lt: Optional[datetime] = None,
        end_date_lte: Optional[datetime] = None,
        end_date_gt: Optional[datetime] = None,
        end_date_gte: Optional[datetime] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Plant outage data including run rates, capacity loss, estimated start/end dates and products affected

        Parameters
        ----------

         unit_name: Optional[Union[list[str], Series[str], str]]
             Name for Production Unit, by default None
         production_unit_code: Optional[Union[list[str], Series[str], str]]
             Production Unit ID (Asset ID), by default None
         alert_status: Optional[Union[list[str], Series[str], str]]
             Alert Status (like Alert, Confirmed, Estimate, Revised Confirmed), by default None
         outage_id: Optional[Union[list[str], Series[str], str]]
             Outage ID, by default None
         plant_code: Optional[Union[list[str], Series[str], str]]
             Plant ID, by default None
         commodity: Optional[Union[list[str], Series[str], str]]
             Name for Product (chemical commodity), by default None
         country: Optional[Union[list[str], Series[str], str]]
             Name for Country (geography), by default None
         region: Optional[Union[list[str], Series[str], str]]
             Name for Region (geography), by default None
         owner: Optional[Union[list[str], Series[str], str]]
             Plant operator (producer), by default None
         outage_type: Optional[Union[list[str], Series[str], str]]
             Outage Type (like Planned, Unplanned, Economic Run Cut etc), by default None
         uom: Optional[Union[list[str], Series[str], str]]
             Name for Unit of Measure (volume), by default None
         capacity: Optional[float], optional
             Capacity Value, by default None
         capacity_gt: Optional[float], optional
             filter by '' capacity > x '', by default None
         capacity_gte: Optional[float], optional
             filter by capacity, by default None
         capacity_lt: Optional[float], optional
             filter by capacity, by default None
         capacity_lte: Optional[float], optional
             filter by capacity, by default None
         capacity_down: Optional[float], optional
             Capacity Loss, by default None
         capacity_down_gt: Optional[float], optional
             filter by '' capacity_down > x '', by default None
         capacity_down_gte: Optional[float], optional
             filter by capacity_down, by default None
         capacity_down_lt: Optional[float], optional
             filter by capacity_down, by default None
         capacity_down_lte: Optional[float], optional
             filter by capacity_down, by default None
         run_rate: Optional[float], optional
             Run Rate, by default None
         run_rate_gt: Optional[float], optional
             filter by '' run_rate > x '', by default None
         run_rate_gte: Optional[float], optional
             filter by run_rate, by default None
         run_rate_lt: Optional[float], optional
             filter by run_rate, by default None
         run_rate_lte: Optional[float], optional
             filter by run_rate, by default None
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
         start_date: Optional[datetime], optional
             Start Date, by default None
         start_date_gt: Optional[datetime], optional
             filter by '' start_date > x '', by default None
         start_date_gte: Optional[datetime], optional
             filter by start_date, by default None
         start_date_lt: Optional[datetime], optional
             filter by start_date, by default None
         start_date_lte: Optional[datetime], optional
             filter by start_date, by default None
         end_date: Optional[datetime], optional
             End Date, by default None
         end_date_gt: Optional[datetime], optional
             filter by '' end_date > x '', by default None
         end_date_gte: Optional[datetime], optional
             filter by end_date, by default None
         end_date_lt: Optional[datetime], optional
             filter by end_date, by default None
         end_date_lte: Optional[datetime], optional
             filter by end_date, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("unit_name", unit_name))
        filter_params.append(list_to_filter("productionUnitCode", production_unit_code))
        filter_params.append(list_to_filter("alertStatus", alert_status))
        filter_params.append(list_to_filter("outage_id", outage_id))
        filter_params.append(list_to_filter("plant_code", plant_code))
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("owner", owner))
        filter_params.append(list_to_filter("outage_type", outage_type))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("capacity", capacity))
        if capacity_gt is not None:
            filter_params.append(f'capacity > "{capacity_gt}"')
        if capacity_gte is not None:
            filter_params.append(f'capacity >= "{capacity_gte}"')
        if capacity_lt is not None:
            filter_params.append(f'capacity < "{capacity_lt}"')
        if capacity_lte is not None:
            filter_params.append(f'capacity <= "{capacity_lte}"')
        filter_params.append(list_to_filter("capacity_down", capacity_down))
        if capacity_down_gt is not None:
            filter_params.append(f'capacity_down > "{capacity_down_gt}"')
        if capacity_down_gte is not None:
            filter_params.append(f'capacity_down >= "{capacity_down_gte}"')
        if capacity_down_lt is not None:
            filter_params.append(f'capacity_down < "{capacity_down_lt}"')
        if capacity_down_lte is not None:
            filter_params.append(f'capacity_down <= "{capacity_down_lte}"')
        filter_params.append(list_to_filter("runRate", run_rate))
        if run_rate_gt is not None:
            filter_params.append(f'runRate > "{run_rate_gt}"')
        if run_rate_gte is not None:
            filter_params.append(f'runRate >= "{run_rate_gte}"')
        if run_rate_lt is not None:
            filter_params.append(f'runRate < "{run_rate_lt}"')
        if run_rate_lte is not None:
            filter_params.append(f'runRate <= "{run_rate_lte}"')
        filter_params.append(list_to_filter("modifiedDate", modified_date))
        if modified_date_gt is not None:
            filter_params.append(f'modifiedDate > "{modified_date_gt}"')
        if modified_date_gte is not None:
            filter_params.append(f'modifiedDate >= "{modified_date_gte}"')
        if modified_date_lt is not None:
            filter_params.append(f'modifiedDate < "{modified_date_lt}"')
        if modified_date_lte is not None:
            filter_params.append(f'modifiedDate <= "{modified_date_lte}"')
        filter_params.append(list_to_filter("start_date", start_date))
        if start_date_gt is not None:
            filter_params.append(f'start_date > "{start_date_gt}"')
        if start_date_gte is not None:
            filter_params.append(f'start_date >= "{start_date_gte}"')
        if start_date_lt is not None:
            filter_params.append(f'start_date < "{start_date_lt}"')
        if start_date_lte is not None:
            filter_params.append(f'start_date <= "{start_date_lte}"')
        filter_params.append(list_to_filter("end_date", end_date))
        if end_date_gt is not None:
            filter_params.append(f'end_date > "{end_date_gt}"')
        if end_date_gte is not None:
            filter_params.append(f'end_date >= "{end_date_gte}"')
        if end_date_lt is not None:
            filter_params.append(f'end_date < "{end_date_lt}"')
        if end_date_lte is not None:
            filter_params.append(f'end_date <= "{end_date_lte}"')

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/v1/chemicals/assets/outages/",
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

        if "start_date" in df.columns:
            df["start_date"] = pd.to_datetime(df["start_date"])  # type: ignore

        if "end_date" in df.columns:
            df["end_date"] = pd.to_datetime(df["end_date"])  # type: ignore
        return df
