from __future__ import annotations
from typing import List, Optional, Union
from requests import Response
from spgci_qa.api_client import get_data
from spgci_qa.utilities import list_to_filter
from pandas import DataFrame, Series
from datetime import date, datetime
import pandas as pd


class Weather:
    _endpoint = "api/v1/"
    _reference_endpoint = "reference/v1/"
    _lng_weather_actual_endpoint = "/actual"
    _lng_weather_forecast_endpoint = "/forecast"

    def get_actual(
        self,
        *,
        market: Optional[Union[list[str], Series[str], str]] = None,
        city: Optional[Union[list[str], Series[str], str]] = None,
        location: Optional[Union[list[str], Series[str], str]] = None,
        weather_date: Optional[date] = None,
        weather_date_lt: Optional[date] = None,
        weather_date_lte: Optional[date] = None,
        weather_date_gt: Optional[date] = None,
        weather_date_gte: Optional[date] = None,
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
        Access Historical and current Weather Actual Data.

        Parameters
        ----------

         market: Optional[Union[list[str], Series[str], str]]
             The market in which the weather data is recorded or observed., by default None
         city: Optional[Union[list[str], Series[str], str]]
             The specific city within the country for which the weather data is being reported., by default None
         location: Optional[Union[list[str], Series[str], str]]
             Weather station which provides Differentiator between country weather data and city weather data., by default None
         weather_date: Optional[date], optional
             The date for which the weather data is recorded or forecasted., by default None
         weather_date_gt: Optional[date], optional
             filter by `weather_date > x`, by default None
         weather_date_gte: Optional[date], optional
             filter by `weather_date >= x`, by default None
         weather_date_lt: Optional[date], optional
             filter by `weather_date < x`, by default None
         weather_date_lte: Optional[date], optional
             filter by `weather_date <= x`, by default None
         modified_date: Optional[datetime], optional
             The latest date of modification for the Weather Actual., by default None
         modified_date_gt: Optional[datetime], optional
             filter by `modified_date > x`, by default None
         modified_date_gte: Optional[datetime], optional
             filter by `modified_date >= x`, by default None
         modified_date_lt: Optional[datetime], optional
             filter by `modified_date < x`, by default None
         modified_date_lte: Optional[datetime], optional
             filter by `modified_date <= x`, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("market", market))
        filter_params.append(list_to_filter("city", city))
        filter_params.append(list_to_filter("location", location))
        filter_params.append(list_to_filter("weatherDate", weather_date))
        if weather_date_gt is not None:
            filter_params.append(f'weatherDate > "{weather_date_gt}"')
        if weather_date_gte is not None:
            filter_params.append(f'weatherDate >= "{weather_date_gte}"')
        if weather_date_lt is not None:
            filter_params.append(f'weatherDate < "{weather_date_lt}"')
        if weather_date_lte is not None:
            filter_params.append(f'weatherDate <= "{weather_date_lte}"')
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
            path=f"/weather/v1/actual",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_forecast(
        self,
        *,
        market: Optional[Union[list[str], Series[str], str]] = None,
        city: Optional[Union[list[str], Series[str], str]] = None,
        location: Optional[Union[list[str], Series[str], str]] = None,
        recorded_date: Optional[date] = None,
        recorded_date_lt: Optional[date] = None,
        recorded_date_lte: Optional[date] = None,
        recorded_date_gt: Optional[date] = None,
        recorded_date_gte: Optional[date] = None,
        weather_date: Optional[date] = None,
        weather_date_lt: Optional[date] = None,
        weather_date_lte: Optional[date] = None,
        weather_date_gt: Optional[date] = None,
        weather_date_gte: Optional[date] = None,
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
        Access Historical and current Weather Forecast Data.

        Parameters
        ----------

         market: Optional[Union[list[str], Series[str], str]]
             The market in which the weather data is recorded or observed., by default None
         city: Optional[Union[list[str], Series[str], str]]
             The specific city within the country for which the weather data is being reported., by default None
         location: Optional[Union[list[str], Series[str], str]]
             Weather station which provides Differentiator between country weather data and city weather data., by default None
         recorded_date: Optional[date], optional
             Recorded Date refers to the specific date on which weather updateds are recorded., by default None
         recorded_date_gt: Optional[date], optional
             filter by `recorded_date > x`, by default None
         recorded_date_gte: Optional[date], optional
             filter by `recorded_date >= x`, by default None
         recorded_date_lt: Optional[date], optional
             filter by `recorded_date < x`, by default None
         recorded_date_lte: Optional[date], optional
             filter by `recorded_date <= x`, by default None
         weather_date: Optional[date], optional
             The date for which the weather data is recorded or forecasted., by default None
         weather_date_gt: Optional[date], optional
             filter by `weather_date > x`, by default None
         weather_date_gte: Optional[date], optional
             filter by `weather_date >= x`, by default None
         weather_date_lt: Optional[date], optional
             filter by `weather_date < x`, by default None
         weather_date_lte: Optional[date], optional
             filter by `weather_date <= x`, by default None
         modified_date: Optional[datetime], optional
             The latest date of modification for the Weather Forecast., by default None
         modified_date_gt: Optional[datetime], optional
             filter by `modified_date > x`, by default None
         modified_date_gte: Optional[datetime], optional
             filter by `modified_date >= x`, by default None
         modified_date_lt: Optional[datetime], optional
             filter by `modified_date < x`, by default None
         modified_date_lte: Optional[datetime], optional
             filter by `modified_date <= x`, by default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("market", market))
        filter_params.append(list_to_filter("city", city))
        filter_params.append(list_to_filter("location", location))
        filter_params.append(list_to_filter("recordedDate", recorded_date))
        if recorded_date_gt is not None:
            filter_params.append(f'recordedDate > "{recorded_date_gt}"')
        if recorded_date_gte is not None:
            filter_params.append(f'recordedDate >= "{recorded_date_gte}"')
        if recorded_date_lt is not None:
            filter_params.append(f'recordedDate < "{recorded_date_lt}"')
        if recorded_date_lte is not None:
            filter_params.append(f'recordedDate <= "{recorded_date_lte}"')
        filter_params.append(list_to_filter("weatherDate", weather_date))
        if weather_date_gt is not None:
            filter_params.append(f'weatherDate > "{weather_date_gt}"')
        if weather_date_gte is not None:
            filter_params.append(f'weatherDate >= "{weather_date_gte}"')
        if weather_date_lt is not None:
            filter_params.append(f'weatherDate < "{weather_date_lt}"')
        if weather_date_lte is not None:
            filter_params.append(f'weatherDate <= "{weather_date_lte}"')
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
            path=f"/weather/v1/forecast",
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

        if "weatherDate" in df.columns:
            df["weatherDate"] = pd.to_datetime(df["weatherDate"])  # type: ignore

        if "modifiedDate" in df.columns:
            df["modifiedDate"] = pd.to_datetime(df["modifiedDate"])  # type: ignore

        if "recordedDate" in df.columns:
            df["recordedDate"] = pd.to_datetime(df["recordedDate"])  # type: ignore
        return df
