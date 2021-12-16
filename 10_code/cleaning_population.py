# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ## Clean and Combine Population Files

# %%
import pandas as pd

# %% [markdown]
# Read in both population files, selecting only relevant columns.

# %%
pop_2000 = pd.read_csv(
    "../00_source/co-est00int-tot.csv",
    encoding="ISO-8859-1",
    usecols=[
        "STNAME",
        "CTYNAME",
        "POPESTIMATE2003",
        "POPESTIMATE2004",
        "POPESTIMATE2005",
        "POPESTIMATE2006",
        "POPESTIMATE2007",
        "POPESTIMATE2008",
        "POPESTIMATE2009",
    ],
)
pop_2010 = pd.read_csv(
    "../00_source/co-est2019-alldata.csv",
    encoding="ISO-8859-1",
    usecols=[
        "STNAME",
        "CTYNAME",
        "POPESTIMATE2010",
        "POPESTIMATE2011",
        "POPESTIMATE2012",
        "POPESTIMATE2013",
        "POPESTIMATE2014",
        "POPESTIMATE2015",
    ],
)

# %% [markdown]
# Melt both datasets by state and county.

# %%
pop_2000_melt = pop_2000.melt(id_vars=["STNAME", "CTYNAME"])
pop_2010_melt = pop_2010.melt(id_vars=["STNAME", "CTYNAME"])

# %% [markdown]
# Combine datasets and rename variables to be more informative.

# %%
pop_total = pop_2000_melt.append(pop_2010_melt)
pop_total.rename(
    {"STNAME": "state", "CTYNAME": "county", "variable": "year", "value": "population"},
    axis=1,
    inplace=True,
)

# %% [markdown]
# Removed "POPESTIMATE" from year column, and then dropped observations that were for the whole state.
#
# Needed to save DC from this, but then added back in.

# %%
pop_total["year"] = pop_total["year"].map(lambda x: x.lstrip("POPESTIMATE")).astype(int)
dc = pop_total[pop_total["state"] == "District of Columbia"].copy()
dc.drop_duplicates(inplace=True)
pop_total = pop_total[pop_total["county"] != pop_total["state"]]
pop_total = pop_total.append(dc)

# %% [markdown]
# Now, do some asserts. Check that there are no duplicates for state, county, year populations.
# Also, checked that all years are between 2003 and 2015, and that all population values are greater than zero.

# %%
assert not pop_total.duplicated(["year", "state", "county"]).any()
assert ((pop_total["year"] >= 2003) & (pop_total["year"] <= 2015)).all()
assert (pop_total["population"] > 0).all()

# %% [markdown]
# Below, I checked that all of the county-years had the same number of observations.
#
# I noticed that there are 9 counties that do not have observations for all years.
#
# It appears that this is due to renaming or changing boundaries between the two datasets.
#
# For now, I'll make note of this and move on, to see what the other datasets look like.
# Alaska Kusilvak Census Area (2010-2015)
#
# Alaska Petersburg Borough (2010-2015)
#
# Alaska Petersburg Census Area (2003-2009)
#
# Alaska Wade Hampton Census Area (2003-2009)
#
# Louisiana La Salle Parish (2003-2009)
#
# Louisiana LaSalle Parish (2010-2015)
#
# South Dakota Oglala Lakota County (2010-2015)
#
# South Dakota Shannon County (2003-2009)
#
# Virginia Bedford City (2003-2009)
#

# %%
num_obs = pop_total.groupby(["state", "county"]).count().reset_index()
num_obs[num_obs["year"] < 13]

# %% [markdown]
# Finally, output to intermediate files folder in parquet format

# %%
pop_total.to_parquet(
    "../20_intermediate_files/population_clean.parquet", engine="fastparquet"
)
