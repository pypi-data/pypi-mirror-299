from __future__ import annotations
from typing import List, Optional, Union
from requests import Response
from spgci_qa.api_client import get_data
from spgci_qa.utilities import list_to_filter
from pandas import DataFrame, Series
from datetime import date, datetime
import pandas as pd


class Crop_science:
    _endpoint = "api/v1/"
    _reference_endpoint = "reference/v1/"
    _tbl_agro_chemicals_product_market_data_endpoint = (
        "/agrochemicals-product-market-data"
    )
    _tbl_biological_product_market_data_endpoint = "/biological-product-market-data"
    _tbl_crop_science_seed_market_data_endpoint = "/seed-market-data"
    _tbl_crop_science_seed_innovation_data_endpoint = "/seed-innovation-data"
    _tbl_agri_food_ma_tracker_endpoint = "/merger-acquisition-tracker"
    _tbl_agri_food_ai_approval_tracker_endpoint = "/active-ingredient-approval-tracker"
    _tbl_global_agro_chemicals_trade_data_endpoint = "/global-agrochemicals-trade-data"

    def get_agrochemicals_product_market_data(
        self,
        *,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        commodity_group: Optional[Union[list[str], Series[str], str]] = None,
        reporting_region: Optional[Union[list[str], Series[str], str]] = None,
        frequency: Optional[Union[list[str], Series[str], str]] = None,
        uom: Optional[Union[list[str], Series[str], str]] = None,
        currency: Optional[Union[list[str], Series[str], str]] = None,
        active_ingredient: Optional[Union[list[str], Series[str], str]] = None,
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
         commodity_group: Optional[Union[list[str], Series[str], str]]
             , by default None
         reporting_region: Optional[Union[list[str], Series[str], str]]
             The geographic region for which the report or model output is reported., by default None
         frequency: Optional[Union[list[str], Series[str], str]]
             The indicator of how often the data is refreshed or collected., by default None
         uom: Optional[Union[list[str], Series[str], str]]
             The unit or units in which the value of the commodity is measured., by default None
         currency: Optional[Union[list[str], Series[str], str]]
             A code representing a standard unit of value of a country or region., by default None
         active_ingredient: Optional[Union[list[str], Series[str], str]]
             , by default None
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
        filter_params.append(list_to_filter("commodityGroup", commodity_group))
        filter_params.append(list_to_filter("reportingRegion", reporting_region))
        filter_params.append(list_to_filter("frequency", frequency))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("currency", currency))
        filter_params.append(list_to_filter("activeIngredient", active_ingredient))
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
            path=f"/analytics/crop-science/v1/agrochemicals-product-market-data",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_biological_product_market_data(
        self,
        *,
        company: Optional[Union[list[str], Series[str], str]] = None,
        company_type: Optional[Union[list[str], Series[str], str]] = None,
        company_region: Optional[Union[list[str], Series[str], str]] = None,
        company_country: Optional[Union[list[str], Series[str], str]] = None,
        product_sector: Optional[Union[list[str], Series[str], str]] = None,
        product: Optional[Union[list[str], Series[str], str]] = None,
        product_class: Optional[Union[list[str], Series[str], str]] = None,
        product_crops: Optional[Union[list[str], Series[str], str]] = None,
        product_crop_group: Optional[Union[list[str], Series[str], str]] = None,
        brand: Optional[Union[list[str], Series[str], str]] = None,
        currency: Optional[Union[list[str], Series[str], str]] = None,
        product_launch_date: Optional[date] = None,
        product_launch_date_lt: Optional[date] = None,
        product_launch_date_lte: Optional[date] = None,
        product_launch_date_gt: Optional[date] = None,
        product_launch_date_gte: Optional[date] = None,
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

         company: Optional[Union[list[str], Series[str], str]]
             The name of company., by default None
         company_type: Optional[Union[list[str], Series[str], str]]
             The type of company, by default None
         company_region: Optional[Union[list[str], Series[str], str]]
             The geographic region of company., by default None
         company_country: Optional[Union[list[str], Series[str], str]]
             The country in which company is operating., by default None
         product_sector: Optional[Union[list[str], Series[str], str]]
             The brief description of the information represented in the data series., by default None
         product: Optional[Union[list[str], Series[str], str]]
             The brief description of the information represented in the data series., by default None
         product_class: Optional[Union[list[str], Series[str], str]]
             The brief description of the information represented in the data series., by default None
         product_crops: Optional[Union[list[str], Series[str], str]]
             The brief description of the information represented in the data series., by default None
         product_crop_group: Optional[Union[list[str], Series[str], str]]
             The brief description of the information represented in the data series., by default None
         brand: Optional[Union[list[str], Series[str], str]]
             , by default None
         currency: Optional[Union[list[str], Series[str], str]]
             A code representing a standard unit of value of a country or region., by default None
         product_launch_date: Optional[date], optional
             The date when product was launched., by default None
         product_launch_date_gt: Optional[date], optional
             filter by '' product_launch_date > x '', by default None
         product_launch_date_gte: Optional[date], optional
             filter by product_launch_date, by default None
         product_launch_date_lt: Optional[date], optional
             filter by product_launch_date, by default None
         product_launch_date_lte: Optional[date], optional
             filter by product_launch_date, by default None
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
        filter_params.append(list_to_filter("company", company))
        filter_params.append(list_to_filter("companyType", company_type))
        filter_params.append(list_to_filter("companyRegion", company_region))
        filter_params.append(list_to_filter("companyCountry", company_country))
        filter_params.append(list_to_filter("productSector", product_sector))
        filter_params.append(list_to_filter("product", product))
        filter_params.append(list_to_filter("productClass", product_class))
        filter_params.append(list_to_filter("productCrops", product_crops))
        filter_params.append(list_to_filter("productCropGroup", product_crop_group))
        filter_params.append(list_to_filter("brand", brand))
        filter_params.append(list_to_filter("currency", currency))
        filter_params.append(list_to_filter("productLaunchDate", product_launch_date))
        if product_launch_date_gt is not None:
            filter_params.append(f'productLaunchDate > "{product_launch_date_gt}"')
        if product_launch_date_gte is not None:
            filter_params.append(f'productLaunchDate >= "{product_launch_date_gte}"')
        if product_launch_date_lt is not None:
            filter_params.append(f'productLaunchDate < "{product_launch_date_lt}"')
        if product_launch_date_lte is not None:
            filter_params.append(f'productLaunchDate <= "{product_launch_date_lte}"')
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
            path=f"/analytics/crop-science/v1/biological-product-market-data",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_seed_market_data(
        self,
        *,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        reporting_region: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
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

         commodity: Optional[Union[list[str], Series[str], str]]
             The name of an economic good, usually a resource, being traded in the derivatives markets., by default None
         reporting_region: Optional[Union[list[str], Series[str], str]]
             The geographic region for which the report or model output is reported., by default None
         concept: Optional[Union[list[str], Series[str], str]]
             The logical grouping or classification of related data elements and entities that are relevant to a particular subject or topic., by default None
         frequency: Optional[Union[list[str], Series[str], str]]
             The indicator of how often the data is refreshed or collected., by default None
         uom: Optional[Union[list[str], Series[str], str]]
             The unit or units in which the value of the commodity is measured., by default None
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
        filter_params.append(list_to_filter("commodity", commodity))
        filter_params.append(list_to_filter("reportingRegion", reporting_region))
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
            path=f"/analytics/crop-science/v1/seed-market-data",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_seed_innovation_data(
        self,
        *,
        commodity: Optional[Union[list[str], Series[str], str]] = None,
        breeding_technique: Optional[Union[list[str], Series[str], str]] = None,
        variety_name: Optional[Union[list[str], Series[str], str]] = None,
        product_name: Optional[Union[list[str], Series[str], str]] = None,
        marketing_company: Optional[Union[list[str], Series[str], str]] = None,
        technology_developing_company: Optional[
            Union[list[str], Series[str], str]
        ] = None,
        technology_owning_company: Optional[Union[list[str], Series[str], str]] = None,
        voluntary_contact_information: Optional[
            Union[list[str], Series[str], str]
        ] = None,
        technology_region: Optional[Union[list[str], Series[str], str]] = None,
        regulatory_agency: Optional[Union[list[str], Series[str], str]] = None,
        regulatory_status: Optional[Union[list[str], Series[str], str]] = None,
        regulation_type: Optional[Union[list[str], Series[str], str]] = None,
        market_status: Optional[Union[list[str], Series[str], str]] = None,
        market_status_info: Optional[Union[list[str], Series[str], str]] = None,
        status_initial_date: Optional[Union[list[str], Series[str], str]] = None,
        status_latest_date: Optional[Union[list[str], Series[str], str]] = None,
        biosafety_expiration: Optional[Union[list[str], Series[str], str]] = None,
        event_name: Optional[Union[list[str], Series[str], str]] = None,
        oecd_identifiers: Optional[Union[list[str], Series[str], str]] = None,
        genome_modification_type: Optional[Union[list[str], Series[str], str]] = None,
        application_creation_technology: Optional[
            Union[list[str], Series[str], str]
        ] = None,
        application_category: Optional[Union[list[str], Series[str], str]] = None,
        application_type: Optional[Union[list[str], Series[str], str]] = None,
        application_type_info: Optional[Union[list[str], Series[str], str]] = None,
        modulated_genes: Optional[Union[list[str], Series[str], str]] = None,
        citation_awareness: Optional[Union[list[str], Series[str], str]] = None,
        consumer_awareness: Optional[Union[list[str], Series[str], str]] = None,
        date_added: Optional[datetime] = None,
        date_added_lt: Optional[datetime] = None,
        date_added_lte: Optional[datetime] = None,
        date_added_gt: Optional[datetime] = None,
        date_added_gte: Optional[datetime] = None,
        date_updated: Optional[datetime] = None,
        date_updated_lt: Optional[datetime] = None,
        date_updated_lte: Optional[datetime] = None,
        date_updated_gt: Optional[datetime] = None,
        date_updated_gte: Optional[datetime] = None,
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
         breeding_technique: Optional[Union[list[str], Series[str], str]]
             , by default None
         variety_name: Optional[Union[list[str], Series[str], str]]
             , by default None
         product_name: Optional[Union[list[str], Series[str], str]]
             , by default None
         marketing_company: Optional[Union[list[str], Series[str], str]]
             , by default None
         technology_developing_company: Optional[Union[list[str], Series[str], str]]
             , by default None
         technology_owning_company: Optional[Union[list[str], Series[str], str]]
             , by default None
         voluntary_contact_information: Optional[Union[list[str], Series[str], str]]
             , by default None
         technology_region: Optional[Union[list[str], Series[str], str]]
             , by default None
         regulatory_agency: Optional[Union[list[str], Series[str], str]]
             , by default None
         regulatory_status: Optional[Union[list[str], Series[str], str]]
             , by default None
         regulation_type: Optional[Union[list[str], Series[str], str]]
             , by default None
         market_status: Optional[Union[list[str], Series[str], str]]
             , by default None
         market_status_info: Optional[Union[list[str], Series[str], str]]
             , by default None
         status_initial_date: Optional[Union[list[str], Series[str], str]]
             , by default None
         status_latest_date: Optional[Union[list[str], Series[str], str]]
             , by default None
         biosafety_expiration: Optional[Union[list[str], Series[str], str]]
             , by default None
         event_name: Optional[Union[list[str], Series[str], str]]
             , by default None
         oecd_identifiers: Optional[Union[list[str], Series[str], str]]
             , by default None
         genome_modification_type: Optional[Union[list[str], Series[str], str]]
             , by default None
         application_creation_technology: Optional[Union[list[str], Series[str], str]]
             , by default None
         application_category: Optional[Union[list[str], Series[str], str]]
             , by default None
         application_type: Optional[Union[list[str], Series[str], str]]
             , by default None
         application_type_info: Optional[Union[list[str], Series[str], str]]
             , by default None
         modulated_genes: Optional[Union[list[str], Series[str], str]]
             , by default None
         citation_awareness: Optional[Union[list[str], Series[str], str]]
             , by default None
         consumer_awareness: Optional[Union[list[str], Series[str], str]]
             , by default None
         date_added: Optional[datetime], optional
             The date and time when a particular record was added, by default None
         date_added_gt: Optional[datetime], optional
             filter by '' date_added > x '', by default None
         date_added_gte: Optional[datetime], optional
             filter by date_added, by default None
         date_added_lt: Optional[datetime], optional
             filter by date_added, by default None
         date_added_lte: Optional[datetime], optional
             filter by date_added, by default None
         date_updated: Optional[datetime], optional
             The date and time when a particular record was updated, by default None
         date_updated_gt: Optional[datetime], optional
             filter by '' date_updated > x '', by default None
         date_updated_gte: Optional[datetime], optional
             filter by date_updated, by default None
         date_updated_lt: Optional[datetime], optional
             filter by date_updated, by default None
         date_updated_lte: Optional[datetime], optional
             filter by date_updated, by default None
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
        filter_params.append(list_to_filter("breedingTechnique", breeding_technique))
        filter_params.append(list_to_filter("varietyName", variety_name))
        filter_params.append(list_to_filter("productName", product_name))
        filter_params.append(list_to_filter("marketingCompany", marketing_company))
        filter_params.append(
            list_to_filter("technologyDevelopingCompany", technology_developing_company)
        )
        filter_params.append(
            list_to_filter("technologyOwningCompany", technology_owning_company)
        )
        filter_params.append(
            list_to_filter("voluntaryContactInformation", voluntary_contact_information)
        )
        filter_params.append(list_to_filter("technologyRegion", technology_region))
        filter_params.append(list_to_filter("regulatoryAgency", regulatory_agency))
        filter_params.append(list_to_filter("regulatoryStatus", regulatory_status))
        filter_params.append(list_to_filter("regulationType", regulation_type))
        filter_params.append(list_to_filter("marketStatus", market_status))
        filter_params.append(list_to_filter("marketStatusInfo", market_status_info))
        filter_params.append(list_to_filter("statusInitialDate", status_initial_date))
        filter_params.append(list_to_filter("statusLatestDate", status_latest_date))
        filter_params.append(
            list_to_filter("biosafetyExpiration", biosafety_expiration)
        )
        filter_params.append(list_to_filter("eventName", event_name))
        filter_params.append(list_to_filter("oecdIdentifiers", oecd_identifiers))
        filter_params.append(
            list_to_filter("genomeModificationType", genome_modification_type)
        )
        filter_params.append(
            list_to_filter(
                "applicationCreationTechnology", application_creation_technology
            )
        )
        filter_params.append(
            list_to_filter("applicationCategory", application_category)
        )
        filter_params.append(list_to_filter("applicationType", application_type))
        filter_params.append(
            list_to_filter("applicationTypeInfo", application_type_info)
        )
        filter_params.append(list_to_filter("modulatedGenes", modulated_genes))
        filter_params.append(list_to_filter("citationAwareness", citation_awareness))
        filter_params.append(list_to_filter("consumerAwareness", consumer_awareness))
        filter_params.append(list_to_filter("dateAdded", date_added))
        if date_added_gt is not None:
            filter_params.append(f'dateAdded > "{date_added_gt}"')
        if date_added_gte is not None:
            filter_params.append(f'dateAdded >= "{date_added_gte}"')
        if date_added_lt is not None:
            filter_params.append(f'dateAdded < "{date_added_lt}"')
        if date_added_lte is not None:
            filter_params.append(f'dateAdded <= "{date_added_lte}"')
        filter_params.append(list_to_filter("dateUpdated", date_updated))
        if date_updated_gt is not None:
            filter_params.append(f'dateUpdated > "{date_updated_gt}"')
        if date_updated_gte is not None:
            filter_params.append(f'dateUpdated >= "{date_updated_gte}"')
        if date_updated_lt is not None:
            filter_params.append(f'dateUpdated < "{date_updated_lt}"')
        if date_updated_lte is not None:
            filter_params.append(f'dateUpdated <= "{date_updated_lte}"')
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
            path=f"/analytics/crop-science/v1/seed-innovation-data",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_merger_acquisition_tracker(
        self,
        *,
        commodity_group: Optional[Union[list[str], Series[str], str]] = None,
        category: Optional[Union[list[str], Series[str], str]] = None,
        deal_type: Optional[Union[list[str], Series[str], str]] = None,
        company: Optional[Union[list[str], Series[str], str]] = None,
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

         commodity_group: Optional[Union[list[str], Series[str], str]]
             The commodity group name of an economic good, usually a resource, being traded in the derivatives markets., by default None
         category: Optional[Union[list[str], Series[str], str]]
             , by default None
         deal_type: Optional[Union[list[str], Series[str], str]]
             , by default None
         company: Optional[Union[list[str], Series[str], str]]
             , by default None
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
        filter_params.append(list_to_filter("commodity_group", commodity_group))
        filter_params.append(list_to_filter("category", category))
        filter_params.append(list_to_filter("dealType", deal_type))
        filter_params.append(list_to_filter("company", company))
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
            path=f"/analytics/crop-science/v1/merger-acquisition-tracker",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_active_ingredient_approval_tracker(
        self,
        *,
        company: Optional[Union[list[str], Series[str], str]] = None,
        active_ingredient: Optional[Union[list[str], Series[str], str]] = None,
        licensee_partner: Optional[Union[list[str], Series[str], str]] = None,
        trade_name: Optional[Union[list[str], Series[str], str]] = None,
        partner_ais: Optional[Union[list[str], Series[str], str]] = None,
        company_region: Optional[Union[list[str], Series[str], str]] = None,
        crops: Optional[Union[list[str], Series[str], str]] = None,
        agrow_publication_date: Optional[date] = None,
        agrow_publication_date_lt: Optional[date] = None,
        agrow_publication_date_lte: Optional[date] = None,
        agrow_publication_date_gt: Optional[date] = None,
        agrow_publication_date_gte: Optional[date] = None,
        approval_tracker_status: Optional[Union[list[str], Series[str], str]] = None,
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

         company: Optional[Union[list[str], Series[str], str]]
             The name of company., by default None
         active_ingredient: Optional[Union[list[str], Series[str], str]]
             , by default None
         licensee_partner: Optional[Union[list[str], Series[str], str]]
             , by default None
         trade_name: Optional[Union[list[str], Series[str], str]]
             , by default None
         partner_ais: Optional[Union[list[str], Series[str], str]]
             , by default None
         company_region: Optional[Union[list[str], Series[str], str]]
             The geographic region of company., by default None
         crops: Optional[Union[list[str], Series[str], str]]
             , by default None
         agrow_publication_date: Optional[date], optional
             The date for which the record applies within the data table, this can be a historical or forecast date., by default None
         agrow_publication_date_gt: Optional[date], optional
             filter by '' agrow_publication_date > x '', by default None
         agrow_publication_date_gte: Optional[date], optional
             filter by agrow_publication_date, by default None
         agrow_publication_date_lt: Optional[date], optional
             filter by agrow_publication_date, by default None
         agrow_publication_date_lte: Optional[date], optional
             filter by agrow_publication_date, by default None
         approval_tracker_status: Optional[Union[list[str], Series[str], str]]
             , by default None
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
        filter_params.append(list_to_filter("company", company))
        filter_params.append(list_to_filter("activeIngredient", active_ingredient))
        filter_params.append(list_to_filter("licenseePartner", licensee_partner))
        filter_params.append(list_to_filter("tradeName", trade_name))
        filter_params.append(list_to_filter("partnerAis", partner_ais))
        filter_params.append(list_to_filter("companyRegion", company_region))
        filter_params.append(list_to_filter("crops", crops))
        filter_params.append(
            list_to_filter("agrowPublicationDate", agrow_publication_date)
        )
        if agrow_publication_date_gt is not None:
            filter_params.append(
                f'agrowPublicationDate > "{agrow_publication_date_gt}"'
            )
        if agrow_publication_date_gte is not None:
            filter_params.append(
                f'agrowPublicationDate >= "{agrow_publication_date_gte}"'
            )
        if agrow_publication_date_lt is not None:
            filter_params.append(
                f'agrowPublicationDate < "{agrow_publication_date_lt}"'
            )
        if agrow_publication_date_lte is not None:
            filter_params.append(
                f'agrowPublicationDate <= "{agrow_publication_date_lte}"'
            )
        filter_params.append(
            list_to_filter("approvalTrackerStatus", approval_tracker_status)
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
            path=f"/analytics/crop-science/v1/active-ingredient-approval-tracker",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response

    def get_global_agrochemicals_trade_data(
        self,
        *,
        commodity_group: Optional[Union[list[str], Series[str], str]] = None,
        reporting_region: Optional[Union[list[str], Series[str], str]] = None,
        partner_region: Optional[Union[list[str], Series[str], str]] = None,
        concept: Optional[Union[list[str], Series[str], str]] = None,
        metrics_type: Optional[Union[list[str], Series[str], str]] = None,
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

         commodity_group: Optional[Union[list[str], Series[str], str]]
             , by default None
         reporting_region: Optional[Union[list[str], Series[str], str]]
             The geographic region for which the report or model output is reported., by default None
         partner_region: Optional[Union[list[str], Series[str], str]]
             The geographic region for which the report or model output is reported., by default None
         concept: Optional[Union[list[str], Series[str], str]]
             The logical grouping or classification of related data elements and entities that are relevant to a particular subject or topic., by default None
         metrics_type: Optional[Union[list[str], Series[str], str]]
             The type of metrics., by default None
         uom: Optional[Union[list[str], Series[str], str]]
             The unit or units in which the value of the commodity is measured., by default None
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
        filter_params.append(list_to_filter("commodityGroup", commodity_group))
        filter_params.append(list_to_filter("reportingRegion", reporting_region))
        filter_params.append(list_to_filter("partnerRegion", partner_region))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("metrics_type", metrics_type))
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
            path=f"/analytics/crop-science/v1/global-agrochemicals-trade-data",
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

        if "productLaunchDate" in df.columns:
            df["productLaunchDate"] = pd.to_datetime(df["productLaunchDate"])  # type: ignore

        if "dateAdded" in df.columns:
            df["dateAdded"] = pd.to_datetime(df["dateAdded"])  # type: ignore

        if "dateUpdated" in df.columns:
            df["dateUpdated"] = pd.to_datetime(df["dateUpdated"])  # type: ignore

        if "agrowPublicationDate" in df.columns:
            df["agrowPublicationDate"] = pd.to_datetime(df["agrowPublicationDate"])  # type: ignore
        return df
