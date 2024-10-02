
from __future__ import annotations
from typing import List, Optional, Union
from requests import Response
from spgci_qa.api_client import get_data
from spgci_qa.utilities import list_to_filter
from pandas import DataFrame, Series
from datetime import date
import pandas as pd

class Agriculture_sustainability:
    _endpoint = "api/v1/"
    _reference_endpoint = "reference/v1/"
    _tbl_sustainable_agri_policy_endpoint = "/publicpolicy"
    _tbl_corporate_carbon_pledges_endpoint = "/corporate-carbon-pledges"


    def get_publicpolicy(
        self, country: Optional[Union[list[str], Series[str], str]] = None, name_title: Optional[Union[list[str], Series[str], str]] = None, summary: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         country: Optional[Union[list[str], Series[str], str]]
             Country name, be default None
         name_title: Optional[Union[list[str], Series[str], str]]
             Name/Title of the policy, be default None
         summary: Optional[Union[list[str], Series[str], str]]
             summary details description, be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("country", country))
        filter_params.append(list_to_filter("name_title", name_title))
        filter_params.append(list_to_filter("summary", summary))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/sustainability-compass/v1/publicpolicy",
            params=params,
            df_fn=self._convert_to_df,
            raw=raw,
            paginate=paginate,
        )
        return response


    def get_corporate_carbon_pledges(
        self, company_name: Optional[Union[list[str], Series[str], str]] = None, primary_industry_ciq_gics: Optional[Union[list[str], Series[str], str]] = None, qop_csa_score: Optional[Union[list[str], Series[str], str]] = None, total_emissions_base_year: Optional[Union[list[str], Series[str], str]] = None, last_reporting_year_emission: Optional[Union[list[str], Series[str], str]] = None, carbon_pledge_objective: Optional[Union[list[str], Series[str], str]] = None, filter_exp: Optional[str] = None, page: int = 1, page_size: int = 1000, raw: bool = False, paginate: bool = False
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        
         company_name: Optional[Union[list[str], Series[str], str]]
             Company Name Details, be default None
         primary_industry_ciq_gics: Optional[Union[list[str], Series[str], str]]
             Primary Industry Ciq Gics, be default None
         qop_csa_score: Optional[Union[list[str], Series[str], str]]
             qop_csa_score, be default None
         total_emissions_base_year: Optional[Union[list[str], Series[str], str]]
             total emissions baseyear, be default None
         last_reporting_year_emission: Optional[Union[list[str], Series[str], str]]
             Last Reporting Year Emission, be default None
         carbon_pledge_objective: Optional[Union[list[str], Series[str], str]]
             carbon pledge objective, be default None
         filter_exp: Optional[str] = None,
         page: int = 1,
         page_size: int = 1000,
         raw: bool = False,
         paginate: bool = False

        """

        filter_params: List[str] = []
        filter_params.append(list_to_filter("company_name", company_name))
        filter_params.append(list_to_filter("primary_industry_ciq_gics", primary_industry_ciq_gics))
        filter_params.append(list_to_filter("qop_csa_score", qop_csa_score))
        filter_params.append(list_to_filter("total_emissions_base_year", total_emissions_base_year))
        filter_params.append(list_to_filter("last_reporting_year_emission", last_reporting_year_emission))
        filter_params.append(list_to_filter("carbon_pledge_objective", carbon_pledge_objective))
        
        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"/analytics/sustainability-compass/v1/corporate-carbon-pledges",
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
        
        return df
    