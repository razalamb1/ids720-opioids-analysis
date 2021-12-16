# %%
import pandas as pd
import numpy as np

# %%
# loading cleaned and population merged mortality and shipment data
merged_mortality = pd.read_parquet(
    "moratality_population.parquet", engine="fastparquet"
)  # mortality data
opioid_population_annual = pd.read_parquet(
    "opioid_population.parquet", engine="fastparquet"
)  # annual opioid shipment data
opioid_population_monthly = pd.read_parquet(
    "opioid_population_monthly.parquet", engine="fastparquet"
)  # montly opioid shipment data

merged_mortality.head(10)


# %%
opioid_population_annual.head(10)


# %%
opioid_population_monthly.sample(10)

# %%
states_choice = ["Florida", "Washington", "Texas"]

# subseting data into each state of interest and other states for analysis
florida_mortality = merged_mortality[merged_mortality["state"] == "Florida"]
texas_mortality = merged_mortality[merged_mortality["state"] == "Texas"]
washington_mortality = merged_mortality[merged_mortality["state"] == "Washington"]
other_mortality = merged_mortality[~merged_mortality["state"].isin(states_choice)]

df_list = [florida_mortality, texas_mortality, washington_mortality, other_mortality]


# %%
from IPython.display import display

for i in df_list:
    display(i.head())


# %%
# looking at years present in the data
print("Years in mortality data are:", merged_mortality.year.unique())
print("Years in opioid shipment data are:", opioid_population_annual.year.unique())


# %%
# subseting data into each state of interest and other states for analysis
florida_shipment_annual = opioid_population_annual[
    opioid_population_annual["state"] == "Florida"
]
texas_shipment_annual = opioid_population_annual[
    opioid_population_annual["state"] == "Texas"
]
washington_shipment_annual = opioid_population_annual[
    opioid_population_annual["state"] == "Washington"
]
other_shipment_annual = opioid_population_annual[
    ~opioid_population_annual["state"].isin(states_choice)
]

df_list2 = [
    florida_shipment_annual,
    texas_shipment_annual,
    washington_shipment_annual,
    other_shipment_annual,
]


# %%
for a in df_list2:
    display(a.head())


# %%
florida_shipment_monthly = opioid_population_monthly[
    opioid_population_monthly["state"] == "Florida"
]
texas_shipment_monthly = opioid_population_monthly[
    opioid_population_monthly["state"] == "Texas"
]
washington_shipment_monthly = opioid_population_monthly[
    opioid_population_monthly["state"] == "Washington"
]
other_shipment_monthly = opioid_population_monthly[
    ~opioid_population_monthly["state"].isin(states_choice)
]

df_list3 = [
    florida_shipment_monthly,
    texas_shipment_monthly,
    washington_shipment_monthly,
    other_shipment_monthly,
]


# %%
for a in df_list3:
    display(a.head())

for a in df_list3:
    display(a.tail())

# %%
# defining pre and post policy ranges for each state's mortality data
category_flo = pd.cut(
    florida_mortality.year, bins=[2002, 2009, 2016], labels=["pre", "post"]
)
category_tex = pd.cut(
    texas_mortality.year, bins=[2002, 2006, 2016], labels=["pre", "post"]
)
category_was = pd.cut(
    washington_mortality.year, bins=[2002, 2011, 2016], labels=["pre", "post"]
)

# adding a flag for pre and post policy
florida_mortality.loc[:, "category_flo"] = category_flo

texas_mortality.loc[:, "category_tex"] = category_tex

washington_mortality.loc[:, "category_was"] = category_was


# %%
# defining pre and post policy ranges for each state's annual shipment data
category_flo_s = pd.cut(
    florida_shipment_annual.year, bins=[2002, 2009, 2016], labels=["pre", "post"]
)
category_tex_s = pd.cut(
    texas_shipment_annual.year, bins=[2002, 2006, 2016], labels=["pre", "post"]
)
category_was_s = pd.cut(
    washington_shipment_annual.year, bins=[2002, 2011, 2016], labels=["pre", "post"]
)

# adding a flag for pre and post policy
florida_shipment_annual.loc[:, "category_flo"] = category_flo_s

texas_shipment_annual.loc[:, "category_tex"] = category_tex_s

washington_shipment_annual.loc[:, "category_was"] = category_was_s


# %%
# defining pre and post policy ranges for all states monthly shipment data
bins_flo = pd.to_datetime(["2005-12-01", "2010-01-01", "2013-01-01"])
category_flo_sm = pd.cut(
    florida_shipment_monthly.year, bins=bins_flo, labels=["pre", "post"]
)

bins_tex = pd.to_datetime(["2005-12-01", "2006-12-01", "2013-01-01"])
category_tex_sm = pd.cut(
    texas_shipment_monthly.year,
    bins=bins_tex,
    labels=["pre", "post"],
)

bins_wash = pd.to_datetime(["2005-12-01", "2011-12-01", "2013-01-01"])
category_was_sm = pd.cut(
    washington_shipment_monthly.year,
    bins=bins_wash,
    labels=["pre", "post"],
)

# adding a flag for pre and post policy
florida_shipment_monthly.loc[:, "category_flo"] = category_flo_sm

texas_shipment_monthly.loc[:, "category_tex"] = category_tex_sm

washington_shipment_monthly.loc[:, "category_was"] = category_was_sm


# %%
for a in df_list:
    display(a.head())

# %%
for a in df_list2:
    display(a.head())

# %%
for a in df_list3:
    display(a.sample(30))

# %%
# # saving data
florida_mortality.to_parquet("florida_mortality.parquet", engine="fastparquet")

texas_mortality.to_parquet("texas_mortality.parquet", engine="fastparquet")

washington_mortality.to_parquet("washington_mortality.parquet", engine="fastparquet")

florida_shipment_annual.to_parquet("florida_shipment.parquet", engine="fastparquet")

texas_shipment_annual.to_parquet("texas_shipment.parquet", engine="fastparquet")

washington_shipment_annual.to_parquet(
    "washington_shipment.parquet", engine="fastparquet"
)

florida_shipment_monthly.to_parquet(
    "florida_shipment_monthly.parquet", engine="fastparquet"
)

texas_shipment_monthly.to_parquet(
    "texas_shipment_monthly.parquet", engine="fastparquet"
)
washington_shipment_monthly.to_parquet(
    "washington_shipment_monthly.parquet", engine="fastparquet"
)

other_mortality.to_parquet("other_mortality.parquet", engine="fastparquet")
other_shipment_annual.to_parquet("other_shipment.parquet", engine="fastparquet")

other_shipment_monthly.to_parquet(
    "other_shipment_monthly.parquet", engine="fastparquet"
)

# %%
