from __future__ import annotations
from typing import List, Optional, Union
from requests import Response
from spgci_qa.api_client import get_data
from spgci_qa.utilities import list_to_filter
from pandas import DataFrame, Series
from datetime import date, datetime
import pandas as pd


class Lng_market_fundamentals:
    _endpoint = "api/v1/"
    _reference_endpoint = "reference/v1/"
    _gas_balances_endpoint = "/gas-balances"
    _gas_demand_endpoint = "/gas-demand"
    _gas_reserves_endpoint = "/gas-reserves"
    _gas_sales_endpoint = "/gas-sales"
    _power_capacity_endpoint = "/power-capacity"
    _power_generation_endpoint = "/power-generation"
    _storage_endpoint = "/storage"
    _prices_endpoint = "/prices"
    _pipeline_endpoint = "/pipeline"
    _fuel_use_endpoint = "/fuel-use"

    def get_gas_balances(
        self,
        *,
        source: Optional[Union[list[str], Series[str], str]] = None,
        market: Optional[Union[list[str], Series[str], str]] = None,
        period_type: Optional[Union[list[str], Series[str], str]] = None,
        period: Optional[date] = None,
        period_lt: Optional[date] = None,
        period_lte: Optional[date] = None,
        period_gt: Optional[date] = None,
        period_gte: Optional[date] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        category: Optional[Union[list[str], Series[str], str]] = None,
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
        Provides natural gas supply-demand levels by market over time. If available, this dataset includes natural gas import and export data.

        Parameters
        ----------

         source: Optional[Union[list[str], Series[str], str]]
             A generalized description of the type of data. This needs to be analyzed in conjunction with the other fields. It is used to avoid confusion in analyzing similar datasets., by default None
         market: Optional[Union[list[str], Series[str], str]]
             The geography that the data refers to., by default None
         period_type: Optional[Union[list[str], Series[str], str]]
             The period type that the data refers to. For example, the data could be in terms of year, quarter, month, or day., by default None
         period: Optional[date], optional
             The date that the data refers to. The period’s date will be defined by the Period Type., by default None
         period_gt: Optional[date], optional
             filter by '' period > x '', by default None
         period_gte: Optional[date], optional
             filter by period, by default None
         period_lt: Optional[date], optional
             filter by period, by default None
         period_lte: Optional[date], optional
             filter by period, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             The unit of measurement., by default None
         category: Optional[Union[list[str], Series[str], str]]
             The specific category or grouping for the data., by default None
         modified_date: Optional[datetime], optional
             Gas Balances record latest modified date., by default None
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
        filter_params.append(list_to_filter("source", source))
        filter_params.append(list_to_filter("market", market))
        filter_params.append(list_to_filter("periodType", period_type))
        filter_params.append(list_to_filter("period", period))
        if period_gt is not None:
            filter_params.append(f'period > "{period_gt}"')
        if period_gte is not None:
            filter_params.append(f'period >= "{period_gte}"')
        if period_lt is not None:
            filter_params.append(f'period < "{period_lt}"')
        if period_lte is not None:
            filter_params.append(f'period <= "{period_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("category", category))
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
            path=f"/lng/v1/market/gas-balances",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_gas_demand(
        self,
        *,
        source: Optional[Union[list[str], Series[str], str]] = None,
        market: Optional[Union[list[str], Series[str], str]] = None,
        period_type: Optional[Union[list[str], Series[str], str]] = None,
        period: Optional[date] = None,
        period_lt: Optional[date] = None,
        period_lte: Optional[date] = None,
        period_gt: Optional[date] = None,
        period_gte: Optional[date] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        category: Optional[Union[list[str], Series[str], str]] = None,
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
        Provides natural gas demand levels by market over time. If available, the dataset includes demand by sector.

        Parameters
        ----------

         source: Optional[Union[list[str], Series[str], str]]
             A generalized description of the type of data. This needs to be analyzed in conjunction with the other fields. It is used to avoid confusion in analyzing similar datasets., by default None
         market: Optional[Union[list[str], Series[str], str]]
             The geography that the data refers to., by default None
         period_type: Optional[Union[list[str], Series[str], str]]
             The period type that the data refers to. For example, the data could be in terms of year, quarter, month, or day., by default None
         period: Optional[date], optional
             The date that the data refers to. The period’s date will be defined by the Period Type., by default None
         period_gt: Optional[date], optional
             filter by '' period > x '', by default None
         period_gte: Optional[date], optional
             filter by period, by default None
         period_lt: Optional[date], optional
             filter by period, by default None
         period_lte: Optional[date], optional
             filter by period, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             The unit of measurement., by default None
         category: Optional[Union[list[str], Series[str], str]]
             The specific category or grouping for the data., by default None
         modified_date: Optional[datetime], optional
             Gas Demand record latest modified date., by default None
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
        filter_params.append(list_to_filter("source", source))
        filter_params.append(list_to_filter("market", market))
        filter_params.append(list_to_filter("periodType", period_type))
        filter_params.append(list_to_filter("period", period))
        if period_gt is not None:
            filter_params.append(f'period > "{period_gt}"')
        if period_gte is not None:
            filter_params.append(f'period >= "{period_gte}"')
        if period_lt is not None:
            filter_params.append(f'period < "{period_lt}"')
        if period_lte is not None:
            filter_params.append(f'period <= "{period_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("category", category))
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
            path=f"/lng/v1/market/gas-demand",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_gas_reserves(
        self,
        *,
        source: Optional[Union[list[str], Series[str], str]] = None,
        market: Optional[Union[list[str], Series[str], str]] = None,
        period_type: Optional[Union[list[str], Series[str], str]] = None,
        period: Optional[date] = None,
        period_lt: Optional[date] = None,
        period_lte: Optional[date] = None,
        period_gt: Optional[date] = None,
        period_gte: Optional[date] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        category: Optional[Union[list[str], Series[str], str]] = None,
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
        Provides natural gas supply reserves levels.

        Parameters
        ----------

         source: Optional[Union[list[str], Series[str], str]]
             A generalized description of the type of data. This needs to be analyzed in conjunction with the other fields. It is used to avoid confusion in analyzing similar datasets., by default None
         market: Optional[Union[list[str], Series[str], str]]
             The geography that the data refers to., by default None
         period_type: Optional[Union[list[str], Series[str], str]]
             The period type that the data refers to. For example, the data could be in terms of year, quarter, month, or day., by default None
         period: Optional[date], optional
             The date that the data refers to. The period’s date will be defined by the Period Type., by default None
         period_gt: Optional[date], optional
             filter by '' period > x '', by default None
         period_gte: Optional[date], optional
             filter by period, by default None
         period_lt: Optional[date], optional
             filter by period, by default None
         period_lte: Optional[date], optional
             filter by period, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             The unit of measurement., by default None
         category: Optional[Union[list[str], Series[str], str]]
             The specific category or grouping for the data., by default None
         modified_date: Optional[datetime], optional
             Gas Reserves record latest modified date., by default None
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
        filter_params.append(list_to_filter("source", source))
        filter_params.append(list_to_filter("market", market))
        filter_params.append(list_to_filter("periodType", period_type))
        filter_params.append(list_to_filter("period", period))
        if period_gt is not None:
            filter_params.append(f'period > "{period_gt}"')
        if period_gte is not None:
            filter_params.append(f'period >= "{period_gte}"')
        if period_lt is not None:
            filter_params.append(f'period < "{period_lt}"')
        if period_lte is not None:
            filter_params.append(f'period <= "{period_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("category", category))
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
            path=f"/lng/v1/market/gas-reserves",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_gas_sales(
        self,
        *,
        source: Optional[Union[list[str], Series[str], str]] = None,
        market: Optional[Union[list[str], Series[str], str]] = None,
        period_type: Optional[Union[list[str], Series[str], str]] = None,
        period: Optional[date] = None,
        period_lt: Optional[date] = None,
        period_lte: Optional[date] = None,
        period_gt: Optional[date] = None,
        period_gte: Optional[date] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        category: Optional[Union[list[str], Series[str], str]] = None,
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
        Provides natural gas sales levels in markets over time. If available, the dataset includes sales by sector or by supplier type.

        Parameters
        ----------

         source: Optional[Union[list[str], Series[str], str]]
             A generalized description of the type of data. This needs to be analyzed in conjunction with the other fields. It is used to avoid confusion in analyzing similar datasets., by default None
         market: Optional[Union[list[str], Series[str], str]]
             The geography that the data refers to., by default None
         period_type: Optional[Union[list[str], Series[str], str]]
             The period type that the data refers to. For example, the data could be in terms of year, quarter, month, or day., by default None
         period: Optional[date], optional
             The date that the data refers to. The period’s date will be defined by the Period Type., by default None
         period_gt: Optional[date], optional
             filter by '' period > x '', by default None
         period_gte: Optional[date], optional
             filter by period, by default None
         period_lt: Optional[date], optional
             filter by period, by default None
         period_lte: Optional[date], optional
             filter by period, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             The unit of measurement., by default None
         category: Optional[Union[list[str], Series[str], str]]
             The specific category or grouping for the data., by default None
         modified_date: Optional[datetime], optional
             Gas Sales record latest modified date., by default None
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
        filter_params.append(list_to_filter("source", source))
        filter_params.append(list_to_filter("market", market))
        filter_params.append(list_to_filter("periodType", period_type))
        filter_params.append(list_to_filter("period", period))
        if period_gt is not None:
            filter_params.append(f'period > "{period_gt}"')
        if period_gte is not None:
            filter_params.append(f'period >= "{period_gte}"')
        if period_lt is not None:
            filter_params.append(f'period < "{period_lt}"')
        if period_lte is not None:
            filter_params.append(f'period <= "{period_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("category", category))
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
            path=f"/lng/v1/market/gas-sales",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_power_capacity(
        self,
        *,
        source: Optional[Union[list[str], Series[str], str]] = None,
        market: Optional[Union[list[str], Series[str], str]] = None,
        period_type: Optional[Union[list[str], Series[str], str]] = None,
        period: Optional[date] = None,
        period_lt: Optional[date] = None,
        period_lte: Optional[date] = None,
        period_gt: Optional[date] = None,
        period_gte: Optional[date] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        category: Optional[Union[list[str], Series[str], str]] = None,
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
        Provides power capacity levels in markets over time. If available, the dataset includes capacity by fuel type or by sector.

        Parameters
        ----------

         source: Optional[Union[list[str], Series[str], str]]
             A generalized description of the type of data. This needs to be analyzed in conjunction with the other fields. It is used to avoid confusion in analyzing similar datasets., by default None
         market: Optional[Union[list[str], Series[str], str]]
             The geography that the data refers to., by default None
         period_type: Optional[Union[list[str], Series[str], str]]
             The period type that the data refers to. For example, the data could be in terms of year, quarter, month, or day., by default None
         period: Optional[date], optional
             The date that the data refers to. The period’s date will be defined by the Period Type., by default None
         period_gt: Optional[date], optional
             filter by '' period > x '', by default None
         period_gte: Optional[date], optional
             filter by period, by default None
         period_lt: Optional[date], optional
             filter by period, by default None
         period_lte: Optional[date], optional
             filter by period, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             The unit of measurement., by default None
         category: Optional[Union[list[str], Series[str], str]]
             The specific category or grouping for the data., by default None
         modified_date: Optional[datetime], optional
             Power Capacity record latest modified date., by default None
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
        filter_params.append(list_to_filter("source", source))
        filter_params.append(list_to_filter("market", market))
        filter_params.append(list_to_filter("periodType", period_type))
        filter_params.append(list_to_filter("period", period))
        if period_gt is not None:
            filter_params.append(f'period > "{period_gt}"')
        if period_gte is not None:
            filter_params.append(f'period >= "{period_gte}"')
        if period_lt is not None:
            filter_params.append(f'period < "{period_lt}"')
        if period_lte is not None:
            filter_params.append(f'period <= "{period_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("category", category))
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
            path=f"/lng/v1/market/power-capacity",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_power_generation(
        self,
        *,
        source: Optional[Union[list[str], Series[str], str]] = None,
        market: Optional[Union[list[str], Series[str], str]] = None,
        period_type: Optional[Union[list[str], Series[str], str]] = None,
        period: Optional[date] = None,
        period_lt: Optional[date] = None,
        period_lte: Optional[date] = None,
        period_gt: Optional[date] = None,
        period_gte: Optional[date] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        category: Optional[Union[list[str], Series[str], str]] = None,
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
        Provides power generation levels in markets over time. If available, the dataset includes generation by fuel type or by sector.

        Parameters
        ----------

         source: Optional[Union[list[str], Series[str], str]]
             A generalized description of the type of data. This needs to be analyzed in conjunction with the other fields. It is used to avoid confusion in analyzing similar datasets., by default None
         market: Optional[Union[list[str], Series[str], str]]
             The geography that the data refers to., by default None
         period_type: Optional[Union[list[str], Series[str], str]]
             The period type that the data refers to. For example, the data could be in terms of year, quarter, month, or day., by default None
         period: Optional[date], optional
             The date that the data refers to. The period’s date will be defined by the Period Type., by default None
         period_gt: Optional[date], optional
             filter by '' period > x '', by default None
         period_gte: Optional[date], optional
             filter by period, by default None
         period_lt: Optional[date], optional
             filter by period, by default None
         period_lte: Optional[date], optional
             filter by period, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             The unit of measurement., by default None
         category: Optional[Union[list[str], Series[str], str]]
             The specific category or grouping for the data., by default None
         modified_date: Optional[datetime], optional
             Power Generation record latest modified date., by default None
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
        filter_params.append(list_to_filter("source", source))
        filter_params.append(list_to_filter("market", market))
        filter_params.append(list_to_filter("periodType", period_type))
        filter_params.append(list_to_filter("period", period))
        if period_gt is not None:
            filter_params.append(f'period > "{period_gt}"')
        if period_gte is not None:
            filter_params.append(f'period >= "{period_gte}"')
        if period_lt is not None:
            filter_params.append(f'period < "{period_lt}"')
        if period_lte is not None:
            filter_params.append(f'period <= "{period_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("category", category))
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
            path=f"/lng/v1/market/power-generation",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_storage(
        self,
        *,
        source: Optional[Union[list[str], Series[str], str]] = None,
        market: Optional[Union[list[str], Series[str], str]] = None,
        period_type: Optional[Union[list[str], Series[str], str]] = None,
        period: Optional[date] = None,
        period_lt: Optional[date] = None,
        period_lte: Optional[date] = None,
        period_gt: Optional[date] = None,
        period_gte: Optional[date] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        category: Optional[Union[list[str], Series[str], str]] = None,
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
        Provides natural gas storage levels in markets.

        Parameters
        ----------

         source: Optional[Union[list[str], Series[str], str]]
             A generalized description of the type of data. This needs to be analyzed in conjunction with the other fields. It is used to avoid confusion in analyzing similar datasets., by default None
         market: Optional[Union[list[str], Series[str], str]]
             The geography that the data refers to., by default None
         period_type: Optional[Union[list[str], Series[str], str]]
             The period type that the data refers to. For example, the data could be in terms of year, quarter, month, or day., by default None
         period: Optional[date], optional
             The date that the data refers to. The period’s date will be defined by the Period Type., by default None
         period_gt: Optional[date], optional
             filter by '' period > x '', by default None
         period_gte: Optional[date], optional
             filter by period, by default None
         period_lt: Optional[date], optional
             filter by period, by default None
         period_lte: Optional[date], optional
             filter by period, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             The unit of measurement., by default None
         category: Optional[Union[list[str], Series[str], str]]
             The specific category or grouping for the data., by default None
         modified_date: Optional[datetime], optional
             Storage record latest modified date., by default None
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
        filter_params.append(list_to_filter("source", source))
        filter_params.append(list_to_filter("market", market))
        filter_params.append(list_to_filter("periodType", period_type))
        filter_params.append(list_to_filter("period", period))
        if period_gt is not None:
            filter_params.append(f'period > "{period_gt}"')
        if period_gte is not None:
            filter_params.append(f'period >= "{period_gte}"')
        if period_lt is not None:
            filter_params.append(f'period < "{period_lt}"')
        if period_lte is not None:
            filter_params.append(f'period <= "{period_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("category", category))
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
            path=f"/lng/v1/market/storage",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_prices(
        self,
        *,
        source: Optional[Union[list[str], Series[str], str]] = None,
        market: Optional[Union[list[str], Series[str], str]] = None,
        period_type: Optional[Union[list[str], Series[str], str]] = None,
        period: Optional[date] = None,
        period_lt: Optional[date] = None,
        period_lte: Optional[date] = None,
        period_gt: Optional[date] = None,
        period_gte: Optional[date] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        category: Optional[Union[list[str], Series[str], str]] = None,
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
        Provides natural gas price levels in markets over time. If available, the dataset includes prices by sector or by import/export type.

        Parameters
        ----------

         source: Optional[Union[list[str], Series[str], str]]
             A generalized description of the type of data. This needs to be analyzed in conjunction with the other fields. It is used to avoid confusion in analyzing similar datasets., by default None
         market: Optional[Union[list[str], Series[str], str]]
             The geography that the data refers to., by default None
         period_type: Optional[Union[list[str], Series[str], str]]
             The period type that the data refers to. For example, the data could be in terms of year, quarter, month, or day., by default None
         period: Optional[date], optional
             The date that the data refers to. The period’s date will be defined by the Period Type., by default None
         period_gt: Optional[date], optional
             filter by '' period > x '', by default None
         period_gte: Optional[date], optional
             filter by period, by default None
         period_lt: Optional[date], optional
             filter by period, by default None
         period_lte: Optional[date], optional
             filter by period, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             The unit of measurement., by default None
         category: Optional[Union[list[str], Series[str], str]]
             The specific category or grouping for the data., by default None
         modified_date: Optional[datetime], optional
             Prices record latest modified date., by default None
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
        filter_params.append(list_to_filter("source", source))
        filter_params.append(list_to_filter("market", market))
        filter_params.append(list_to_filter("periodType", period_type))
        filter_params.append(list_to_filter("period", period))
        if period_gt is not None:
            filter_params.append(f'period > "{period_gt}"')
        if period_gte is not None:
            filter_params.append(f'period >= "{period_gte}"')
        if period_lt is not None:
            filter_params.append(f'period < "{period_lt}"')
        if period_lte is not None:
            filter_params.append(f'period <= "{period_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("category", category))
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
            path=f"/lng/v1/market/prices",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_pipeline(
        self,
        *,
        source: Optional[Union[list[str], Series[str], str]] = None,
        market: Optional[Union[list[str], Series[str], str]] = None,
        period_type: Optional[Union[list[str], Series[str], str]] = None,
        period: Optional[date] = None,
        period_lt: Optional[date] = None,
        period_lte: Optional[date] = None,
        period_gt: Optional[date] = None,
        period_gte: Optional[date] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        category: Optional[Union[list[str], Series[str], str]] = None,
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
        Provides natural gas pipeline information by market.

        Parameters
        ----------

         source: Optional[Union[list[str], Series[str], str]]
             A generalized description of the type of data. This needs to be analyzed in conjunction with the other fields. It is used to avoid confusion in analyzing similar datasets., by default None
         market: Optional[Union[list[str], Series[str], str]]
             The geography that the data refers to., by default None
         period_type: Optional[Union[list[str], Series[str], str]]
             The period type that the data refers to. For example, the data could be in terms of year, quarter, month, or day., by default None
         period: Optional[date], optional
             The date that the data refers to. The period’s date will be defined by the Period Type., by default None
         period_gt: Optional[date], optional
             filter by '' period > x '', by default None
         period_gte: Optional[date], optional
             filter by period, by default None
         period_lt: Optional[date], optional
             filter by period, by default None
         period_lte: Optional[date], optional
             filter by period, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             The unit of measurement., by default None
         category: Optional[Union[list[str], Series[str], str]]
             The specific category or grouping for the data., by default None
         modified_date: Optional[datetime], optional
             Pipelines record latest modified date., by default None
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
        filter_params.append(list_to_filter("source", source))
        filter_params.append(list_to_filter("market", market))
        filter_params.append(list_to_filter("periodType", period_type))
        filter_params.append(list_to_filter("period", period))
        if period_gt is not None:
            filter_params.append(f'period > "{period_gt}"')
        if period_gte is not None:
            filter_params.append(f'period >= "{period_gte}"')
        if period_lt is not None:
            filter_params.append(f'period < "{period_lt}"')
        if period_lte is not None:
            filter_params.append(f'period <= "{period_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("category", category))
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
            path=f"/lng/v1/market/pipeline",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_fuel_use(
        self,
        *,
        source: Optional[Union[list[str], Series[str], str]] = None,
        market: Optional[Union[list[str], Series[str], str]] = None,
        period_type: Optional[Union[list[str], Series[str], str]] = None,
        period: Optional[date] = None,
        period_lt: Optional[date] = None,
        period_lte: Optional[date] = None,
        period_gt: Optional[date] = None,
        period_gte: Optional[date] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        category: Optional[Union[list[str], Series[str], str]] = None,
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
        Provides energy balances by market and by fuel over time.

        Parameters
        ----------

         source: Optional[Union[list[str], Series[str], str]]
             A generalized description of the type of data. This needs to be analyzed in conjunction with the other fields. It is used to avoid confusion in analyzing similar datasets., by default None
         market: Optional[Union[list[str], Series[str], str]]
             The geography that the data refers to., by default None
         period_type: Optional[Union[list[str], Series[str], str]]
             The period type that the data refers to. For example, the data could be in terms of year, quarter, month, or day., by default None
         period: Optional[date], optional
             The date that the data refers to. The period’s date will be defined by the Period Type., by default None
         period_gt: Optional[date], optional
             filter by '' period > x '', by default None
         period_gte: Optional[date], optional
             filter by period, by default None
         period_lt: Optional[date], optional
             filter by period, by default None
         period_lte: Optional[date], optional
             filter by period, by default None
         uom: Optional[Union[list[str], Series[str], str]]
             The unit of measurement., by default None
         category: Optional[Union[list[str], Series[str], str]]
             The specific category or grouping for the data., by default None
         modified_date: Optional[datetime], optional
             Fuel Use record latest modified date., by default None
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
        filter_params.append(list_to_filter("source", source))
        filter_params.append(list_to_filter("market", market))
        filter_params.append(list_to_filter("periodType", period_type))
        filter_params.append(list_to_filter("period", period))
        if period_gt is not None:
            filter_params.append(f'period > "{period_gt}"')
        if period_gte is not None:
            filter_params.append(f'period >= "{period_gte}"')
        if period_lt is not None:
            filter_params.append(f'period < "{period_lt}"')
        if period_lte is not None:
            filter_params.append(f'period <= "{period_lte}"')
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("category", category))
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
            path=f"/lng/v1/market/fuel-use",
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

        if "period" in df.columns:
            df["period"] = pd.to_datetime(df["period"])  # type: ignore

        if "modifiedDate" in df.columns:
            df["modifiedDate"] = pd.to_datetime(df["modifiedDate"])  # type: ignore
        return df
