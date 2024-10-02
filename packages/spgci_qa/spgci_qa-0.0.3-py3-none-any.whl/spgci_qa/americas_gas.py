
from __future__ import annotations
from typing import List, Optional, Union
from requests import Response
from spgci_qa.api_client import get_data
from spgci_qa.utilities import list_to_filter
from pandas import DataFrame, Series
from datetime import date
import pandas as pd

class Americas_gas:
    _endpoint = "api/v1/"
    _reference_endpoint = "reference/v1/"
    _americasgas_geography_master_endpoint = "/americasgas-geography-master"
    _americasgas_metadata_pipelineflows_endpoint = "/americasgas-pipelineflows-master"
    _nagas_production_flow_data_endpoint = "/natural-gas-production"
    _demand_actual_data_endpoint = "/modeled-demand-actual"
    _denormalized_flowdata_endpoint = "/pipeline-flows"
    _weather_flow_data_endpoint = "/population-weighted-weather"
    _demand_forecast_data_endpoint = "/modeled-demand-forecast"
    _no_notice_flow_data_endpoint = "/no-notice-flow-data"
    _gas_quality_data_endpoint = "/gas-quality-data"
    _notices_data_endpoint = "/notices-data"
    _tariff_rate_data_endpoint = "/tariff-rate-data"
    _regional_summaries_flowdata_endpoint = "/regional-summaries-flowdata"
    _outlook_production_play_endpoint = "/outlook-production-play"
    _market_balances_data_endpoint = "/market-balances-data"
    _index_of_customer_data_endpoint = "/index-of-customer-data"
    _outlook_balances_prices_data_endpoint = "/outlook-marketbalances-prices"
    _production_oil_data_endpoint = "/production-oil-data"
    _facility_flow_data_endpoint = "/facility-flow-data"
    _pipeline_profiles_data_endpoint = "/pipeline-profiles-data"
    _storage_data_endpoint = "/storage-data"
    _americasgas_pipeline_storage_projects_endpoint = "/americasgas-pipeline-storage-projects"


    def get_americasgas_geography_master(
        self, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, domain: Optional[Union[list[str], Series[str], str]] = None, domainID: Optional[Union[list[str], Series[str], str]] = None, region: Optional[Union[list[str], Series[str], str]] = None, regionID: Optional[Union[list[str], Series[str], str]] = None, subregion: Optional[Union[list[str], Series[str], str]] = None, subregionID: Optional[Union[list[str], Series[str], str]] = None, gulfcoastSubstate: Optional[Union[list[str], Series[str], str]] = None, gulfcoastSubstateID: Optional[Union[list[str], Series[str], str]] = None, stateAbbreviation: Optional[Union[list[str], Series[str], str]] = None, state: Optional[Union[list[str], Series[str], str]] = None, stateID: Optional[Union[list[str], Series[str], str]] = None, county: Optional[Union[list[str], Series[str], str]] = None, countyID: Optional[Union[list[str], Series[str], str]] = None, producingArea: Optional[Union[list[str], Series[str], str]] = None, producingAreaID: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         domain: Optional[Union[list[str], Series[str], str]]
             US Lower-48, Canada and Mexico., be default None
         domainID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the domain., be default None
         region: Optional[Union[list[str], Series[str], str]]
             A defined geographic region within the Americas Gas service. Regions are an aggregation of states or provinces within a country., be default None
         regionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic region., be default None
         subregion: Optional[Union[list[str], Series[str], str]]
             A defined geographic subregion within the Americas Gas service. A substate geography is sometimes referred to as a subregion. Subregions are an aggregation of specific counties within a region and a country., be default None
         subregionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic subregion., be default None
         gulfcoastSubstate: Optional[Union[list[str], Series[str], str]]
             The name of substate region or special area within the Gulf Coast region., be default None
         gulfcoastSubstateID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic substate regions within the Gulf Coast area., be default None
         stateAbbreviation: Optional[Union[list[str], Series[str], str]]
             Abbreviation for a state or province within country., be default None
         state: Optional[Union[list[str], Series[str], str]]
             The political boundaries that define a state or province within country., be default None
         stateID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the state or province utilizes legacy Bentek IDs., be default None
         county: Optional[Union[list[str], Series[str], str]]
             The political boundaries of a defined county within a US state in which a meter or point resides., be default None
         countyID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the county within a US state in which a meter or point resides, utilizes legacy Bentek IDs., be default None
         producingArea: Optional[Union[list[str], Series[str], str]]
             Defined aggregation of counties within a state that is a best fit representation of prominent oil and gas plays and basins., be default None
         producingAreaID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for a defined Producing Area utilizes legacy PointLogic IDs., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("domain", domain))
        filter_params.append(list_to_filter("domainID", domainID))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("regionID", regionID))
        filter_params.append(list_to_filter("subregion", subregion))
        filter_params.append(list_to_filter("subregionID", subregionID))
        filter_params.append(list_to_filter("gulfcoastSubstate", gulfcoastSubstate))
        filter_params.append(list_to_filter("gulfcoastSubstateID", gulfcoastSubstateID))
        filter_params.append(list_to_filter("stateAbbreviation", stateAbbreviation))
        filter_params.append(list_to_filter("state", state))
        filter_params.append(list_to_filter("stateID", stateID))
        filter_params.append(list_to_filter("county", county))
        filter_params.append(list_to_filter("countyID", countyID))
        filter_params.append(list_to_filter("producingArea", producingArea))
        filter_params.append(list_to_filter("producingAreaID", producingAreaID))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/americasgas-geography-master",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_americasgas_pipelineflows_master(
        self, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, legacyPointLogicPointID: Optional[Union[list[str], Series[str], str]] = None, legacyPointLogicLCIID: Optional[Union[list[str], Series[str], str]] = None, legacyBentekPointID: Optional[Union[list[str], Series[str], str]] = None, componentPointID: Optional[Union[list[str], Series[str], str]] = None, pipelineOperatorID: Optional[Union[list[str], Series[str], str]] = None, pipelineOperatorName: Optional[Union[list[str], Series[str], str]] = None, pipelineID: Optional[Union[list[str], Series[str], str]] = None, pipelineName: Optional[Union[list[str], Series[str], str]] = None, pointName: Optional[Union[list[str], Series[str], str]] = None, meterTypePrimary: Optional[Union[list[str], Series[str], str]] = None, meterTypeIDPrimary: Optional[Union[list[str], Series[str], str]] = None, meterTypeIDSecondary: Optional[Union[list[str], Series[str], str]] = None, meterTypeSecondary: Optional[Union[list[str], Series[str], str]] = None, flowDirection: Optional[Union[list[str], Series[str], str]] = None, flowDirectionCode: Optional[Union[list[str], Series[str], str]] = None, flowDirectionID: Optional[Union[list[str], Series[str], str]] = None, zone: Optional[Union[list[str], Series[str], str]] = None, companyID: Optional[Union[list[str], Series[str], str]] = None, connectingParty: Optional[Union[list[str], Series[str], str]] = None, locProp: Optional[Union[list[str], Series[str], str]] = None, pointIsActive: Optional[Union[list[str], Series[str], str]] = None, domain: Optional[Union[list[str], Series[str], str]] = None, domainID: Optional[Union[list[str], Series[str], str]] = None, regionID: Optional[Union[list[str], Series[str], str]] = None, region: Optional[Union[list[str], Series[str], str]] = None, subregionID: Optional[Union[list[str], Series[str], str]] = None, subregion: Optional[Union[list[str], Series[str], str]] = None, stateID: Optional[Union[list[str], Series[str], str]] = None, state: Optional[Union[list[str], Series[str], str]] = None, countyID: Optional[Union[list[str], Series[str], str]] = None, county: Optional[Union[list[str], Series[str], str]] = None, producingArea: Optional[Union[list[str], Series[str], str]] = None, producingAreaID: Optional[Union[list[str], Series[str], str]] = None, latitude: Optional[Union[list[str], Series[str], str]] = None, longitude: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         legacyPointLogicPointID: Optional[Union[list[str], Series[str], str]]
             Point ID for a meter used by the legacy PointLogic service., be default None
         legacyPointLogicLCIID: Optional[Union[list[str], Series[str], str]]
             Alternative point ID for a meter used by the legacy PointLogic service., be default None
         legacyBentekPointID: Optional[Union[list[str], Series[str], str]]
             Point ID for a meter used by the legacy Bentek service., be default None
         componentPointID: Optional[Union[list[str], Series[str], str]]
             Point ID for a meter used by the Americas Gas service., be default None
         pipelineOperatorID: Optional[Union[list[str], Series[str], str]]
             ID associated with the common parent owner or operator of a pipeline system., be default None
         pipelineOperatorName: Optional[Union[list[str], Series[str], str]]
             The name of the common parent owner or operator of a pipeline system., be default None
         pipelineID: Optional[Union[list[str], Series[str], str]]
             The ID given to a pipeline system, utilizes legacy Bentek pipeline ids when applicable., be default None
         pipelineName: Optional[Union[list[str], Series[str], str]]
             The display name of a pipeline system, utilizes legacy Bentek names when applicable., be default None
         pointName: Optional[Union[list[str], Series[str], str]]
             The display name of a meter or point, utilizes legacy Bentek point name when applicable., be default None
         meterTypePrimary: Optional[Union[list[str], Series[str], str]]
             The primary type of classification and purpose of a meter or point, utilizes legacy PointLogic definitions., be default None
         meterTypeIDPrimary: Optional[Union[list[str], Series[str], str]]
             An ID for the primary type of classification and purpose of a meter or point, utilizes legacy PointLogic definitions and ID., be default None
         meterTypeIDSecondary: Optional[Union[list[str], Series[str], str]]
             A secondary type classification and purpose of a meter or point, meant to provide an extra level of detail and utilizes legacy Bentek ids., be default None
         meterTypeSecondary: Optional[Union[list[str], Series[str], str]]
             A secondary type classification and purpose of a meter or point, meant to provide an extra level of detail, utilizes legacy Bentek definitions., be default None
         flowDirection: Optional[Union[list[str], Series[str], str]]
             Flow direction indicates the orientation of a point such as receipt, delivery, bi-directional or the reported flow direction of segment or compressor. Attribute is sourced from legacy PointLogic. Flow direction is primary to the similar and secondary attribute of Location Type., be default None
         flowDirectionCode: Optional[Union[list[str], Series[str], str]]
             A one letter code for Flow Direction such as ‘R’ for receipt or ‘D’ for delivery. Attribute is sourced from legacy PointLogic. Flow direction is primary to the similar and secondary attribute of Location Type., be default None
         flowDirectionID: Optional[Union[list[str], Series[str], str]]
             Flow direction identification number for the orientation of a point such as receipt, delivery, bi-directional or the reported flow direction of segment or compressor. Attribute is sourced from legacy PointLogic. Flow direction is primary to the similar and secondary attribute of Location Type., be default None
         zone: Optional[Union[list[str], Series[str], str]]
             A designation for where on the pipeline system the point is located, corresponding to a pipeline’s operational and market design. Zonal information is sourced from the legacy Bentek service., be default None
         companyID: Optional[Union[list[str], Series[str], str]]
             An ID sourced from the legacy Bentek service used to identify the connecting business or company name of a meter., be default None
         connectingParty: Optional[Union[list[str], Series[str], str]]
             The downstream connecting business name of a meter as reported by the pipeline, utilizes legacy Bentek service., be default None
         locProp: Optional[Union[list[str], Series[str], str]]
             The location propriety code reported by the pipeline for a specific meter., be default None
         pointIsActive: Optional[Union[list[str], Series[str], str]]
             A true or false return if a point or meter is active and in use within the Americas Gas service., be default None
         domain: Optional[Union[list[str], Series[str], str]]
             US Lower-48, Canada and Mexico., be default None
         domainID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the domain., be default None
         regionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic region., be default None
         region: Optional[Union[list[str], Series[str], str]]
             A defined geographic region within the Americas Gas service. Regions are an aggregation of states or provinces within a country., be default None
         subregionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic subregion., be default None
         subregion: Optional[Union[list[str], Series[str], str]]
             A defined geographic subregion within the Americas Gas service. A substate geography is sometimes referred to as a subregion. Subregions are an aggregation of specific counties within a region and a country., be default None
         stateID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the state or province utilizes legacy Bentek IDs., be default None
         state: Optional[Union[list[str], Series[str], str]]
             The political boundaries that define a state or province within country., be default None
         countyID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the county within a US state in which a meter or point resides, utilizes legacy Bentek IDs., be default None
         county: Optional[Union[list[str], Series[str], str]]
             The political boundaries of a defined county within a US state in which a meter or point resides., be default None
         producingArea: Optional[Union[list[str], Series[str], str]]
             Defined aggregation of counties within a state that is a best fit representation of prominent oil and gas plays and basins., be default None
         producingAreaID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for a defined Producing Area utilizes legacy PointLogic IDs., be default None
         latitude: Optional[Union[list[str], Series[str], str]]
             A geography based coordinate that specifies the north–south position of a point on the surface of the Earth. Latitude and longitude are used to identify the precise location of a pipeline meter or point., be default None
         longitude: Optional[Union[list[str], Series[str], str]]
             A geography based coordinate that specifies the east–west position of a point on the surface of the Earth. Latitude and longitude are used to identify the precise location of a pipeline meter or point., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("legacyPointLogicPointID", legacyPointLogicPointID))
        filter_params.append(list_to_filter("legacyPointLogicLCIID", legacyPointLogicLCIID))
        filter_params.append(list_to_filter("legacyBentekPointID", legacyBentekPointID))
        filter_params.append(list_to_filter("componentPointID", componentPointID))
        filter_params.append(list_to_filter("pipelineOperatorID", pipelineOperatorID))
        filter_params.append(list_to_filter("pipelineOperatorName", pipelineOperatorName))
        filter_params.append(list_to_filter("pipelineID", pipelineID))
        filter_params.append(list_to_filter("pipelineName", pipelineName))
        filter_params.append(list_to_filter("pointName", pointName))
        filter_params.append(list_to_filter("meterTypePrimary", meterTypePrimary))
        filter_params.append(list_to_filter("meterTypeIDPrimary", meterTypeIDPrimary))
        filter_params.append(list_to_filter("meterTypeIDSecondary", meterTypeIDSecondary))
        filter_params.append(list_to_filter("meterTypeSecondary", meterTypeSecondary))
        filter_params.append(list_to_filter("flowDirection", flowDirection))
        filter_params.append(list_to_filter("flowDirectionCode", flowDirectionCode))
        filter_params.append(list_to_filter("flowDirectionID", flowDirectionID))
        filter_params.append(list_to_filter("zone", zone))
        filter_params.append(list_to_filter("companyID", companyID))
        filter_params.append(list_to_filter("connectingParty", connectingParty))
        filter_params.append(list_to_filter("locProp", locProp))
        filter_params.append(list_to_filter("pointIsActive", pointIsActive))
        filter_params.append(list_to_filter("domain", domain))
        filter_params.append(list_to_filter("domainID", domainID))
        filter_params.append(list_to_filter("regionID", regionID))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("subregionID", subregionID))
        filter_params.append(list_to_filter("subregion", subregion))
        filter_params.append(list_to_filter("stateID", stateID))
        filter_params.append(list_to_filter("state", state))
        filter_params.append(list_to_filter("countyID", countyID))
        filter_params.append(list_to_filter("county", county))
        filter_params.append(list_to_filter("producingArea", producingArea))
        filter_params.append(list_to_filter("producingAreaID", producingAreaID))
        filter_params.append(list_to_filter("latitude", latitude))
        filter_params.append(list_to_filter("longitude", longitude))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/americasgas-pipelineflows-master",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_natural_gas_production(
        self, flowDate: Optional[Union[list[date], Series[date], date]] = None, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, dateFrequency: Optional[Union[list[str], Series[str], str]] = None, dateFrequencyDesc: Optional[Union[list[str], Series[str], str]] = None, modelID: Optional[Union[list[str], Series[str], str]] = None, modelType: Optional[Union[list[str], Series[str], str]] = None, modelTypeID: Optional[Union[list[str], Series[str], str]] = None, marketType: Optional[Union[list[str], Series[str], str]] = None, marketTypeID: Optional[Union[list[str], Series[str], str]] = None, functionType: Optional[Union[list[str], Series[str], str]] = None, functionTypeID: Optional[Union[list[str], Series[str], str]] = None, pointOfView: Optional[Union[list[str], Series[str], str]] = None, domain: Optional[Union[list[str], Series[str], str]] = None, domainID: Optional[Union[list[str], Series[str], str]] = None, region: Optional[Union[list[str], Series[str], str]] = None, regionID: Optional[Union[list[str], Series[str], str]] = None, subregion: Optional[Union[list[str], Series[str], str]] = None, subregionID: Optional[Union[list[str], Series[str], str]] = None, state: Optional[Union[list[str], Series[str], str]] = None, stateID: Optional[Union[list[str], Series[str], str]] = None, producingArea: Optional[Union[list[str], Series[str], str]] = None, producingAreaID: Optional[Union[list[str], Series[str], str]] = None, uom: Optional[Union[list[str], Series[str], str]] = None, volume: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         flowDate: Optional[Union[list[date], Series[date], date]]
             The calendar date or gas day the activity occurred., be default None
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         dateFrequency: Optional[Union[list[str], Series[str], str]]
             Daily, Weekly, Monthly, Seasonal, Annual., be default None
         dateFrequencyDesc: Optional[Union[list[str], Series[str], str]]
             The time period averages of the dataset such as Daily, Weekly, Monthly, Seasonal, Annual. Weekly date frequencies are based on the defined EIA storage week of Friday-Thursday. Seasonal date frequencies define Summer as April to October and Winter as November to March., be default None
         modelID: Optional[Union[list[str], Series[str], str]]
             Internal use, Model ID value., be default None
         modelType: Optional[Union[list[str], Series[str], str]]
             Model types can vary among supply, demand and other market fundamentals. The type describes the fundamentals the model output represents., be default None
         modelTypeID: Optional[Union[list[str], Series[str], str]]
             ID associated with Model type., be default None
         marketType: Optional[Union[list[str], Series[str], str]]
             Market Type name, actual or forecast., be default None
         marketTypeID: Optional[Union[list[str], Series[str], str]]
             ID associated with Market type., be default None
         functionType: Optional[Union[list[str], Series[str], str]]
             The name of the Function Type such as prediction, aggregation, allocation, ten year average., be default None
         functionTypeID: Optional[Union[list[str], Series[str], str]]
             The ID given to a Function Type such as 1 is prediction, 2 is aggregation, 3 is allocation, 4 is ten year average., be default None
         pointOfView: Optional[Union[list[str], Series[str], str]]
             Point of View for the values. Point of view based on a geographic hierarchy of country, region, subregion, or producing area., be default None
         domain: Optional[Union[list[str], Series[str], str]]
             US Lower-48, Canada and Mexico., be default None
         domainID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the domain., be default None
         region: Optional[Union[list[str], Series[str], str]]
             A defined geographic region within the Americas Gas service. Regions are an aggregation of states or provinces within a country., be default None
         regionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic region., be default None
         subregion: Optional[Union[list[str], Series[str], str]]
             A defined geographic subregion within the Americas Gas service. A substate geography is sometimes referred to as a subregion. Subregions are an aggregation of specific counties within a region and a country., be default None
         subregionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic subregion., be default None
         state: Optional[Union[list[str], Series[str], str]]
             The political boundaries that define a state or province within country., be default None
         stateID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the state or province utilizes legacy Bentek IDs., be default None
         producingArea: Optional[Union[list[str], Series[str], str]]
             Defined aggregation of counties within a state that is a best fit representation of prominent oil and gas plays and basins., be default None
         producingAreaID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for a defined Producing Area utilizes legacy PointLogic IDs., be default None
         uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure., be default None
         volume: Optional[Union[list[str], Series[str], str]]
             Volume., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("flowDate", flowDate))
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("dateFrequency", dateFrequency))
        filter_params.append(list_to_filter("dateFrequencyDesc", dateFrequencyDesc))
        filter_params.append(list_to_filter("modelID", modelID))
        filter_params.append(list_to_filter("modelType", modelType))
        filter_params.append(list_to_filter("modelTypeID", modelTypeID))
        filter_params.append(list_to_filter("marketType", marketType))
        filter_params.append(list_to_filter("marketTypeID", marketTypeID))
        filter_params.append(list_to_filter("functionType", functionType))
        filter_params.append(list_to_filter("functionTypeID", functionTypeID))
        filter_params.append(list_to_filter("pointOfView", pointOfView))
        filter_params.append(list_to_filter("domain", domain))
        filter_params.append(list_to_filter("domainID", domainID))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("regionID", regionID))
        filter_params.append(list_to_filter("subregion", subregion))
        filter_params.append(list_to_filter("subregionID", subregionID))
        filter_params.append(list_to_filter("state", state))
        filter_params.append(list_to_filter("stateID", stateID))
        filter_params.append(list_to_filter("producingArea", producingArea))
        filter_params.append(list_to_filter("producingAreaID", producingAreaID))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("volume", volume))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/natural-gas-production",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_modeled_demand_actual(
        self, flowDate: Optional[Union[list[date], Series[date], date]] = None, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, forecastDate: Optional[Union[list[str], Series[str], str]] = None, dateFrequency: Optional[Union[list[str], Series[str], str]] = None, dateFrequencyDesc: Optional[Union[list[str], Series[str], str]] = None, modelID: Optional[Union[list[str], Series[str], str]] = None, modelType: Optional[Union[list[str], Series[str], str]] = None, modelTypeID: Optional[Union[list[str], Series[str], str]] = None, marketType: Optional[Union[list[str], Series[str], str]] = None, marketTypeID: Optional[Union[list[str], Series[str], str]] = None, functionType: Optional[Union[list[str], Series[str], str]] = None, functionTypeID: Optional[Union[list[str], Series[str], str]] = None, pointOfView: Optional[Union[list[str], Series[str], str]] = None, domain: Optional[Union[list[str], Series[str], str]] = None, domainID: Optional[Union[list[str], Series[str], str]] = None, region: Optional[Union[list[str], Series[str], str]] = None, regionID: Optional[Union[list[str], Series[str], str]] = None, subregion: Optional[Union[list[str], Series[str], str]] = None, subregionID: Optional[Union[list[str], Series[str], str]] = None, uom: Optional[Union[list[str], Series[str], str]] = None, volume: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         flowDate: Optional[Union[list[date], Series[date], date]]
             The calendar date or gas day the activity occurred., be default None
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         forecastDate: Optional[Union[list[str], Series[str], str]]
             Standard Forecast Date., be default None
         dateFrequency: Optional[Union[list[str], Series[str], str]]
             Daily, Weekly, Monthly, Seasonal, Annual., be default None
         dateFrequencyDesc: Optional[Union[list[str], Series[str], str]]
             The time period averages of the dataset such as Daily, Weekly, Monthly, Seasonal, Annual. Weekly date frequencies are based on the defined EIA storage week of Friday-Thursday. Seasonal date frequencies define Summer as April to October and Winter as November to March., be default None
         modelID: Optional[Union[list[str], Series[str], str]]
             Internal use, Model ID value., be default None
         modelType: Optional[Union[list[str], Series[str], str]]
             Model types can vary among supply, demand and other market fundamentals. The type describes the fundamentals the model output represents., be default None
         modelTypeID: Optional[Union[list[str], Series[str], str]]
             ID associated with Model type., be default None
         marketType: Optional[Union[list[str], Series[str], str]]
             Market Type name, actual or forecast., be default None
         marketTypeID: Optional[Union[list[str], Series[str], str]]
             ID associated with Market type., be default None
         functionType: Optional[Union[list[str], Series[str], str]]
             The name of the Function Type such as prediction, aggregation, allocation, ten year average., be default None
         functionTypeID: Optional[Union[list[str], Series[str], str]]
             The ID given to a Function Type such as 1 is prediction, 2 is aggregation, 3 is allocation, 4 is ten year average., be default None
         pointOfView: Optional[Union[list[str], Series[str], str]]
             Point of View for the values. Point of view based on a geographic hierarchy of country, region, subregion, or producing area., be default None
         domain: Optional[Union[list[str], Series[str], str]]
             US Lower-48, Canada and Mexico., be default None
         domainID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the domain., be default None
         region: Optional[Union[list[str], Series[str], str]]
             A defined geographic region within the Americas Gas service. Regions are an aggregation of states or provinces within a country., be default None
         regionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic region., be default None
         subregion: Optional[Union[list[str], Series[str], str]]
             A defined geographic subregion within the Americas Gas service. A substate geography is sometimes referred to as a subregion. Subregions are an aggregation of specific counties within a region and a country., be default None
         subregionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic subregion., be default None
         uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure., be default None
         volume: Optional[Union[list[str], Series[str], str]]
             Volume., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("flowDate", flowDate))
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("forecastDate", forecastDate))
        filter_params.append(list_to_filter("dateFrequency", dateFrequency))
        filter_params.append(list_to_filter("dateFrequencyDesc", dateFrequencyDesc))
        filter_params.append(list_to_filter("modelID", modelID))
        filter_params.append(list_to_filter("modelType", modelType))
        filter_params.append(list_to_filter("modelTypeID", modelTypeID))
        filter_params.append(list_to_filter("marketType", marketType))
        filter_params.append(list_to_filter("marketTypeID", marketTypeID))
        filter_params.append(list_to_filter("functionType", functionType))
        filter_params.append(list_to_filter("functionTypeID", functionTypeID))
        filter_params.append(list_to_filter("pointOfView", pointOfView))
        filter_params.append(list_to_filter("domain", domain))
        filter_params.append(list_to_filter("domainID", domainID))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("regionID", regionID))
        filter_params.append(list_to_filter("subregion", subregion))
        filter_params.append(list_to_filter("subregionID", subregionID))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("volume", volume))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/modeled-demand-actual",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_pipeline_flows(
        self, flowDate: Optional[Union[list[date], Series[date], date]] = None, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, dateFrequency: Optional[Union[list[str], Series[str], str]] = None, dateFrequencyDesc: Optional[Union[list[str], Series[str], str]] = None, nominationCycle: Optional[Union[list[str], Series[str], str]] = None, legacyPointLogicPointID: Optional[Union[list[str], Series[str], str]] = None, legacyPointLogicLCIID: Optional[Union[list[str], Series[str], str]] = None, legacyBentekPointID: Optional[Union[list[str], Series[str], str]] = None, componentPointID: Optional[Union[list[str], Series[str], str]] = None, pipelineOperatorID: Optional[Union[list[str], Series[str], str]] = None, pipelineOperatorName: Optional[Union[list[str], Series[str], str]] = None, pipelineID: Optional[Union[list[str], Series[str], str]] = None, pipelineName: Optional[Union[list[str], Series[str], str]] = None, pointName: Optional[Union[list[str], Series[str], str]] = None, meterTypePrimary: Optional[Union[list[str], Series[str], str]] = None, meterTypeIDPrimary: Optional[Union[list[str], Series[str], str]] = None, meterTypeIDSecondary: Optional[Union[list[str], Series[str], str]] = None, meterTypeSecondary: Optional[Union[list[str], Series[str], str]] = None, locationTypeCode: Optional[Union[list[str], Series[str], str]] = None, locationDescription: Optional[Union[list[str], Series[str], str]] = None, locationTypeID: Optional[Union[list[str], Series[str], str]] = None, flowDirection: Optional[Union[list[str], Series[str], str]] = None, flowDirectionCode: Optional[Union[list[str], Series[str], str]] = None, flowDirectionID: Optional[Union[list[str], Series[str], str]] = None, zone: Optional[Union[list[str], Series[str], str]] = None, companyID: Optional[Union[list[str], Series[str], str]] = None, connectingParty: Optional[Union[list[str], Series[str], str]] = None, locProp: Optional[Union[list[str], Series[str], str]] = None, pointIsActive: Optional[Union[list[str], Series[str], str]] = None, domain: Optional[Union[list[str], Series[str], str]] = None, domainID: Optional[Union[list[str], Series[str], str]] = None, regionID: Optional[Union[list[str], Series[str], str]] = None, region: Optional[Union[list[str], Series[str], str]] = None, subregionID: Optional[Union[list[str], Series[str], str]] = None, subregion: Optional[Union[list[str], Series[str], str]] = None, stateID: Optional[Union[list[str], Series[str], str]] = None, state: Optional[Union[list[str], Series[str], str]] = None, countyID: Optional[Union[list[str], Series[str], str]] = None, county: Optional[Union[list[str], Series[str], str]] = None, producingArea: Optional[Union[list[str], Series[str], str]] = None, producingAreaID: Optional[Union[list[str], Series[str], str]] = None, latitude: Optional[Union[list[str], Series[str], str]] = None, longitude: Optional[Union[list[str], Series[str], str]] = None, designCapacity: Optional[Union[list[str], Series[str], str]] = None, uom: Optional[Union[list[str], Series[str], str]] = None, operationalCapacity: Optional[Union[list[str], Series[str], str]] = None, scheduledVolume: Optional[Union[list[str], Series[str], str]] = None, utilization: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         flowDate: Optional[Union[list[date], Series[date], date]]
             The calendar date or gas day the activity occurred., be default None
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         dateFrequency: Optional[Union[list[str], Series[str], str]]
             Daily, Weekly, Monthly, Seasonal, Annual., be default None
         dateFrequencyDesc: Optional[Union[list[str], Series[str], str]]
             The time period averages of the dataset such as Daily, Weekly, Monthly, Seasonal, Annual. Weekly date frequencies are based on the defined EIA storage week of Friday-Thursday. Seasonal date frequencies define Summer as April to October and Winter as November to March., be default None
         nominationCycle: Optional[Union[list[str], Series[str], str]]
             Standard NAESB defined nomination cycles for timely (T), evening (E), intraday 1 (I1), intraday 2 (I2) or intraday 3 (I3)., be default None
         legacyPointLogicPointID: Optional[Union[list[str], Series[str], str]]
             Point ID for a meter used by the legacy PointLogic service., be default None
         legacyPointLogicLCIID: Optional[Union[list[str], Series[str], str]]
             Alternative point ID for a meter used by the legacy PointLogic service., be default None
         legacyBentekPointID: Optional[Union[list[str], Series[str], str]]
             Point ID for a meter used by the legacy Bentek service., be default None
         componentPointID: Optional[Union[list[str], Series[str], str]]
             Point ID for a meter used by the Americas Gas service., be default None
         pipelineOperatorID: Optional[Union[list[str], Series[str], str]]
             ID associated with the common parent owner or operator of a pipeline system., be default None
         pipelineOperatorName: Optional[Union[list[str], Series[str], str]]
             The name of the common parent owner or operator of a pipeline system., be default None
         pipelineID: Optional[Union[list[str], Series[str], str]]
             The ID given to a pipeline system, utilizes legacy Bentek pipeline ids when applicable., be default None
         pipelineName: Optional[Union[list[str], Series[str], str]]
             The display name of a pipeline system, utilizes legacy Bentek names when applicable., be default None
         pointName: Optional[Union[list[str], Series[str], str]]
             The display name of a meter or point, utilizes legacy Bentek point name when applicable., be default None
         meterTypePrimary: Optional[Union[list[str], Series[str], str]]
             The primary type of classification and purpose of a meter or point, utilizes legacy PointLogic definitions., be default None
         meterTypeIDPrimary: Optional[Union[list[str], Series[str], str]]
             An ID for the primary type of classification and purpose of a meter or point, utilizes legacy PointLogic definitions and ID., be default None
         meterTypeIDSecondary: Optional[Union[list[str], Series[str], str]]
             A secondary type classification and purpose of a meter or point, meant to provide an extra level of detail and utilizes legacy Bentek ids., be default None
         meterTypeSecondary: Optional[Union[list[str], Series[str], str]]
             A secondary type classification and purpose of a meter or point, meant to provide an extra level of detail, utilizes legacy Bentek definitions., be default None
         locationTypeCode: Optional[Union[list[str], Series[str], str]]
             Location type code is a one letter abbreviation of the location description. Location types are sourced from legacy Bentek. These are similar to Flow Direction but serve as a secondary attribute., be default None
         locationDescription: Optional[Union[list[str], Series[str], str]]
             Location types are sourced from legacy Bentek. These are similar to Flow Direction but serve as a secondary attribute., be default None
         locationTypeID: Optional[Union[list[str], Series[str], str]]
             An ID for the location type sourced from legacy Bentek. These are similar to Flow Direction but serve as a secondary attribute., be default None
         flowDirection: Optional[Union[list[str], Series[str], str]]
             Flow direction indicates the orientation of a point such as receipt, delivery, bi-directional or the reported flow direction of segment or compressor. Attribute is sourced from legacy PointLogic. Flow direction is primary to the similar and secondary attribute of Location Type., be default None
         flowDirectionCode: Optional[Union[list[str], Series[str], str]]
             A one letter code for Flow Direction such as ‘R’ for receipt or ‘D’ for delivery. Attribute is sourced from legacy PointLogic. Flow direction is primary to the similar and secondary attribute of Location Type., be default None
         flowDirectionID: Optional[Union[list[str], Series[str], str]]
             Flow direction identification number for the orientation of a point such as receipt, delivery, bi-directional or the reported flow direction of segment or compressor. Attribute is sourced from legacy PointLogic. Flow direction is primary to the similar and secondary attribute of Location Type., be default None
         zone: Optional[Union[list[str], Series[str], str]]
             A designation for where on the pipeline system the point is located, corresponding to a pipeline’s operational and market design. Zonal information is sourced from the legacy Bentek service., be default None
         companyID: Optional[Union[list[str], Series[str], str]]
             An ID sourced from the legacy Bentek service used to identify the connecting business or company name of a meter., be default None
         connectingParty: Optional[Union[list[str], Series[str], str]]
             The downstream connecting business name of a meter as reported by the pipeline, utilizes legacy Bentek service., be default None
         locProp: Optional[Union[list[str], Series[str], str]]
             The location propriety code reported by the pipeline for a specific meter., be default None
         pointIsActive: Optional[Union[list[str], Series[str], str]]
             A true or false return if a point or meter is active and in use within the Americas Gas service., be default None
         domain: Optional[Union[list[str], Series[str], str]]
             US Lower-48, Canada and Mexico., be default None
         domainID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the domain., be default None
         regionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic region., be default None
         region: Optional[Union[list[str], Series[str], str]]
             A defined geographic region within the Americas Gas service. Regions are an aggregation of states or provinces within a country., be default None
         subregionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic subregion., be default None
         subregion: Optional[Union[list[str], Series[str], str]]
             A defined geographic subregion within the Americas Gas service. A substate geography is sometimes referred to as a subregion. Subregions are an aggregation of specific counties within a region and a country., be default None
         stateID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the state or province utilizes legacy Bentek IDs., be default None
         state: Optional[Union[list[str], Series[str], str]]
             The political boundaries that define a state or province within country., be default None
         countyID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the county within a US state in which a meter or point resides, utilizes legacy Bentek IDs., be default None
         county: Optional[Union[list[str], Series[str], str]]
             The political boundaries of a defined county within a US state in which a meter or point resides., be default None
         producingArea: Optional[Union[list[str], Series[str], str]]
             Defined aggregation of counties within a state that is a best fit representation of prominent oil and gas plays and basins., be default None
         producingAreaID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for a defined Producing Area utilizes legacy PointLogic IDs., be default None
         latitude: Optional[Union[list[str], Series[str], str]]
             A geography based coordinate that specifies the north–south position of a point on the surface of the Earth. Latitude and longitude are used to identify the precise location of a pipeline meter or point., be default None
         longitude: Optional[Union[list[str], Series[str], str]]
             A geography based coordinate that specifies the east–west position of a point on the surface of the Earth. Latitude and longitude are used to identify the precise location of a pipeline meter or point., be default None
         designCapacity: Optional[Union[list[str], Series[str], str]]
             The volumetric max that a given meter, segment or compressor can receive or deliver as reported by the pipeline., be default None
         uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure., be default None
         operationalCapacity: Optional[Union[list[str], Series[str], str]]
             The pipeline’s reported daily operational capacity for a specific meter, segment or compressor can receive or deliver., be default None
         scheduledVolume: Optional[Union[list[str], Series[str], str]]
             Scheduled volume as reported by the pipeline for a specific meter, segment or compressor., be default None
         utilization: Optional[Union[list[str], Series[str], str]]
             Utilization rate in decimal form or in percentage terms. Utilization for a given meter is calculated by dividing the scheduled volume by its operational capacity., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("flowDate", flowDate))
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("dateFrequency", dateFrequency))
        filter_params.append(list_to_filter("dateFrequencyDesc", dateFrequencyDesc))
        filter_params.append(list_to_filter("nominationCycle", nominationCycle))
        filter_params.append(list_to_filter("legacyPointLogicPointID", legacyPointLogicPointID))
        filter_params.append(list_to_filter("legacyPointLogicLCIID", legacyPointLogicLCIID))
        filter_params.append(list_to_filter("legacyBentekPointID", legacyBentekPointID))
        filter_params.append(list_to_filter("componentPointID", componentPointID))
        filter_params.append(list_to_filter("pipelineOperatorID", pipelineOperatorID))
        filter_params.append(list_to_filter("pipelineOperatorName", pipelineOperatorName))
        filter_params.append(list_to_filter("pipelineID", pipelineID))
        filter_params.append(list_to_filter("pipelineName", pipelineName))
        filter_params.append(list_to_filter("pointName", pointName))
        filter_params.append(list_to_filter("meterTypePrimary", meterTypePrimary))
        filter_params.append(list_to_filter("meterTypeIDPrimary", meterTypeIDPrimary))
        filter_params.append(list_to_filter("meterTypeIDSecondary", meterTypeIDSecondary))
        filter_params.append(list_to_filter("meterTypeSecondary", meterTypeSecondary))
        filter_params.append(list_to_filter("locationTypeCode", locationTypeCode))
        filter_params.append(list_to_filter("locationDescription", locationDescription))
        filter_params.append(list_to_filter("locationTypeID", locationTypeID))
        filter_params.append(list_to_filter("flowDirection", flowDirection))
        filter_params.append(list_to_filter("flowDirectionCode", flowDirectionCode))
        filter_params.append(list_to_filter("flowDirectionID", flowDirectionID))
        filter_params.append(list_to_filter("zone", zone))
        filter_params.append(list_to_filter("companyID", companyID))
        filter_params.append(list_to_filter("connectingParty", connectingParty))
        filter_params.append(list_to_filter("locProp", locProp))
        filter_params.append(list_to_filter("pointIsActive", pointIsActive))
        filter_params.append(list_to_filter("domain", domain))
        filter_params.append(list_to_filter("domainID", domainID))
        filter_params.append(list_to_filter("regionID", regionID))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("subregionID", subregionID))
        filter_params.append(list_to_filter("subregion", subregion))
        filter_params.append(list_to_filter("stateID", stateID))
        filter_params.append(list_to_filter("state", state))
        filter_params.append(list_to_filter("countyID", countyID))
        filter_params.append(list_to_filter("county", county))
        filter_params.append(list_to_filter("producingArea", producingArea))
        filter_params.append(list_to_filter("producingAreaID", producingAreaID))
        filter_params.append(list_to_filter("latitude", latitude))
        filter_params.append(list_to_filter("longitude", longitude))
        filter_params.append(list_to_filter("designCapacity", designCapacity))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("operationalCapacity", operationalCapacity))
        filter_params.append(list_to_filter("scheduledVolume", scheduledVolume))
        filter_params.append(list_to_filter("utilization", utilization))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/pipeline-flows",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_population_weighted_weather(
        self, flowDate: Optional[Union[list[date], Series[date], date]] = None, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, forecastDate: Optional[Union[list[str], Series[str], str]] = None, dateFrequency: Optional[Union[list[str], Series[str], str]] = None, dateFrequencyDesc: Optional[Union[list[str], Series[str], str]] = None, marketType: Optional[Union[list[str], Series[str], str]] = None, marketTypeID: Optional[Union[list[str], Series[str], str]] = None, pointOfView: Optional[Union[list[str], Series[str], str]] = None, geographyID: Optional[Union[list[str], Series[str], str]] = None, domain: Optional[Union[list[str], Series[str], str]] = None, domainID: Optional[Union[list[str], Series[str], str]] = None, region: Optional[Union[list[str], Series[str], str]] = None, regionID: Optional[Union[list[str], Series[str], str]] = None, subregion: Optional[Union[list[str], Series[str], str]] = None, subregionID: Optional[Union[list[str], Series[str], str]] = None, temperatureUnitOfMeasure: Optional[Union[list[str], Series[str], str]] = None, weightedTemperature: Optional[Union[list[str], Series[str], str]] = None, normalTemperature: Optional[Union[list[str], Series[str], str]] = None, heatingDegreeDay: Optional[Union[list[str], Series[str], str]] = None, coolingDegreeDay: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         flowDate: Optional[Union[list[date], Series[date], date]]
             The calendar date or gas day the activity occurred., be default None
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         forecastDate: Optional[Union[list[str], Series[str], str]]
             Standard Forecast Date., be default None
         dateFrequency: Optional[Union[list[str], Series[str], str]]
             Daily, Weekly, Monthly, Seasonal, Annual., be default None
         dateFrequencyDesc: Optional[Union[list[str], Series[str], str]]
             The time period averages of the dataset such as Daily, Weekly, Monthly, Seasonal, Annual. Weekly date frequencies are based on the defined EIA storage week of Friday-Thursday. Seasonal date frequencies define Summer as April to October and Winter as November to March., be default None
         marketType: Optional[Union[list[str], Series[str], str]]
             Market Type name, actual or forecast, be default None
         marketTypeID: Optional[Union[list[str], Series[str], str]]
             ID associated with Market type., be default None
         pointOfView: Optional[Union[list[str], Series[str], str]]
             Point of View for the values. Point of view based on a geographic hierarchy of country, region, subregion, or producing area., be default None
         geographyID: Optional[Union[list[str], Series[str], str]]
             Geography ID value for the point of view., be default None
         domain: Optional[Union[list[str], Series[str], str]]
             US Lower-48, Canada and Mexico., be default None
         domainID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the domain., be default None
         region: Optional[Union[list[str], Series[str], str]]
             A defined geographic region within the Americas Gas service. Regions are an aggregation of states or provinces within a country., be default None
         regionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic region., be default None
         subregion: Optional[Union[list[str], Series[str], str]]
             A defined geographic subregion within the Americas Gas service. A substate geography is sometimes referred to as a subregion. Subregions are an aggregation of specific counties within a region and a country., be default None
         subregionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic subregion., be default None
         temperatureUnitOfMeasure: Optional[Union[list[str], Series[str], str]]
             Temperature unit of measure., be default None
         weightedTemperature: Optional[Union[list[str], Series[str], str]]
             Population weighted temperature value., be default None
         normalTemperature: Optional[Union[list[str], Series[str], str]]
             10-year normal temperature value., be default None
         heatingDegreeDay: Optional[Union[list[str], Series[str], str]]
             Heating Degree Day value., be default None
         coolingDegreeDay: Optional[Union[list[str], Series[str], str]]
             Cooling Degree Day value., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("flowDate", flowDate))
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("forecastDate", forecastDate))
        filter_params.append(list_to_filter("dateFrequency", dateFrequency))
        filter_params.append(list_to_filter("dateFrequencyDesc", dateFrequencyDesc))
        filter_params.append(list_to_filter("marketType", marketType))
        filter_params.append(list_to_filter("marketTypeID", marketTypeID))
        filter_params.append(list_to_filter("pointOfView", pointOfView))
        filter_params.append(list_to_filter("geographyID", geographyID))
        filter_params.append(list_to_filter("domain", domain))
        filter_params.append(list_to_filter("domainID", domainID))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("regionID", regionID))
        filter_params.append(list_to_filter("subregion", subregion))
        filter_params.append(list_to_filter("subregionID", subregionID))
        filter_params.append(list_to_filter("temperatureUnitOfMeasure", temperatureUnitOfMeasure))
        filter_params.append(list_to_filter("weightedTemperature", weightedTemperature))
        filter_params.append(list_to_filter("normalTemperature", normalTemperature))
        filter_params.append(list_to_filter("heatingDegreeDay", heatingDegreeDay))
        filter_params.append(list_to_filter("coolingDegreeDay", coolingDegreeDay))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/population-weighted-weather",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_modeled_demand_forecast(
        self, flowDate: Optional[Union[list[date], Series[date], date]] = None, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, forecastDate: Optional[Union[list[str], Series[str], str]] = None, dateFrequency: Optional[Union[list[str], Series[str], str]] = None, dateFrequencyDesc: Optional[Union[list[str], Series[str], str]] = None, modelID: Optional[Union[list[str], Series[str], str]] = None, modelType: Optional[Union[list[str], Series[str], str]] = None, modelTypeID: Optional[Union[list[str], Series[str], str]] = None, marketType: Optional[Union[list[str], Series[str], str]] = None, marketTypeID: Optional[Union[list[str], Series[str], str]] = None, functionType: Optional[Union[list[str], Series[str], str]] = None, functionTypeID: Optional[Union[list[str], Series[str], str]] = None, pointOfView: Optional[Union[list[str], Series[str], str]] = None, domain: Optional[Union[list[str], Series[str], str]] = None, domainID: Optional[Union[list[str], Series[str], str]] = None, region: Optional[Union[list[str], Series[str], str]] = None, regionID: Optional[Union[list[str], Series[str], str]] = None, subregion: Optional[Union[list[str], Series[str], str]] = None, subregionID: Optional[Union[list[str], Series[str], str]] = None, uom: Optional[Union[list[str], Series[str], str]] = None, volume: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         flowDate: Optional[Union[list[date], Series[date], date]]
             The calendar date or gas day the activity occurred., be default None
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         forecastDate: Optional[Union[list[str], Series[str], str]]
             Standard Forecast Date., be default None
         dateFrequency: Optional[Union[list[str], Series[str], str]]
             Daily, Weekly, Monthly, Seasonal, Annual., be default None
         dateFrequencyDesc: Optional[Union[list[str], Series[str], str]]
             The time period averages of the dataset such as Daily, Weekly, Monthly, Seasonal, Annual. Weekly date frequencies are based on the defined EIA storage week of Friday-Thursday. Seasonal date frequencies define Summer as April to October and Winter as November to March., be default None
         modelID: Optional[Union[list[str], Series[str], str]]
             Internal use, Model ID value., be default None
         modelType: Optional[Union[list[str], Series[str], str]]
             Model types can vary among supply, demand and other market fundamentals. The type describes the fundamentals the model output represents., be default None
         modelTypeID: Optional[Union[list[str], Series[str], str]]
             ID associated with Model type., be default None
         marketType: Optional[Union[list[str], Series[str], str]]
             Market Type name, actual or forecast, be default None
         marketTypeID: Optional[Union[list[str], Series[str], str]]
             ID associated with Market type., be default None
         functionType: Optional[Union[list[str], Series[str], str]]
             The name of the Function Type such as prediction, aggregation, allocation, ten year average., be default None
         functionTypeID: Optional[Union[list[str], Series[str], str]]
             The ID given to a Function Type such as 1 is prediction, 2 is aggregation, 3 is allocation, 4 is ten year average., be default None
         pointOfView: Optional[Union[list[str], Series[str], str]]
             Point of View for the values. Point of view based on a geographic hierarchy of country, region, subregion, or producing area., be default None
         domain: Optional[Union[list[str], Series[str], str]]
             US Lower-48, Canada and Mexico., be default None
         domainID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the domain., be default None
         region: Optional[Union[list[str], Series[str], str]]
             A defined geographic region within the Americas Gas service. Regions are an aggregation of states or provinces within a country., be default None
         regionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic region., be default None
         subregion: Optional[Union[list[str], Series[str], str]]
             A defined geographic subregion within the Americas Gas service. A substate geography is sometimes referred to as a subregion. Subregions are an aggregation of specific counties within a region and a country., be default None
         subregionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic subregion., be default None
         uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure., be default None
         volume: Optional[Union[list[str], Series[str], str]]
             Volume., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("flowDate", flowDate))
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("forecastDate", forecastDate))
        filter_params.append(list_to_filter("dateFrequency", dateFrequency))
        filter_params.append(list_to_filter("dateFrequencyDesc", dateFrequencyDesc))
        filter_params.append(list_to_filter("modelID", modelID))
        filter_params.append(list_to_filter("modelType", modelType))
        filter_params.append(list_to_filter("modelTypeID", modelTypeID))
        filter_params.append(list_to_filter("marketType", marketType))
        filter_params.append(list_to_filter("marketTypeID", marketTypeID))
        filter_params.append(list_to_filter("functionType", functionType))
        filter_params.append(list_to_filter("functionTypeID", functionTypeID))
        filter_params.append(list_to_filter("pointOfView", pointOfView))
        filter_params.append(list_to_filter("domain", domain))
        filter_params.append(list_to_filter("domainID", domainID))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("regionID", regionID))
        filter_params.append(list_to_filter("subregion", subregion))
        filter_params.append(list_to_filter("subregionID", subregionID))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("volume", volume))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/modeled-demand-forecast",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_no_notice_flow_data(
        self, flowDate: Optional[Union[list[date], Series[date], date]] = None, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, dateFrequency: Optional[Union[list[str], Series[str], str]] = None, dateFrequencyDesc: Optional[Union[list[str], Series[str], str]] = None, legacyBentekPointID: Optional[Union[list[str], Series[str], str]] = None, componentPointID: Optional[Union[list[str], Series[str], str]] = None, pipelineOperatorID: Optional[Union[list[str], Series[str], str]] = None, pipelineOperatorName: Optional[Union[list[str], Series[str], str]] = None, pipelineID: Optional[Union[list[str], Series[str], str]] = None, pipelineName: Optional[Union[list[str], Series[str], str]] = None, pointName: Optional[Union[list[str], Series[str], str]] = None, meterTypeIDPrimary: Optional[Union[list[str], Series[str], str]] = None, meterTypePrimary: Optional[Union[list[str], Series[str], str]] = None, meterTypeIDSecondary: Optional[Union[list[str], Series[str], str]] = None, meterTypeSecondary: Optional[Union[list[str], Series[str], str]] = None, locationTypeCode: Optional[Union[list[str], Series[str], str]] = None, locationDescription: Optional[Union[list[str], Series[str], str]] = None, locationTypeID: Optional[Union[list[str], Series[str], str]] = None, flowDirection: Optional[Union[list[str], Series[str], str]] = None, commonCode: Optional[Union[list[str], Series[str], str]] = None, zone: Optional[Union[list[str], Series[str], str]] = None, companyID: Optional[Union[list[str], Series[str], str]] = None, connectingParty: Optional[Union[list[str], Series[str], str]] = None, locProp: Optional[Union[list[str], Series[str], str]] = None, pointIsActive: Optional[Union[list[str], Series[str], str]] = None, domainID: Optional[Union[list[str], Series[str], str]] = None, domain: Optional[Union[list[str], Series[str], str]] = None, regionID: Optional[Union[list[str], Series[str], str]] = None, region: Optional[Union[list[str], Series[str], str]] = None, subregionID: Optional[Union[list[str], Series[str], str]] = None, subregion: Optional[Union[list[str], Series[str], str]] = None, stateID: Optional[Union[list[str], Series[str], str]] = None, state: Optional[Union[list[str], Series[str], str]] = None, countyID: Optional[Union[list[str], Series[str], str]] = None, county: Optional[Union[list[str], Series[str], str]] = None, producingAreaID: Optional[Union[list[str], Series[str], str]] = None, producingArea: Optional[Union[list[str], Series[str], str]] = None, latitude: Optional[Union[list[str], Series[str], str]] = None, longitude: Optional[Union[list[str], Series[str], str]] = None, uom: Optional[Union[list[str], Series[str], str]] = None, scheduledVolume: Optional[Union[list[str], Series[str], str]] = None, actualVolume: Optional[Union[list[str], Series[str], str]] = None, utilization: Optional[Union[list[str], Series[str], str]] = None, designCapacity: Optional[Union[list[str], Series[str], str]] = None, operationalCapacity: Optional[Union[list[str], Series[str], str]] = None, actualCapacity: Optional[Union[list[str], Series[str], str]] = None, operationallyAvailable: Optional[Union[list[str], Series[str], str]] = None, interruptibleFlow: Optional[Union[list[str], Series[str], str]] = None, dataSource: Optional[Union[list[str], Series[str], str]] = None, postingDatetime: Optional[Union[list[str], Series[str], str]] = None, createDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         flowDate: Optional[Union[list[date], Series[date], date]]
             The calendar date or gas day the activity occurred., be default None
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         dateFrequency: Optional[Union[list[str], Series[str], str]]
             Daily, Weekly, Monthly, Seasonal, Annual., be default None
         dateFrequencyDesc: Optional[Union[list[str], Series[str], str]]
             The time period averages of the dataset such as Daily, Weekly, Monthly, Seasonal, Annual. Weekly date frequencies are based on the defined EIA storage week of Friday-Thursday. Seasonal date frequencies define Summer as April to October and Winter as November to March., be default None
         legacyBentekPointID: Optional[Union[list[str], Series[str], str]]
             Point ID for a meter used by the legacy Bentek service., be default None
         componentPointID: Optional[Union[list[str], Series[str], str]]
             Point ID for a meter used by the Americas Gas service., be default None
         pipelineOperatorID: Optional[Union[list[str], Series[str], str]]
             ID associated with the common parent owner or operator of a pipeline system., be default None
         pipelineOperatorName: Optional[Union[list[str], Series[str], str]]
             The name of the common parent owner or operator of a pipeline system., be default None
         pipelineID: Optional[Union[list[str], Series[str], str]]
             The ID given to a pipeline system, utilizes legacy Bentek pipeline ids when applicable., be default None
         pipelineName: Optional[Union[list[str], Series[str], str]]
             The display name of a pipeline system, utilizes legacy Bentek names when applicable., be default None
         pointName: Optional[Union[list[str], Series[str], str]]
             The display name of a meter or point, utilizes legacy Bentek point name when applicable., be default None
         meterTypeIDPrimary: Optional[Union[list[str], Series[str], str]]
             An ID for the primary type of classification and purpose of a meter or point, utilizes legacy PointLogic definitions and ID., be default None
         meterTypePrimary: Optional[Union[list[str], Series[str], str]]
             The primary type of classification and purpose of a meter or point, utilizes legacy PointLogic definitions., be default None
         meterTypeIDSecondary: Optional[Union[list[str], Series[str], str]]
             A secondary type classification and purpose of a meter or point, meant to provide an extra level of detail and utilizes legacy Bentek ids., be default None
         meterTypeSecondary: Optional[Union[list[str], Series[str], str]]
             A secondary type classification and purpose of a meter or point, meant to provide an extra level of detail, utilizes legacy Bentek definitions., be default None
         locationTypeCode: Optional[Union[list[str], Series[str], str]]
             Location type code is a one letter abbreviation of the location description. Location types are sourced from legacy Bentek. These are similar to Flow Direction but serve as a secondary attribute., be default None
         locationDescription: Optional[Union[list[str], Series[str], str]]
             Location types are sourced from legacy Bentek. These are similar to Flow Direction but serve as a secondary attribute., be default None
         locationTypeID: Optional[Union[list[str], Series[str], str]]
             An ID for the location type sourced from legacy Bentek. These are similar to Flow Direction but serve as a secondary attribute., be default None
         flowDirection: Optional[Union[list[str], Series[str], str]]
             Flow direction indicates the orientation of a point such as receipt, delivery, bi-directional or the reported flow direction of segment or compressor. Attribute is sourced from legacy PointLogic. Flow direction is primary to the similar and secondary attribute of Location Type., be default None
         commonCode: Optional[Union[list[str], Series[str], str]]
             Common Code, when used, may provide additional information about the point as reported by the pipeline., be default None
         zone: Optional[Union[list[str], Series[str], str]]
             A designation for where on the pipeline system the point is located, corresponding to a pipeline’s operational and market design. Zonal information is sourced from the legacy Bentek service., be default None
         companyID: Optional[Union[list[str], Series[str], str]]
             An ID sourced from the legacy Bentek service used to identify the connecting business or company name of a meter., be default None
         connectingParty: Optional[Union[list[str], Series[str], str]]
             The downstream connecting business name of a meter as reported by the pipeline, utilizes legacy Bentek service., be default None
         locProp: Optional[Union[list[str], Series[str], str]]
             The location propriety code reported by the pipeline for a specific meter., be default None
         pointIsActive: Optional[Union[list[str], Series[str], str]]
             A true or false return if a point or meter is active and in use within the Americas Gas service., be default None
         domainID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the domain., be default None
         domain: Optional[Union[list[str], Series[str], str]]
             US Lower-48, Canada and Mexico., be default None
         regionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic region., be default None
         region: Optional[Union[list[str], Series[str], str]]
             A defined geographic region within the Americas Gas service. Regions are an aggregation of states or provinces within a country., be default None
         subregionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic subregion in which a meter or point resides., be default None
         subregion: Optional[Union[list[str], Series[str], str]]
             A defined geographic subregion within the Americas Gas service. A substate geography is sometimes referred to as a subregion. Subregions are an aggregation of specific counties within a region and a country., be default None
         stateID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the state or province utilizes legacy Bentek IDs., be default None
         state: Optional[Union[list[str], Series[str], str]]
             The political boundaries that define a state or province within country., be default None
         countyID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the county within a US state in which a meter or point resides, utilizes legacy Bentek IDs., be default None
         county: Optional[Union[list[str], Series[str], str]]
             The political boundaries of a defined county within a US state in which a meter or point resides., be default None
         producingAreaID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for a defined Producing Area, utilizes legacy PointLogic IDs., be default None
         producingArea: Optional[Union[list[str], Series[str], str]]
             Defined aggregation of counties within a state that is a best fit representation of prominent oil and gas plays and basins., be default None
         latitude: Optional[Union[list[str], Series[str], str]]
             A geography based coordinate that specifies the north–south position of a point on the surface of the Earth. Latitude and longitude are used to identify the precise location of a pipeline meter or point., be default None
         longitude: Optional[Union[list[str], Series[str], str]]
             A geography based coordinate that specifies the east–west position of a point on the surface of the Earth. Latitude and longitude are used to identify the precise location of a pipeline meter or point., be default None
         uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure., be default None
         scheduledVolume: Optional[Union[list[str], Series[str], str]]
             Scheduled volume as reported by the pipeline for a specific meter, segment or compressor., be default None
         actualVolume: Optional[Union[list[str], Series[str], str]]
             Actual volume as reported by the pipeline for a specific meter, segment or compressor., be default None
         utilization: Optional[Union[list[str], Series[str], str]]
             Utilization rate in decimal form or in percentage terms. Utilization for a given meter is calculated by dividing the scheduled volume by its operational capacity., be default None
         designCapacity: Optional[Union[list[str], Series[str], str]]
             The volumetric max that a given meter, segment or compressor can receive or deliver as reported by the pipeline., be default None
         operationalCapacity: Optional[Union[list[str], Series[str], str]]
             The pipeline’s reported daily operational capacity for a specific meter, segment or compressor can receive or deliver., be default None
         actualCapacity: Optional[Union[list[str], Series[str], str]]
             The actual capacity for a specific meter, segment or compressor can receive or deliver., be default None
         operationallyAvailable: Optional[Union[list[str], Series[str], str]]
             The remaining volume available for a given meter as reported by the pipeline. The difference between operational capacity and scheduled volume., be default None
         interruptibleFlow: Optional[Union[list[str], Series[str], str]]
             If available, the volume scheduled on an interruptible contract., be default None
         dataSource: Optional[Union[list[str], Series[str], str]]
             Source of the data., be default None
         postingDatetime: Optional[Union[list[str], Series[str], str]]
             Day and time the record was last posted., be default None
         createDate: Optional[Union[list[str], Series[str], str]]
             The date and time stamp of when the record was created., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("flowDate", flowDate))
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("dateFrequency", dateFrequency))
        filter_params.append(list_to_filter("dateFrequencyDesc", dateFrequencyDesc))
        filter_params.append(list_to_filter("legacyBentekPointID", legacyBentekPointID))
        filter_params.append(list_to_filter("componentPointID", componentPointID))
        filter_params.append(list_to_filter("pipelineOperatorID", pipelineOperatorID))
        filter_params.append(list_to_filter("pipelineOperatorName", pipelineOperatorName))
        filter_params.append(list_to_filter("pipelineID", pipelineID))
        filter_params.append(list_to_filter("pipelineName", pipelineName))
        filter_params.append(list_to_filter("pointName", pointName))
        filter_params.append(list_to_filter("meterTypeIDPrimary", meterTypeIDPrimary))
        filter_params.append(list_to_filter("meterTypePrimary", meterTypePrimary))
        filter_params.append(list_to_filter("meterTypeIDSecondary", meterTypeIDSecondary))
        filter_params.append(list_to_filter("meterTypeSecondary", meterTypeSecondary))
        filter_params.append(list_to_filter("locationTypeCode", locationTypeCode))
        filter_params.append(list_to_filter("locationDescription", locationDescription))
        filter_params.append(list_to_filter("locationTypeID", locationTypeID))
        filter_params.append(list_to_filter("flowDirection", flowDirection))
        filter_params.append(list_to_filter("commonCode", commonCode))
        filter_params.append(list_to_filter("zone", zone))
        filter_params.append(list_to_filter("companyID", companyID))
        filter_params.append(list_to_filter("connectingParty", connectingParty))
        filter_params.append(list_to_filter("locProp", locProp))
        filter_params.append(list_to_filter("pointIsActive", pointIsActive))
        filter_params.append(list_to_filter("domainID", domainID))
        filter_params.append(list_to_filter("domain", domain))
        filter_params.append(list_to_filter("regionID", regionID))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("subregionID", subregionID))
        filter_params.append(list_to_filter("subregion", subregion))
        filter_params.append(list_to_filter("stateID", stateID))
        filter_params.append(list_to_filter("state", state))
        filter_params.append(list_to_filter("countyID", countyID))
        filter_params.append(list_to_filter("county", county))
        filter_params.append(list_to_filter("producingAreaID", producingAreaID))
        filter_params.append(list_to_filter("producingArea", producingArea))
        filter_params.append(list_to_filter("latitude", latitude))
        filter_params.append(list_to_filter("longitude", longitude))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("scheduledVolume", scheduledVolume))
        filter_params.append(list_to_filter("actualVolume", actualVolume))
        filter_params.append(list_to_filter("utilization", utilization))
        filter_params.append(list_to_filter("designCapacity", designCapacity))
        filter_params.append(list_to_filter("operationalCapacity", operationalCapacity))
        filter_params.append(list_to_filter("actualCapacity", actualCapacity))
        filter_params.append(list_to_filter("operationallyAvailable", operationallyAvailable))
        filter_params.append(list_to_filter("interruptibleFlow", interruptibleFlow))
        filter_params.append(list_to_filter("dataSource", dataSource))
        filter_params.append(list_to_filter("postingDatetime", postingDatetime))
        filter_params.append(list_to_filter("createDate", createDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/no-notice-flow-data",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_gas_quality_data(
        self, measurementDate: Optional[Union[list[str], Series[str], str]] = None, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, dateFrequency: Optional[Union[list[str], Series[str], str]] = None, dateFrequencyDesc: Optional[Union[list[str], Series[str], str]] = None, legacyBentekPointID: Optional[Union[list[str], Series[str], str]] = None, componentPointID: Optional[Union[list[str], Series[str], str]] = None, pipelineOperatorID: Optional[Union[list[str], Series[str], str]] = None, pipelineOperatorName: Optional[Union[list[str], Series[str], str]] = None, pipelineID: Optional[Union[list[str], Series[str], str]] = None, pipelineName: Optional[Union[list[str], Series[str], str]] = None, gasCompositionTypeID: Optional[Union[list[str], Series[str], str]] = None, gasCompositionName: Optional[Union[list[str], Series[str], str]] = None, pointName: Optional[Union[list[str], Series[str], str]] = None, meterTypeID: Optional[Union[list[str], Series[str], str]] = None, meterType: Optional[Union[list[str], Series[str], str]] = None, commonCode: Optional[Union[list[str], Series[str], str]] = None, zone: Optional[Union[list[str], Series[str], str]] = None, companyID: Optional[Union[list[str], Series[str], str]] = None, connectingParty: Optional[Union[list[str], Series[str], str]] = None, locProp: Optional[Union[list[str], Series[str], str]] = None, domainID: Optional[Union[list[str], Series[str], str]] = None, domain: Optional[Union[list[str], Series[str], str]] = None, regionID: Optional[Union[list[str], Series[str], str]] = None, region: Optional[Union[list[str], Series[str], str]] = None, subregionID: Optional[Union[list[str], Series[str], str]] = None, subregion: Optional[Union[list[str], Series[str], str]] = None, stateID: Optional[Union[list[str], Series[str], str]] = None, state: Optional[Union[list[str], Series[str], str]] = None, countyID: Optional[Union[list[str], Series[str], str]] = None, county: Optional[Union[list[str], Series[str], str]] = None, producingAreaID: Optional[Union[list[str], Series[str], str]] = None, producingArea: Optional[Union[list[str], Series[str], str]] = None, latitude: Optional[Union[list[str], Series[str], str]] = None, longitude: Optional[Union[list[str], Series[str], str]] = None, uom: Optional[Union[list[str], Series[str], str]] = None, value: Optional[Union[list[str], Series[str], str]] = None, heatingValue: Optional[Union[list[str], Series[str], str]] = None, specificGravity: Optional[Union[list[str], Series[str], str]] = None, wobbe: Optional[Union[list[str], Series[str], str]] = None, createDate: Optional[Union[list[str], Series[str], str]] = None, dataActive: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         measurementDate: Optional[Union[list[str], Series[str], str]]
             Measurement date is when the analysis occured and is equal to the gas day or flow date., be default None
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         dateFrequency: Optional[Union[list[str], Series[str], str]]
             Daily, Weekly, Monthly, Seasonal, Annual., be default None
         dateFrequencyDesc: Optional[Union[list[str], Series[str], str]]
             The time period averages of the dataset such as Daily, Weekly, Monthly, Seasonal, Annual. Weekly date frequencies are based on the defined EIA storage week of Friday-Thursday. Seasonal date frequencies define Summer as April to October and Winter as November to March., be default None
         legacyBentekPointID: Optional[Union[list[str], Series[str], str]]
             Point ID for a meter used by the legacy Bentek service., be default None
         componentPointID: Optional[Union[list[str], Series[str], str]]
             Point ID for a meter used by the Americas Gas service., be default None
         pipelineOperatorID: Optional[Union[list[str], Series[str], str]]
             ID associated with the common parent owner or operator of a pipeline system., be default None
         pipelineOperatorName: Optional[Union[list[str], Series[str], str]]
             The name of the common parent owner or operator of a pipeline system., be default None
         pipelineID: Optional[Union[list[str], Series[str], str]]
             The ID given to a pipeline system, utilizes legacy Bentek pipeline ids when applicable., be default None
         pipelineName: Optional[Union[list[str], Series[str], str]]
             The display name of a pipeline system, utilizes legacy Bentek names when applicable., be default None
         gasCompositionTypeID: Optional[Union[list[str], Series[str], str]]
             Unique ID for the reported gas composition name., be default None
         gasCompositionName: Optional[Union[list[str], Series[str], str]]
             Reported gases within the gas stream such as methane, ethane, propane, butane, pentanes and others., be default None
         pointName: Optional[Union[list[str], Series[str], str]]
             The display name of a meter or point, utilizes legacy Bentek point name when applicable., be default None
         meterTypeID: Optional[Union[list[str], Series[str], str]]
             The classification and purpose of a meter or point, meant to provide an extra level of detail and utilizes legacy Bentek ids., be default None
         meterType: Optional[Union[list[str], Series[str], str]]
             The classification and purpose of a meter or point, meant to provide an extra level of detail, utilizes legacy Bentek definitions., be default None
         commonCode: Optional[Union[list[str], Series[str], str]]
             Common code, when used, may provide additional information about the point as reported by the pipeline., be default None
         zone: Optional[Union[list[str], Series[str], str]]
             A designation for where on the pipeline system the point is located, corresponding to a pipeline’s operational and market design. Zonal information is sourced from the legacy Bentek service., be default None
         companyID: Optional[Union[list[str], Series[str], str]]
             An ID sourced from the legacy Bentek service used to identify the connecting business or company name of a meter., be default None
         connectingParty: Optional[Union[list[str], Series[str], str]]
             The downstream connecting business name of a meter as reported by the pipeline, utilizes legacy Bentek service., be default None
         locProp: Optional[Union[list[str], Series[str], str]]
             The location propriety code reported by the pipeline for a specific meter., be default None
         domainID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the domain., be default None
         domain: Optional[Union[list[str], Series[str], str]]
             US Lower-48, Canada and Mexico., be default None
         regionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic region., be default None
         region: Optional[Union[list[str], Series[str], str]]
             A defined geographic region within the Americas Gas service. Regions are an aggregation of states or provinces within a country., be default None
         subregionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic subregion., be default None
         subregion: Optional[Union[list[str], Series[str], str]]
             A defined geographic subregion within the Americas Gas service. A substate geography is sometimes referred to as a subregion. Subregions are an aggregation of specific counties within a region and a country., be default None
         stateID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the state or province utilizes legacy Bentek IDs., be default None
         state: Optional[Union[list[str], Series[str], str]]
             The political boundaries that define a state or province within country., be default None
         countyID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the county within a US state in which a meter or point resides, utilizes legacy Bentek IDs., be default None
         county: Optional[Union[list[str], Series[str], str]]
             The political boundaries of a defined county within a US state in which a meter or point resides., be default None
         producingAreaID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for a defined Producing Area, utilizes legacy PointLogic IDs., be default None
         producingArea: Optional[Union[list[str], Series[str], str]]
             Defined aggregation of counties within a state that is a best fit representation of prominent oil and gas plays and basins., be default None
         latitude: Optional[Union[list[str], Series[str], str]]
             A geography based coordinate that specifies the north–south position of a point on the surface of the Earth. Latitude and longitude are used to identify the precise location of a pipeline meter or point., be default None
         longitude: Optional[Union[list[str], Series[str], str]]
             A geography based coordinate that specifies the east–west position of a point on the surface of the Earth. Latitude and longitude are used to identify the precise location of a pipeline meter or point., be default None
         uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure., be default None
         value: Optional[Union[list[str], Series[str], str]]
             Reported pipeline value., be default None
         heatingValue: Optional[Union[list[str], Series[str], str]]
             A measure of the heat content of the gas stream, expreessed in Btu per cubic foot., be default None
         specificGravity: Optional[Union[list[str], Series[str], str]]
             A measure of the density of a substance in comparison to the density of water., be default None
         wobbe: Optional[Union[list[str], Series[str], str]]
             A measure of the interchangeability of gases when they are used as a fuel., be default None
         createDate: Optional[Union[list[str], Series[str], str]]
             The date and time stamp of when the record was created., be default None
         dataActive: Optional[Union[list[str], Series[str], str]]
             A true or false return if the record is active., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("measurementDate", measurementDate))
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("dateFrequency", dateFrequency))
        filter_params.append(list_to_filter("dateFrequencyDesc", dateFrequencyDesc))
        filter_params.append(list_to_filter("legacyBentekPointID", legacyBentekPointID))
        filter_params.append(list_to_filter("componentPointID", componentPointID))
        filter_params.append(list_to_filter("pipelineOperatorID", pipelineOperatorID))
        filter_params.append(list_to_filter("pipelineOperatorName", pipelineOperatorName))
        filter_params.append(list_to_filter("pipelineID", pipelineID))
        filter_params.append(list_to_filter("pipelineName", pipelineName))
        filter_params.append(list_to_filter("gasCompositionTypeID", gasCompositionTypeID))
        filter_params.append(list_to_filter("gasCompositionName", gasCompositionName))
        filter_params.append(list_to_filter("pointName", pointName))
        filter_params.append(list_to_filter("meterTypeID", meterTypeID))
        filter_params.append(list_to_filter("meterType", meterType))
        filter_params.append(list_to_filter("commonCode", commonCode))
        filter_params.append(list_to_filter("zone", zone))
        filter_params.append(list_to_filter("companyID", companyID))
        filter_params.append(list_to_filter("connectingParty", connectingParty))
        filter_params.append(list_to_filter("locProp", locProp))
        filter_params.append(list_to_filter("domainID", domainID))
        filter_params.append(list_to_filter("domain", domain))
        filter_params.append(list_to_filter("regionID", regionID))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("subregionID", subregionID))
        filter_params.append(list_to_filter("subregion", subregion))
        filter_params.append(list_to_filter("stateID", stateID))
        filter_params.append(list_to_filter("state", state))
        filter_params.append(list_to_filter("countyID", countyID))
        filter_params.append(list_to_filter("county", county))
        filter_params.append(list_to_filter("producingAreaID", producingAreaID))
        filter_params.append(list_to_filter("producingArea", producingArea))
        filter_params.append(list_to_filter("latitude", latitude))
        filter_params.append(list_to_filter("longitude", longitude))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("value", value))
        filter_params.append(list_to_filter("heatingValue", heatingValue))
        filter_params.append(list_to_filter("specificGravity", specificGravity))
        filter_params.append(list_to_filter("wobbe", wobbe))
        filter_params.append(list_to_filter("createDate", createDate))
        filter_params.append(list_to_filter("dataActive", dataActive))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/gas-quality-data",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_notices_data(
        self, postingDatetime: Optional[Union[list[str], Series[str], str]] = None, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, effectiveDate: Optional[Union[list[str], Series[str], str]] = None, endDate: Optional[Union[list[str], Series[str], str]] = None, pipelineID: Optional[Union[list[str], Series[str], str]] = None, pipelineShortName: Optional[Union[list[str], Series[str], str]] = None, pipelineName: Optional[Union[list[str], Series[str], str]] = None, noticeCategoryID: Optional[Union[list[str], Series[str], str]] = None, categoryCode: Optional[Union[list[str], Series[str], str]] = None, category: Optional[Union[list[str], Series[str], str]] = None, noticeTypeID: Optional[Union[list[str], Series[str], str]] = None, noticeType: Optional[Union[list[str], Series[str], str]] = None, noticeStatusID: Optional[Union[list[str], Series[str], str]] = None, noticeStatus: Optional[Union[list[str], Series[str], str]] = None, responseCodeID: Optional[Union[list[str], Series[str], str]] = None, response: Optional[Union[list[str], Series[str], str]] = None, noticeID: Optional[Union[list[str], Series[str], str]] = None, priorNoticeIdentifier: Optional[Union[list[str], Series[str], str]] = None, subject: Optional[Union[list[str], Series[str], str]] = None, comments: Optional[Union[list[str], Series[str], str]] = None, content: Optional[Union[list[str], Series[str], str]] = None, createDate: Optional[Union[list[str], Series[str], str]] = None, validFrom: Optional[Union[list[str], Series[str], str]] = None, validTo: Optional[Union[list[str], Series[str], str]] = None, dataActive: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         postingDatetime: Optional[Union[list[str], Series[str], str]]
             Day and time the record was last posted., be default None
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         effectiveDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         endDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was ended., be default None
         pipelineID: Optional[Union[list[str], Series[str], str]]
             The ID given to a pipeline system, utilizes legacy Bentek pipeline ids when applicable., be default None
         pipelineShortName: Optional[Union[list[str], Series[str], str]]
             The short name of a pipeline system, utilizes legacy Bentek names when applicable., be default None
         pipelineName: Optional[Union[list[str], Series[str], str]]
             The display name of a pipeline system, utilizes legacy Bentek names when applicable., be default None
         noticeCategoryID: Optional[Union[list[str], Series[str], str]]
             A unique identifier number assigned to different catogories of the notice., be default None
         categoryCode: Optional[Union[list[str], Series[str], str]]
             A short code or abbreviation for each category., be default None
         category: Optional[Union[list[str], Series[str], str]]
             The nature or significance of the pipeline category., be default None
         noticeTypeID: Optional[Union[list[str], Series[str], str]]
             A unique identifier number assigned to different types of the notice., be default None
         noticeType: Optional[Union[list[str], Series[str], str]]
             The type of the notice., be default None
         noticeStatusID: Optional[Union[list[str], Series[str], str]]
             A unique identifier number assigned to different statuses of the notice., be default None
         noticeStatus: Optional[Union[list[str], Series[str], str]]
             Current status of the notice., be default None
         responseCodeID: Optional[Union[list[str], Series[str], str]]
             A unique identifier number assigned to different types of responses required for the notice., be default None
         response: Optional[Union[list[str], Series[str], str]]
             The urgency and timeline associated with each response code., be default None
         noticeID: Optional[Union[list[str], Series[str], str]]
             Notice identifier of the notice., be default None
         priorNoticeIdentifier: Optional[Union[list[str], Series[str], str]]
             Prior notice identifier of the notice., be default None
         subject: Optional[Union[list[str], Series[str], str]]
             The subject of the pipeline notice., be default None
         comments: Optional[Union[list[str], Series[str], str]]
             Comments of the pipeline notice., be default None
         content: Optional[Union[list[str], Series[str], str]]
             The content of the pipeline notice., be default None
         createDate: Optional[Union[list[str], Series[str], str]]
             The date and time stamp of when the record was created., be default None
         validFrom: Optional[Union[list[str], Series[str], str]]
             Valid from Date, be default None
         validTo: Optional[Union[list[str], Series[str], str]]
             The date and time of when the record was valid to., be default None
         dataActive: Optional[Union[list[str], Series[str], str]]
             A true or false return if the record is active., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("postingDatetime", postingDatetime))
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("effectiveDate", effectiveDate))
        filter_params.append(list_to_filter("endDate", endDate))
        filter_params.append(list_to_filter("pipelineID", pipelineID))
        filter_params.append(list_to_filter("pipelineShortName", pipelineShortName))
        filter_params.append(list_to_filter("pipelineName", pipelineName))
        filter_params.append(list_to_filter("noticeCategoryID", noticeCategoryID))
        filter_params.append(list_to_filter("categoryCode", categoryCode))
        filter_params.append(list_to_filter("category", category))
        filter_params.append(list_to_filter("noticeTypeID", noticeTypeID))
        filter_params.append(list_to_filter("noticeType", noticeType))
        filter_params.append(list_to_filter("noticeStatusID", noticeStatusID))
        filter_params.append(list_to_filter("noticeStatus", noticeStatus))
        filter_params.append(list_to_filter("responseCodeID", responseCodeID))
        filter_params.append(list_to_filter("response", response))
        filter_params.append(list_to_filter("noticeID", noticeID))
        filter_params.append(list_to_filter("priorNoticeIdentifier", priorNoticeIdentifier))
        filter_params.append(list_to_filter("subject", subject))
        filter_params.append(list_to_filter("comments", comments))
        filter_params.append(list_to_filter("content", content))
        filter_params.append(list_to_filter("createDate", createDate))
        filter_params.append(list_to_filter("validFrom", validFrom))
        filter_params.append(list_to_filter("validTo", validTo))
        filter_params.append(list_to_filter("dataActive", dataActive))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/notices-data",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_tariff_rate_data(
        self, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, pipelineID: Optional[Union[list[str], Series[str], str]] = None, pipelineName: Optional[Union[list[str], Series[str], str]] = None, serviceTypeID: Optional[Union[list[str], Series[str], str]] = None, serviceType: Optional[Union[list[str], Series[str], str]] = None, rateName: Optional[Union[list[str], Series[str], str]] = None, rateItemName: Optional[Union[list[str], Series[str], str]] = None, rateDescription: Optional[Union[list[str], Series[str], str]] = None, rateTypeID: Optional[Union[list[str], Series[str], str]] = None, rateAmount: Optional[Union[list[str], Series[str], str]] = None, rateUnitID: Optional[Union[list[str], Series[str], str]] = None, rateUnit: Optional[Union[list[str], Series[str], str]] = None, rateFrequencyID: Optional[Union[list[str], Series[str], str]] = None, rateFrequency: Optional[Union[list[str], Series[str], str]] = None, seasonID: Optional[Union[list[str], Series[str], str]] = None, season: Optional[Union[list[str], Series[str], str]] = None, gasUnitID: Optional[Union[list[str], Series[str], str]] = None, gasUnitName: Optional[Union[list[str], Series[str], str]] = None, zoneIDReceipt: Optional[Union[list[str], Series[str], str]] = None, receiptZone: Optional[Union[list[str], Series[str], str]] = None, zoneIDDelivery: Optional[Union[list[str], Series[str], str]] = None, deliveryZone: Optional[Union[list[str], Series[str], str]] = None, dateEffective: Optional[Union[list[str], Series[str], str]] = None, dateRetire: Optional[Union[list[str], Series[str], str]] = None, dateIssued: Optional[Union[list[str], Series[str], str]] = None, validFrom: Optional[Union[list[str], Series[str], str]] = None, validTo: Optional[Union[list[str], Series[str], str]] = None, dataActive: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         pipelineID: Optional[Union[list[str], Series[str], str]]
             The ID given to a pipeline system, utilizes legacy Bentek pipeline ids when applicable., be default None
         pipelineName: Optional[Union[list[str], Series[str], str]]
             The display name of a pipeline system, utilizes legacy Bentek names when applicable., be default None
         serviceTypeID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the service type., be default None
         serviceType: Optional[Union[list[str], Series[str], str]]
             The specific type or category of transportation service being offered by the pipeline., be default None
         rateName: Optional[Union[list[str], Series[str], str]]
             The specific name or identifier assigned to a particular rate or charge in the pipeline tariff., be default None
         rateItemName: Optional[Union[list[str], Series[str], str]]
             The specific name or description of the rate or charge being applied., be default None
         rateDescription: Optional[Union[list[str], Series[str], str]]
             The category or classification of the rate being applied., be default None
         rateTypeID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the rate type., be default None
         rateAmount: Optional[Union[list[str], Series[str], str]]
             The numerical value or percentage associated with the rate or charge., be default None
         rateUnitID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the rate unit., be default None
         rateUnit: Optional[Union[list[str], Series[str], str]]
             The unit of measurement used to quantify the monetary value or percentage associated with the rate or charge., be default None
         rateFrequencyID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the rate frequency., be default None
         rateFrequency: Optional[Union[list[str], Series[str], str]]
             The frequency at which the rate or charge is applied or calculated., be default None
         seasonID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the season., be default None
         season: Optional[Union[list[str], Series[str], str]]
             Season per gas industry standards (April - October in the same year = summer and November - March bridge the calendar years = winter)., be default None
         gasUnitID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the gas unit., be default None
         gasUnitName: Optional[Union[list[str], Series[str], str]]
             The unit of measurement used to quantify the volume or quantity of gas being transported or supplied., be default None
         zoneIDReceipt: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the receipt zone., be default None
         receiptZone: Optional[Union[list[str], Series[str], str]]
             A designated area where the gas is received or collected from., be default None
         zoneIDDelivery: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the delivery zone., be default None
         deliveryZone: Optional[Union[list[str], Series[str], str]]
             A designated area where the gas is delivered or transported to., be default None
         dateEffective: Optional[Union[list[str], Series[str], str]]
             The date when the rate becomes effective., be default None
         dateRetire: Optional[Union[list[str], Series[str], str]]
             The date when the rate is retired or no longer applicable., be default None
         dateIssued: Optional[Union[list[str], Series[str], str]]
             The date when the rate was issued., be default None
         validFrom: Optional[Union[list[str], Series[str], str]]
             The date and time stamp of when the record was valid from., be default None
         validTo: Optional[Union[list[str], Series[str], str]]
             The date and time stamp of when the record was valid to., be default None
         dataActive: Optional[Union[list[str], Series[str], str]]
             A true or false return if the record is active., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("pipelineID", pipelineID))
        filter_params.append(list_to_filter("pipelineName", pipelineName))
        filter_params.append(list_to_filter("serviceTypeID", serviceTypeID))
        filter_params.append(list_to_filter("serviceType", serviceType))
        filter_params.append(list_to_filter("rateName", rateName))
        filter_params.append(list_to_filter("rateItemName", rateItemName))
        filter_params.append(list_to_filter("rateDescription", rateDescription))
        filter_params.append(list_to_filter("rateTypeID", rateTypeID))
        filter_params.append(list_to_filter("rateAmount", rateAmount))
        filter_params.append(list_to_filter("rateUnitID", rateUnitID))
        filter_params.append(list_to_filter("rateUnit", rateUnit))
        filter_params.append(list_to_filter("rateFrequencyID", rateFrequencyID))
        filter_params.append(list_to_filter("rateFrequency", rateFrequency))
        filter_params.append(list_to_filter("seasonID", seasonID))
        filter_params.append(list_to_filter("season", season))
        filter_params.append(list_to_filter("gasUnitID", gasUnitID))
        filter_params.append(list_to_filter("gasUnitName", gasUnitName))
        filter_params.append(list_to_filter("zoneIDReceipt", zoneIDReceipt))
        filter_params.append(list_to_filter("receiptZone", receiptZone))
        filter_params.append(list_to_filter("zoneIDDelivery", zoneIDDelivery))
        filter_params.append(list_to_filter("deliveryZone", deliveryZone))
        filter_params.append(list_to_filter("dateEffective", dateEffective))
        filter_params.append(list_to_filter("dateRetire", dateRetire))
        filter_params.append(list_to_filter("dateIssued", dateIssued))
        filter_params.append(list_to_filter("validFrom", validFrom))
        filter_params.append(list_to_filter("validTo", validTo))
        filter_params.append(list_to_filter("dataActive", dataActive))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/tariff-rate-data",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_regional_summaries_flowdata(
        self, flowDate: Optional[Union[list[date], Series[date], date]] = None, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, dateFrequency: Optional[Union[list[str], Series[str], str]] = None, dateFrequencyDesc: Optional[Union[list[str], Series[str], str]] = None, modelID: Optional[Union[list[str], Series[str], str]] = None, viewType: Optional[Union[list[str], Series[str], str]] = None, viewTypeID: Optional[Union[list[str], Series[str], str]] = None, domain: Optional[Union[list[str], Series[str], str]] = None, domainID: Optional[Union[list[str], Series[str], str]] = None, region: Optional[Union[list[str], Series[str], str]] = None, regionID: Optional[Union[list[str], Series[str], str]] = None, subregion: Optional[Union[list[str], Series[str], str]] = None, subregionID: Optional[Union[list[str], Series[str], str]] = None, geographyPov: Optional[Union[list[str], Series[str], str]] = None, geographyPovID: Optional[Union[list[str], Series[str], str]] = None, name: Optional[Union[list[str], Series[str], str]] = None, rowOrderRanking: Optional[Union[list[str], Series[str], str]] = None, neighboringGeography: Optional[Union[list[str], Series[str], str]] = None, neighboringGeographyID: Optional[Union[list[str], Series[str], str]] = None, volume: Optional[Union[list[str], Series[str], str]] = None, uom: Optional[Union[list[str], Series[str], str]] = None, dataActive: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         flowDate: Optional[Union[list[date], Series[date], date]]
             The calendar date or gas day the activity occurred., be default None
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         dateFrequency: Optional[Union[list[str], Series[str], str]]
             Daily, Weekly, Monthly, Seasonal, Annual., be default None
         dateFrequencyDesc: Optional[Union[list[str], Series[str], str]]
             The time period averages of the dataset such as Daily, Weekly, Monthly, Seasonal, Annual. Weekly date frequencies are based on the defined EIA storage week of Friday-Thursday. Seasonal date frequencies define Summer as April to October and Winter as November to March., be default None
         modelID: Optional[Union[list[str], Series[str], str]]
             Internal use, Model ID value., be default None
         viewType: Optional[Union[list[str], Series[str], str]]
             The name of the View Type such as Country Summary, Region Summary, Region Detail, Subregion Detail. Additional and more granular view types exist for the Gulf Coast region such as Gulf Coast: Subregion Summary, Gulf Coast: Substate Detail and Gulf Coast: Special Area Detail., be default None
         viewTypeID: Optional[Union[list[str], Series[str], str]]
             The ID given to a View Type. Country Summary =1, Region Summary =2, Region Detail =3, Subregion Detail =4, Gulf Coast: Subregion Summary =5, Gulf Coast: Substate Detail =6, Gulf Coast: Special Area Detail =7, be default None
         domain: Optional[Union[list[str], Series[str], str]]
             US Lower-48, Canada or Mexico., be default None
         domainID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the domain., be default None
         region: Optional[Union[list[str], Series[str], str]]
             A defined geographic region within the Americas Gas service. Regions are an aggregation of states or provinces within a country., be default None
         regionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic region., be default None
         subregion: Optional[Union[list[str], Series[str], str]]
             A defined geographic subregion within the Americas Gas service. A substate geography is sometimes referred to as a subregion. Subregions are an aggregation of specific counties within a region and a country., be default None
         subregionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic subregion., be default None
         geographyPov: Optional[Union[list[str], Series[str], str]]
             Geography point of view based on geographic heirarchy of country, region, subregion, substate, or special area., be default None
         geographyPovID: Optional[Union[list[str], Series[str], str]]
             An ID for the geography point of view., be default None
         name: Optional[Union[list[str], Series[str], str]]
             Name of the pipeline summary or regional flows., be default None
         rowOrderRanking: Optional[Union[list[str], Series[str], str]]
             A number used to define a consistent row order of the data within a geography point of view., be default None
         neighboringGeography: Optional[Union[list[str], Series[str], str]]
             Neighboring geography point of view based on geographic heirarchy of country, region, subregion, substate, or special area., be default None
         neighboringGeographyID: Optional[Union[list[str], Series[str], str]]
             An ID for the neighboring geography point of view., be default None
         volume: Optional[Union[list[str], Series[str], str]]
             Volume., be default None
         uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure., be default None
         dataActive: Optional[Union[list[str], Series[str], str]]
             A true or false return if the record is active., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("flowDate", flowDate))
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("dateFrequency", dateFrequency))
        filter_params.append(list_to_filter("dateFrequencyDesc", dateFrequencyDesc))
        filter_params.append(list_to_filter("modelID", modelID))
        filter_params.append(list_to_filter("viewType", viewType))
        filter_params.append(list_to_filter("viewTypeID", viewTypeID))
        filter_params.append(list_to_filter("domain", domain))
        filter_params.append(list_to_filter("domainID", domainID))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("regionID", regionID))
        filter_params.append(list_to_filter("subregion", subregion))
        filter_params.append(list_to_filter("subregionID", subregionID))
        filter_params.append(list_to_filter("geographyPov", geographyPov))
        filter_params.append(list_to_filter("geographyPovID", geographyPovID))
        filter_params.append(list_to_filter("name", name))
        filter_params.append(list_to_filter("rowOrderRanking", rowOrderRanking))
        filter_params.append(list_to_filter("neighboringGeography", neighboringGeography))
        filter_params.append(list_to_filter("neighboringGeographyID", neighboringGeographyID))
        filter_params.append(list_to_filter("volume", volume))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("dataActive", dataActive))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/regional-summaries-flowdata",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_outlook_production_play(
        self, date: Optional[Union[list[date], Series[date], date]] = None, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, dateFrequency: Optional[Union[list[str], Series[str], str]] = None, dateFrequencyDesc: Optional[Union[list[str], Series[str], str]] = None, year: Optional[Union[list[str], Series[str], str]] = None, vintage: Optional[Union[list[str], Series[str], str]] = None, vintageType: Optional[Union[list[str], Series[str], str]] = None, aggregateType: Optional[Union[list[str], Series[str], str]] = None, aggregatePlay: Optional[Union[list[str], Series[str], str]] = None, subplay: Optional[Union[list[str], Series[str], str]] = None, domain: Optional[Union[list[str], Series[str], str]] = None, domainID: Optional[Union[list[str], Series[str], str]] = None, region: Optional[Union[list[str], Series[str], str]] = None, regionID: Optional[Union[list[str], Series[str], str]] = None, subregion: Optional[Union[list[str], Series[str], str]] = None, subregionID: Optional[Union[list[str], Series[str], str]] = None, gulfcoastSubstate: Optional[Union[list[str], Series[str], str]] = None, gulfcoastSubstateID: Optional[Union[list[str], Series[str], str]] = None, stateAbbreviation: Optional[Union[list[str], Series[str], str]] = None, stateID: Optional[Union[list[str], Series[str], str]] = None, value: Optional[Union[list[str], Series[str], str]] = None, uom: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         date: Optional[Union[list[date], Series[date], date]]
             The calendar date or the date when the activity occurred., be default None
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         dateFrequency: Optional[Union[list[str], Series[str], str]]
             Daily, Weekly, Monthly, Seasonal, Annual., be default None
         dateFrequencyDesc: Optional[Union[list[str], Series[str], str]]
             The time period averages of the dataset such as Daily, Weekly, Monthly, Seasonal, Annual. Weekly date frequencies are based on the defined EIA storage week of Friday-Thursday. Seasonal date frequencies define Summer as April to October and Winter as November to March., be default None
         year: Optional[Union[list[str], Series[str], str]]
             The calendar year or the year when the activity occurred., be default None
         vintage: Optional[Union[list[str], Series[str], str]]
             The year and month the short term outlook (STO) was issued.  Long term outlook (LTO) is bi-annual and expressed by year and instance., be default None
         vintageType: Optional[Union[list[str], Series[str], str]]
             The outlook type for each vintage is either short term outlook or long term outlook. In general, short term outlooks are a five-year forecast and long term outlooks can be for up to 30 years., be default None
         aggregateType: Optional[Union[list[str], Series[str], str]]
             An aggregation of US Lower-48 sub plays into five  high-level expressions such as associated (oil-driven plays), Haynesville, Marcellus/Utica, Gulf of Mexico and Other Dry Gas., be default None
         aggregatePlay: Optional[Union[list[str], Series[str], str]]
             Aggregate Play is mid-level summary of Sub Plays, but more granular than Aggregate Type.  In some cases Aggregate Play and Sub Play will match., be default None
         subplay: Optional[Union[list[str], Series[str], str]]
             Production forecasts at a Sub Play level in its most granular expression and compliments the regional aggregation of production within the short and long term outlooks., be default None
         domain: Optional[Union[list[str], Series[str], str]]
             US Lower-48, Canada or Mexico., be default None
         domainID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the domain., be default None
         region: Optional[Union[list[str], Series[str], str]]
             A defined geographic region within the Americas Gas service. Regions are an aggregation of states or provinces within a country., be default None
         regionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic region., be default None
         subregion: Optional[Union[list[str], Series[str], str]]
             A defined geographic subregion within the Americas Gas service. A substate geography is sometimes referred to as a subregion. Subregions are an aggregation of specific counties within a region and a country., be default None
         subregionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic subregion., be default None
         gulfcoastSubstate: Optional[Union[list[str], Series[str], str]]
             The name of substate region or special area within the Gulf Coast region., be default None
         gulfcoastSubstateID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic substate regions within the Gulf Coast area., be default None
         stateAbbreviation: Optional[Union[list[str], Series[str], str]]
             Abbreviation for a state or province within country., be default None
         stateID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the state or province utilizes legacy Bentek IDs., be default None
         value: Optional[Union[list[str], Series[str], str]]
             The dry natural gas production volume expressed in a daily average format., be default None
         uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("date", date))
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("dateFrequency", dateFrequency))
        filter_params.append(list_to_filter("dateFrequencyDesc", dateFrequencyDesc))
        filter_params.append(list_to_filter("year", year))
        filter_params.append(list_to_filter("vintage", vintage))
        filter_params.append(list_to_filter("vintageType", vintageType))
        filter_params.append(list_to_filter("aggregateType", aggregateType))
        filter_params.append(list_to_filter("aggregatePlay", aggregatePlay))
        filter_params.append(list_to_filter("subplay", subplay))
        filter_params.append(list_to_filter("domain", domain))
        filter_params.append(list_to_filter("domainID", domainID))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("regionID", regionID))
        filter_params.append(list_to_filter("subregion", subregion))
        filter_params.append(list_to_filter("subregionID", subregionID))
        filter_params.append(list_to_filter("gulfcoastSubstate", gulfcoastSubstate))
        filter_params.append(list_to_filter("gulfcoastSubstateID", gulfcoastSubstateID))
        filter_params.append(list_to_filter("stateAbbreviation", stateAbbreviation))
        filter_params.append(list_to_filter("stateID", stateID))
        filter_params.append(list_to_filter("value", value))
        filter_params.append(list_to_filter("uom", uom))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/outlook-production-play",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_market_balances_data(
        self, flowDate: Optional[Union[list[date], Series[date], date]] = None, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, dateFrequency: Optional[Union[list[str], Series[str], str]] = None, dateFrequencyDesc: Optional[Union[list[str], Series[str], str]] = None, domain: Optional[Union[list[str], Series[str], str]] = None, domainID: Optional[Union[list[str], Series[str], str]] = None, region: Optional[Union[list[str], Series[str], str]] = None, regionID: Optional[Union[list[str], Series[str], str]] = None, subregion: Optional[Union[list[str], Series[str], str]] = None, subregionID: Optional[Union[list[str], Series[str], str]] = None, geographyType: Optional[Union[list[str], Series[str], str]] = None, geographyPov: Optional[Union[list[str], Series[str], str]] = None, geographyPovID: Optional[Union[list[str], Series[str], str]] = None, modelID: Optional[Union[list[str], Series[str], str]] = None, concept: Optional[Union[list[str], Series[str], str]] = None, category: Optional[Union[list[str], Series[str], str]] = None, rowOrderRanking: Optional[Union[list[str], Series[str], str]] = None, uom: Optional[Union[list[str], Series[str], str]] = None, value: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         flowDate: Optional[Union[list[date], Series[date], date]]
             The calendar date or gas day the activity occurred., be default None
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         dateFrequency: Optional[Union[list[str], Series[str], str]]
             Daily, Weekly, Monthly, Seasonal, Annual., be default None
         dateFrequencyDesc: Optional[Union[list[str], Series[str], str]]
             The time period averages of the dataset such as Daily, Weekly, Monthly, Seasonal, Annual. Weekly date frequencies are based on the defined EIA storage week of Friday-Thursday. Seasonal date frequencies define Summer as April to October and Winter as November to March., be default None
         domain: Optional[Union[list[str], Series[str], str]]
             US Lower-48, Canada and Mexico., be default None
         domainID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the domain., be default None
         region: Optional[Union[list[str], Series[str], str]]
             A defined geographic region within the Americas Gas service. Regions are an aggregation of states or provinces within a country., be default None
         regionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic region., be default None
         subregion: Optional[Union[list[str], Series[str], str]]
             A defined geographic subregion within the Americas Gas service. A substate geography is sometimes referred to as a subregion. Subregions are an aggregation of specific counties within a region and a country., be default None
         subregionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic subregion., be default None
         geographyType: Optional[Union[list[str], Series[str], str]]
             Geography type for the point of view based on geographic hierarchy of country, region, subregion, substate, or special area., be default None
         geographyPov: Optional[Union[list[str], Series[str], str]]
             Geography point of view based on geographic heirarchy of country, region, subregion, substate, or special area., be default None
         geographyPovID: Optional[Union[list[str], Series[str], str]]
             An ID for the geography point of view., be default None
         modelID: Optional[Union[list[str], Series[str], str]]
             Internal use, Model ID value., be default None
         concept: Optional[Union[list[str], Series[str], str]]
             Data concept such as Supply, Demand, LNG, Storage, Flows, etc., be default None
         category: Optional[Union[list[str], Series[str], str]]
             Category that is unique within a Concept., be default None
         rowOrderRanking: Optional[Union[list[str], Series[str], str]]
             A number used to define a consistent row order of the data within a geography point of view., be default None
         uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure., be default None
         value: Optional[Union[list[str], Series[str], str]]
             Value of the record., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("flowDate", flowDate))
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("dateFrequency", dateFrequency))
        filter_params.append(list_to_filter("dateFrequencyDesc", dateFrequencyDesc))
        filter_params.append(list_to_filter("domain", domain))
        filter_params.append(list_to_filter("domainID", domainID))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("regionID", regionID))
        filter_params.append(list_to_filter("subregion", subregion))
        filter_params.append(list_to_filter("subregionID", subregionID))
        filter_params.append(list_to_filter("geographyType", geographyType))
        filter_params.append(list_to_filter("geographyPov", geographyPov))
        filter_params.append(list_to_filter("geographyPovID", geographyPovID))
        filter_params.append(list_to_filter("modelID", modelID))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("category", category))
        filter_params.append(list_to_filter("rowOrderRanking", rowOrderRanking))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("value", value))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/market-balances-data",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_index_of_customer_data(
        self, year: Optional[Union[list[str], Series[str], str]] = None, quarter: Optional[Union[list[str], Series[str], str]] = None, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, pipelineFilerName: Optional[Union[list[str], Series[str], str]] = None, pipelineName: Optional[Union[list[str], Series[str], str]] = None, pipelineID: Optional[Union[list[str], Series[str], str]] = None, shipperName: Optional[Union[list[str], Series[str], str]] = None, legacyPointLogicPointID: Optional[Union[list[str], Series[str], str]] = None, plePointID: Optional[Union[list[str], Series[str], str]] = None, legacyPointLogicLCIID: Optional[Union[list[str], Series[str], str]] = None, componentPointID: Optional[Union[list[str], Series[str], str]] = None, meterTypePrimary: Optional[Union[list[str], Series[str], str]] = None, meterTypeIDPrimary: Optional[Union[list[str], Series[str], str]] = None, dir: Optional[Union[list[str], Series[str], str]] = None, locProp: Optional[Union[list[str], Series[str], str]] = None, zone: Optional[Union[list[str], Series[str], str]] = None, county: Optional[Union[list[str], Series[str], str]] = None, countyID: Optional[Union[list[str], Series[str], str]] = None, state: Optional[Union[list[str], Series[str], str]] = None, stateID: Optional[Union[list[str], Series[str], str]] = None, subRegion: Optional[Union[list[str], Series[str], str]] = None, subRegionID: Optional[Union[list[str], Series[str], str]] = None, region: Optional[Union[list[str], Series[str], str]] = None, regionID: Optional[Union[list[str], Series[str], str]] = None, maxTrans: Optional[Union[list[str], Series[str], str]] = None, maxStorage: Optional[Union[list[str], Series[str], str]] = None, pointMaxTrans: Optional[Union[list[str], Series[str], str]] = None, pointMaxStor: Optional[Union[list[str], Series[str], str]] = None, uom: Optional[Union[list[str], Series[str], str]] = None, agent: Optional[Union[list[str], Series[str], str]] = None, rateSchedule: Optional[Union[list[str], Series[str], str]] = None, contractNumber: Optional[Union[list[str], Series[str], str]] = None, contractStartDate: Optional[Union[list[date], Series[date], date]] = None, contractEndDate: Optional[Union[list[date], Series[date], date]] = None, contractMonths: Optional[Union[list[str], Series[str], str]] = None, rollOverPeriod: Optional[Union[list[str], Series[str], str]] = None, negotiatedRate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         year: Optional[Union[list[str], Series[str], str]]
             The year of when the record was reported., be default None
         quarter: Optional[Union[list[str], Series[str], str]]
             The quarter of when the record was reported., be default None
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         pipelineFilerName: Optional[Union[list[str], Series[str], str]]
             The filer name of a pipeline system., be default None
         pipelineName: Optional[Union[list[str], Series[str], str]]
             The display name of a pipeline system, utilizes legacy Bentek names when applicable., be default None
         pipelineID: Optional[Union[list[str], Series[str], str]]
             The ID given to a pipeline system, utilizes legacy Bentek pipeline ids when applicable., be default None
         shipperName: Optional[Union[list[str], Series[str], str]]
             The name of the company responsible for transporting natural gas from the production or supply source to the end consumer., be default None
         legacyPointLogicPointID: Optional[Union[list[str], Series[str], str]]
             The display name of a meter or point, utilizes legacy Bentek point name when applicable., be default None
         plePointID: Optional[Union[list[str], Series[str], str]]
             Point ID for a meter used by the legacy PointLogic service., be default None
         legacyPointLogicLCIID: Optional[Union[list[str], Series[str], str]]
             Alternative point ID for a meter used by the legacy PointLogic service., be default None
         componentPointID: Optional[Union[list[str], Series[str], str]]
             Point ID for a meter used by the Americas Gas service., be default None
         meterTypePrimary: Optional[Union[list[str], Series[str], str]]
             The primary type of classification and purpose of a meter or point, utilizes legacy PointLogic definitions., be default None
         meterTypeIDPrimary: Optional[Union[list[str], Series[str], str]]
             An ID for the primary type of classification and purpose of a meter or point, utilizes legacy PointLogic definitions and ID., be default None
         dir: Optional[Union[list[str], Series[str], str]]
             Direction indicates the orientation of a point such as receipt, delivery, bi-directional or the reported flow direction of segment or compressor. These codes are from the NAESB Business Practice Standards Manual relating to the Capacity Release - Firm Transportation and Storage - Award Notice (Award Download), N1 Record. M2 - Receipt Point MQ - Delivery Point MV - Mainline S8 - Pipeline Segment defined by 2 Point records (second of 2 Point records) S9 - Pipeline Segment defined by 1 Point record (or first of 2 Point records) SB - Storage Area IJ - Injection Point WR - Withdrawal Point., be default None
         locProp: Optional[Union[list[str], Series[str], str]]
             The location propriety code reported by the pipeline for a specific meter., be default None
         zone: Optional[Union[list[str], Series[str], str]]
             A designation for where on the pipeline system the point is located, corresponding to a pipeline’s operational and market design. Zonal information is sourced from the legacy Bentek service., be default None
         county: Optional[Union[list[str], Series[str], str]]
             The political boundaries of a defined county within a US state in which a meter or point resides., be default None
         countyID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the county within a US state in which a meter or point resides, utilizes legacy Bentek IDs., be default None
         state: Optional[Union[list[str], Series[str], str]]
             The political boundaries that define a state or province within country., be default None
         stateID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the state or province utilizes legacy Bentek IDs., be default None
         subRegion: Optional[Union[list[str], Series[str], str]]
             A defined geographic subregion within the Americas Gas service. A substate geography is sometimes referred to as a subregion. Subregions are an aggregation of specific counties within a region and a country., be default None
         subRegionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic subregion., be default None
         region: Optional[Union[list[str], Series[str], str]]
             A defined geographic region within the Americas Gas service. Regions are an aggregation of states or provinces within a country., be default None
         regionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic region., be default None
         maxTrans: Optional[Union[list[str], Series[str], str]]
             Maximum quantity of natural gas that can be transported per day., be default None
         maxStorage: Optional[Union[list[str], Series[str], str]]
             Maximum quantity or the largest quantity of natural gas the pipeline is obligated to store for the Shipper under the contract., be default None
         pointMaxTrans: Optional[Union[list[str], Series[str], str]]
             The maximum amount of natural gas that can be transported to a specific point per day., be default None
         pointMaxStor: Optional[Union[list[str], Series[str], str]]
             The maximum amount of natural gas that can be stored at a specific point., be default None
         uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure., be default None
         agent: Optional[Union[list[str], Series[str], str]]
             The company or entity responsible for the natural gas trading.  Agent or Asset Manager., be default None
         rateSchedule: Optional[Union[list[str], Series[str], str]]
             The specific rate schedule associated with the contract.  The rate is the as reported rate on the FERC Form 2 or 2A., be default None
         contractNumber: Optional[Union[list[str], Series[str], str]]
             The unique identifier for the contract., be default None
         contractStartDate: Optional[Union[list[date], Series[date], date]]
             Start date of the contract., be default None
         contractEndDate: Optional[Union[list[date], Series[date], date]]
             End date of the contract., be default None
         contractMonths: Optional[Union[list[str], Series[str], str]]
             Total number of months for the contract., be default None
         rollOverPeriod: Optional[Union[list[str], Series[str], str]]
             The number of days in the roll-over period after which the contract can be renewed or extended. Also know as evergreen period. If the contract continues on a monthly basis then 31 should be entered if annual enter 365, if unknown leave blank., be default None
         negotiatedRate: Optional[Union[list[str], Series[str], str]]
             Indicates whether the rate was negotiated (Yes/No)., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("year", year))
        filter_params.append(list_to_filter("quarter", quarter))
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("pipelineFilerName", pipelineFilerName))
        filter_params.append(list_to_filter("pipelineName", pipelineName))
        filter_params.append(list_to_filter("pipelineID", pipelineID))
        filter_params.append(list_to_filter("shipperName", shipperName))
        filter_params.append(list_to_filter("legacyPointLogicPointID", legacyPointLogicPointID))
        filter_params.append(list_to_filter("plePointID", plePointID))
        filter_params.append(list_to_filter("legacyPointLogicLCIID", legacyPointLogicLCIID))
        filter_params.append(list_to_filter("componentPointID", componentPointID))
        filter_params.append(list_to_filter("meterTypePrimary", meterTypePrimary))
        filter_params.append(list_to_filter("meterTypeIDPrimary", meterTypeIDPrimary))
        filter_params.append(list_to_filter("dir", dir))
        filter_params.append(list_to_filter("locProp", locProp))
        filter_params.append(list_to_filter("zone", zone))
        filter_params.append(list_to_filter("county", county))
        filter_params.append(list_to_filter("countyID", countyID))
        filter_params.append(list_to_filter("state", state))
        filter_params.append(list_to_filter("stateID", stateID))
        filter_params.append(list_to_filter("subRegion", subRegion))
        filter_params.append(list_to_filter("subRegionID", subRegionID))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("regionID", regionID))
        filter_params.append(list_to_filter("maxTrans", maxTrans))
        filter_params.append(list_to_filter("maxStorage", maxStorage))
        filter_params.append(list_to_filter("pointMaxTrans", pointMaxTrans))
        filter_params.append(list_to_filter("pointMaxStor", pointMaxStor))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("agent", agent))
        filter_params.append(list_to_filter("rateSchedule", rateSchedule))
        filter_params.append(list_to_filter("contractNumber", contractNumber))
        filter_params.append(list_to_filter("contractStartDate", contractStartDate))
        filter_params.append(list_to_filter("contractEndDate", contractEndDate))
        filter_params.append(list_to_filter("contractMonths", contractMonths))
        filter_params.append(list_to_filter("rollOverPeriod", rollOverPeriod))
        filter_params.append(list_to_filter("negotiatedRate", negotiatedRate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/index-of-customer-data",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_outlook_marketbalances_prices(
        self, vintageType: Optional[Union[list[str], Series[str], str]] = None, vintage: Optional[Union[list[str], Series[str], str]] = None, dateFrequency: Optional[Union[list[str], Series[str], str]] = None, dateFrequencyDesc: Optional[Union[list[str], Series[str], str]] = None, year: Optional[Union[list[str], Series[str], str]] = None, date: Optional[Union[list[date], Series[date], date]] = None, concept: Optional[Union[list[str], Series[str], str]] = None, category: Optional[Union[list[str], Series[str], str]] = None, domain: Optional[Union[list[str], Series[str], str]] = None, domainID: Optional[Union[list[str], Series[str], str]] = None, region: Optional[Union[list[str], Series[str], str]] = None, regionID: Optional[Union[list[str], Series[str], str]] = None, geographyPointOfView: Optional[Union[list[str], Series[str], str]] = None, geographyID: Optional[Union[list[str], Series[str], str]] = None, uom: Optional[Union[list[str], Series[str], str]] = None, value: Optional[Union[list[str], Series[str], str]] = None, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         vintageType: Optional[Union[list[str], Series[str], str]]
             The outlook type for each vintage is either short term outlook or long term outlook. In general, short term outlooks are a five-year forecast and long term outlooks can be for up to 30 years., be default None
         vintage: Optional[Union[list[str], Series[str], str]]
             The year and month the short term outlook (STO) was issued.  Long term outlook (LTO) is bi-annual and expressed by year and instance., be default None
         dateFrequency: Optional[Union[list[str], Series[str], str]]
             Daily, Weekly, Monthly, Seasonal, Annual., be default None
         dateFrequencyDesc: Optional[Union[list[str], Series[str], str]]
             The time period averages of the dataset such as Monthly, Seasonal, Annual. Seasonal date frequencies define Summer as April to October and Winter as November to March., be default None
         year: Optional[Union[list[str], Series[str], str]]
             The calendar year or the year when the activity occurred., be default None
         date: Optional[Union[list[date], Series[date], date]]
             The calendar date or the date when the activity occurred., be default None
         concept: Optional[Union[list[str], Series[str], str]]
             Data concept such as Supply, Demand, LNG, Storage, Flows, etc., be default None
         category: Optional[Union[list[str], Series[str], str]]
             Category that is unique within a Concept., be default None
         domain: Optional[Union[list[str], Series[str], str]]
             US Lower-48, Canada and Mexico., be default None
         domainID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the domain., be default None
         region: Optional[Union[list[str], Series[str], str]]
             A defined geographic region within the Americas Gas service. Regions are an aggregation of states or provinces within a country., be default None
         regionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic region., be default None
         geographyPointOfView: Optional[Union[list[str], Series[str], str]]
             The geography in which the data perspective is expressed., be default None
         geographyID: Optional[Union[list[str], Series[str], str]]
             Geography ID value for the point of view., be default None
         uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure., be default None
         value: Optional[Union[list[str], Series[str], str]]
             Value of the record., be default None
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("vintageType", vintageType))
        filter_params.append(list_to_filter("vintage", vintage))
        filter_params.append(list_to_filter("dateFrequency", dateFrequency))
        filter_params.append(list_to_filter("dateFrequencyDesc", dateFrequencyDesc))
        filter_params.append(list_to_filter("year", year))
        filter_params.append(list_to_filter("date", date))
        filter_params.append(list_to_filter("concept", concept))
        filter_params.append(list_to_filter("category", category))
        filter_params.append(list_to_filter("domain", domain))
        filter_params.append(list_to_filter("domainID", domainID))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("regionID", regionID))
        filter_params.append(list_to_filter("geographyPointOfView", geographyPointOfView))
        filter_params.append(list_to_filter("geographyID", geographyID))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("value", value))
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/outlook-marketbalances-prices",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_production_oil_data(
        self, flowDate: Optional[Union[list[date], Series[date], date]] = None, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, dateFrequency: Optional[Union[list[str], Series[str], str]] = None, dateFrequencyDesc: Optional[Union[list[str], Series[str], str]] = None, modelID: Optional[Union[list[str], Series[str], str]] = None, modelType: Optional[Union[list[str], Series[str], str]] = None, modelTypeID: Optional[Union[list[str], Series[str], str]] = None, marketType: Optional[Union[list[str], Series[str], str]] = None, marketTypeID: Optional[Union[list[str], Series[str], str]] = None, functionType: Optional[Union[list[str], Series[str], str]] = None, functionTypeID: Optional[Union[list[str], Series[str], str]] = None, pointOfView: Optional[Union[list[str], Series[str], str]] = None, domain: Optional[Union[list[str], Series[str], str]] = None, domainID: Optional[Union[list[str], Series[str], str]] = None, region: Optional[Union[list[str], Series[str], str]] = None, regionID: Optional[Union[list[str], Series[str], str]] = None, subregion: Optional[Union[list[str], Series[str], str]] = None, subregionID: Optional[Union[list[str], Series[str], str]] = None, state: Optional[Union[list[str], Series[str], str]] = None, stateID: Optional[Union[list[str], Series[str], str]] = None, producingArea: Optional[Union[list[str], Series[str], str]] = None, producingAreaID: Optional[Union[list[str], Series[str], str]] = None, padd: Optional[Union[list[str], Series[str], str]] = None, paddName: Optional[Union[list[str], Series[str], str]] = None, uom: Optional[Union[list[str], Series[str], str]] = None, volume: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         flowDate: Optional[Union[list[date], Series[date], date]]
             The calendar date or gas day the activity occurred., be default None
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         dateFrequency: Optional[Union[list[str], Series[str], str]]
             Oil production can only be Monthly, Seasonal, Annual., be default None
         dateFrequencyDesc: Optional[Union[list[str], Series[str], str]]
             The time period averages of the dataset such as Monthly, Seasonal, Annual. Weekly date frequencies are based on the defined EIA storage week of Friday-Thursday. Seasonal date frequencies define Summer as April to October and Winter as November to March., be default None
         modelID: Optional[Union[list[str], Series[str], str]]
             Internal use, Model ID value., be default None
         modelType: Optional[Union[list[str], Series[str], str]]
             Model types can vary among supply, demand and other market fundamentals. The type describes the fundamentals the model output represents., be default None
         modelTypeID: Optional[Union[list[str], Series[str], str]]
             ID associated with Model type., be default None
         marketType: Optional[Union[list[str], Series[str], str]]
             Oil market type relates to the point of view data, such as country, region, subregion, special area or producing area., be default None
         marketTypeID: Optional[Union[list[str], Series[str], str]]
             ID associated with Market type., be default None
         functionType: Optional[Union[list[str], Series[str], str]]
             The name of the Function Type such as prediction, aggregation, allocation, ten year average., be default None
         functionTypeID: Optional[Union[list[str], Series[str], str]]
             The ID given to a Function Type such as 1 is prediction, 2 is aggregation, 3 is allocation, 4 is ten year average., be default None
         pointOfView: Optional[Union[list[str], Series[str], str]]
             Point of View for the values. Point of view based on a geographic hierarchy of country, region, subregion, or producing area., be default None
         domain: Optional[Union[list[str], Series[str], str]]
             US Lower-48, Canada and Mexico., be default None
         domainID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the domain., be default None
         region: Optional[Union[list[str], Series[str], str]]
             A defined geographic region within the Americas Gas service. Regions are an aggregation of states or provinces within a country., be default None
         regionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic region., be default None
         subregion: Optional[Union[list[str], Series[str], str]]
             A defined geographic subregion within the Americas Gas service. A substate geography is sometimes referred to as a subregion. Subregions are an aggregation of specific counties within a region and a country., be default None
         subregionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic subregion., be default None
         state: Optional[Union[list[str], Series[str], str]]
             The political boundaries that define a state or province within country., be default None
         stateID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the state or province utilizes legacy Bentek IDs., be default None
         producingArea: Optional[Union[list[str], Series[str], str]]
             Defined aggregation of counties within a state that is a best fit representation of prominent oil and gas plays and basins., be default None
         producingAreaID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for a defined Producing Area utilizes legacy PointLogic IDs., be default None
         padd: Optional[Union[list[str], Series[str], str]]
             Petroleum Administration for Defense Districts (PADDs) are geographic aggregations of the 50 States and the District of Columbia into five districts: PADD 1 is the East Coast, PADD 2 the Midwest, PADD 3 the Gulf Coast, PADD 4 the Rocky Mountain Region, and PADD 5 the West Coast., be default None
         paddName: Optional[Union[list[str], Series[str], str]]
             Petroleum Administration for Defense Districts (PADDs) are geographic aggregations of the 50 States and the District of Columbia into five districts., be default None
         uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure., be default None
         volume: Optional[Union[list[str], Series[str], str]]
             Volume., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("flowDate", flowDate))
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("dateFrequency", dateFrequency))
        filter_params.append(list_to_filter("dateFrequencyDesc", dateFrequencyDesc))
        filter_params.append(list_to_filter("modelID", modelID))
        filter_params.append(list_to_filter("modelType", modelType))
        filter_params.append(list_to_filter("modelTypeID", modelTypeID))
        filter_params.append(list_to_filter("marketType", marketType))
        filter_params.append(list_to_filter("marketTypeID", marketTypeID))
        filter_params.append(list_to_filter("functionType", functionType))
        filter_params.append(list_to_filter("functionTypeID", functionTypeID))
        filter_params.append(list_to_filter("pointOfView", pointOfView))
        filter_params.append(list_to_filter("domain", domain))
        filter_params.append(list_to_filter("domainID", domainID))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("regionID", regionID))
        filter_params.append(list_to_filter("subregion", subregion))
        filter_params.append(list_to_filter("subregionID", subregionID))
        filter_params.append(list_to_filter("state", state))
        filter_params.append(list_to_filter("stateID", stateID))
        filter_params.append(list_to_filter("producingArea", producingArea))
        filter_params.append(list_to_filter("producingAreaID", producingAreaID))
        filter_params.append(list_to_filter("padd", padd))
        filter_params.append(list_to_filter("paddName", paddName))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("volume", volume))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/production-oil-data",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_facility_flow_data(
        self, flowDate: Optional[Union[list[date], Series[date], date]] = None, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, dateFrequency: Optional[Union[list[str], Series[str], str]] = None, dateFrequencyDesc: Optional[Union[list[str], Series[str], str]] = None, facilityType: Optional[Union[list[str], Series[str], str]] = None, facilityTypeID: Optional[Union[list[str], Series[str], str]] = None, viewType: Optional[Union[list[str], Series[str], str]] = None, name: Optional[Union[list[str], Series[str], str]] = None, modelID: Optional[Union[list[str], Series[str], str]] = None, componentPointID: Optional[Union[list[str], Series[str], str]] = None, pipelineName: Optional[Union[list[str], Series[str], str]] = None, pipelineID: Optional[Union[list[str], Series[str], str]] = None, pointName: Optional[Union[list[str], Series[str], str]] = None, meterTypePrimary: Optional[Union[list[str], Series[str], str]] = None, meterTypeIDPrimary: Optional[Union[list[str], Series[str], str]] = None, meterTypeSecondary: Optional[Union[list[str], Series[str], str]] = None, meterTypeIDSecondary: Optional[Union[list[str], Series[str], str]] = None, locationTypeCode: Optional[Union[list[str], Series[str], str]] = None, locationDescription: Optional[Union[list[str], Series[str], str]] = None, locationTypeID: Optional[Union[list[str], Series[str], str]] = None, zone: Optional[Union[list[str], Series[str], str]] = None, connectingParty: Optional[Union[list[str], Series[str], str]] = None, locProp: Optional[Union[list[str], Series[str], str]] = None, domain: Optional[Union[list[str], Series[str], str]] = None, domainID: Optional[Union[list[str], Series[str], str]] = None, region: Optional[Union[list[str], Series[str], str]] = None, regionID: Optional[Union[list[str], Series[str], str]] = None, subregion: Optional[Union[list[str], Series[str], str]] = None, subregionID: Optional[Union[list[str], Series[str], str]] = None, state: Optional[Union[list[str], Series[str], str]] = None, stateID: Optional[Union[list[str], Series[str], str]] = None, county: Optional[Union[list[str], Series[str], str]] = None, countyID: Optional[Union[list[str], Series[str], str]] = None, producingArea: Optional[Union[list[str], Series[str], str]] = None, producingAreaID: Optional[Union[list[str], Series[str], str]] = None, paddName: Optional[Union[list[str], Series[str], str]] = None, latitude: Optional[Union[list[str], Series[str], str]] = None, longitude: Optional[Union[list[str], Series[str], str]] = None, plantFieldName: Optional[Union[list[str], Series[str], str]] = None, plantFieldCode: Optional[Union[list[str], Series[str], str]] = None, utilityCompanyName: Optional[Union[list[str], Series[str], str]] = None, utilityCompanyID: Optional[Union[list[str], Series[str], str]] = None, nercRegion: Optional[Union[list[str], Series[str], str]] = None, balancingAuthorityName: Optional[Union[list[str], Series[str], str]] = None, balancingAuthorityCode: Optional[Union[list[str], Series[str], str]] = None, sectorName: Optional[Union[list[str], Series[str], str]] = None, storageReservoirName: Optional[Union[list[str], Series[str], str]] = None, storageFieldType: Optional[Union[list[str], Series[str], str]] = None, eiaStorageRegion: Optional[Union[list[str], Series[str], str]] = None, uom: Optional[Union[list[str], Series[str], str]] = None, volume: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         flowDate: Optional[Union[list[date], Series[date], date]]
             The calendar date or gas day the activity occurred., be default None
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         dateFrequency: Optional[Union[list[str], Series[str], str]]
             Daily, Weekly, Monthly, Seasonal, Annual., be default None
         dateFrequencyDesc: Optional[Union[list[str], Series[str], str]]
             The time period averages of the dataset such as Daily, Weekly, Monthly, Seasonal, Annual. Weekly date frequencies are based on the defined EIA storage week of Friday-Thursday. Seasonal date frequencies define Summer as April to October and Winter as November to March., be default None
         facilityType: Optional[Union[list[str], Series[str], str]]
             The type of facility that is being served by the pipeline such as Gas Processing Plant, Power Plant, Storage, LNG Feedgas or LNG Sendout., be default None
         facilityTypeID: Optional[Union[list[str], Series[str], str]]
             The facility type ID is a numeric value (1 to 5) that corresponds to the sequential order of the facility types described., be default None
         viewType: Optional[Union[list[str], Series[str], str]]
             The nature of the line item data and its time series. Facility view type contains the named facilty and applicable metadata. Sample view type details the underlining meter-level data in the aggregated Facility view type., be default None
         name: Optional[Union[list[str], Series[str], str]]
             The name of the facility., be default None
         modelID: Optional[Union[list[str], Series[str], str]]
             Internal use, Model ID value., be default None
         componentPointID: Optional[Union[list[str], Series[str], str]]
             Point ID for a meter used by the Americas Gas service., be default None
         pipelineName: Optional[Union[list[str], Series[str], str]]
             The display name of a pipeline system, utilizes legacy Bentek names when applicable., be default None
         pipelineID: Optional[Union[list[str], Series[str], str]]
             The ID given to a pipeline system, utilizes legacy Bentek pipeline ids when applicable., be default None
         pointName: Optional[Union[list[str], Series[str], str]]
             The display name of a meter or point, utilizes legacy Bentek point name when applicable., be default None
         meterTypePrimary: Optional[Union[list[str], Series[str], str]]
             The primary type of classification and purpose of a meter or point, utilizes legacy PointLogic definitions., be default None
         meterTypeIDPrimary: Optional[Union[list[str], Series[str], str]]
             An ID for the primary type of classification and purpose of a meter or point, utilizes legacy PointLogic definitions and ID., be default None
         meterTypeSecondary: Optional[Union[list[str], Series[str], str]]
             A secondary type classification and purpose of a meter or point, meant to provide an extra level of detail, utilizes legacy Bentek definitions., be default None
         meterTypeIDSecondary: Optional[Union[list[str], Series[str], str]]
             A secondary type classification and purpose of a meter or point, meant to provide an extra level of detail and utilizes legacy Bentek ids., be default None
         locationTypeCode: Optional[Union[list[str], Series[str], str]]
             Location type code is a one letter abbreviation of the location description. Location types are sourced from legacy Bentek. These are similar to Flow Direction but serve as a secondary attribute., be default None
         locationDescription: Optional[Union[list[str], Series[str], str]]
             Location types are sourced from legacy Bentek. These are similar to Flow Direction but serve as a secondary attribute., be default None
         locationTypeID: Optional[Union[list[str], Series[str], str]]
             An ID for the location type sourced from legacy Bentek. These are similar to Flow Direction but serve as a secondary attribute., be default None
         zone: Optional[Union[list[str], Series[str], str]]
             A designation for where on the pipeline system the point is located, corresponding to a pipeline’s operational and market design. Zonal information is sourced from the legacy Bentek service., be default None
         connectingParty: Optional[Union[list[str], Series[str], str]]
             The downstream connecting business name of a meter as reported by the pipeline, utilizes legacy Bentek service., be default None
         locProp: Optional[Union[list[str], Series[str], str]]
             The location propriety code reported by the pipeline for a specific meter., be default None
         domain: Optional[Union[list[str], Series[str], str]]
             US Lower-48, Canada and Mexico., be default None
         domainID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the domain., be default None
         region: Optional[Union[list[str], Series[str], str]]
             A defined geographic region within the Americas Gas service. Regions are an aggregation of states or provinces within a country., be default None
         regionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic region., be default None
         subregion: Optional[Union[list[str], Series[str], str]]
             A defined geographic subregion within the Americas Gas service. A substate geography is sometimes referred to as a subregion. Subregions are an aggregation of specific counties within a region and a country., be default None
         subregionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic subregion., be default None
         state: Optional[Union[list[str], Series[str], str]]
             The political boundaries that define a state or province within country., be default None
         stateID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the state or province utilizes legacy Bentek IDs., be default None
         county: Optional[Union[list[str], Series[str], str]]
             The political boundaries of a defined county within a US state in which a meter or point resides., be default None
         countyID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the county within a US state in which a meter or point resides, utilizes legacy Bentek IDs., be default None
         producingArea: Optional[Union[list[str], Series[str], str]]
             Defined aggregation of counties within a state that is a best fit representation of prominent oil and gas plays and basins., be default None
         producingAreaID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for a defined Producing Area, utilizes legacy PointLogic IDs., be default None
         paddName: Optional[Union[list[str], Series[str], str]]
             Petroleum Administration for Defense Districts (PADDs) are geographic aggregations of the 50 States and the District of Columbia into five districts., be default None
         latitude: Optional[Union[list[str], Series[str], str]]
             A geography based coordinate that specifies the north–south position of a point on the surface of the Earth. Latitude and longitude are used to identify the precise location of a pipeline meter or point., be default None
         longitude: Optional[Union[list[str], Series[str], str]]
             A geography based coordinate that specifies the east–west position of a point on the surface of the Earth. Latitude and longitude are used to identify the precise location of a pipeline meter or point., be default None
         plantFieldName: Optional[Union[list[str], Series[str], str]]
             The plant or field name where the facility resides. When applicable, the name will align to EIA-860 or EIA-191 data., be default None
         plantFieldCode: Optional[Union[list[str], Series[str], str]]
             The plant or field code where the facility resides. When applicable, the code will align to EIA-860 or EIA-191 data., be default None
         utilityCompanyName: Optional[Union[list[str], Series[str], str]]
             The name of the utility company that owns or operates the facility. When applicable, the name will align to EIA-860 or EIA-191 data., be default None
         utilityCompanyID: Optional[Union[list[str], Series[str], str]]
             The assigned ID of the utility company that ownes or operates the facility. When applicable, the name will align to EIA-860 or EIA-191 data., be default None
         nercRegion: Optional[Union[list[str], Series[str], str]]
             North American Reliability Council region., be default None
         balancingAuthorityName: Optional[Union[list[str], Series[str], str]]
             The name of a balancing authority. When applicable, the name will align to EIA-860., be default None
         balancingAuthorityCode: Optional[Union[list[str], Series[str], str]]
             The code assigned to a balancing authority by the FERC. When applicable, the name will align to EIA-860., be default None
         sectorName: Optional[Union[list[str], Series[str], str]]
             The sector which the facility resides. Power for example can be an IPP Non-CHP = Independent Power Producer and Not a commercial combined heat and power plant aka: cogen facility. When applicable, the name will align to EIA-860., be default None
         storageReservoirName: Optional[Union[list[str], Series[str], str]]
             The name of the storage reservoir. When applicable, the name will align to EIA-191., be default None
         storageFieldType: Optional[Union[list[str], Series[str], str]]
             The type of storage field. When applicable, the name will align to EIA-191., be default None
         eiaStorageRegion: Optional[Union[list[str], Series[str], str]]
             The storage region names as assigned by the EIA- Energy Information Administration., be default None
         uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure., be default None
         volume: Optional[Union[list[str], Series[str], str]]
             Volume., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("flowDate", flowDate))
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("dateFrequency", dateFrequency))
        filter_params.append(list_to_filter("dateFrequencyDesc", dateFrequencyDesc))
        filter_params.append(list_to_filter("facilityType", facilityType))
        filter_params.append(list_to_filter("facilityTypeID", facilityTypeID))
        filter_params.append(list_to_filter("viewType", viewType))
        filter_params.append(list_to_filter("name", name))
        filter_params.append(list_to_filter("modelID", modelID))
        filter_params.append(list_to_filter("componentPointID", componentPointID))
        filter_params.append(list_to_filter("pipelineName", pipelineName))
        filter_params.append(list_to_filter("pipelineID", pipelineID))
        filter_params.append(list_to_filter("pointName", pointName))
        filter_params.append(list_to_filter("meterTypePrimary", meterTypePrimary))
        filter_params.append(list_to_filter("meterTypeIDPrimary", meterTypeIDPrimary))
        filter_params.append(list_to_filter("meterTypeSecondary", meterTypeSecondary))
        filter_params.append(list_to_filter("meterTypeIDSecondary", meterTypeIDSecondary))
        filter_params.append(list_to_filter("locationTypeCode", locationTypeCode))
        filter_params.append(list_to_filter("locationDescription", locationDescription))
        filter_params.append(list_to_filter("locationTypeID", locationTypeID))
        filter_params.append(list_to_filter("zone", zone))
        filter_params.append(list_to_filter("connectingParty", connectingParty))
        filter_params.append(list_to_filter("locProp", locProp))
        filter_params.append(list_to_filter("domain", domain))
        filter_params.append(list_to_filter("domainID", domainID))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("regionID", regionID))
        filter_params.append(list_to_filter("subregion", subregion))
        filter_params.append(list_to_filter("subregionID", subregionID))
        filter_params.append(list_to_filter("state", state))
        filter_params.append(list_to_filter("stateID", stateID))
        filter_params.append(list_to_filter("county", county))
        filter_params.append(list_to_filter("countyID", countyID))
        filter_params.append(list_to_filter("producingArea", producingArea))
        filter_params.append(list_to_filter("producingAreaID", producingAreaID))
        filter_params.append(list_to_filter("paddName", paddName))
        filter_params.append(list_to_filter("latitude", latitude))
        filter_params.append(list_to_filter("longitude", longitude))
        filter_params.append(list_to_filter("plantFieldName", plantFieldName))
        filter_params.append(list_to_filter("plantFieldCode", plantFieldCode))
        filter_params.append(list_to_filter("utilityCompanyName", utilityCompanyName))
        filter_params.append(list_to_filter("utilityCompanyID", utilityCompanyID))
        filter_params.append(list_to_filter("nercRegion", nercRegion))
        filter_params.append(list_to_filter("balancingAuthorityName", balancingAuthorityName))
        filter_params.append(list_to_filter("balancingAuthorityCode", balancingAuthorityCode))
        filter_params.append(list_to_filter("sectorName", sectorName))
        filter_params.append(list_to_filter("storageReservoirName", storageReservoirName))
        filter_params.append(list_to_filter("storageFieldType", storageFieldType))
        filter_params.append(list_to_filter("eiaStorageRegion", eiaStorageRegion))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("volume", volume))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/facility-flow-data",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_pipeline_profiles_data(
        self, year: Optional[Union[list[str], Series[str], str]] = None, quarter: Optional[Union[list[str], Series[str], str]] = None, pipelineFilerName: Optional[Union[list[str], Series[str], str]] = None, pipelineName: Optional[Union[list[str], Series[str], str]] = None, pipelineID: Optional[Union[list[str], Series[str], str]] = None, operatingRevenuesGas: Optional[Union[list[str], Series[str], str]] = None, operatingRevenuesTotal: Optional[Union[list[str], Series[str], str]] = None, operationExpensesGas: Optional[Union[list[str], Series[str], str]] = None, operatingExpensesTotal: Optional[Union[list[str], Series[str], str]] = None, maintenanceExpensesGas: Optional[Union[list[str], Series[str], str]] = None, maintenanceExpensesTotal: Optional[Union[list[str], Series[str], str]] = None, taxesOtherThanIncomeTaxesTotal: Optional[Union[list[str], Series[str], str]] = None, utilityEbitda: Optional[Union[list[str], Series[str], str]] = None, transmissionPipelineLength: Optional[Union[list[str], Series[str], str]] = None, trptGasForOthersTransmsnVolMmcf: Optional[Union[list[str], Series[str], str]] = None, landAndRightsTransEoy000: Optional[Union[list[str], Series[str], str]] = None, rightsOfWayTransEoy000: Optional[Union[list[str], Series[str], str]] = None, strucAndImprovTranEoy000: Optional[Union[list[str], Series[str], str]] = None, mainsTransmissionEoy000: Optional[Union[list[str], Series[str], str]] = None, comprstaequipTransEoy000: Optional[Union[list[str], Series[str], str]] = None, measRegStaEqTransEoy000: Optional[Union[list[str], Series[str], str]] = None, communicationEquipTransEoy000: Optional[Union[list[str], Series[str], str]] = None, totalTransmissionPlantAddns000: Optional[Union[list[str], Series[str], str]] = None, totalTransmissionPlantRet000: Optional[Union[list[str], Series[str], str]] = None, totalTransmissionPlantAdjust000: Optional[Union[list[str], Series[str], str]] = None, totalTransmissionPlantTransf000: Optional[Union[list[str], Series[str], str]] = None, totalTransmissionPlantEoy000: Optional[Union[list[str], Series[str], str]] = None, totalGasPlantInServiceEoy: Optional[Union[list[str], Series[str], str]] = None, plantInServClassifiedTotal: Optional[Union[list[str], Series[str], str]] = None, plantPurchasedOrSoldTotal: Optional[Union[list[str], Series[str], str]] = None, completeConstrUnclassTotal: Optional[Union[list[str], Series[str], str]] = None, exptlPlantUnclassifiedTotal: Optional[Union[list[str], Series[str], str]] = None, constrWipTotal: Optional[Union[list[str], Series[str], str]] = None, totalUtilityPlantTotal: Optional[Union[list[str], Series[str], str]] = None, tranOpSupAndEngineering: Optional[Union[list[str], Series[str], str]] = None, transmissOperLoadDispatch: Optional[Union[list[str], Series[str], str]] = None, operTransCommunicationSysExp: Optional[Union[list[str], Series[str], str]] = None, operTransComprStaLaborAndExp: Optional[Union[list[str], Series[str], str]] = None, operTransGasForComprStFuel: Optional[Union[list[str], Series[str], str]] = None, operTransOthFuelAndPwrForComprSt: Optional[Union[list[str], Series[str], str]] = None, operTransMainsExp: Optional[Union[list[str], Series[str], str]] = None, operTransMeasAndRegStaExp: Optional[Union[list[str], Series[str], str]] = None, operTransTransmAndComprByOth: Optional[Union[list[str], Series[str], str]] = None, tranOpMiscTransmissionExp: Optional[Union[list[str], Series[str], str]] = None, transmissOperRents: Optional[Union[list[str], Series[str], str]] = None, transmissTranOperationExp: Optional[Union[list[str], Series[str], str]] = None, transmissMaintSupvsnAndEngin: Optional[Union[list[str], Series[str], str]] = None, transmissMaintOfStructures: Optional[Union[list[str], Series[str], str]] = None, maintTransMains: Optional[Union[list[str], Series[str], str]] = None, maintTransCompressorStaEquip: Optional[Union[list[str], Series[str], str]] = None, maintTransMeasAndRegStaEquip: Optional[Union[list[str], Series[str], str]] = None, maintTransCommunicationEquip: Optional[Union[list[str], Series[str], str]] = None, transmissMaintOfMiscTranPlt: Optional[Union[list[str], Series[str], str]] = None, transmissMaintExp: Optional[Union[list[str], Series[str], str]] = None, transmissOandMExp: Optional[Union[list[str], Series[str], str]] = None, peak1IntPipeNoNoticeTransp: Optional[Union[list[str], Series[str], str]] = None, peak1OthDthNoNoticeTransport: Optional[Union[list[str], Series[str], str]] = None, peak1TotalDthNoNoticeTransp: Optional[Union[list[str], Series[str], str]] = None, peak1IntPipeDthOthFirmTransp: Optional[Union[list[str], Series[str], str]] = None, peak1OthDthOtherFirmTransport: Optional[Union[list[str], Series[str], str]] = None, peak1TotalDthOthFirmTransport: Optional[Union[list[str], Series[str], str]] = None, peak1IntPipeDthInterrTransp: Optional[Union[list[str], Series[str], str]] = None, peak1OthDthInterrTransport: Optional[Union[list[str], Series[str], str]] = None, peak1TotalDthInterrTransport: Optional[Union[list[str], Series[str], str]] = None, peak1IntPipeDthOthTransp: Optional[Union[list[str], Series[str], str]] = None, peak1OthDthOtherTransport: Optional[Union[list[str], Series[str], str]] = None, peak1TotalDthOthTransport: Optional[Union[list[str], Series[str], str]] = None, peak1IntPipeDthTransp: Optional[Union[list[str], Series[str], str]] = None, peak1OthDthTransport: Optional[Union[list[str], Series[str], str]] = None, peak1TotalDthTransport: Optional[Union[list[str], Series[str], str]] = None, peak3IntPipeNoNoticeTransp: Optional[Union[list[str], Series[str], str]] = None, peak3OthNoNoticeTransport: Optional[Union[list[str], Series[str], str]] = None, peak3TotalNoNoticeTransport: Optional[Union[list[str], Series[str], str]] = None, peak3IntPipeDthOthFirmTransp: Optional[Union[list[str], Series[str], str]] = None, peak3OthDthOtherFirmTransport: Optional[Union[list[str], Series[str], str]] = None, peak3TotalDthOthFirmTransp: Optional[Union[list[str], Series[str], str]] = None, peak3IntPipeDthInterrTransp: Optional[Union[list[str], Series[str], str]] = None, peak3OthDthInterrTransport: Optional[Union[list[str], Series[str], str]] = None, peak3TotalDthInterrTransport: Optional[Union[list[str], Series[str], str]] = None, peak3IntPipeDthOthTransp: Optional[Union[list[str], Series[str], str]] = None, peak3OthDthOtherTransport: Optional[Union[list[str], Series[str], str]] = None, peak3TotalDthOtherTransport: Optional[Union[list[str], Series[str], str]] = None, peak3IntPipeDthTransp: Optional[Union[list[str], Series[str], str]] = None, peak3OthDthTransport: Optional[Union[list[str], Series[str], str]] = None, peak3TotalDthTransport: Optional[Union[list[str], Series[str], str]] = None, gasOfOthRecdForGathering: Optional[Union[list[str], Series[str], str]] = None, reciepts: Optional[Union[list[str], Series[str], str]] = None, delivOfGasTransOrComprOth: Optional[Union[list[str], Series[str], str]] = None, gasDeliveredAsImbalances: Optional[Union[list[str], Series[str], str]] = None, gasUsedForCompressorStaFuel: Optional[Union[list[str], Series[str], str]] = None, natGasOtherDeliv: Optional[Union[list[str], Series[str], str]] = None, totalDeliveries: Optional[Union[list[str], Series[str], str]] = None, gasStoredBoy: Optional[Union[list[str], Series[str], str]] = None, gasStoredGasDelivToStorage: Optional[Union[list[str], Series[str], str]] = None, gasStoredGasWithdrFromStor: Optional[Union[list[str], Series[str], str]] = None, gasStoredOthDebOrCredNet: Optional[Union[list[str], Series[str], str]] = None, gasStoredEoy: Optional[Union[list[str], Series[str], str]] = None, gasStoredGasVolumeDth: Optional[Union[list[str], Series[str], str]] = None, gasStoredAmountPerDth: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         year: Optional[Union[list[str], Series[str], str]]
             The year the data was reported to the US Federal Energy Regulatory Commission (FERC)., be default None
         quarter: Optional[Union[list[str], Series[str], str]]
             The quarter of the year data was reported to the US Federal Energy Regulatory Commission (FERC)., be default None
         pipelineFilerName: Optional[Union[list[str], Series[str], str]]
             The filer name of a pipeline system., be default None
         pipelineName: Optional[Union[list[str], Series[str], str]]
             The display name of a pipeline system, utilizes legacy Bentek names when applicable., be default None
         pipelineID: Optional[Union[list[str], Series[str], str]]
             The ID given to a pipeline system, utilizes legacy Bentek pipeline ids when applicable., be default None
         operatingRevenuesGas: Optional[Union[list[str], Series[str], str]]
             Operating revenues gas are the gas component of the revenues., be default None
         operatingRevenuesTotal: Optional[Union[list[str], Series[str], str]]
             Total operating revenues for the entire pipeline., be default None
         operationExpensesGas: Optional[Union[list[str], Series[str], str]]
             The operating expenses of pipeline - maintenance, supervision etc., be default None
         operatingExpensesTotal: Optional[Union[list[str], Series[str], str]]
             The total operating expense for the pipeline., be default None
         maintenanceExpensesGas: Optional[Union[list[str], Series[str], str]]
             The maintenance expenses for natural gas associated to the pipeline., be default None
         maintenanceExpensesTotal: Optional[Union[list[str], Series[str], str]]
             The total maintenance expenses including gas and other maintenance expenses., be default None
         taxesOtherThanIncomeTaxesTotal: Optional[Union[list[str], Series[str], str]]
             The total associated taxes other than income taxes for the pipeline., be default None
         utilityEbitda: Optional[Union[list[str], Series[str], str]]
             The pipeline EBITDA = Earnings Before Interest, Taxes, Depreciation and Amortization., be default None
         transmissionPipelineLength: Optional[Union[list[str], Series[str], str]]
             The pipeline length in miles., be default None
         trptGasForOthersTransmsnVolMmcf: Optional[Union[list[str], Series[str], str]]
             Transportation of gas for others in MMcf., be default None
         landAndRightsTransEoy000: Optional[Union[list[str], Series[str], str]]
             The land and rights of way costs associated with the transport of natural gas for the pipeline at end of year (EOY)., be default None
         rightsOfWayTransEoy000: Optional[Union[list[str], Series[str], str]]
             Specific right of way costs associated with the transport of natural gas for the pipeline at end of year (EOY)., be default None
         strucAndImprovTranEoy000: Optional[Union[list[str], Series[str], str]]
             Specific structure and improvement costs in the transportation of natural gas for the pipeline at end of year (EOY)., be default None
         mainsTransmissionEoy000: Optional[Union[list[str], Series[str], str]]
             Specific maintenance costs in the transportation of natural gas for the pipeline at end of year (EOY)., be default None
         comprstaequipTransEoy000: Optional[Union[list[str], Series[str], str]]
             Specific compressor station equipment costs accrued by the pipeline in the transportation of natural gas for the pipeline at end of year (EOY)., be default None
         measRegStaEqTransEoy000: Optional[Union[list[str], Series[str], str]]
             Specific measuring, regulating station equipment costs accrued by the pipeline in the transportation of natural gas for the pipeline at end of year (EOY)., be default None
         communicationEquipTransEoy000: Optional[Union[list[str], Series[str], str]]
             Specific communication equipment costs accrued by the pipeline in the transportation of natural gas for the pipeline at end of year (EOY)., be default None
         totalTransmissionPlantAddns000: Optional[Union[list[str], Series[str], str]]
             The cost of additional meters, meter installation, house regulator installations, industrial measuring and regulating station equipment, other property on customers' premises, asset retirement costs for distribution, land and land rights, structures and improvements, office furniture and equipment, transportation equipment, stores equipment, tools, shop, and garage equipment, laboratory equipment etc., be default None
         totalTransmissionPlantRet000: Optional[Union[list[str], Series[str], str]]
             Total pipeline asset retirement costs., be default None
         totalTransmissionPlantAdjust000: Optional[Union[list[str], Series[str], str]]
             The cost of adjustments of meters, meter installation, house regulator installations, industrial measuring and regulating station equipment, other property on customers' premises, asset retirement costs for distribution, land and land rights, structures and improvements, office furniture and equipment, transportation equipment, stores equipment, tools, shop, and garage equipment, laboratory equipment etc., be default None
         totalTransmissionPlantTransf000: Optional[Union[list[str], Series[str], str]]
             The transfer costs of meters, meter installation, house regulator installations, industrial measuring and regulating station equipment, other property on customers' premises, asset retirement costs for distribution, land and land rights, structures and improvements, office furniture and equipment, transportation equipment, stores equipment, tools, shop, and garage equipment, laboratory equipment etc., be default None
         totalTransmissionPlantEoy000: Optional[Union[list[str], Series[str], str]]
             The total costs of operating a pipeline with respect to additions, retirements, adjustments, and transfers (includes land and land rights, structures and improvements, maintenance, compressor station equipment etc., be default None
         totalGasPlantInServiceEoy: Optional[Union[list[str], Series[str], str]]
             The total costs of operating a pipeline., be default None
         plantInServClassifiedTotal: Optional[Union[list[str], Series[str], str]]
             Unclassified costs associated in operating a pipeline., be default None
         plantPurchasedOrSoldTotal: Optional[Union[list[str], Series[str], str]]
             The cost of property purchased or sold., be default None
         completeConstrUnclassTotal: Optional[Union[list[str], Series[str], str]]
              Completed construction not classified total., be default None
         exptlPlantUnclassifiedTotal: Optional[Union[list[str], Series[str], str]]
             Total experimental unclassified plant costs that are experimental or general research expenses., be default None
         constrWipTotal: Optional[Union[list[str], Series[str], str]]
             Construction Work in Progress total., be default None
         totalUtilityPlantTotal: Optional[Union[list[str], Series[str], str]]
             All costs associated in operating a pipeline + construction work in progress expenses., be default None
         tranOpSupAndEngineering: Optional[Union[list[str], Series[str], str]]
             Transmission facility operation, supervision and engineering costs., be default None
         transmissOperLoadDispatch: Optional[Union[list[str], Series[str], str]]
             Transmission facility operation system control and load dispatching costs., be default None
         operTransCommunicationSysExp: Optional[Union[list[str], Series[str], str]]
             Communication system expenses at the transmission facility., be default None
         operTransComprStaLaborAndExp: Optional[Union[list[str], Series[str], str]]
             Compressor station labor and expenses., be default None
         operTransGasForComprStFuel: Optional[Union[list[str], Series[str], str]]
             Gas for compressor station fuel expenses., be default None
         operTransOthFuelAndPwrForComprSt: Optional[Union[list[str], Series[str], str]]
             Other fuel and power expenses at compressor stations, be default None
         operTransMainsExp: Optional[Union[list[str], Series[str], str]]
             Transmission facility mains expenses., be default None
         operTransMeasAndRegStaExp: Optional[Union[list[str], Series[str], str]]
             Transmission facility Measuring and Regulating Station Expenses., be default None
         operTransTransmAndComprByOth: Optional[Union[list[str], Series[str], str]]
             Expenses associate with the transmission and compression of gas by others., be default None
         tranOpMiscTransmissionExp: Optional[Union[list[str], Series[str], str]]
             Miscellaneous expenses associated with the transmission of gas., be default None
         transmissOperRents: Optional[Union[list[str], Series[str], str]]
             Rent expenses associated with the transmission of gas., be default None
         transmissTranOperationExp: Optional[Union[list[str], Series[str], str]]
             The total transmission expenses: operation supervision and engineering, system control and load dispatching, communication system expenses, compressor station labor and expenses, gas for compressor station fuel, other fuel and power for compressor stations, mains expenses, measuring and regulating station expenses, transmission and compression of gas by others, other expenses and rents., be default None
         transmissMaintSupvsnAndEngin: Optional[Union[list[str], Series[str], str]]
             Operation, supervision and engineering maintenance expenses., be default None
         transmissMaintOfStructures: Optional[Union[list[str], Series[str], str]]
             Maintenance of structures and improvements expenses., be default None
         maintTransMains: Optional[Union[list[str], Series[str], str]]
             Maintenance of mains expenses., be default None
         maintTransCompressorStaEquip: Optional[Union[list[str], Series[str], str]]
             Compressor station equipment maintenance expenses., be default None
         maintTransMeasAndRegStaEquip: Optional[Union[list[str], Series[str], str]]
             Transmission maintenance of measuring and regulation station equipment., be default None
         maintTransCommunicationEquip: Optional[Union[list[str], Series[str], str]]
             Maintenance expenses associated with communication equipment., be default None
         transmissMaintOfMiscTranPlt: Optional[Union[list[str], Series[str], str]]
             Total of other maintenance expenses., be default None
         transmissMaintExp: Optional[Union[list[str], Series[str], str]]
             The total maintenance expenses for the pipeline., be default None
         transmissOandMExp: Optional[Union[list[str], Series[str], str]]
             Operation and maintenance expenses., be default None
         peak1IntPipeNoNoticeTransp: Optional[Union[list[str], Series[str], str]]
             Single day peak deliveries for interstate pipelines Dth., be default None
         peak1OthDthNoNoticeTransport: Optional[Union[list[str], Series[str], str]]
             Single day peak deliveries for no notice transport for others Dth., be default None
         peak1TotalDthNoNoticeTransp: Optional[Union[list[str], Series[str], str]]
             Total single day peak deliveries for no notice transported volumes Dth., be default None
         peak1IntPipeDthOthFirmTransp: Optional[Union[list[str], Series[str], str]]
             Single peak day other firm transportation-Dth of Gas Delivered to Interstate Pipelines., be default None
         peak1OthDthOtherFirmTransport: Optional[Union[list[str], Series[str], str]]
             Single peak day other firm transportation-Dth of gas delivered to others., be default None
         peak1TotalDthOthFirmTransport: Optional[Union[list[str], Series[str], str]]
             Total single day peak deliveries for other firm transportation Dth., be default None
         peak1IntPipeDthInterrTransp: Optional[Union[list[str], Series[str], str]]
             Peak day interruptible transportation-Dth of gas delivered to interstate pipelines., be default None
         peak1OthDthInterrTransport: Optional[Union[list[str], Series[str], str]]
             Peak day interruptible transportation-Dth of gas delivered to others., be default None
         peak1TotalDthInterrTransport: Optional[Union[list[str], Series[str], str]]
             Peak day interruptible transportation-total Dth., be default None
         peak1IntPipeDthOthTransp: Optional[Union[list[str], Series[str], str]]
             Other-single peak day-Dth of gas delivered to interstate pipelines., be default None
         peak1OthDthOtherTransport: Optional[Union[list[str], Series[str], str]]
             Other-single peak day-Dth of gas delivered to others., be default None
         peak1TotalDthOthTransport: Optional[Union[list[str], Series[str], str]]
             Other-single peak day total Dth., be default None
         peak1IntPipeDthTransp: Optional[Union[list[str], Series[str], str]]
             Single peak day-Dth of gas delivered to interstate pipelines total., be default None
         peak1OthDthTransport: Optional[Union[list[str], Series[str], str]]
             Single peak day-Dth of gas delivered to others total., be default None
         peak1TotalDthTransport: Optional[Union[list[str], Series[str], str]]
             Single peak day-Dth of gas delivered total., be default None
         peak3IntPipeNoNoticeTransp: Optional[Union[list[str], Series[str], str]]
             Peak 3 Day No-Notice Transportation-Dth of Gas Delivered to Interstate Pipelines., be default None
         peak3OthNoNoticeTransport: Optional[Union[list[str], Series[str], str]]
             Peak 3 Day No-Notice Transportation-Dth of Gas Delivered to Others., be default None
         peak3TotalNoNoticeTransport: Optional[Union[list[str], Series[str], str]]
             Total Peak 3 Day No-Notice Transportation Dth., be default None
         peak3IntPipeDthOthFirmTransp: Optional[Union[list[str], Series[str], str]]
             Peak 3 day Other Firm Transportation-Dth of Gas Delivered to Interstate Pipelines., be default None
         peak3OthDthOtherFirmTransport: Optional[Union[list[str], Series[str], str]]
             Peak 3 day Other Firm Transportation-Dth of Gas Delivered to Others., be default None
         peak3TotalDthOthFirmTransp: Optional[Union[list[str], Series[str], str]]
             Total 3 day peak other firm transportation Dth., be default None
         peak3IntPipeDthInterrTransp: Optional[Union[list[str], Series[str], str]]
             Peak 3 day interruptible transportation-Dth of gas delivered to interstate pipelines., be default None
         peak3OthDthInterrTransport: Optional[Union[list[str], Series[str], str]]
             Peak 3 day interruptible transportation-Dth of gas delivered to others., be default None
         peak3TotalDthInterrTransport: Optional[Union[list[str], Series[str], str]]
             Peak 3 day total interruptible transportation Dth., be default None
         peak3IntPipeDthOthTransp: Optional[Union[list[str], Series[str], str]]
             Peak 3 day other-Dth of gas delivered to interstate pipelines., be default None
         peak3OthDthOtherTransport: Optional[Union[list[str], Series[str], str]]
             Peak 3 day other-Dth of gas delivered to others., be default None
         peak3TotalDthOtherTransport: Optional[Union[list[str], Series[str], str]]
             Total 3 day peak other-Dth of gas delivered to others., be default None
         peak3IntPipeDthTransp: Optional[Union[list[str], Series[str], str]]
             Total 3 day peak-Dth of gas delivered to interstate pipelines., be default None
         peak3OthDthTransport: Optional[Union[list[str], Series[str], str]]
             Total 3 day peak-Dth of gas delivered to others., be default None
         peak3TotalDthTransport: Optional[Union[list[str], Series[str], str]]
             Total peak 3 day-Dth transport., be default None
         gasOfOthRecdForGathering: Optional[Union[list[str], Series[str], str]]
             Gas of others received for gathering., be default None
         reciepts: Optional[Union[list[str], Series[str], str]]
             Total receipts of gas received., be default None
         delivOfGasTransOrComprOth: Optional[Union[list[str], Series[str], str]]
             Deliveries of gas transported for others., be default None
         gasDeliveredAsImbalances: Optional[Union[list[str], Series[str], str]]
             Gas delivered as imbalances., be default None
         gasUsedForCompressorStaFuel: Optional[Union[list[str], Series[str], str]]
             Gas used for compressor station fuel., be default None
         natGasOtherDeliv: Optional[Union[list[str], Series[str], str]]
             Natural gas other deliveries., be default None
         totalDeliveries: Optional[Union[list[str], Series[str], str]]
             Total deliveries of natural gas., be default None
         gasStoredBoy: Optional[Union[list[str], Series[str], str]]
             Stored gas balance-beginning of year (BOY)., be default None
         gasStoredGasDelivToStorage: Optional[Union[list[str], Series[str], str]]
             Gas delivered to storage-beginning of year (BOY)., be default None
         gasStoredGasWithdrFromStor: Optional[Union[list[str], Series[str], str]]
             Gas withdrawn from storage- beginning of year (BOY)., be default None
         gasStoredOthDebOrCredNet: Optional[Union[list[str], Series[str], str]]
             Gas stored other debits and credits., be default None
         gasStoredEoy: Optional[Union[list[str], Series[str], str]]
             Stored gas- end of year Dth (EOY)., be default None
         gasStoredGasVolumeDth: Optional[Union[list[str], Series[str], str]]
             Gas volume stored Dth., be default None
         gasStoredAmountPerDth: Optional[Union[list[str], Series[str], str]]
             Gas stored per Dth., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("year", year))
        filter_params.append(list_to_filter("quarter", quarter))
        filter_params.append(list_to_filter("pipelineFilerName", pipelineFilerName))
        filter_params.append(list_to_filter("pipelineName", pipelineName))
        filter_params.append(list_to_filter("pipelineID", pipelineID))
        filter_params.append(list_to_filter("operatingRevenuesGas", operatingRevenuesGas))
        filter_params.append(list_to_filter("operatingRevenuesTotal", operatingRevenuesTotal))
        filter_params.append(list_to_filter("operationExpensesGas", operationExpensesGas))
        filter_params.append(list_to_filter("operatingExpensesTotal", operatingExpensesTotal))
        filter_params.append(list_to_filter("maintenanceExpensesGas", maintenanceExpensesGas))
        filter_params.append(list_to_filter("maintenanceExpensesTotal", maintenanceExpensesTotal))
        filter_params.append(list_to_filter("taxesOtherThanIncomeTaxesTotal", taxesOtherThanIncomeTaxesTotal))
        filter_params.append(list_to_filter("utilityEbitda", utilityEbitda))
        filter_params.append(list_to_filter("transmissionPipelineLength", transmissionPipelineLength))
        filter_params.append(list_to_filter("trptGasForOthersTransmsnVolMmcf", trptGasForOthersTransmsnVolMmcf))
        filter_params.append(list_to_filter("landAndRightsTransEoy000", landAndRightsTransEoy000))
        filter_params.append(list_to_filter("rightsOfWayTransEoy000", rightsOfWayTransEoy000))
        filter_params.append(list_to_filter("strucAndImprovTranEoy000", strucAndImprovTranEoy000))
        filter_params.append(list_to_filter("mainsTransmissionEoy000", mainsTransmissionEoy000))
        filter_params.append(list_to_filter("comprstaequipTransEoy000", comprstaequipTransEoy000))
        filter_params.append(list_to_filter("measRegStaEqTransEoy000", measRegStaEqTransEoy000))
        filter_params.append(list_to_filter("communicationEquipTransEoy000", communicationEquipTransEoy000))
        filter_params.append(list_to_filter("totalTransmissionPlantAddns000", totalTransmissionPlantAddns000))
        filter_params.append(list_to_filter("totalTransmissionPlantRet000", totalTransmissionPlantRet000))
        filter_params.append(list_to_filter("totalTransmissionPlantAdjust000", totalTransmissionPlantAdjust000))
        filter_params.append(list_to_filter("totalTransmissionPlantTransf000", totalTransmissionPlantTransf000))
        filter_params.append(list_to_filter("totalTransmissionPlantEoy000", totalTransmissionPlantEoy000))
        filter_params.append(list_to_filter("totalGasPlantInServiceEoy", totalGasPlantInServiceEoy))
        filter_params.append(list_to_filter("plantInServClassifiedTotal", plantInServClassifiedTotal))
        filter_params.append(list_to_filter("plantPurchasedOrSoldTotal", plantPurchasedOrSoldTotal))
        filter_params.append(list_to_filter("completeConstrUnclassTotal", completeConstrUnclassTotal))
        filter_params.append(list_to_filter("exptlPlantUnclassifiedTotal", exptlPlantUnclassifiedTotal))
        filter_params.append(list_to_filter("constrWipTotal", constrWipTotal))
        filter_params.append(list_to_filter("totalUtilityPlantTotal", totalUtilityPlantTotal))
        filter_params.append(list_to_filter("tranOpSupAndEngineering", tranOpSupAndEngineering))
        filter_params.append(list_to_filter("transmissOperLoadDispatch", transmissOperLoadDispatch))
        filter_params.append(list_to_filter("operTransCommunicationSysExp", operTransCommunicationSysExp))
        filter_params.append(list_to_filter("operTransComprStaLaborAndExp", operTransComprStaLaborAndExp))
        filter_params.append(list_to_filter("operTransGasForComprStFuel", operTransGasForComprStFuel))
        filter_params.append(list_to_filter("operTransOthFuelAndPwrForComprSt", operTransOthFuelAndPwrForComprSt))
        filter_params.append(list_to_filter("operTransMainsExp", operTransMainsExp))
        filter_params.append(list_to_filter("operTransMeasAndRegStaExp", operTransMeasAndRegStaExp))
        filter_params.append(list_to_filter("operTransTransmAndComprByOth", operTransTransmAndComprByOth))
        filter_params.append(list_to_filter("tranOpMiscTransmissionExp", tranOpMiscTransmissionExp))
        filter_params.append(list_to_filter("transmissOperRents", transmissOperRents))
        filter_params.append(list_to_filter("transmissTranOperationExp", transmissTranOperationExp))
        filter_params.append(list_to_filter("transmissMaintSupvsnAndEngin", transmissMaintSupvsnAndEngin))
        filter_params.append(list_to_filter("transmissMaintOfStructures", transmissMaintOfStructures))
        filter_params.append(list_to_filter("maintTransMains", maintTransMains))
        filter_params.append(list_to_filter("maintTransCompressorStaEquip", maintTransCompressorStaEquip))
        filter_params.append(list_to_filter("maintTransMeasAndRegStaEquip", maintTransMeasAndRegStaEquip))
        filter_params.append(list_to_filter("maintTransCommunicationEquip", maintTransCommunicationEquip))
        filter_params.append(list_to_filter("transmissMaintOfMiscTranPlt", transmissMaintOfMiscTranPlt))
        filter_params.append(list_to_filter("transmissMaintExp", transmissMaintExp))
        filter_params.append(list_to_filter("transmissOandMExp", transmissOandMExp))
        filter_params.append(list_to_filter("peak1IntPipeNoNoticeTransp", peak1IntPipeNoNoticeTransp))
        filter_params.append(list_to_filter("peak1OthDthNoNoticeTransport", peak1OthDthNoNoticeTransport))
        filter_params.append(list_to_filter("peak1TotalDthNoNoticeTransp", peak1TotalDthNoNoticeTransp))
        filter_params.append(list_to_filter("peak1IntPipeDthOthFirmTransp", peak1IntPipeDthOthFirmTransp))
        filter_params.append(list_to_filter("peak1OthDthOtherFirmTransport", peak1OthDthOtherFirmTransport))
        filter_params.append(list_to_filter("peak1TotalDthOthFirmTransport", peak1TotalDthOthFirmTransport))
        filter_params.append(list_to_filter("peak1IntPipeDthInterrTransp", peak1IntPipeDthInterrTransp))
        filter_params.append(list_to_filter("peak1OthDthInterrTransport", peak1OthDthInterrTransport))
        filter_params.append(list_to_filter("peak1TotalDthInterrTransport", peak1TotalDthInterrTransport))
        filter_params.append(list_to_filter("peak1IntPipeDthOthTransp", peak1IntPipeDthOthTransp))
        filter_params.append(list_to_filter("peak1OthDthOtherTransport", peak1OthDthOtherTransport))
        filter_params.append(list_to_filter("peak1TotalDthOthTransport", peak1TotalDthOthTransport))
        filter_params.append(list_to_filter("peak1IntPipeDthTransp", peak1IntPipeDthTransp))
        filter_params.append(list_to_filter("peak1OthDthTransport", peak1OthDthTransport))
        filter_params.append(list_to_filter("peak1TotalDthTransport", peak1TotalDthTransport))
        filter_params.append(list_to_filter("peak3IntPipeNoNoticeTransp", peak3IntPipeNoNoticeTransp))
        filter_params.append(list_to_filter("peak3OthNoNoticeTransport", peak3OthNoNoticeTransport))
        filter_params.append(list_to_filter("peak3TotalNoNoticeTransport", peak3TotalNoNoticeTransport))
        filter_params.append(list_to_filter("peak3IntPipeDthOthFirmTransp", peak3IntPipeDthOthFirmTransp))
        filter_params.append(list_to_filter("peak3OthDthOtherFirmTransport", peak3OthDthOtherFirmTransport))
        filter_params.append(list_to_filter("peak3TotalDthOthFirmTransp", peak3TotalDthOthFirmTransp))
        filter_params.append(list_to_filter("peak3IntPipeDthInterrTransp", peak3IntPipeDthInterrTransp))
        filter_params.append(list_to_filter("peak3OthDthInterrTransport", peak3OthDthInterrTransport))
        filter_params.append(list_to_filter("peak3TotalDthInterrTransport", peak3TotalDthInterrTransport))
        filter_params.append(list_to_filter("peak3IntPipeDthOthTransp", peak3IntPipeDthOthTransp))
        filter_params.append(list_to_filter("peak3OthDthOtherTransport", peak3OthDthOtherTransport))
        filter_params.append(list_to_filter("peak3TotalDthOtherTransport", peak3TotalDthOtherTransport))
        filter_params.append(list_to_filter("peak3IntPipeDthTransp", peak3IntPipeDthTransp))
        filter_params.append(list_to_filter("peak3OthDthTransport", peak3OthDthTransport))
        filter_params.append(list_to_filter("peak3TotalDthTransport", peak3TotalDthTransport))
        filter_params.append(list_to_filter("gasOfOthRecdForGathering", gasOfOthRecdForGathering))
        filter_params.append(list_to_filter("reciepts", reciepts))
        filter_params.append(list_to_filter("delivOfGasTransOrComprOth", delivOfGasTransOrComprOth))
        filter_params.append(list_to_filter("gasDeliveredAsImbalances", gasDeliveredAsImbalances))
        filter_params.append(list_to_filter("gasUsedForCompressorStaFuel", gasUsedForCompressorStaFuel))
        filter_params.append(list_to_filter("natGasOtherDeliv", natGasOtherDeliv))
        filter_params.append(list_to_filter("totalDeliveries", totalDeliveries))
        filter_params.append(list_to_filter("gasStoredBoy", gasStoredBoy))
        filter_params.append(list_to_filter("gasStoredGasDelivToStorage", gasStoredGasDelivToStorage))
        filter_params.append(list_to_filter("gasStoredGasWithdrFromStor", gasStoredGasWithdrFromStor))
        filter_params.append(list_to_filter("gasStoredOthDebOrCredNet", gasStoredOthDebOrCredNet))
        filter_params.append(list_to_filter("gasStoredEoy", gasStoredEoy))
        filter_params.append(list_to_filter("gasStoredGasVolumeDth", gasStoredGasVolumeDth))
        filter_params.append(list_to_filter("gasStoredAmountPerDth", gasStoredAmountPerDth))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/pipeline-profiles-data",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_storage_data(
        self, flowDate: Optional[Union[list[date], Series[date], date]] = None, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, dateFrequency: Optional[Union[list[str], Series[str], str]] = None, dateFrequencyDesc: Optional[Union[list[str], Series[str], str]] = None, source: Optional[Union[list[str], Series[str], str]] = None, viewType: Optional[Union[list[str], Series[str], str]] = None, viewTypeID: Optional[Union[list[str], Series[str], str]] = None, valueType: Optional[Union[list[str], Series[str], str]] = None, valueTypeID: Optional[Union[list[str], Series[str], str]] = None, domain: Optional[Union[list[str], Series[str], str]] = None, domainID: Optional[Union[list[str], Series[str], str]] = None, region: Optional[Union[list[str], Series[str], str]] = None, regionID: Optional[Union[list[str], Series[str], str]] = None, subregion: Optional[Union[list[str], Series[str], str]] = None, subregionID: Optional[Union[list[str], Series[str], str]] = None, geographyPov: Optional[Union[list[str], Series[str], str]] = None, geographyPovID: Optional[Union[list[str], Series[str], str]] = None, geographyType: Optional[Union[list[str], Series[str], str]] = None, modelID: Optional[Union[list[str], Series[str], str]] = None, workingCapacity: Optional[Union[list[str], Series[str], str]] = None, utilization: Optional[Union[list[str], Series[str], str]] = None, uom: Optional[Union[list[str], Series[str], str]] = None, volume: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         flowDate: Optional[Union[list[date], Series[date], date]]
             The calendar date or gas day the activity occurred., be default None
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         dateFrequency: Optional[Union[list[str], Series[str], str]]
             Daily, Weekly, Monthly, Seasonal, Annual., be default None
         dateFrequencyDesc: Optional[Union[list[str], Series[str], str]]
             The time period averages of the dataset such as Daily, Weekly, Monthly, Seasonal, Annual. Weekly date frequencies are based on the defined EIA storage week of Friday-Thursday. Seasonal date frequencies define Summer as April to October and Winter as November to March., be default None
         source: Optional[Union[list[str], Series[str], str]]
             Source of the data, EIA or Americas Gas., be default None
         viewType: Optional[Union[list[str], Series[str], str]]
             The type of view, which can be either Inventory, Activity, or Sample., be default None
         viewTypeID: Optional[Union[list[str], Series[str], str]]
             The ID given to a view type where Inventory is equal to 1, Activity 2 and Sample 3., be default None
         valueType: Optional[Union[list[str], Series[str], str]]
             The types of values presented in the view, such as Actual/Estimate, 5-Year Average, Delta to 5-Year Average, 5-Year Maximum, 5-Year Minimum, Last Year, Delta to Last Year, Delta to 5-Year Maximum, Delta to 5-Year Minimum., be default None
         valueTypeID: Optional[Union[list[str], Series[str], str]]
             The ID given to a value type numbered 1 through 9 listed in order as expressed in Value Type description., be default None
         domain: Optional[Union[list[str], Series[str], str]]
             US Lower-48, Canada and Mexico., be default None
         domainID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the domain., be default None
         region: Optional[Union[list[str], Series[str], str]]
             A defined geographic region within the Americas Gas service. Regions are an aggregation of states or provinces within a country., be default None
         regionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic region., be default None
         subregion: Optional[Union[list[str], Series[str], str]]
             A defined geographic subregion within the Americas Gas service. A substate geography is sometimes referred to as a subregion. Subregions are an aggregation of specific counties within a region and a country., be default None
         subregionID: Optional[Union[list[str], Series[str], str]]
             A unique identification number for the geographic subregion., be default None
         geographyPov: Optional[Union[list[str], Series[str], str]]
             Geography point of view based on geographic heirarchy of country, region, subregion, substate, or special area., be default None
         geographyPovID: Optional[Union[list[str], Series[str], str]]
             An ID for the geography point of view., be default None
         geographyType: Optional[Union[list[str], Series[str], str]]
             Geography type for the point of view based on geographic hierarchy of country, region, subregion, substate, or special area., be default None
         modelID: Optional[Union[list[str], Series[str], str]]
             Internal use, Model ID value., be default None
         workingCapacity: Optional[Union[list[str], Series[str], str]]
             Working storage capacity of a given geography based state level aggregations of EIA or other reported benchmarks., be default None
         utilization: Optional[Union[list[str], Series[str], str]]
             Utilization rate in decimal form or in percentage terms. Utilization is calculated by dividing the volume by its working capacity., be default None
         uom: Optional[Union[list[str], Series[str], str]]
             Unit of measure., be default None
         volume: Optional[Union[list[str], Series[str], str]]
             Volume., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("flowDate", flowDate))
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        filter_params.append(list_to_filter("dateFrequency", dateFrequency))
        filter_params.append(list_to_filter("dateFrequencyDesc", dateFrequencyDesc))
        filter_params.append(list_to_filter("source", source))
        filter_params.append(list_to_filter("viewType", viewType))
        filter_params.append(list_to_filter("viewTypeID", viewTypeID))
        filter_params.append(list_to_filter("valueType", valueType))
        filter_params.append(list_to_filter("valueTypeID", valueTypeID))
        filter_params.append(list_to_filter("domain", domain))
        filter_params.append(list_to_filter("domainID", domainID))
        filter_params.append(list_to_filter("region", region))
        filter_params.append(list_to_filter("regionID", regionID))
        filter_params.append(list_to_filter("subregion", subregion))
        filter_params.append(list_to_filter("subregionID", subregionID))
        filter_params.append(list_to_filter("geographyPov", geographyPov))
        filter_params.append(list_to_filter("geographyPovID", geographyPovID))
        filter_params.append(list_to_filter("geographyType", geographyType))
        filter_params.append(list_to_filter("modelID", modelID))
        filter_params.append(list_to_filter("workingCapacity", workingCapacity))
        filter_params.append(list_to_filter("utilization", utilization))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("volume", volume))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/storage-data",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_americasgas_pipeline_storage_projects(
        self, projectName: Optional[Union[list[str], Series[str], str]] = None, companyName: Optional[Union[list[str], Series[str], str]] = None, companyID: Optional[Union[list[str], Series[str], str]] = None, infrastructureType: Optional[Union[list[str], Series[str], str]] = None, projectID: Optional[Union[list[str], Series[str], str]] = None, storageFieldName: Optional[Union[list[str], Series[str], str]] = None, storageFieldType: Optional[Union[list[str], Series[str], str]] = None, projectType: Optional[Union[list[str], Series[str], str]] = None, projectSource: Optional[Union[list[str], Series[str], str]] = None, capacity: Optional[Union[list[str], Series[str], str]] = None, uom: Optional[Union[list[str], Series[str], str]] = None, inServiceDate: Optional[Union[list[date], Series[date], date]] = None, inServiceYear: Optional[Union[list[str], Series[str], str]] = None, inserviceQuarter: Optional[Union[list[str], Series[str], str]] = None, projectCreatedDate: Optional[Union[list[date], Series[date], date]] = None, projectUpdatedDate: Optional[Union[list[date], Series[date], date]] = None, preFileDate: Optional[Union[list[date], Series[date], date]] = None, projectFileDate: Optional[Union[list[date], Series[date], date]] = None, projectApprovalDate: Optional[Union[list[date], Series[date], date]] = None, productionEnabling: Optional[Union[list[str], Series[str], str]] = None, playWhereProductionIsEnabled: Optional[Union[list[str], Series[str], str]] = None, additionalProductionEnablingCapacityMMcfd: Optional[Union[list[str], Series[str], str]] = None, lngRelated: Optional[Union[list[str], Series[str], str]] = None, functionServedByPipeline: Optional[Union[list[str], Series[str], str]] = None, nameOfLNGFacilityServed: Optional[Union[list[str], Series[str], str]] = None, capacityAvailableToLNGFacilityMMcfd: Optional[Union[list[str], Series[str], str]] = None, miles: Optional[Union[list[str], Series[str], str]] = None, authority: Optional[Union[list[str], Series[str], str]] = None, regulatoryDocumentIdentifier: Optional[Union[list[str], Series[str], str]] = None, projectIsActive: Optional[Union[list[str], Series[str], str]] = None, fromDomain: Optional[Union[list[str], Series[str], str]] = None, fromDomainID: Optional[Union[list[str], Series[str], str]] = None, toDomain: Optional[Union[list[str], Series[str], str]] = None, toDomainID: Optional[Union[list[str], Series[str], str]] = None, fromStateName: Optional[Union[list[str], Series[str], str]] = None, fromStateID: Optional[Union[list[str], Series[str], str]] = None, toStateName: Optional[Union[list[str], Series[str], str]] = None, toStateID: Optional[Union[list[str], Series[str], str]] = None, fromCounty: Optional[Union[list[str], Series[str], str]] = None, fromCountyID: Optional[Union[list[str], Series[str], str]] = None, toCounty: Optional[Union[list[str], Series[str], str]] = None, toCountyID: Optional[Union[list[str], Series[str], str]] = None, flowPathStates: Optional[Union[list[str], Series[str], str]] = None, regionStart: Optional[Union[list[str], Series[str], str]] = None, regionStartID: Optional[Union[list[str], Series[str], str]] = None, regionEnd: Optional[Union[list[str], Series[str], str]] = None, regionEndID: Optional[Union[list[str], Series[str], str]] = None, subRegionStart: Optional[Union[list[str], Series[str], str]] = None, subRegionStartID: Optional[Union[list[str], Series[str], str]] = None, subRegionEnd: Optional[Union[list[str], Series[str], str]] = None, subRegionEndID: Optional[Union[list[str], Series[str], str]] = None, pipelineProjectEstimatedCostThousandUSD: Optional[Union[list[str], Series[str], str]] = None, rateUSDDth: Optional[Union[list[str], Series[str], str]] = None, commRateUSDDth: Optional[Union[list[str], Series[str], str]] = None, createdBy: Optional[Union[list[str], Series[str], str]] = None, modifiedBy: Optional[Union[list[str], Series[str], str]] = None, createDate: Optional[Union[list[str], Series[str], str]] = None, lastModifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         projectName: Optional[Union[list[str], Series[str], str]]
             The name of the project as it is displayed on Platts Connect., be default None
         companyName: Optional[Union[list[str], Series[str], str]]
             The name of the project's company or related pipeline name., be default None
         companyID: Optional[Union[list[str], Series[str], str]]
             An ID sourced from the legacy Bentek service used to identify the connecting business or company name of a meter., be default None
         infrastructureType: Optional[Union[list[str], Series[str], str]]
             The name of the type of project- Pipeline, LNG facility or Storage., be default None
         projectID: Optional[Union[list[str], Series[str], str]]
             The integer project id for the project., be default None
         storageFieldName: Optional[Union[list[str], Series[str], str]]
             The storage field name where the project is located., be default None
         storageFieldType: Optional[Union[list[str], Series[str], str]]
             The type of storage field. When applicable, the name will align to EIA-191., be default None
         projectType: Optional[Union[list[str], Series[str], str]]
             The project type description such as New Pipeline, Expansion, Compression, Reversal, Active facility expansion among many others., be default None
         projectSource: Optional[Union[list[str], Series[str], str]]
             Where information about the project was collected., be default None
         capacity: Optional[Union[list[str], Series[str], str]]
             The capacity of the project- How much gas can be transported or stored., be default None
         uom: Optional[Union[list[str], Series[str], str]]
             The unit of measure for gas- in this case MMcf or MMcf/d., be default None
         inServiceDate: Optional[Union[list[date], Series[date], date]]
             The date the project was put in service by the company., be default None
         inServiceYear: Optional[Union[list[str], Series[str], str]]
             The year the project started service., be default None
         inserviceQuarter: Optional[Union[list[str], Series[str], str]]
             The in-service quarter of the project., be default None
         projectCreatedDate: Optional[Union[list[date], Series[date], date]]
             The create date of the project record., be default None
         projectUpdatedDate: Optional[Union[list[date], Series[date], date]]
             Date of the last update of the project record., be default None
         preFileDate: Optional[Union[list[date], Series[date], date]]
             The date the project pre-filed with the regulatory authority., be default None
         projectFileDate: Optional[Union[list[date], Series[date], date]]
             The date when the project filed with the regulatory authority., be default None
         projectApprovalDate: Optional[Union[list[date], Series[date], date]]
             The date the project was approved by the regulatory agency., be default None
         productionEnabling: Optional[Union[list[str], Series[str], str]]
             Indicates whether a project provides an incremental production outlet connecting to downstream markets (i.e., a production-enabling project)., be default None
         playWhereProductionIsEnabled: Optional[Union[list[str], Series[str], str]]
             The production play where the project is located., be default None
         additionalProductionEnablingCapacityMMcfd: Optional[Union[list[str], Series[str], str]]
             For projects classified as production-enabling, the size of the incremental production outlet., be default None
         lngRelated: Optional[Union[list[str], Series[str], str]]
             Is this related to an LNG facility?  Yes or No., be default None
         functionServedByPipeline: Optional[Union[list[str], Series[str], str]]
             The overall function what the project serves to do once built., be default None
         nameOfLNGFacilityServed: Optional[Union[list[str], Series[str], str]]
             The name of the projects primary cutomer., be default None
         capacityAvailableToLNGFacilityMMcfd: Optional[Union[list[str], Series[str], str]]
             The available capacity to the LNG facility in MMcf/d., be default None
         miles: Optional[Union[list[str], Series[str], str]]
             The length of the project in miles., be default None
         authority: Optional[Union[list[str], Series[str], str]]
             The project regulatory authority name., be default None
         regulatoryDocumentIdentifier: Optional[Union[list[str], Series[str], str]]
             The name of the project's regulatory record ID., be default None
         projectIsActive: Optional[Union[list[str], Series[str], str]]
             Is the project active or not- True it should show up on Platts Connect and False it should not show up on Platts Connect., be default None
         fromDomain: Optional[Union[list[str], Series[str], str]]
             The name of the country- US lower 48, Canada and Mexico where the project originates., be default None
         fromDomainID: Optional[Union[list[str], Series[str], str]]
             The integer id of the country- US lower 48, Canada and Mexico where the project originates., be default None
         toDomain: Optional[Union[list[str], Series[str], str]]
             The name of the country- US lower 48, Canada and Mexico where the project terminates., be default None
         toDomainID: Optional[Union[list[str], Series[str], str]]
             The integer id of the country- US lower 48, Canada and Mexico where the project terminates., be default None
         fromStateName: Optional[Union[list[str], Series[str], str]]
             The name of the state where the project originates., be default None
         fromStateID: Optional[Union[list[str], Series[str], str]]
             The integer id of the state where the project originates., be default None
         toStateName: Optional[Union[list[str], Series[str], str]]
             The name of the state where the project terminates., be default None
         toStateID: Optional[Union[list[str], Series[str], str]]
             The integer id of the state where the project terminates., be default None
         fromCounty: Optional[Union[list[str], Series[str], str]]
             The name of the county where the project originates., be default None
         fromCountyID: Optional[Union[list[str], Series[str], str]]
             The integer id of the county where the project originates., be default None
         toCounty: Optional[Union[list[str], Series[str], str]]
             The name of the county where the project terminates., be default None
         toCountyID: Optional[Union[list[str], Series[str], str]]
             The integer id of the county where the project terminates., be default None
         flowPathStates: Optional[Union[list[str], Series[str], str]]
             The abreviated names of the states that the project resides in or exists in as infrastructure., be default None
         regionStart: Optional[Union[list[str], Series[str], str]]
             The name of the region where the project originates., be default None
         regionStartID: Optional[Union[list[str], Series[str], str]]
             The integer id of the region where the project originates., be default None
         regionEnd: Optional[Union[list[str], Series[str], str]]
             The name of the region where the project terminates., be default None
         regionEndID: Optional[Union[list[str], Series[str], str]]
             The integer id of the region where the project terminates., be default None
         subRegionStart: Optional[Union[list[str], Series[str], str]]
             The name of the sub-region where the project originates., be default None
         subRegionStartID: Optional[Union[list[str], Series[str], str]]
             The integer id of the sub-region where the project originates., be default None
         subRegionEnd: Optional[Union[list[str], Series[str], str]]
             The name of the sub-region where the project terminates., be default None
         subRegionEndID: Optional[Union[list[str], Series[str], str]]
             The integer id of the sub-region where the project terminates., be default None
         pipelineProjectEstimatedCostThousandUSD: Optional[Union[list[str], Series[str], str]]
             The estimated cost of the project in thousands- US dollers., be default None
         rateUSDDth: Optional[Union[list[str], Series[str], str]]
             Rate in US dollars per dekatherm., be default None
         commRateUSDDth: Optional[Union[list[str], Series[str], str]]
             Project transportation costs classified as the commodity (usage) rate in USD per Dekatherm = commRateUSDDth Value., be default None
         createdBy: Optional[Union[list[str], Series[str], str]]
             The person who intially created the project record., be default None
         modifiedBy: Optional[Union[list[str], Series[str], str]]
             The individual who modified the record., be default None
         createDate: Optional[Union[list[str], Series[str], str]]
             The date and time stamp of when the record was created., be default None
         lastModifiedDate: Optional[Union[list[str], Series[str], str]]
             Date and time the record was last updated., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("projectName", projectName))
        filter_params.append(list_to_filter("companyName", companyName))
        filter_params.append(list_to_filter("companyID", companyID))
        filter_params.append(list_to_filter("infrastructureType", infrastructureType))
        filter_params.append(list_to_filter("projectID", projectID))
        filter_params.append(list_to_filter("storageFieldName", storageFieldName))
        filter_params.append(list_to_filter("storageFieldType", storageFieldType))
        filter_params.append(list_to_filter("projectType", projectType))
        filter_params.append(list_to_filter("projectSource", projectSource))
        filter_params.append(list_to_filter("capacity", capacity))
        filter_params.append(list_to_filter("uom", uom))
        filter_params.append(list_to_filter("inServiceDate", inServiceDate))
        filter_params.append(list_to_filter("inServiceYear", inServiceYear))
        filter_params.append(list_to_filter("inserviceQuarter", inserviceQuarter))
        filter_params.append(list_to_filter("projectCreatedDate", projectCreatedDate))
        filter_params.append(list_to_filter("projectUpdatedDate", projectUpdatedDate))
        filter_params.append(list_to_filter("preFileDate", preFileDate))
        filter_params.append(list_to_filter("projectFileDate", projectFileDate))
        filter_params.append(list_to_filter("projectApprovalDate", projectApprovalDate))
        filter_params.append(list_to_filter("productionEnabling", productionEnabling))
        filter_params.append(list_to_filter("playWhereProductionIsEnabled", playWhereProductionIsEnabled))
        filter_params.append(list_to_filter("additionalProductionEnablingCapacityMMcfd", additionalProductionEnablingCapacityMMcfd))
        filter_params.append(list_to_filter("lngRelated", lngRelated))
        filter_params.append(list_to_filter("functionServedByPipeline", functionServedByPipeline))
        filter_params.append(list_to_filter("nameOfLNGFacilityServed", nameOfLNGFacilityServed))
        filter_params.append(list_to_filter("capacityAvailableToLNGFacilityMMcfd", capacityAvailableToLNGFacilityMMcfd))
        filter_params.append(list_to_filter("miles", miles))
        filter_params.append(list_to_filter("authority", authority))
        filter_params.append(list_to_filter("regulatoryDocumentIdentifier", regulatoryDocumentIdentifier))
        filter_params.append(list_to_filter("projectIsActive", projectIsActive))
        filter_params.append(list_to_filter("fromDomain", fromDomain))
        filter_params.append(list_to_filter("fromDomainID", fromDomainID))
        filter_params.append(list_to_filter("toDomain", toDomain))
        filter_params.append(list_to_filter("toDomainID", toDomainID))
        filter_params.append(list_to_filter("fromStateName", fromStateName))
        filter_params.append(list_to_filter("fromStateID", fromStateID))
        filter_params.append(list_to_filter("toStateName", toStateName))
        filter_params.append(list_to_filter("toStateID", toStateID))
        filter_params.append(list_to_filter("fromCounty", fromCounty))
        filter_params.append(list_to_filter("fromCountyID", fromCountyID))
        filter_params.append(list_to_filter("toCounty", toCounty))
        filter_params.append(list_to_filter("toCountyID", toCountyID))
        filter_params.append(list_to_filter("flowPathStates", flowPathStates))
        filter_params.append(list_to_filter("regionStart", regionStart))
        filter_params.append(list_to_filter("regionStartID", regionStartID))
        filter_params.append(list_to_filter("regionEnd", regionEnd))
        filter_params.append(list_to_filter("regionEndID", regionEndID))
        filter_params.append(list_to_filter("subRegionStart", subRegionStart))
        filter_params.append(list_to_filter("subRegionStartID", subRegionStartID))
        filter_params.append(list_to_filter("subRegionEnd", subRegionEnd))
        filter_params.append(list_to_filter("subRegionEndID", subRegionEndID))
        filter_params.append(list_to_filter("pipelineProjectEstimatedCostThousandUSD", pipelineProjectEstimatedCostThousandUSD))
        filter_params.append(list_to_filter("rateUSDDth", rateUSDDth))
        filter_params.append(list_to_filter("commRateUSDDth", commRateUSDDth))
        filter_params.append(list_to_filter("createdBy", createdBy))
        filter_params.append(list_to_filter("modifiedBy", modifiedBy))
        filter_params.append(list_to_filter("createDate", createDate))
        filter_params.append(list_to_filter("lastModifiedDate", lastModifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/americas-gas/v1/na-gas/americasgas-pipeline-storage-projects",
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
        
        if "lastModifiedDate" in df.columns:
            df["lastModifiedDate"] = pd.to_datetime(df["lastModifiedDate"])  # type: ignore

        if "flowDate" in df.columns:
            df["flowDate"] = pd.to_datetime(df["flowDate"])  # type: ignore

        if "forecastDate" in df.columns:
            df["forecastDate"] = pd.to_datetime(df["forecastDate"])  # type: ignore

        if "postingDatetime" in df.columns:
            df["postingDatetime"] = pd.to_datetime(df["postingDatetime"])  # type: ignore

        if "createDate" in df.columns:
            df["createDate"] = pd.to_datetime(df["createDate"])  # type: ignore

        if "measurementDate" in df.columns:
            df["measurementDate"] = pd.to_datetime(df["measurementDate"])  # type: ignore

        if "effectiveDate" in df.columns:
            df["effectiveDate"] = pd.to_datetime(df["effectiveDate"])  # type: ignore

        if "endDate" in df.columns:
            df["endDate"] = pd.to_datetime(df["endDate"])  # type: ignore

        if "validFrom" in df.columns:
            df["validFrom"] = pd.to_datetime(df["validFrom"])  # type: ignore

        if "validTo" in df.columns:
            df["validTo"] = pd.to_datetime(df["validTo"])  # type: ignore

        if "dateEffective" in df.columns:
            df["dateEffective"] = pd.to_datetime(df["dateEffective"])  # type: ignore

        if "dateRetire" in df.columns:
            df["dateRetire"] = pd.to_datetime(df["dateRetire"])  # type: ignore

        if "dateIssued" in df.columns:
            df["dateIssued"] = pd.to_datetime(df["dateIssued"])  # type: ignore

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])  # type: ignore

        if "contractStartDate" in df.columns:
            df["contractStartDate"] = pd.to_datetime(df["contractStartDate"])  # type: ignore

        if "contractEndDate" in df.columns:
            df["contractEndDate"] = pd.to_datetime(df["contractEndDate"])  # type: ignore

        if "inServiceDate" in df.columns:
            df["inServiceDate"] = pd.to_datetime(df["inServiceDate"])  # type: ignore

        if "projectCreatedDate" in df.columns:
            df["projectCreatedDate"] = pd.to_datetime(df["projectCreatedDate"])  # type: ignore

        if "projectUpdatedDate" in df.columns:
            df["projectUpdatedDate"] = pd.to_datetime(df["projectUpdatedDate"])  # type: ignore

        if "preFileDate" in df.columns:
            df["preFileDate"] = pd.to_datetime(df["preFileDate"])  # type: ignore

        if "projectFileDate" in df.columns:
            df["projectFileDate"] = pd.to_datetime(df["projectFileDate"])  # type: ignore

        if "projectApprovalDate" in df.columns:
            df["projectApprovalDate"] = pd.to_datetime(df["projectApprovalDate"])  # type: ignore
        return df
    