# %% [markdown]
# # Combining Population and Shipment Data

# %% [markdown]
# First, I read in the data.

# %%
import pandas as pd

# %%
pop = pd.read_parquet("../20_intermediate_files/population_clean.parquet")
opioid = pd.read_parquet("../20_intermediate_files/opioid_annual_total.parquet")

# %%
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))


# %% [markdown]
# Here, I converted state abbreviations in the shipment data to the full state name.
#
# After checking for null values, I found that Palau is included in this data, so I dropped those values.

# %%


# %%
opioid["BUYER_STATE"] = opioid["BUYER_STATE"].map(abbrev_to_us_state)
opioid[opioid["BUYER_STATE"].isnull().values]


# %%
opioid = opioid[~opioid["BUYER_STATE"].isnull().values]


# %% [markdown]
# I next turned the year column into an integer and changed the column names for merging and sorted by values for easier comparison

# %%
opioid["year"] = opioid["TRANSACTION_YEAR"].dt.year
opioid.rename(
    {
        "BUYER_COUNTY": "county",
        "BUYER_STATE": "state",
        "shipment_quantity": "shipment",
    },
    axis=1,
    inplace=True,
)
opioid.drop(["TRANSACTION_YEAR"], axis=1, inplace=True)
opioid = opioid[["state", "county", "year", "shipment"]].sort_values(
    ["state", "county", "year"]
)


# %% [markdown]
# Here, I do all the data cleaning necessary to make sure that the two sets merge appropriately on county values.
#
# The two datasets often refer to counties differently, with extra spaces, or little differences like "saint" vs "st.".
#
# The general strategy is to make everything lowercase and delete all spaces.
#
# There are also specific changes that had to be made.

# %%
opioid["county"] = opioid["county"].str.replace(
    "^[Ss][Tt][Ee]?(\.)? ", "saint", regex=True
)
pop["county"] = pop["county"].str.replace("^[Ss][Tt][Ee]?(\.)? ", "saint", regex=True)
opioid["county"] = opioid["county"].str.replace("SAINTE", "saint")
pop["county"] = pop["county"].str.replace("ñ", "n")
opioid["county"] = opioid["county"].str.lower()
pop["county"] = pop["county"].str.lower()
pop["county"] = pop["county"].str.replace(" county", "")
pop["county"] = pop["county"].str.replace(" ", "")
opioid["county"] = opioid["county"].str.replace(" ", "")
pop["county"] = pop["county"].str.replace("[^\w\s]", "", regex=True)
opioid["county"] = opioid["county"].str.replace("[^\w\s]", "", regex=True)
pop["county"] = pop["county"].str.replace("parish", "")
pop["county"] = pop["county"].str.replace("bristolcity", "bristol")
pop["county"] = pop["county"].str.replace("radfordcity", "radford")
pop["county"] = pop["county"].str.replace("salemcity", "salem")


# %% [markdown]
# Here, I merge, and then remove Alaska per Nick's instructions
#
# I also remove U.S. territories to limit this analysis to States and D.C.

# %%
opioid_pop = opioid.merge(
    pop, how="outer", on=["state", "county", "year"], sort=True, validate="1:1"
)
opioid_pop = opioid_pop[
    (opioid_pop["state"] != "Alaska")
    & (opioid_pop["state"] != "Guam")
    & (opioid_pop["state"] != "Northern Mariana Islands")
    & (opioid_pop["state"] != "Puerto Rico")
    & (opioid_pop["state"] != "U.S. Virgin Islands")
]


# %% [markdown]
# Here, I check to make sure there are no null values for population.

# %%
opioid_pop[opioid_pop["population"].isnull().values]


# %% [markdown]
# Limit the data to relevant years.

# %%
opioid_pop = opioid_pop[(opioid_pop["year"] >= 2006) & (opioid_pop["year"] <= 2012)]

# %% [markdown]
# Check for number of missing values. There are 914, and they are spread fairly evenly across states.

# %%
opioid_pop[opioid_pop["shipment"].isnull().values]


# %%
opioid_pop[opioid_pop["shipment"].isnull().values][["state", "county", "year"]].groupby(
    ["state"]
).count()

# %% [markdown]
# Filled NAs with 0s, assuming that's what they are.
#
# Created column for opioid shipments per 1,000 people.

# %%
opioid_pop.fillna(0, inplace=True)
opioid_pop["shipment_per_resident"] = opioid_pop["shipment"] / opioid_pop["population"]


# %% [markdown]
# Checked for counties that changed names between census years.
#
# In this case, Louisiana's two counties were merged, because of the string manipulation done. The population seems fine so it's okay to keep.
#
# However, I will drop South Dakota and Virginia still.
#
#

# %%
temp = [
    "lasalle",
    "oglalalakota",
    "shannon",
    "bedfordcity",
]
opioid_pop[opioid_pop["county"].isin(temp)]


# %%
drop = ["South Dakota", "Virginia"]
opioid_pop = opioid_pop[~opioid_pop["state"].isin(drop)]

# %% [markdown]
# Now I conducted asserts to make sure the data is reasonable.
#
# population greater than 0 and less than 10 mil (most populous county in the time period)
#
# Shipment rate is non-negative
#
# same number of observations for each year
#

# %%
assert ((opioid_pop["population"] >= 0) & (opioid_pop["population"] <= 10000000)).all()
assert (opioid_pop["shipment_per_resident"] >= 0).all()
assert (opioid_pop.groupby(["year"])["county"].count() == 2914).all()


# %%
opioid_pop.to_parquet(
    "../20_intermediate_files/opioid_population.parquet", engine="fastparquet"
)
