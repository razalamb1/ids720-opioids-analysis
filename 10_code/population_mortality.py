# %% [markdown]
# ## Combining population and mortality data
#
# First, I read in the cleaned mortality and population files.

# %%
import pandas as pd
import numpy as np

# %% [markdown]
# Read in data for both population and mortality

# %%
pop = pd.read_parquet("../20_intermediate_files/population_clean.parquet")
mortality = pd.read_parquet("../20_intermediate_files/df_clean_mortality.parquet")


# %% [markdown]
# Mortality files states are in abbreviation format, so use below to convert to names (after stripping extra space from state abbreviations column).

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
mortality["State"] = mortality["State"].str.strip()
mortality["State"] = mortality["State"].map(abbrev_to_us_state)


# %% [markdown]
# After merging initially, I checked for rows that did not have population values.
#
# I noticed that there were different names for some counties, which I changed in the mortality dataset.
#
# "La Porte" county is "LaPorte" in the population dataset, so I changed it in the mortality.
#
# Also, Dona Ana county is Doña Ana County.
#
# Continually, in the mortality McKean county is "Mc Kean", which I fixed.

# %%
mortality.loc[:, "County"][
    mortality.loc[:, "County"] == "La Porte County"
] = "LaPorte County"
mortality.loc[:, "County"][
    mortality.loc[:, "County"] == "Dona Ana County"
] = "Doña Ana County"
mortality.loc[:, "County"][
    mortality.loc[:, "County"] == "Mc Kean County"
] = "McKean County"


# %% [markdown]
# Renamed columns in mortality dataset to match population dataset.

# %%
mortality.rename(
    {"State": "state", "County": "county", "Year": "year"}, axis=1, inplace=True
)


# %% [markdown]
# Conducted outer merge.

# %%
mortality_pop = mortality.merge(
    pop, how="outer", on=["state", "county", "year"], sort=True, validate="1:1"
)


# %% [markdown]
# Checked for any missing values in the population column.
# Yay, there are none!

# %% [markdown]
# Now, looked at the counties that did not have observations for all 13 years.
#
# Because none of them had observations for mortality, I decided to drop those states (AK, LA, SD).
#
# I dropped them becasue none are our policy change, and the changes in borders could screw with population.

# %%
temp = [
    "Petersburg Borough",
    "Wade Hampton Census Area",
    "La Salle Parish",
    "LaSalle Parish",
    "Oglala Lakota County",
    "Shannon County",
    "Bedford city",
]
mortality_pop[mortality_pop["county"].isin(temp)]


# %%
drop_states = ["Alaska, Louisiana", "South Dakota", "Virginia"]
mortality_pop = mortality_pop[
    ~mortality_pop["state"].isin(["Alaska", "Louisiana", "South Dakota", "Virginia"])
]


# %% [markdown]
# Filled NA values with 0, because these indicate counties with deaths <10, and that's important to include.
#
# Created column with opioid overdose deaths per 100,000 residents.

# %%
mortality_pop["deaths_per_100k"] = (
    100000 * mortality_pop["Deaths"] / mortality_pop["population"]
)


# %%
mortality_pop["replaced"] = np.nan


def replace_values(state, year):
    mortality_pop.loc[
        (mortality_pop.loc[:, "state"] == state)
        & (mortality_pop.loc[:, "Deaths"].isnull())
        & (mortality_pop.loc[:, "year"] == year),
        "deaths_per_100k",
    ] = mortality_pop.loc[
        (mortality_pop["state"] == state) & (mortality_pop["year"] == year),
        "deaths_per_100k",
    ].mean()


years = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
for i in us_state_to_abbrev.keys():
    for j in years:
        replace_values(i, j)


# %%
mortality_pop.loc[mortality_pop["Deaths"].isnull(), "Deaths"] = (
    mortality_pop.loc[mortality_pop["Deaths"].isnull(), "deaths_per_100k"]
    * mortality_pop.loc[mortality_pop["Deaths"].isnull(), "population"]
    / 1000000
)


# %%
mortality_pop.shape

# %%
null_states = list(
    mortality_pop[mortality_pop["Deaths"].isnull()].state.value_counts().index
)


def replace_values2(state):
    mortality_pop.loc[
        (mortality_pop.loc[:, "state"] == state)
        & (mortality_pop.loc[:, "Deaths"].isnull()),
        "deaths_per_100k",
    ] = mortality_pop.loc[
        (mortality_pop["state"] == state),
        "deaths_per_100k",
    ].mean()


for i in null_states:
    replace_values2(i)

mortality_pop.loc[mortality_pop["Deaths"].isnull(), "Deaths"] = (
    mortality_pop.loc[mortality_pop["Deaths"].isnull(), "deaths_per_100k"]
    * mortality_pop.loc[mortality_pop["Deaths"].isnull(), "population"]
    / 1000000
)


# %%
mortality_pop["Deaths"].describe()

# %%
mortality_pop["deaths_per_100k"].describe()

# %% [markdown]
# Conducted asserts to make sure data is in reasonable bounds.
#
# population greater than 0 and less than 10.2 mil (most populous county in the time period)
#
# mortality rate is non-negative and less than everyone in the county dying
#
# same number of observations for each year

# %%
assert (
    (mortality_pop["population"] >= 0) & (mortality_pop["population"] <= 10200000)
).all()
assert ((mortality_pop["deaths_per_100k"]) > 0).all()
assert (mortality_pop.groupby(["year"])["county"].count() == 2850).all()


# %% [markdown]
# output to parquet.

# %%
mortality_pop.to_parquet(
    "../20_intermediate_files/moratality_population.parquet", engine="fastparquet"
)
