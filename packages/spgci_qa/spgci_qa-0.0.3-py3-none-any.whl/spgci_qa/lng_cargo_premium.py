from __future__ import annotations
from typing import List, Optional, Union
from requests import Response
from spgci_qa.api_client import get_data
from spgci_qa.utilities import list_to_filter
from pandas import DataFrame, Series
from datetime import date, datetime
import pandas as pd


class Lng_cargo_premium:
    _endpoint = "api/v1/"
    _reference_endpoint = "reference/v1/"
    _event_bunkering_endpoint = "/events/bunkering"
    _event_trade_route_endpoint = "/events/trade-route"
    _event_journey_point_endpoint = "/events/journey-point"
    _event_idling_endpoint = "/events/idling"
    _event_diversion_endpoint = "/events/diversion"

    def get_events_bunkering(
        self,
        *,
        id: Optional[int] = None,
        id_lt: Optional[int] = None,
        id_lte: Optional[int] = None,
        id_gt: Optional[int] = None,
        id_gte: Optional[int] = None,
        bunkering_start_date: Optional[datetime] = None,
        bunkering_start_date_lt: Optional[datetime] = None,
        bunkering_start_date_lte: Optional[datetime] = None,
        bunkering_start_date_gt: Optional[datetime] = None,
        bunkering_start_date_gte: Optional[datetime] = None,
        bunkering_location: Optional[Union[list[str], Series[str], str]] = None,
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
        The events record the date and location a vessel has engaged in bunkering (or re-fueling activity).

        Parameters
        ----------

         id: Optional[int], optional
             Event ID, by default None
         id_gt: Optional[int], optional
             filter by '' id > x '', by default None
         id_gte: Optional[int], optional
             filter by id, by default None
         id_lt: Optional[int], optional
             filter by id, by default None
         id_lte: Optional[int], optional
             filter by id, by default None
         bunkering_start_date: Optional[datetime], optional
             The start date of bunkering operations, by default None
         bunkering_start_date_gt: Optional[datetime], optional
             filter by '' bunkering_start_date > x '', by default None
         bunkering_start_date_gte: Optional[datetime], optional
             filter by bunkering_start_date, by default None
         bunkering_start_date_lt: Optional[datetime], optional
             filter by bunkering_start_date, by default None
         bunkering_start_date_lte: Optional[datetime], optional
             filter by bunkering_start_date, by default None
         bunkering_location: Optional[Union[list[str], Series[str], str]]
             The specific name of the location, by default None
         modified_date: Optional[datetime], optional
             Event record latest modified date, by default None
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
        filter_params.append(list_to_filter("id", id))
        if id_gt is not None:
            filter_params.append(f'id > "{id_gt}"')
        if id_gte is not None:
            filter_params.append(f'id >= "{id_gte}"')
        if id_lt is not None:
            filter_params.append(f'id < "{id_lt}"')
        if id_lte is not None:
            filter_params.append(f'id <= "{id_lte}"')
        filter_params.append(list_to_filter("bunkeringStartDate", bunkering_start_date))
        if bunkering_start_date_gt is not None:
            filter_params.append(f'bunkeringStartDate > "{bunkering_start_date_gt}"')
        if bunkering_start_date_gte is not None:
            filter_params.append(f'bunkeringStartDate >= "{bunkering_start_date_gte}"')
        if bunkering_start_date_lt is not None:
            filter_params.append(f'bunkeringStartDate < "{bunkering_start_date_lt}"')
        if bunkering_start_date_lte is not None:
            filter_params.append(f'bunkeringStartDate <= "{bunkering_start_date_lte}"')
        filter_params.append(list_to_filter("bunkeringLocation", bunkering_location))
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
            path=f"/lng/v1/cargo-premium/events/bunkering",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_events_trade_route(
        self,
        *,
        id: Optional[int] = None,
        id_lt: Optional[int] = None,
        id_lte: Optional[int] = None,
        id_gt: Optional[int] = None,
        id_gte: Optional[int] = None,
        route_transit_date: Optional[datetime] = None,
        route_transit_date_lt: Optional[datetime] = None,
        route_transit_date_lte: Optional[datetime] = None,
        route_transit_date_gt: Optional[datetime] = None,
        route_transit_date_gte: Optional[datetime] = None,
        trade_route: Optional[Union[list[str], Series[str], str]] = None,
        vessel_direction: Optional[Union[list[str], Series[str], str]] = None,
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
        The events record the date, location, and duration a vessel has crossed through a major trade route.

        Parameters
        ----------

         id: Optional[int], optional
             Event ID, by default None
         id_gt: Optional[int], optional
             filter by '' id > x '', by default None
         id_gte: Optional[int], optional
             filter by id, by default None
         id_lt: Optional[int], optional
             filter by id, by default None
         id_lte: Optional[int], optional
             filter by id, by default None
         route_transit_date: Optional[datetime], optional
             The date the vessel transited the trade route, by default None
         route_transit_date_gt: Optional[datetime], optional
             filter by '' route_transit_date > x '', by default None
         route_transit_date_gte: Optional[datetime], optional
             filter by route_transit_date, by default None
         route_transit_date_lt: Optional[datetime], optional
             filter by route_transit_date, by default None
         route_transit_date_lte: Optional[datetime], optional
             filter by route_transit_date, by default None
         trade_route: Optional[Union[list[str], Series[str], str]]
             The trade route which the vessel passed through, by default None
         vessel_direction: Optional[Union[list[str], Series[str], str]]
             The general direction the vessel passed through the trade (specific to some routes), by default None
         modified_date: Optional[datetime], optional
             Event record latest modified date, by default None
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
        filter_params.append(list_to_filter("id", id))
        if id_gt is not None:
            filter_params.append(f'id > "{id_gt}"')
        if id_gte is not None:
            filter_params.append(f'id >= "{id_gte}"')
        if id_lt is not None:
            filter_params.append(f'id < "{id_lt}"')
        if id_lte is not None:
            filter_params.append(f'id <= "{id_lte}"')
        filter_params.append(list_to_filter("routeTransitDate", route_transit_date))
        if route_transit_date_gt is not None:
            filter_params.append(f'routeTransitDate > "{route_transit_date_gt}"')
        if route_transit_date_gte is not None:
            filter_params.append(f'routeTransitDate >= "{route_transit_date_gte}"')
        if route_transit_date_lt is not None:
            filter_params.append(f'routeTransitDate < "{route_transit_date_lt}"')
        if route_transit_date_lte is not None:
            filter_params.append(f'routeTransitDate <= "{route_transit_date_lte}"')
        filter_params.append(list_to_filter("tradeRoute", trade_route))
        filter_params.append(list_to_filter("vesselDirection", vessel_direction))
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
            path=f"/lng/v1/cargo-premium/events/trade-route",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_events_journey_point(
        self,
        *,
        id: Optional[int] = None,
        id_lt: Optional[int] = None,
        id_lte: Optional[int] = None,
        id_gt: Optional[int] = None,
        id_gte: Optional[int] = None,
        arrival_date: Optional[datetime] = None,
        arrival_date_lt: Optional[datetime] = None,
        arrival_date_lte: Optional[datetime] = None,
        arrival_date_gt: Optional[datetime] = None,
        arrival_date_gte: Optional[datetime] = None,
        location: Optional[Union[list[str], Series[str], str]] = None,
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
        The events record the date and location a vessel has crossed through an identified point along its journey.

        Parameters
        ----------

         id: Optional[int], optional
             Event ID, by default None
         id_gt: Optional[int], optional
             filter by '' id > x '', by default None
         id_gte: Optional[int], optional
             filter by id, by default None
         id_lt: Optional[int], optional
             filter by id, by default None
         id_lte: Optional[int], optional
             filter by id, by default None
         arrival_date: Optional[datetime], optional
             The date the vessel passed through journey point, by default None
         arrival_date_gt: Optional[datetime], optional
             filter by '' arrival_date > x '', by default None
         arrival_date_gte: Optional[datetime], optional
             filter by arrival_date, by default None
         arrival_date_lt: Optional[datetime], optional
             filter by arrival_date, by default None
         arrival_date_lte: Optional[datetime], optional
             filter by arrival_date, by default None
         location: Optional[Union[list[str], Series[str], str]]
             The specific name of the location, by default None
         modified_date: Optional[datetime], optional
             Event record latest modified date, by default None
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
        filter_params.append(list_to_filter("id", id))
        if id_gt is not None:
            filter_params.append(f'id > "{id_gt}"')
        if id_gte is not None:
            filter_params.append(f'id >= "{id_gte}"')
        if id_lt is not None:
            filter_params.append(f'id < "{id_lt}"')
        if id_lte is not None:
            filter_params.append(f'id <= "{id_lte}"')
        filter_params.append(list_to_filter("arrivalDate", arrival_date))
        if arrival_date_gt is not None:
            filter_params.append(f'arrivalDate > "{arrival_date_gt}"')
        if arrival_date_gte is not None:
            filter_params.append(f'arrivalDate >= "{arrival_date_gte}"')
        if arrival_date_lt is not None:
            filter_params.append(f'arrivalDate < "{arrival_date_lt}"')
        if arrival_date_lte is not None:
            filter_params.append(f'arrivalDate <= "{arrival_date_lte}"')
        filter_params.append(list_to_filter("location", location))
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
            path=f"/lng/v1/cargo-premium/events/journey-point",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_events_idling(
        self,
        *,
        id: Optional[int] = None,
        id_lt: Optional[int] = None,
        id_lte: Optional[int] = None,
        id_gt: Optional[int] = None,
        id_gte: Optional[int] = None,
        idling_start_date: Optional[datetime] = None,
        idling_start_date_lt: Optional[datetime] = None,
        idling_start_date_lte: Optional[datetime] = None,
        idling_start_date_gt: Optional[datetime] = None,
        idling_start_date_gte: Optional[datetime] = None,
        idling_location: Optional[Union[list[str], Series[str], str]] = None,
        idling_finish_date: Optional[datetime] = None,
        idling_finish_date_lt: Optional[datetime] = None,
        idling_finish_date_lte: Optional[datetime] = None,
        idling_finish_date_gt: Optional[datetime] = None,
        idling_finish_date_gte: Optional[datetime] = None,
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
        The events record the date and location a vessel has been idled or in a relatively localized area for an extended period of time.

        Parameters
        ----------

         id: Optional[int], optional
             Event ID, by default None
         id_gt: Optional[int], optional
             filter by '' id > x '', by default None
         id_gte: Optional[int], optional
             filter by id, by default None
         id_lt: Optional[int], optional
             filter by id, by default None
         id_lte: Optional[int], optional
             filter by id, by default None
         idling_start_date: Optional[datetime], optional
             The start date of the idling activity, by default None
         idling_start_date_gt: Optional[datetime], optional
             filter by '' idling_start_date > x '', by default None
         idling_start_date_gte: Optional[datetime], optional
             filter by idling_start_date, by default None
         idling_start_date_lt: Optional[datetime], optional
             filter by idling_start_date, by default None
         idling_start_date_lte: Optional[datetime], optional
             filter by idling_start_date, by default None
         idling_location: Optional[Union[list[str], Series[str], str]]
             The specific name of the location, by default None
         idling_finish_date: Optional[datetime], optional
             The event date of the idling activity, by default None
         idling_finish_date_gt: Optional[datetime], optional
             filter by '' idling_finish_date > x '', by default None
         idling_finish_date_gte: Optional[datetime], optional
             filter by idling_finish_date, by default None
         idling_finish_date_lt: Optional[datetime], optional
             filter by idling_finish_date, by default None
         idling_finish_date_lte: Optional[datetime], optional
             filter by idling_finish_date, by default None
         modified_date: Optional[datetime], optional
             Event record latest modified date, by default None
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
        filter_params.append(list_to_filter("id", id))
        if id_gt is not None:
            filter_params.append(f'id > "{id_gt}"')
        if id_gte is not None:
            filter_params.append(f'id >= "{id_gte}"')
        if id_lt is not None:
            filter_params.append(f'id < "{id_lt}"')
        if id_lte is not None:
            filter_params.append(f'id <= "{id_lte}"')
        filter_params.append(list_to_filter("idlingStartDate", idling_start_date))
        if idling_start_date_gt is not None:
            filter_params.append(f'idlingStartDate > "{idling_start_date_gt}"')
        if idling_start_date_gte is not None:
            filter_params.append(f'idlingStartDate >= "{idling_start_date_gte}"')
        if idling_start_date_lt is not None:
            filter_params.append(f'idlingStartDate < "{idling_start_date_lt}"')
        if idling_start_date_lte is not None:
            filter_params.append(f'idlingStartDate <= "{idling_start_date_lte}"')
        filter_params.append(list_to_filter("idlingLocation", idling_location))
        filter_params.append(list_to_filter("idlingFinishDate", idling_finish_date))
        if idling_finish_date_gt is not None:
            filter_params.append(f'idlingFinishDate > "{idling_finish_date_gt}"')
        if idling_finish_date_gte is not None:
            filter_params.append(f'idlingFinishDate >= "{idling_finish_date_gte}"')
        if idling_finish_date_lt is not None:
            filter_params.append(f'idlingFinishDate < "{idling_finish_date_lt}"')
        if idling_finish_date_lte is not None:
            filter_params.append(f'idlingFinishDate <= "{idling_finish_date_lte}"')
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
            path=f"/lng/v1/cargo-premium/events/idling",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_events_diversion(
        self,
        *,
        id: Optional[int] = None,
        id_lt: Optional[int] = None,
        id_lte: Optional[int] = None,
        id_gt: Optional[int] = None,
        id_gte: Optional[int] = None,
        diversion_date: Optional[datetime] = None,
        diversion_date_lt: Optional[datetime] = None,
        diversion_date_lte: Optional[datetime] = None,
        diversion_date_gt: Optional[datetime] = None,
        diversion_date_gte: Optional[datetime] = None,
        diversion_location: Optional[Union[list[str], Series[str], str]] = None,
        destination_before: Optional[Union[list[str], Series[str], str]] = None,
        destination_after: Optional[Union[list[str], Series[str], str]] = None,
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
        The events record the date and location a vessel has changed course during its journey. It also provides important information about the initial destination and the new destination.

        Parameters
        ----------

         id: Optional[int], optional
             Event ID, by default None
         id_gt: Optional[int], optional
             filter by '' id > x '', by default None
         id_gte: Optional[int], optional
             filter by id, by default None
         id_lt: Optional[int], optional
             filter by id, by default None
         id_lte: Optional[int], optional
             filter by id, by default None
         diversion_date: Optional[datetime], optional
             The date a diversion occurred, by default None
         diversion_date_gt: Optional[datetime], optional
             filter by '' diversion_date > x '', by default None
         diversion_date_gte: Optional[datetime], optional
             filter by diversion_date, by default None
         diversion_date_lt: Optional[datetime], optional
             filter by diversion_date, by default None
         diversion_date_lte: Optional[datetime], optional
             filter by diversion_date, by default None
         diversion_location: Optional[Union[list[str], Series[str], str]]
             The specific name of the location, by default None
         destination_before: Optional[Union[list[str], Series[str], str]]
             The specific name of the initial destination, by default None
         destination_after: Optional[Union[list[str], Series[str], str]]
             The specific name of the new destination, by default None
         modified_date: Optional[datetime], optional
             Event record latest modified date, by default None
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
        filter_params.append(list_to_filter("id", id))
        if id_gt is not None:
            filter_params.append(f'id > "{id_gt}"')
        if id_gte is not None:
            filter_params.append(f'id >= "{id_gte}"')
        if id_lt is not None:
            filter_params.append(f'id < "{id_lt}"')
        if id_lte is not None:
            filter_params.append(f'id <= "{id_lte}"')
        filter_params.append(list_to_filter("diversionDate", diversion_date))
        if diversion_date_gt is not None:
            filter_params.append(f'diversionDate > "{diversion_date_gt}"')
        if diversion_date_gte is not None:
            filter_params.append(f'diversionDate >= "{diversion_date_gte}"')
        if diversion_date_lt is not None:
            filter_params.append(f'diversionDate < "{diversion_date_lt}"')
        if diversion_date_lte is not None:
            filter_params.append(f'diversionDate <= "{diversion_date_lte}"')
        filter_params.append(list_to_filter("diversionLocation", diversion_location))
        filter_params.append(list_to_filter("destinationBefore", destination_before))
        filter_params.append(list_to_filter("destinationAfter", destination_after))
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
            path=f"/lng/v1/cargo-premium/events/diversion",
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

        if "bunkeringStartDate" in df.columns:
            df["bunkeringStartDate"] = pd.to_datetime(df["bunkeringStartDate"])  # type: ignore

        if "createdDate" in df.columns:
            df["createdDate"] = pd.to_datetime(df["createdDate"])  # type: ignore

        if "modifiedDate" in df.columns:
            df["modifiedDate"] = pd.to_datetime(df["modifiedDate"])  # type: ignore

        if "routeTransitDate" in df.columns:
            df["routeTransitDate"] = pd.to_datetime(df["routeTransitDate"])  # type: ignore

        if "arrivalDate" in df.columns:
            df["arrivalDate"] = pd.to_datetime(df["arrivalDate"])  # type: ignore

        if "idlingStartDate" in df.columns:
            df["idlingStartDate"] = pd.to_datetime(df["idlingStartDate"])  # type: ignore

        if "idlingFinishDate" in df.columns:
            df["idlingFinishDate"] = pd.to_datetime(df["idlingFinishDate"])  # type: ignore

        if "diversionDate" in df.columns:
            df["diversionDate"] = pd.to_datetime(df["diversionDate"])  # type: ignore
        return df
