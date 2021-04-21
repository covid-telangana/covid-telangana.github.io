import requests
import pandas as pd
from pathlib import Path


STORE = Path(__file__).parent.absolute() / "data"
STORE.mkdir(parents=True, exist_ok=True)


def beds_df(text, hospital_type=None):
    df = pd.read_html(text, attrs={"id": "datatable-default1"})
    df = df[0]
    df = df.iloc[:-1]
    df.columns = [" ".join(c[1:]) if c[1] != c[2] else c[1] for c in df.columns]
    if hospital_type:
        df["TYPE"] = {"P": "Private", "G": "Government"}.get(hospital_type)
    return df


def beds(url="http://164.100.112.24/SpringMVC/getHospital_Beds_Status_Citizen.htm"):
    df = []
    for hospital_type in ["P", "G"]:
        r = requests.post(url, data={"hospital": hospital_type})
        df_h = beds_df(r.text, hospital_type)
        df.append(df_h)
    df = pd.concat(df, ignore_index=True)
    columns = [
        "DISTRICT",
        "NAME OF THE HOSPITAL",
        "REGULAR BEDS TOTAL",
        "REGULAR BEDS OCCUPIED",
        "REGULAR BEDS VACANT",
        "OXYGEN BEDS TOTAL",
        "OXYGEN BEDS OCCUPIED",
        "OXYGEN BEDS VACANT",
        "ICU BEDS (Ventilator/ CPAP) TOTAL",
        "ICU BEDS (Ventilator/ CPAP) OCCUPIED",
        "ICU BEDS (Ventilator/ CPAP) VACANT",
        "TOTAL BEDS TOTAL",
        "TOTAL BEDS OCCUPIED",
        "TOTAL BEDS VACANT",
        "TYPE",
    ]
    df = df[columns]
    df.to_csv(STORE / "beds.csv", index=False)
    # archive hourly
    now = pd.to_datetime("now").tz_localize("UTC").tz_convert("Asia/Calcutta")
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"At {now} with {len(df)} hospitals")
    return df


if __name__ == "__main__":
    #
    beds()
