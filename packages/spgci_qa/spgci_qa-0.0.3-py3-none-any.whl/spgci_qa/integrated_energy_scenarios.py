
from __future__ import annotations
from typing import List, Optional, Union
from requests import Response
from spgci_qa.api_client import get_data
from spgci_qa.utilities import list_to_filter
from pandas import DataFrame, Series
from datetime import date
import pandas as pd

class Integrated_energy_scenarios:
    _endpoint = "api/v1/"
    _reference_endpoint = "reference/v1/"
    _coal_markets_endpoint = "/coal-market"
    _employment_endpoint = "/employment"
    _final_energy_consumption_endpoint = "/final-energy-consumption"
    _gdp_endpoint = "/gdp"
    _ghg_emissions_endpoint = "/ghg-emission"
    _natural_gas_markets_endpoint = "/natural-gas-market"
    _oil_consumption_by_product_endpoint = "/oil-consumption-by-product"
    _oil_consumption_by_sector_endpoint = "/oil-consumption-by-sector"
    _population_by_age_endpoint = "/population-by-age"
    _population_urban_rural_endpoint = "/population-urban-rural"
    _power_markets_by_technology_endpoint = "/power-market-by-technology"
    _power_markets_demand_endpoint = "/power-market-demand"
    _primary_energy_demand_endpoint = "/primary-energy-demand"
    _demand_sector_hierarchy_endpoint = "/hierarchy/demand-sector"
    _geo_hierarchy_endpoint = "/hierarchy/geo"
    _ghg_sector_hierarchy_endpoint = "/hierarchy/ghg-sector"
    _ghg_source_hierarchy_endpoint = "/hierarchy/ghg-source"


    def get_coal_market(
        self, longName: Optional[Union[list[str], Series[str], str]] = None, scenario: Optional[Union[list[str], Series[str], str]] = None, modelVintage: Optional[Union[list[str], Series[str], str]] = None, energyType: Optional[Union[list[str], Series[str], str]] = None, subsector: Optional[Union[list[str], Series[str], str]] = None, theme: Optional[Union[list[str], Series[str], str]] = None, country: Optional[Union[list[str], Series[str], str]] = None, unit: Optional[Union[list[str], Series[str], str]] = None, year: Optional[Union[list[str], Series[str], str]] = None, value: Optional[Union[list[str], Series[str], str]] = None, modifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         longName: Optional[Union[list[str], Series[str], str]]
             Long name for the series., be default None
         scenario: Optional[Union[list[str], Series[str], str]]
             S&P Global's Energy and Climate Scenarios: Green Rules, Discord and Inflections (base planning scenario), and low emission cases: Accelerated CCS and Multitech Mitigation., be default None
         modelVintage: Optional[Union[list[str], Series[str], str]]
             Indicates the year of execution for the forecast model, providing the temporal context of the model's data and assumptions used in generating the forecast results., be default None
         energyType: Optional[Union[list[str], Series[str], str]]
             Set to coal., be default None
         subsector: Optional[Union[list[str], Series[str], str]]
             Coal consumption sectors: power and heat, gas works, own use and other, industry, feedstocks, rail transport, other transport, residential, agricultural, and commercial., be default None
         theme: Optional[Union[list[str], Series[str], str]]
             Set to coal consumption., be default None
         country: Optional[Union[list[str], Series[str], str]]
             Geography for which data is forecast., be default None
         unit: Optional[Union[list[str], Series[str], str]]
             Unit of measurement. Ex: mtoe (million tonnes of oil equivalent), be default None
         year: Optional[Union[list[str], Series[str], str]]
             Forecast year, includes actuals for historic values., be default None
         value: Optional[Union[list[str], Series[str], str]]
             Coal consumption values in million tonnes of oil equivalent., be default None
         modifiedDate: Optional[Union[list[str], Series[str], str]]
             The last modified date for the corresponding record., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("longName", longName))
        filter_params.append(list_to_filter("scenario", scenario))
        filter_params.append(list_to_filter("modelVintage", modelVintage))
        filter_params.append(list_to_filter("energyType", energyType))
        filter_params.append(list_to_filter("subsector", subsector))
        filter_params.append(list_to_filter("theme", theme))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("unit", unit))
        filter_params.append(list_to_filter("year", year))
        filter_params.append(list_to_filter("value", value))
        filter_params.append(list_to_filter("modifiedDate", modifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/carbon-scenarios/ies/v1/coal-market",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_employment(
        self, longName: Optional[Union[list[str], Series[str], str]] = None, scenario: Optional[Union[list[str], Series[str], str]] = None, modelVintage: Optional[Union[list[str], Series[str], str]] = None, series: Optional[Union[list[str], Series[str], str]] = None, theme: Optional[Union[list[str], Series[str], str]] = None, country: Optional[Union[list[str], Series[str], str]] = None, unit: Optional[Union[list[str], Series[str], str]] = None, year: Optional[Union[list[str], Series[str], str]] = None, value: Optional[Union[list[str], Series[str], str]] = None, modifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         longName: Optional[Union[list[str], Series[str], str]]
             Long name for the series., be default None
         scenario: Optional[Union[list[str], Series[str], str]]
             S&P Global's Energy and Climate Scenarios: Green Rules, Discord and Inflections (base planning scenario), and low emission cases: Accelerated CCS and Multitech Mitigation., be default None
         modelVintage: Optional[Union[list[str], Series[str], str]]
             Indicates the year of execution for the forecast model, providing the temporal context of the model's data and assumptions used in generating the forecast results., be default None
         series: Optional[Union[list[str], Series[str], str]]
             Total employment., be default None
         theme: Optional[Union[list[str], Series[str], str]]
             Set to employment., be default None
         country: Optional[Union[list[str], Series[str], str]]
             Geography for which data is forecast., be default None
         unit: Optional[Union[list[str], Series[str], str]]
             Unit of measurement. Ex: million, be default None
         year: Optional[Union[list[str], Series[str], str]]
             Forecast year, includes actuals for historic values., be default None
         value: Optional[Union[list[str], Series[str], str]]
             Values in million persons., be default None
         modifiedDate: Optional[Union[list[str], Series[str], str]]
             The last modified date for the corresponding record., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("longName", longName))
        filter_params.append(list_to_filter("scenario", scenario))
        filter_params.append(list_to_filter("modelVintage", modelVintage))
        filter_params.append(list_to_filter("series", series))
        filter_params.append(list_to_filter("theme", theme))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("unit", unit))
        filter_params.append(list_to_filter("year", year))
        filter_params.append(list_to_filter("value", value))
        filter_params.append(list_to_filter("modifiedDate", modifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/carbon-scenarios/ies/v1/employment",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_final_energy_consumption(
        self, longName: Optional[Union[list[str], Series[str], str]] = None, scenario: Optional[Union[list[str], Series[str], str]] = None, modelVintage: Optional[Union[list[str], Series[str], str]] = None, energyType: Optional[Union[list[str], Series[str], str]] = None, subsector: Optional[Union[list[str], Series[str], str]] = None, theme: Optional[Union[list[str], Series[str], str]] = None, country: Optional[Union[list[str], Series[str], str]] = None, unit: Optional[Union[list[str], Series[str], str]] = None, year: Optional[Union[list[str], Series[str], str]] = None, value: Optional[Union[list[str], Series[str], str]] = None, modifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         longName: Optional[Union[list[str], Series[str], str]]
             Long name for the series., be default None
         scenario: Optional[Union[list[str], Series[str], str]]
             S&P Global's Energy and Climate Scenarios: Green Rules, Discord and Inflections (base planning scenario), and low emission cases: Accelerated CCS and Multitech Mitigation., be default None
         modelVintage: Optional[Union[list[str], Series[str], str]]
             Indicates the year of execution for the forecast model, providing the temporal context of the model's data and assumptions used in generating the forecast results., be default None
         energyType: Optional[Union[list[str], Series[str], str]]
             Energy types: electricity, oil, natural gas, coal, hydrogen, and other energy., be default None
         subsector: Optional[Union[list[str], Series[str], str]]
             Final energy consumption sectors: residential, agricultural, commercial, industry, feedstocks, road transport, rail transport, aviation transport, shipping transport, and other transport., be default None
         theme: Optional[Union[list[str], Series[str], str]]
             Set to final energy consumption., be default None
         country: Optional[Union[list[str], Series[str], str]]
             Geography for which data is forecast., be default None
         unit: Optional[Union[list[str], Series[str], str]]
             Unit of measurement. Ex: mtoe (million tonnes of oil equivalent), be default None
         year: Optional[Union[list[str], Series[str], str]]
             Forecast year, includes actuals for historic values., be default None
         value: Optional[Union[list[str], Series[str], str]]
             Energy consumption by sector values in million tonnes of oil equivalent., be default None
         modifiedDate: Optional[Union[list[str], Series[str], str]]
             The last modified date for the corresponding record., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("longName", longName))
        filter_params.append(list_to_filter("scenario", scenario))
        filter_params.append(list_to_filter("modelVintage", modelVintage))
        filter_params.append(list_to_filter("energyType", energyType))
        filter_params.append(list_to_filter("subsector", subsector))
        filter_params.append(list_to_filter("theme", theme))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("unit", unit))
        filter_params.append(list_to_filter("year", year))
        filter_params.append(list_to_filter("value", value))
        filter_params.append(list_to_filter("modifiedDate", modifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/carbon-scenarios/ies/v1/final-energy-consumption",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_gdp(
        self, longName: Optional[Union[list[str], Series[str], str]] = None, scenario: Optional[Union[list[str], Series[str], str]] = None, modelVintage: Optional[Union[list[str], Series[str], str]] = None, theme: Optional[Union[list[str], Series[str], str]] = None, country: Optional[Union[list[str], Series[str], str]] = None, unit: Optional[Union[list[str], Series[str], str]] = None, year: Optional[Union[list[str], Series[str], str]] = None, value: Optional[Union[list[str], Series[str], str]] = None, modifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         longName: Optional[Union[list[str], Series[str], str]]
             Long name for the series., be default None
         scenario: Optional[Union[list[str], Series[str], str]]
             S&P Global's Energy and Climate Scenarios: Green Rules, Discord and Inflections (base planning scenario), and low emission cases: Accelerated CCS and Multitech Mitigation., be default None
         modelVintage: Optional[Union[list[str], Series[str], str]]
             Indicates the year of execution for the forecast model, providing the temporal context of the model's data and assumptions used in generating the forecast results., be default None
         theme: Optional[Union[list[str], Series[str], str]]
             Options available: real GDP, real GDP PPP basis, nominal GDP, nominal GDP PPP basis., be default None
         country: Optional[Union[list[str], Series[str], str]]
             Geography for which data is forecast., be default None
         unit: Optional[Union[list[str], Series[str], str]]
             Unit of measurement. Ex: billion real US dollars, billion nominal US dollars, be default None
         year: Optional[Union[list[str], Series[str], str]]
             Forecast year, includes actuals for historic values., be default None
         value: Optional[Union[list[str], Series[str], str]]
             GDP forecast value in billion real US dollars and in billion nominal US dollars., be default None
         modifiedDate: Optional[Union[list[str], Series[str], str]]
             The last modified date for the corresponding record., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("longName", longName))
        filter_params.append(list_to_filter("scenario", scenario))
        filter_params.append(list_to_filter("modelVintage", modelVintage))
        filter_params.append(list_to_filter("theme", theme))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("unit", unit))
        filter_params.append(list_to_filter("year", year))
        filter_params.append(list_to_filter("value", value))
        filter_params.append(list_to_filter("modifiedDate", modifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/carbon-scenarios/ies/v1/gdp",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_ghg_emission(
        self, longName: Optional[Union[list[str], Series[str], str]] = None, scenario: Optional[Union[list[str], Series[str], str]] = None, modelVintage: Optional[Union[list[str], Series[str], str]] = None, ccusSavings: Optional[Union[list[str], Series[str], str]] = None, sector: Optional[Union[list[str], Series[str], str]] = None, sourceOfEmissions: Optional[Union[list[str], Series[str], str]] = None, theme: Optional[Union[list[str], Series[str], str]] = None, country: Optional[Union[list[str], Series[str], str]] = None, unit: Optional[Union[list[str], Series[str], str]] = None, year: Optional[Union[list[str], Series[str], str]] = None, value: Optional[Union[list[str], Series[str], str]] = None, modifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         longName: Optional[Union[list[str], Series[str], str]]
             Long name for the series., be default None
         scenario: Optional[Union[list[str], Series[str], str]]
             S&P Global's Energy and Climate Scenarios: Green Rules, Discord and Inflections (base planning scenario), and low emission cases: Accelerated CCS and Multitech Mitigation., be default None
         modelVintage: Optional[Union[list[str], Series[str], str]]
             Indicates the year of execution for the forecast model, providing the temporal context of the model's data and assumptions used in generating the forecast results., be default None
         ccusSavings: Optional[Union[list[str], Series[str], str]]
             Carbon capture, utilization, and storage (CCUS). Options available: including CCUS, excluding CCUS, and CCUS savings., be default None
         sector: Optional[Union[list[str], Series[str], str]]
             Sectors: power generation, district heating, refining, other sectors, residential, agricultural, commercial, industry, road and rail transport, international and domestic aviation and shipping transport, other transport, coke ovens, hydrogen generation, and non-energy from waste-related, agricultural, LULUCF, industrial processes and geo-engineering., be default None
         sourceOfEmissions: Optional[Union[list[str], Series[str], str]]
             Source of emissions: oil, natural gas, coal, biomass, undefined and non-energy., be default None
         theme: Optional[Union[list[str], Series[str], str]]
             Set to GHG emissions., be default None
         country: Optional[Union[list[str], Series[str], str]]
             Geography for which data is forecast., be default None
         unit: Optional[Union[list[str], Series[str], str]]
             Unit of measurement. Ex: million tonnes of CO2 equivalent, be default None
         year: Optional[Union[list[str], Series[str], str]]
             Forecast year, includes actuals for historic values., be default None
         value: Optional[Union[list[str], Series[str], str]]
             Emissions volumes in million tonnes of CO2 equivalent., be default None
         modifiedDate: Optional[Union[list[str], Series[str], str]]
             The last modified date for the corresponding record., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("longName", longName))
        filter_params.append(list_to_filter("scenario", scenario))
        filter_params.append(list_to_filter("modelVintage", modelVintage))
        filter_params.append(list_to_filter("ccusSavings", ccusSavings))
        filter_params.append(list_to_filter("sector", sector))
        filter_params.append(list_to_filter("sourceOfEmissions", sourceOfEmissions))
        filter_params.append(list_to_filter("theme", theme))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("unit", unit))
        filter_params.append(list_to_filter("year", year))
        filter_params.append(list_to_filter("value", value))
        filter_params.append(list_to_filter("modifiedDate", modifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/carbon-scenarios/ies/v1/ghg-emission",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_natural_gas_market(
        self, longName: Optional[Union[list[str], Series[str], str]] = None, scenario: Optional[Union[list[str], Series[str], str]] = None, modelVintage: Optional[Union[list[str], Series[str], str]] = None, energyType: Optional[Union[list[str], Series[str], str]] = None, subsector: Optional[Union[list[str], Series[str], str]] = None, theme: Optional[Union[list[str], Series[str], str]] = None, country: Optional[Union[list[str], Series[str], str]] = None, unit: Optional[Union[list[str], Series[str], str]] = None, year: Optional[Union[list[str], Series[str], str]] = None, value: Optional[Union[list[str], Series[str], str]] = None, modifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         longName: Optional[Union[list[str], Series[str], str]]
             Long name for the series., be default None
         scenario: Optional[Union[list[str], Series[str], str]]
             S&P Global's Energy and Climate Scenarios: Green Rules, Discord and Inflections (base planning scenario), and low emission cases: Accelerated CCS and Multitech Mitigation., be default None
         modelVintage: Optional[Union[list[str], Series[str], str]]
             Indicates the year of execution for the forecast model, providing the temporal context of the model's data and assumptions used in generating the forecast results., be default None
         energyType: Optional[Union[list[str], Series[str], str]]
             Set to natural gas., be default None
         subsector: Optional[Union[list[str], Series[str], str]]
             Natural gas consumption sectors: power and heat, own use and other, industry, feedstocks, road transport, rail transport, shipping transport, other transport, residential, agricultural, and commercial., be default None
         theme: Optional[Union[list[str], Series[str], str]]
             Set to natural gas consumption., be default None
         country: Optional[Union[list[str], Series[str], str]]
             Geography for which data is forecast., be default None
         unit: Optional[Union[list[str], Series[str], str]]
             Unit of measurement. Ex: mtoe (million tonnes of oil equivalent), be default None
         year: Optional[Union[list[str], Series[str], str]]
             Forecast year, includes actuals for historic values., be default None
         value: Optional[Union[list[str], Series[str], str]]
             Natural gas consumption values in million tonnes of oil equivalent., be default None
         modifiedDate: Optional[Union[list[str], Series[str], str]]
             The last modified date for the corresponding record., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("longName", longName))
        filter_params.append(list_to_filter("scenario", scenario))
        filter_params.append(list_to_filter("modelVintage", modelVintage))
        filter_params.append(list_to_filter("energyType", energyType))
        filter_params.append(list_to_filter("subsector", subsector))
        filter_params.append(list_to_filter("theme", theme))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("unit", unit))
        filter_params.append(list_to_filter("year", year))
        filter_params.append(list_to_filter("value", value))
        filter_params.append(list_to_filter("modifiedDate", modifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/carbon-scenarios/ies/v1/natural-gas-market",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_oil_consumption_by_product(
        self, longName: Optional[Union[list[str], Series[str], str]] = None, scenario: Optional[Union[list[str], Series[str], str]] = None, modelVintage: Optional[Union[list[str], Series[str], str]] = None, energyType: Optional[Union[list[str], Series[str], str]] = None, flow: Optional[Union[list[str], Series[str], str]] = None, theme: Optional[Union[list[str], Series[str], str]] = None, country: Optional[Union[list[str], Series[str], str]] = None, unit: Optional[Union[list[str], Series[str], str]] = None, year: Optional[Union[list[str], Series[str], str]] = None, value: Optional[Union[list[str], Series[str], str]] = None, modifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         longName: Optional[Union[list[str], Series[str], str]]
             Long name for the series., be default None
         scenario: Optional[Union[list[str], Series[str], str]]
             S&P Global's Energy and Climate Scenarios: Green Rules, Discord and Inflections (base planning scenario), and low emission cases: Accelerated CCS and Multitech Mitigation., be default None
         modelVintage: Optional[Union[list[str], Series[str], str]]
             Indicates the year of execution for the forecast model, providing the temporal context of the model's data and assumptions used in generating the forecast results., be default None
         energyType: Optional[Union[list[str], Series[str], str]]
             Energy products: gasoline, aviation gasoline, gas diesel oil, residual fuel oil, liquefied petroleum gas, jet fuel, kerosene, naphtha, other liquids, crude oil (direct), and refinery losses and adjustments., be default None
         flow: Optional[Union[list[str], Series[str], str]]
             Set to total consumption., be default None
         theme: Optional[Union[list[str], Series[str], str]]
             Set to total oil liquids consumption by product., be default None
         country: Optional[Union[list[str], Series[str], str]]
             Geography for which data is forecast., be default None
         unit: Optional[Union[list[str], Series[str], str]]
             Unit of measurement. Ex: kbbld (thousand barrels per day) , mtoe (million tonnes of oil equivalent), be default None
         year: Optional[Union[list[str], Series[str], str]]
             Forecast year, includes actuals for historic values., be default None
         value: Optional[Union[list[str], Series[str], str]]
             Oil consumption by product values in thousand barrels per day and in million tonnes of oil equivalent., be default None
         modifiedDate: Optional[Union[list[str], Series[str], str]]
             The last modified date for the corresponding record., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("longName", longName))
        filter_params.append(list_to_filter("scenario", scenario))
        filter_params.append(list_to_filter("modelVintage", modelVintage))
        filter_params.append(list_to_filter("energyType", energyType))
        filter_params.append(list_to_filter("flow", flow))
        filter_params.append(list_to_filter("theme", theme))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("unit", unit))
        filter_params.append(list_to_filter("year", year))
        filter_params.append(list_to_filter("value", value))
        filter_params.append(list_to_filter("modifiedDate", modifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/carbon-scenarios/ies/v1/oil-consumption-by-product",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_oil_consumption_by_sector(
        self, longName: Optional[Union[list[str], Series[str], str]] = None, scenario: Optional[Union[list[str], Series[str], str]] = None, modelVintage: Optional[Union[list[str], Series[str], str]] = None, energyType: Optional[Union[list[str], Series[str], str]] = None, subsector: Optional[Union[list[str], Series[str], str]] = None, theme: Optional[Union[list[str], Series[str], str]] = None, country: Optional[Union[list[str], Series[str], str]] = None, unit: Optional[Union[list[str], Series[str], str]] = None, year: Optional[Union[list[str], Series[str], str]] = None, value: Optional[Union[list[str], Series[str], str]] = None, modifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         longName: Optional[Union[list[str], Series[str], str]]
             Long name for the series., be default None
         scenario: Optional[Union[list[str], Series[str], str]]
             S&P Global's Energy and Climate Scenarios: Green Rules, Discord and Inflections (base planning scenario), and low emission cases: Accelerated CCS and Multitech Mitigation., be default None
         modelVintage: Optional[Union[list[str], Series[str], str]]
             Indicates the year of execution for the forecast model, providing the temporal context of the model's data and assumptions used in generating the forecast results., be default None
         energyType: Optional[Union[list[str], Series[str], str]]
             Set to total oil liquids., be default None
         subsector: Optional[Union[list[str], Series[str], str]]
             Oil consumption sectors: residential, commercial, agricultural, industry, feedstocks, road transport, aviation transport, rail transport, shipping transport, other transport, power and heat, refinery, own use and other, and refinery losses and adjustments., be default None
         theme: Optional[Union[list[str], Series[str], str]]
             Set to total oil liquids consumption by sector., be default None
         country: Optional[Union[list[str], Series[str], str]]
             Geography for which data is forecast., be default None
         unit: Optional[Union[list[str], Series[str], str]]
             Unit of measurement. Ex: kbbld (thousand barrels per day) , mtoe (million tonnes of oil equivalent), be default None
         year: Optional[Union[list[str], Series[str], str]]
             Forecast year, includes actuals for historic values., be default None
         value: Optional[Union[list[str], Series[str], str]]
             Oil consumption by sector values in thousand barrels per day and in million tonnes of oil equivalent., be default None
         modifiedDate: Optional[Union[list[str], Series[str], str]]
             The last modified date for the corresponding record., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("longName", longName))
        filter_params.append(list_to_filter("scenario", scenario))
        filter_params.append(list_to_filter("modelVintage", modelVintage))
        filter_params.append(list_to_filter("energyType", energyType))
        filter_params.append(list_to_filter("subsector", subsector))
        filter_params.append(list_to_filter("theme", theme))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("unit", unit))
        filter_params.append(list_to_filter("year", year))
        filter_params.append(list_to_filter("value", value))
        filter_params.append(list_to_filter("modifiedDate", modifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/carbon-scenarios/ies/v1/oil-consumption-by-sector",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_population_by_age(
        self, longName: Optional[Union[list[str], Series[str], str]] = None, scenario: Optional[Union[list[str], Series[str], str]] = None, modelVintage: Optional[Union[list[str], Series[str], str]] = None, series: Optional[Union[list[str], Series[str], str]] = None, theme: Optional[Union[list[str], Series[str], str]] = None, country: Optional[Union[list[str], Series[str], str]] = None, unit: Optional[Union[list[str], Series[str], str]] = None, year: Optional[Union[list[str], Series[str], str]] = None, value: Optional[Union[list[str], Series[str], str]] = None, modifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         longName: Optional[Union[list[str], Series[str], str]]
             Long name for the series., be default None
         scenario: Optional[Union[list[str], Series[str], str]]
             S&P Global's Energy and Climate Scenarios: Green Rules, Discord and Inflections (base planning scenario), and low emission cases: Accelerated CCS and Multitech Mitigation., be default None
         modelVintage: Optional[Union[list[str], Series[str], str]]
             Indicates the year of execution for the forecast model, providing the temporal context of the model's data and assumptions used in generating the forecast results., be default None
         series: Optional[Union[list[str], Series[str], str]]
             Age groups: age 0-14 (youth), age 15-64 (working age), age 64+ (older)., be default None
         theme: Optional[Union[list[str], Series[str], str]]
             Set to population by age group., be default None
         country: Optional[Union[list[str], Series[str], str]]
             Geography for which data is forecast., be default None
         unit: Optional[Union[list[str], Series[str], str]]
             Unit of measurement. Ex: million persons., be default None
         year: Optional[Union[list[str], Series[str], str]]
             Forecast year, includes actuals for historic values., be default None
         value: Optional[Union[list[str], Series[str], str]]
             Values in million persons., be default None
         modifiedDate: Optional[Union[list[str], Series[str], str]]
             The last modified date for the corresponding record., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("longName", longName))
        filter_params.append(list_to_filter("scenario", scenario))
        filter_params.append(list_to_filter("modelVintage", modelVintage))
        filter_params.append(list_to_filter("series", series))
        filter_params.append(list_to_filter("theme", theme))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("unit", unit))
        filter_params.append(list_to_filter("year", year))
        filter_params.append(list_to_filter("value", value))
        filter_params.append(list_to_filter("modifiedDate", modifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/carbon-scenarios/ies/v1/population-by-age",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_population_urban_rural(
        self, longName: Optional[Union[list[str], Series[str], str]] = None, scenario: Optional[Union[list[str], Series[str], str]] = None, modelVintage: Optional[Union[list[str], Series[str], str]] = None, series: Optional[Union[list[str], Series[str], str]] = None, theme: Optional[Union[list[str], Series[str], str]] = None, country: Optional[Union[list[str], Series[str], str]] = None, unit: Optional[Union[list[str], Series[str], str]] = None, year: Optional[Union[list[str], Series[str], str]] = None, value: Optional[Union[list[str], Series[str], str]] = None, modifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         longName: Optional[Union[list[str], Series[str], str]]
             Long name for the series., be default None
         scenario: Optional[Union[list[str], Series[str], str]]
             S&P Global's Energy and Climate Scenarios: Green Rules, Discord and Inflections (base planning scenario), and low emission cases: Accelerated CCS and Multitech Mitigation., be default None
         modelVintage: Optional[Union[list[str], Series[str], str]]
             Indicates the year of execution for the forecast model, providing the temporal context of the model's data and assumptions used in generating the forecast results., be default None
         series: Optional[Union[list[str], Series[str], str]]
             Urban or rural population., be default None
         theme: Optional[Union[list[str], Series[str], str]]
             Set to population - urban and rural., be default None
         country: Optional[Union[list[str], Series[str], str]]
             Geography for which data is forecast., be default None
         unit: Optional[Union[list[str], Series[str], str]]
             Unit of measurement. Ex: million persons., be default None
         year: Optional[Union[list[str], Series[str], str]]
             Forecast year, includes actuals for historic values., be default None
         value: Optional[Union[list[str], Series[str], str]]
             Values in million persons., be default None
         modifiedDate: Optional[Union[list[str], Series[str], str]]
             The last modified date for the corresponding record., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("longName", longName))
        filter_params.append(list_to_filter("scenario", scenario))
        filter_params.append(list_to_filter("modelVintage", modelVintage))
        filter_params.append(list_to_filter("series", series))
        filter_params.append(list_to_filter("theme", theme))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("unit", unit))
        filter_params.append(list_to_filter("year", year))
        filter_params.append(list_to_filter("value", value))
        filter_params.append(list_to_filter("modifiedDate", modifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/carbon-scenarios/ies/v1/population-urban-rural",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_power_market_by_technology(
        self, longName: Optional[Union[list[str], Series[str], str]] = None, scenario: Optional[Union[list[str], Series[str], str]] = None, modelVintage: Optional[Union[list[str], Series[str], str]] = None, energyOrTechnologyType: Optional[Union[list[str], Series[str], str]] = None, theme: Optional[Union[list[str], Series[str], str]] = None, country: Optional[Union[list[str], Series[str], str]] = None, unit: Optional[Union[list[str], Series[str], str]] = None, year: Optional[Union[list[str], Series[str], str]] = None, value: Optional[Union[list[str], Series[str], str]] = None, modifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         longName: Optional[Union[list[str], Series[str], str]]
             Long name for the series., be default None
         scenario: Optional[Union[list[str], Series[str], str]]
             S&P Global's Energy and Climate Scenarios: Green Rules, Discord and Inflections (base planning scenario), and low emission cases: Accelerated CCS and Multitech Mitigation., be default None
         modelVintage: Optional[Union[list[str], Series[str], str]]
             Indicates the year of execution for the forecast model, providing the temporal context of the model's data and assumptions used in generating the forecast results., be default None
         energyOrTechnologyType: Optional[Union[list[str], Series[str], str]]
             Technology types: coal, natural gas, oil, hydro, nuclear, onshore wind, offshore wind, solar PV, solar CSP, geothermal, biomass and waste, tidal, battery storage, and hydrogen fuel cells., be default None
         theme: Optional[Union[list[str], Series[str], str]]
             Options available: installed capacity, fuel input into power generation, electricity generated, capacity net additions, capacity additions, capacity retirements., be default None
         country: Optional[Union[list[str], Series[str], str]]
             Geography for which data is forecast., be default None
         unit: Optional[Union[list[str], Series[str], str]]
             Unit of measurement. Ex: GW (gigawatt), mtoe (million tonnes of oil equivalent), TWh (terrawatt-hours), be default None
         year: Optional[Union[list[str], Series[str], str]]
             Forecast year, includes actuals for historic values., be default None
         value: Optional[Union[list[str], Series[str], str]]
             Various power generation related values in gigawatt, in million tonnes of oil equivalent, and in terrawatt-hours respectively., be default None
         modifiedDate: Optional[Union[list[str], Series[str], str]]
             The last modified date for the corresponding record., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("longName", longName))
        filter_params.append(list_to_filter("scenario", scenario))
        filter_params.append(list_to_filter("modelVintage", modelVintage))
        filter_params.append(list_to_filter("energyOrTechnologyType", energyOrTechnologyType))
        filter_params.append(list_to_filter("theme", theme))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("unit", unit))
        filter_params.append(list_to_filter("year", year))
        filter_params.append(list_to_filter("value", value))
        filter_params.append(list_to_filter("modifiedDate", modifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/carbon-scenarios/ies/v1/power-market-by-technology",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_power_market_demand(
        self, longName: Optional[Union[list[str], Series[str], str]] = None, scenario: Optional[Union[list[str], Series[str], str]] = None, modelVintage: Optional[Union[list[str], Series[str], str]] = None, subsector: Optional[Union[list[str], Series[str], str]] = None, theme: Optional[Union[list[str], Series[str], str]] = None, country: Optional[Union[list[str], Series[str], str]] = None, unit: Optional[Union[list[str], Series[str], str]] = None, year: Optional[Union[list[str], Series[str], str]] = None, value: Optional[Union[list[str], Series[str], str]] = None, modifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         longName: Optional[Union[list[str], Series[str], str]]
             Long name for the series., be default None
         scenario: Optional[Union[list[str], Series[str], str]]
             S&P Global's Energy and Climate Scenarios: Green Rules, Discord and Inflections (base planning scenario), and low emission cases: Accelerated CCS and Multitech Mitigation., be default None
         modelVintage: Optional[Union[list[str], Series[str], str]]
             Indicates the year of execution for the forecast model, providing the temporal context of the model's data and assumptions used in generating the forecast results., be default None
         subsector: Optional[Union[list[str], Series[str], str]]
             Total consumption., be default None
         theme: Optional[Union[list[str], Series[str], str]]
             Set to electricity demand by sector., be default None
         country: Optional[Union[list[str], Series[str], str]]
             Geography for which data is forecast., be default None
         unit: Optional[Union[list[str], Series[str], str]]
             Unit of measurement. Ex: mtoe (million tonnes of oil equivalent), be default None
         year: Optional[Union[list[str], Series[str], str]]
             Forecast year, includes actuals for historic values., be default None
         value: Optional[Union[list[str], Series[str], str]]
             Power demand by sector values in million tonnes of oil equivalent., be default None
         modifiedDate: Optional[Union[list[str], Series[str], str]]
             The last modified date for the corresponding record., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("longName", longName))
        filter_params.append(list_to_filter("scenario", scenario))
        filter_params.append(list_to_filter("modelVintage", modelVintage))
        filter_params.append(list_to_filter("subsector", subsector))
        filter_params.append(list_to_filter("theme", theme))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("unit", unit))
        filter_params.append(list_to_filter("year", year))
        filter_params.append(list_to_filter("value", value))
        filter_params.append(list_to_filter("modifiedDate", modifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/carbon-scenarios/ies/v1/power-market-demand",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_primary_energy_demand(
        self, longName: Optional[Union[list[str], Series[str], str]] = None, scenario: Optional[Union[list[str], Series[str], str]] = None, modelVintage: Optional[Union[list[str], Series[str], str]] = None, energyType: Optional[Union[list[str], Series[str], str]] = None, theme: Optional[Union[list[str], Series[str], str]] = None, country: Optional[Union[list[str], Series[str], str]] = None, unit: Optional[Union[list[str], Series[str], str]] = None, year: Optional[Union[list[str], Series[str], str]] = None, value: Optional[Union[list[str], Series[str], str]] = None, modifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         longName: Optional[Union[list[str], Series[str], str]]
             Long name for the series., be default None
         scenario: Optional[Union[list[str], Series[str], str]]
             S&P Global's Energy and Climate Scenarios: Green Rules, Discord and Inflections (base planning scenario), and low emission cases: Accelerated CCS and Multitech Mitigation., be default None
         modelVintage: Optional[Union[list[str], Series[str], str]]
             Indicates the year of execution for the forecast model, providing the temporal context of the model's data and assumptions used in generating the forecast results., be default None
         energyType: Optional[Union[list[str], Series[str], str]]
             Energy types: oil, natural gas, coal, hydro, nuclear, wind, solar, other renewables, traditional biomass, modern biomass, and other energy., be default None
         theme: Optional[Union[list[str], Series[str], str]]
             Set to primary energy demand., be default None
         country: Optional[Union[list[str], Series[str], str]]
             Geography for which data is forecast., be default None
         unit: Optional[Union[list[str], Series[str], str]]
             Unit of measurement. Ex: mtoe (million tonnes of oil equivalent), be default None
         year: Optional[Union[list[str], Series[str], str]]
             Forecast year, includes actuals for historic values., be default None
         value: Optional[Union[list[str], Series[str], str]]
             Primary energy demand values in million tonnes of oil equivalent., be default None
         modifiedDate: Optional[Union[list[str], Series[str], str]]
             The last modified date for the corresponding record., be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("longName", longName))
        filter_params.append(list_to_filter("scenario", scenario))
        filter_params.append(list_to_filter("modelVintage", modelVintage))
        filter_params.append(list_to_filter("energyType", energyType))
        filter_params.append(list_to_filter("theme", theme))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("unit", unit))
        filter_params.append(list_to_filter("year", year))
        filter_params.append(list_to_filter("value", value))
        filter_params.append(list_to_filter("modifiedDate", modifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/carbon-scenarios/ies/v1/primary-energy-demand",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_hierarchy_demand_sector(
        self, id: Optional[Union[list[str], Series[str], str]] = None, source: Optional[Union[list[str], Series[str], str]] = None, consumption: Optional[Union[list[str], Series[str], str]] = None, mainSector: Optional[Union[list[str], Series[str], str]] = None, subsector: Optional[Union[list[str], Series[str], str]] = None, subsectorRanking: Optional[Union[list[str], Series[str], str]] = None, mainSectorRanking: Optional[Union[list[str], Series[str], str]] = None, ranking: Optional[Union[list[str], Series[str], str]] = None, modifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         id: Optional[Union[list[str], Series[str], str]]
             Unique row identifier, be default None
         source: Optional[Union[list[str], Series[str], str]]
             source table name, be default None
         consumption: Optional[Union[list[str], Series[str], str]]
             Total consumption by coal,gas,oil and final consumption., be default None
         mainSector: Optional[Union[list[str], Series[str], str]]
             Main sectors for coal, gas, oil (Transformation and own use, Industry including Feedstocks, Domestic, Transport) and final sectors(Industry including Feedstocks, Domestic, Transport), be default None
         subsector: Optional[Union[list[str], Series[str], str]]
             Subsectors for coal, gas, oil and final sector consumption(Power and heat, Own use and other, Industry, Feedstocks, Commercial, Residential, Agricultural, Road transport, Rail transport, Shipping transport, Other transport etc.), be default None
         subsectorRanking: Optional[Union[list[str], Series[str], str]]
             Subsector ranking, be default None
         mainSectorRanking: Optional[Union[list[str], Series[str], str]]
             Main sector ranking, be default None
         ranking: Optional[Union[list[str], Series[str], str]]
             Ranking for coal, gas, oil and final consumption, be default None
         modifiedDate: Optional[Union[list[str], Series[str], str]]
             Last modified date for this record, be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("id", id))
        filter_params.append(list_to_filter("source", source))
        filter_params.append(list_to_filter("consumption", consumption))
        filter_params.append(list_to_filter("mainSector", mainSector))
        filter_params.append(list_to_filter("subsector", subsector))
        filter_params.append(list_to_filter("subsectorRanking", subsectorRanking))
        filter_params.append(list_to_filter("mainSectorRanking", mainSectorRanking))
        filter_params.append(list_to_filter("ranking", ranking))
        filter_params.append(list_to_filter("modifiedDate", modifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/carbon-scenarios/ies/v1/hierarchy/demand-sector",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_hierarchy_geo(
        self, id: Optional[Union[list[str], Series[str], str]] = None, world: Optional[Union[list[str], Series[str], str]] = None, mainRegion: Optional[Union[list[str], Series[str], str]] = None, subregion: Optional[Union[list[str], Series[str], str]] = None, country: Optional[Union[list[str], Series[str], str]] = None, countryRanking: Optional[Union[list[str], Series[str], str]] = None, subregionRanking: Optional[Union[list[str], Series[str], str]] = None, mainRegionRanking: Optional[Union[list[str], Series[str], str]] = None, worldRanking: Optional[Union[list[str], Series[str], str]] = None, modifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         id: Optional[Union[list[str], Series[str], str]]
             Unique row identifier, be default None
         world: Optional[Union[list[str], Series[str], str]]
             World, be default None
         mainRegion: Optional[Union[list[str], Series[str], str]]
             This contains seven main regions(Africa, Asia Pacific, CIS, Europe, Latin America, Middle East, North America), be default None
         subregion: Optional[Union[list[str], Series[str], str]]
             Subregion ranking column, be default None
         country: Optional[Union[list[str], Series[str], str]]
             Geography for which data is forecast, be default None
         countryRanking: Optional[Union[list[str], Series[str], str]]
             Countries ranking column, be default None
         subregionRanking: Optional[Union[list[str], Series[str], str]]
             Subregion ranking column, be default None
         mainRegionRanking: Optional[Union[list[str], Series[str], str]]
             Main region ranking column, be default None
         worldRanking: Optional[Union[list[str], Series[str], str]]
             World ranking, be default None
         modifiedDate: Optional[Union[list[str], Series[str], str]]
             Last modified date for this record, be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("id", id))
        filter_params.append(list_to_filter("world", world))
        filter_params.append(list_to_filter("mainRegion", mainRegion))
        filter_params.append(list_to_filter("subregion", subregion))
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("countryRanking", countryRanking))
        filter_params.append(list_to_filter("subregionRanking", subregionRanking))
        filter_params.append(list_to_filter("mainRegionRanking", mainRegionRanking))
        filter_params.append(list_to_filter("worldRanking", worldRanking))
        filter_params.append(list_to_filter("modifiedDate", modifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/carbon-scenarios/ies/v1/hierarchy/geo",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_hierarchy_ghg_sector(
        self, id: Optional[Union[list[str], Series[str], str]] = None, emissions: Optional[Union[list[str], Series[str], str]] = None, totalConsumptionLevel: Optional[Union[list[str], Series[str], str]] = None, mainSectorLevel: Optional[Union[list[str], Series[str], str]] = None, subsectorLevel: Optional[Union[list[str], Series[str], str]] = None, energyAndNonEnergyRelatedRanking: Optional[Union[list[str], Series[str], str]] = None, totalConsumptionLevelRanking: Optional[Union[list[str], Series[str], str]] = None, mainSectorLevelRanking: Optional[Union[list[str], Series[str], str]] = None, subsectorLevelRanking: Optional[Union[list[str], Series[str], str]] = None, modifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         id: Optional[Union[list[str], Series[str], str]]
             Unique row identifier, be default None
         emissions: Optional[Union[list[str], Series[str], str]]
             Energy related emissions and Non-energy related emissions, be default None
         totalConsumptionLevel: Optional[Union[list[str], Series[str], str]]
             Non-energy from waste-related, Non-energy from agricultural, Non-energy from LULUCF, Non-energy from industrial processes, Non-energy from geo-engineering, Transformation and other, Final sectors, be default None
         mainSectorLevel: Optional[Union[list[str], Series[str], str]]
             Non-energy from waste-related, Non-energy from agricultural, Non-energy from LULUCF, Non-energy from industrial processes, Non-energy from geo-engineering, Power generation, District heating, Hydrogen generation, Refining, Coke ovens, Other sectors, Industry, Transport, Domestic sectors, be default None
         subsectorLevel: Optional[Union[list[str], Series[str], str]]
             Non-energy from waste-related, Non-energy from agricultural, Non-energy from LULUCF, Non-energy from industrial processes, Non-energy from geo-engineering, Power generation, District heating, Hydrogen generation, Refining, Coke ovens, Other sectors, Industry, Road transport, Rail transport, International aviation transport, Domestic aviation transport, International shipping transport, Domestic shipping transport, Other transport, be default None
         energyAndNonEnergyRelatedRanking: Optional[Union[list[str], Series[str], str]]
             Energy and non energy related ranking, be default None
         totalConsumptionLevelRanking: Optional[Union[list[str], Series[str], str]]
             Total consumption level ranking, be default None
         mainSectorLevelRanking: Optional[Union[list[str], Series[str], str]]
             Main sector level ranking, be default None
         subsectorLevelRanking: Optional[Union[list[str], Series[str], str]]
             Subsector level ranking, be default None
         modifiedDate: Optional[Union[list[str], Series[str], str]]
             Last modified date for this record, be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("id", id))
        filter_params.append(list_to_filter("emissions", emissions))
        filter_params.append(list_to_filter("totalConsumptionLevel", totalConsumptionLevel))
        filter_params.append(list_to_filter("mainSectorLevel", mainSectorLevel))
        filter_params.append(list_to_filter("subsectorLevel", subsectorLevel))
        filter_params.append(list_to_filter("energyAndNonEnergyRelatedRanking", energyAndNonEnergyRelatedRanking))
        filter_params.append(list_to_filter("totalConsumptionLevelRanking", totalConsumptionLevelRanking))
        filter_params.append(list_to_filter("mainSectorLevelRanking", mainSectorLevelRanking))
        filter_params.append(list_to_filter("subsectorLevelRanking", subsectorLevelRanking))
        filter_params.append(list_to_filter("modifiedDate", modifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/carbon-scenarios/ies/v1/hierarchy/ghg-sector",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_hierarchy_ghg_source(
        self, id: Optional[Union[list[str], Series[str], str]] = None, emissions: Optional[Union[list[str], Series[str], str]] = None, energyAndNonEnergy: Optional[Union[list[str], Series[str], str]] = None, sourceOfEmission: Optional[Union[list[str], Series[str], str]] = None, totalGhgEmissionsRanking: Optional[Union[list[str], Series[str], str]] = None, energyAndNonEnergyRanking: Optional[Union[list[str], Series[str], str]] = None, sourceOfEmissionsRanking: Optional[Union[list[str], Series[str], str]] = None, modifiedDate: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         id: Optional[Union[list[str], Series[str], str]]
             Unique row identifier, be default None
         emissions: Optional[Union[list[str], Series[str], str]]
             Total GHG emissions, be default None
         energyAndNonEnergy: Optional[Union[list[str], Series[str], str]]
             Energy related emissions and Non-energy related emissions, be default None
         sourceOfEmission: Optional[Union[list[str], Series[str], str]]
             Energy related emissions from oil, natural gas, coal, biomass and undefined (methane), and Non-energy related emissions, be default None
         totalGhgEmissionsRanking: Optional[Union[list[str], Series[str], str]]
             Total GHG emissions ranking, be default None
         energyAndNonEnergyRanking: Optional[Union[list[str], Series[str], str]]
             Energy and non energy ranking, be default None
         sourceOfEmissionsRanking: Optional[Union[list[str], Series[str], str]]
             Source of emissions ranking, be default None
         modifiedDate: Optional[Union[list[str], Series[str], str]]
             Last modified date for this record, be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("id", id))
        filter_params.append(list_to_filter("emissions", emissions))
        filter_params.append(list_to_filter("energyAndNonEnergy", energyAndNonEnergy))
        filter_params.append(list_to_filter("sourceOfEmission", sourceOfEmission))
        filter_params.append(list_to_filter("totalGhgEmissionsRanking", totalGhgEmissionsRanking))
        filter_params.append(list_to_filter("energyAndNonEnergyRanking", energyAndNonEnergyRanking))
        filter_params.append(list_to_filter("sourceOfEmissionsRanking", sourceOfEmissionsRanking))
        filter_params.append(list_to_filter("modifiedDate", modifiedDate))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/carbon-scenarios/ies/v1/hierarchy/ghg-source",
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
        return df
    