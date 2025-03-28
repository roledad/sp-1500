"""
This module output the data for the constituents of the S&P 1500 index.
Source: Wikipedia and EDGAR
"""

import requests
import pandas as pd

# pylint: disable=C0116
# pylint: disable=C0301

def get_wiki_data(output: str = "constituents"):

    sp_df = pd.DataFrame()
    chg_df = pd.DataFrame()
    for sp_index in ["500", "400", "600"]:
        wiki_sp = pd.read_html(f"https://en.wikipedia.org/wiki/List_of_S%26P_{sp_index}_companies")
        cons_df = wiki_sp[0]
        if "CIK" in cons_df.columns:
            cons_df["CIK"] = cons_df["CIK"].astype(str).str.zfill(10)
        if "Date added" in cons_df.columns:
            cons_df["Date added"] = pd.to_datetime(cons_df["Date added"])
        cons_df["index_series"] = sp_index
        sp_df = pd.concat([sp_df, cons_df])

        df_chg = wiki_sp[1]
        df_chg.columns = [
            "Date", "Added_Ticker", "Added_Security", "Removed_Ticker", "Removed_Security", "Reason"
            ]
        df_chg["index_series"] = sp_index
        chg_df = pd.concat([chg_df, df_chg])

    sp_df["Security"] = sp_df["Security"].fillna(sp_df["Company"])
    sp_df = sp_df.drop(columns=["SEC filings", "Company"]).reset_index(drop=True)

    chg_df["Date"] = pd.to_datetime(chg_df["Date"].str.split("[", expand=True)[0])
    chg_df = chg_df.reset_index(drop=True)

    return sp_df if output == "constituents" else chg_df

def get_edgar_identifiers():
    res = requests.get(
        url="https://www.sec.gov/files/company_tickers_exchange.json",
        headers={"User-Agent": "ricky_summer@live.com"}, timeout=10)
    if res.ok:
        edgar_id = pd.DataFrame(columns = res.json()["fields"], data=res.json()["data"])
        edgar_id["cik"] = edgar_id["cik"].astype(str).str.zfill(10)
    else:
        edgar_id = None
    return edgar_id

def consolidate_data():

    edgar_data = get_edgar_identifiers()
    wiki_data = get_wiki_data()
    print(f"{len(wiki_data)} records of the S&P 1500 index constituents are found in the Wikipedia page.")

    if wiki_data is None or edgar_data is None:
        return None

    df = pd.merge(wiki_data, edgar_data, left_on="Symbol", right_on="ticker", how="left")
    null_df = df[df["ticker"].isnull()].drop(columns=["cik", "ticker", "name", "exchange"])
    print(f"{len(null_df)} records of the S&P 1500 index constituents are not found in the EDGAR database.")

    # consistent in the symbol/ticker format
    null_df["Symbol"] = null_df["Symbol"].str.replace(".", "-")
    df = pd.concat([df, pd.merge(null_df, edgar_data, left_on="Symbol", right_on="ticker", how="left")])
    df = df[df["ticker"].notnull()]

    # remerge the missing records with cik
    null_df = pd.merge(null_df, edgar_data, left_on="Symbol", right_on="ticker", how="left")
    null_df = null_df[null_df["ticker"].isnull()].drop(columns=["cik", "ticker", "name", "exchange"])
    null_df = pd.merge(null_df, edgar_data, left_on="CIK", right_on="cik", how="left").drop_duplicates("cik", keep="first")

    df = pd.concat([df, null_df])
    assert len(df) == len(wiki_data)

    # concat duplicated CIK companies with different tickers
    dup_cik = df[df["cik"].duplicated()]["cik"]
    print(f"{len(dup_cik)} records of the S&P 1500 index constituents are with duplicate CIK")
    dup_df = df[df["cik"].isin(dup_cik)].fillna('').astype(str)
    dup_cols = ["index_series", "cik", "name", "exchange", "GICS Sector", "GICS Sub-Industry", "Headquarters Location", "CIK", "Founded"]
    dup_df = dup_df.groupby(by=dup_cols).agg(', '.join).reset_index()
    df = pd.concat([df[~df["cik"].isin(dup_cik)], dup_df]).reset_index(drop=True)
    df = df.drop(columns=["CIK"])
    print(f"{len(df)} records of the S&P 1500 index constituents are mapped with the EDGAR database.")

    return df

if __name__ == "__main__":
    data = consolidate_data()
    print(data.head())
    chg_data = get_wiki_data("changes")
    print(chg_data.head())
