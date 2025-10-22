"""
This module outputs the dei data for the constituents of the S&P 1500 index
Source: EDGAR API
"""

from typing import Union
import requests
import pandas as pd

# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=C0301

class EdgarAPI:

    BASE_URL = "https://data.sec.gov"
    HEADER = {"User-Agent": "ricky_summer@live.com"}
    METADATA = [
        'cik', 'entityType', 'sic', 'sicDescription', 'ownerOrg',
        'insiderTransactionForOwnerExists', 'insiderTransactionForIssuerExists',
        'name', 'tickers', 'exchanges', 'ein', 'lei', 'description', 'fiscalYearEnd',
        'website', 'investorWebsite', 'category', 'stateOfIncorporation', 'stateOfIncorporationDescription'
    ]

    def __init__(self, retrieval: str, cik: str):
        self.retrieval = retrieval
        self.cik = cik
        if self.retrieval == "dei":
            self.url = f"{EdgarAPI.BASE_URL}/api/xbrl/companyfacts/CIK{cik}.json"
        elif self.retrieval == "submission":
            self.url = f"{EdgarAPI.BASE_URL}/submissions/CIK{cik}.json"
        else:
            raise ValueError("Invalid retrieval type. Use 'dei' or 'metadata' or 'filings'.")

        try:
            res = requests.get(url=self.url, headers=EdgarAPI.HEADER, timeout=10)
            res.raise_for_status()  # Raise HTTPError for bad responses
            self.json_data = res.json()
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None


    def get_company_dei(self):

        company_facts = self.json_data
        if "entityName" in company_facts:
            entity_name = company_facts["entityName"]
            print(f"Entity Name: {entity_name}")

        dei_df = pd.DataFrame()
        if "dei" in company_facts["facts"]:
            dei = company_facts["facts"].get("dei")
            for item in dei:
                units = dei[item]["units"].keys()
                for unit in units:
                    dff = pd.DataFrame(dei[item]["units"][unit])
                    dff['end'] = pd.to_datetime(dff['end'])
                    dff["filed"] = pd.to_datetime(dff["filed"])
                    dff["cik"] = self.cik
                    dff["entity_name"] = entity_name
                    dff["item"] = item
                    dff["unit"] = unit
                    dei_df = pd.concat([dei_df, dff])
        return dei_df

    def get_company_meta(self):

        meta_data = {}
        for key in EdgarAPI.METADATA:
            value = self.json_data.get(key, None)
            if isinstance(value, list):
                value = ",".join(map(str, value))
            if value is None:
                value = ""
            meta_data[key] = value
        return meta_data #pd.DataFrame(meta_data, index=[0])

    def get_company_filings(self, filing_type: Union[str, list, None]=None):

        filings_df = pd.DataFrame(self.json_data.get("filings", {}).get("recent", []))
        filings_df["cik"] = self.cik
        if filing_type is not None:
            if isinstance(filing_type, str):
                filing_type = [filing_type]
            filings_df = filings_df[filings_df["form"].isin(filing_type)]
        return filings_df


if __name__ == "__main__":

    Edgar_API = EdgarAPI(retrieval="dei", cik="0000858877")
    df_dei = Edgar_API.get_company_dei()
    print(df_dei.shape)
    print(df_dei.head())

    Edgar_API = EdgarAPI(retrieval="submission", cik="0000858877")
    metadata = Edgar_API.get_company_meta()
    print(metadata)
    filings = Edgar_API.get_company_filings()
    print(filings.shape)
    df = filings.assign(**metadata)
    print(df.head())
