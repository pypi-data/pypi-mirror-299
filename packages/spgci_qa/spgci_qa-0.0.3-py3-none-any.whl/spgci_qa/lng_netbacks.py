
from __future__ import annotations
from typing import List, Optional, Union
from requests import Response
from spgci_qa.api_client import get_data
from spgci_qa.utilities import list_to_filter
from pandas import DataFrame, Series
from datetime import date
import pandas as pd

class Lng_netbacks:
    _endpoint = "api/v1/"
    _reference_endpoint = "reference/v1/"
    _netbacks_endpoint = "/"


    def get_data(
        self, date: Optional[Union[list[date], Series[date], date]] = None, export_geography: Optional[Union[list[str], Series[str], str]] = None, import_geography: Optional[Union[list[str], Series[str], str]] = None, netback: Optional[Union[list[str], Series[str], str]] = None, modified_date: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         date: Optional[Union[list[date], Series[date], date]]
             The day for which the netback calculation is attributed to, be default None
         export_geography: Optional[Union[list[str], Series[str], str]]
             Geography where the LNG is exported from, be default None
         import_geography: Optional[Union[list[str], Series[str], str]]
             Geography where the LNG is imported to, be default None
         netback: Optional[Union[list[str], Series[str], str]]
             Price to the supplier after accounting for the 5-day moving average end market price and five-day moving average shipping cost based on the specified supply geography and import geography, be default None
         modified_date: Optional[Union[list[str], Series[str], str]]
             The latest date of modification for netbacks, be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("date", date))
        filter_params.append(list_to_filter("export_geography", export_geography))
        filter_params.append(list_to_filter("import_geography", import_geography))
        filter_params.append(list_to_filter("netback", netback))
        filter_params.append(list_to_filter("modified_date", modified_date))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/lng/v1/netbacks/",
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

        if "modified_date" in df.columns:
            df["modified_date"] = pd.to_datetime(df["modified_date"])  # type: ignore
        return df
    