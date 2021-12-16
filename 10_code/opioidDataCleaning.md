---
jupyter:
  jupytext:
    formats: ipynb,md
    main_language: python
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.0
  kernelspec:
    display_name: 'Python 3.9.7 64-bit (''general'': conda)'
    name: python3
---

# Opioid Data Cleaning
### Date: 10/31/2021  
<br />
    
## Step 1: Load In Top 50K rows

```python
import numpy as np
import pandas as pd
from tqdm import tqdm

```

```python
# This is a very big file, so we will first load in a few lines to explore the structure
head = pd.read_csv(
    "C:/Users/Robert/Desktop/arcos_all_washpost.tsv.gz",
    compression="gzip",
    sep="\t",
    nrows=50000,
)

# See what columns we have
# head.sample(10)

```

```python
# Keep these columns
# keep = ['TRANSACTION_DATE', 'BUYER_STATE', 'BUYER_COUNTY', 'BUYER_ZIP', 'DRUG_CODE', 'DRUG_NAME', 'CALC_BASE_WT_IN_GM', 'DOSAGE_UNIT', 'MME_Conversion_Factor', 'dos_str']
# keeping 'CALC_BASE_WT_IN_GM', 'DOSAGE_UNIT', 'MME_Conversion_Factor', 'dos_str' to later help us decide which column is the best representation of shipment
head = head[
    [
        "TRANSACTION_DATE",
        "BUYER_STATE",
        "BUYER_COUNTY",
        "BUYER_ZIP",
        "DRUG_CODE",
        "DRUG_NAME",
        "CALC_BASE_WT_IN_GM",
        "DOSAGE_UNIT",
        "MME_Conversion_Factor",
        "dos_str",
    ]
]


```

```python
# Convert TRANSACTION_DATE column to a usable format

# The TRANSACTION_DATE column is in the format of (m)mddyyyy
# Months are not zero-padded, and days are zero-padded
# As such, 1022020 means January 2nd, 2020 rather than October 2nd, 2020. In other words, it's 1/02/2020

# Convert the TRANSACTION_DATE column to yyyy/(m)m/dd
head["TRANSACTION_DATE"] = (
    head["TRANSACTION_DATE"].astype(str).str[-4:]
    + "/"
    + head["TRANSACTION_DATE"].astype(str).str[:-6]
    + "/"
    + head["TRANSACTION_DATE"].astype(str).str[-6:-4]
)
# Convert to datetime format
head["TRANSACTION_DATE"] = pd.to_datetime(head["TRANSACTION_DATE"], format="%Y/%m/%d")

# add a year column
head["TRANSACTION_YEAR"] = head["TRANSACTION_DATE"].astype("datetime64[Y]")
# add a month column
head["TRANSACTION_MONTH"] = head["TRANSACTION_DATE"].astype("datetime64[M]")
```

```python
# Zip code needs to be 5-digits
# For zipcode that are not 5-digits, pad with 0s at the beginning
head["BUYER_ZIP"] = head["BUYER_ZIP"].astype(str)
head["BUYER_ZIP"] = head["BUYER_ZIP"].str.pad(width=5, side="left", fillchar="0")

```

### Step 1.1 Explore Null Values & Decide Which Column to Use to Represent Opioid Shipment

```python
head.info()
```

```python
# Why are there nulls for county?
head.loc[
    head["BUYER_COUNTY"].isna() == True,
]
# I looked up the zip code 02401. It's an inactive zip code
# It used to belong to Brockton, MA according to Google
# However, USPS doesn't have this zip code anymore - it might have gone inactive

# If there are only a small proportion of rows with this issue, we can drop those rows
# Since only 2 out of the first 50K rows have this issue, it's possible that this is very rare, and we're safe to drop them

```

```python
# Why are there nulls for dos_str?
head.loc[
    head["dos_str"].isna() == True,
]

# Are all these drugs OXYCODONE?
# Yes
head.loc[
    (head["dos_str"].isna() == True) & (head["DRUG_NAME"] != "OXYCODONE"),
]

# Do all OXYCODONEs have NaN dos_str?
# No. A lot of OXYCODONE shipments have values for dos_str
head.loc[
    (head["dos_str"].isna() == False) & (head["DRUG_NAME"] == "OXYCODONE"),
]

# Are there other patterns?
# Most NaN dos_str occur in NY and PA
head.loc[
    head["dos_str"].isna() == True,
].BUYER_STATE.value_counts()
# No pattern regarding TRANSACTION_YEAR
head.loc[
    head["dos_str"].isna() == True,
].TRANSACTION_YEAR.value_counts()

# 86 / 50,000 rows have missing dos_str, giving a 0.172% missing rate
# Seems fine to drop the missing rows if the final decision is to use 'dos_str' for the analysis
```

```python
# Which column should we use to represent opioid shipment?
head.head()

# Looking at the data, it's pretty clear that CALC_BASE_WT_IN_GM ~ DOSAGE_UNIT * dos_str * X
# CALC_BASE_WT_IN_GM: DEA added field indicating the total active weight of the drug in the transaction, in grams.
# We should use this column
```

### Step 1.2: Group by county, state, year

```python
# Opioid shipment per county per year
annual = head.groupby(['TRANSACTION_YEAR', 'BUYER_COUNTY', 'BUYER_STATE'], as_index=False)['CALC_BASE_WT_IN_GM'].sum()

# Opioid shipment per county per month
monthly = head.groupby(['TRANSACTION_MONTH', 'BUYER_COUNTY', 'BUYER_STATE'], as_index=False)['CALC_BASE_WT_IN_GM'].sum()
```

## Step 2: Load In Full Data Set

```python
# Read in full data set
opioid = pd.DataFrame()
annual_total = pd.DataFrame()
monthly_total = pd.DataFrame()

for chunk in tqdm(
    pd.read_csv(
        "C:/Users/Robert/Desktop/arcos_all_washpost.tsv.gz",
        compression="gzip",
        sep="\t",
        header=0,
        usecols=[
            "TRANSACTION_DATE",
            "BUYER_STATE",
            "BUYER_COUNTY",
            "BUYER_ZIP",
            "DRUG_CODE",
            "DRUG_NAME",
            "CALC_BASE_WT_IN_GM",
            "DOSAGE_UNIT",
            "MME_Conversion_Factor",
            "dos_str",
        ],
        dtype={
            "TRANSACTION_DATE": np.int32,
            "BUYER_STATE": object,
            "BUYER_COUNTY": object,
            "BUYER_ZIP": object,
            "DRUG_CODE": np.int32,
            "DRUG_NAME": object,
            "CALC_BASE_WT_IN_GM": np.float32,
            "DOSAGE_UNIT": np.float32,
            "MME_Conversion_Factor": np.float16,
            "dos_str": np.float16,
        },
        iterator=True,
        chunksize=3000000,
    )
):
    # Correct TRANSACTION_DATE
    # Convert the TRANSACTION_DATE column to yyyy/(m)m/dd
    chunk["TRANSACTION_DATE"] = (
        chunk["TRANSACTION_DATE"].astype(str).str[-4:]
        + "/"
        + chunk["TRANSACTION_DATE"].astype(str).str[:-6]
        + "/"
        + chunk["TRANSACTION_DATE"].astype(str).str[-6:-4]
    )
    # Convert to datetime format
    chunk["TRANSACTION_DATE"] = pd.to_datetime(
        chunk["TRANSACTION_DATE"], format="%Y/%m/%d"
    )
    # add a year column
    chunk["TRANSACTION_YEAR"] = chunk["TRANSACTION_DATE"].astype("datetime64[Y]")
    # add a month column
    chunk["TRANSACTION_MONTH"] = chunk["TRANSACTION_DATE"].astype("datetime64[M]")

    # Correct zip code
    # pad zip codes with 0s to make them 5-digit long
    chunk["BUYER_ZIP"] = chunk["BUYER_ZIP"].astype(str)
    chunk["BUYER_ZIP"] = chunk["BUYER_ZIP"].str.pad(width=5, side="left", fillchar="0")

    # Group by to get annual and monthly shipments
    # Opioid shipment per county per year
    annual = chunk.groupby(
        ["TRANSACTION_YEAR", "BUYER_COUNTY", "BUYER_STATE"], as_index=False
    )["CALC_BASE_WT_IN_GM"].sum()
    # Opioid shipment per county per month
    monthly = chunk.groupby(
        ["TRANSACTION_MONTH", "BUYER_COUNTY", "BUYER_STATE"], as_index=False
    )["CALC_BASE_WT_IN_GM"].sum()

    # append
    # opioid = opioid.append(chunk)
    annual_total = annual_total.append(annual)
    monthly_total = monthly_total.append(monthly)

# save data to parquet
annual_total.to_parquet(
    "C:/Users/Robert/Desktop/annual_total.parquet", engine="fastparquet"
)
monthly_total.to_parquet(
    "C:/Users/Robert/Desktop/monthly_total.parquet", engine="fastparquet"
)

```

```python
# We need to group by again in case there are ungrouped rows as we appended
annual_total = annual_total.groupby(
    ["TRANSACTION_YEAR", "BUYER_COUNTY", "BUYER_STATE"], as_index=False
)["CALC_BASE_WT_IN_GM"].sum()
monthly_total = monthly_total.groupby(
    ["TRANSACTION_MONTH", "BUYER_COUNTY", "BUYER_STATE"], as_index=False
)["CALC_BASE_WT_IN_GM"].sum()

```

```python
# Ensure we don't have duplicates
assert not annual_total[["TRANSACTION_YEAR", "BUYER_COUNTY", "BUYER_STATE"]].duplicated().any()
assert not monthly_total[["TRANSACTION_MONTH", "BUYER_COUNTY", "BUYER_STATE"]].duplicated().any()
```

```python
# save data again
annual_total.to_parquet(
    "C:/Users/Robert/Desktop/annual_total.parquet", engine="fastparquet"
)
monthly_total.to_parquet(
    "C:/Users/Robert/Desktop/monthly_total.parquet", engine="fastparquet"
)

```

## Step 3: Basic EDA

```python
# Load data
annual_total = pd.read_parquet("C:/Users/Robert/Desktop/annual_total.parquet")
monthly_total = pd.read_parquet("C:/Users/Robert/Desktop/monthly_total.parquet")
```

```python
# Add a COUNTY_STATE column to help us count the number of distinct counties more easily
# Because counties can have the same name across states
annual_total['COUNTY_STATE'] = annual_total['BUYER_COUNTY'] + ',' + annual_total['BUYER_STATE']
monthly_total['COUNTY_STATE'] = monthly_total['BUYER_COUNTY'] + ',' + monthly_total['BUYER_STATE']
```

```python
# How many counties do we have?
    # 3119
annual_total[['COUNTY_STATE']].drop_duplicates()

# What about by year?
annual_total.groupby(['TRANSACTION_YEAR'])['COUNTY_STATE'].nunique()

# What about by month?
monthly_total.groupby(['TRANSACTION_MONTH'])['COUNTY_STATE'].nunique()
```
