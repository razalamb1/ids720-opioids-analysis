# %%
import pandas as pd

# %%
# importing parquet files used in final analysis
florida_mortality = pd.read_parquet("florida_mortality.parquet")
florida_shipment_annual = pd.read_parquet("florida_shipment_annual.parquet")
florida_shipment_monthly = pd.read_parquet("florida_shipment_monthly.parquet")
washington_mortality = pd.read_parquet("washington_mortality.parquet")
washington_shipment_annual = pd.read_parquet("washington_shipment_annual.parquet")
washington_shipment_monthly = pd.read_parquet("washington_shipment_monthly.parquet")
texas_mortality = pd.read_parquet("texas_mortality.parquet")
texas_shipment_annual = pd.read_parquet("texas_shipment_annual.parquet")
texas_shipment_monthly = pd.read_parquet("texas_shipment_monthly.parquet")
pop_clean = pd.read_parquet("population_clean.parquet")

df_list = [
    florida_mortality,
    florida_shipment_annual,
    florida_shipment_monthly,
    washington_mortality,
    washington_shipment_annual,
    washington_shipment_monthly,
    texas_mortality,
    texas_shipment_annual,
    texas_shipment_monthly,
    pop_clean,
]
df_list_mort = [
    florida_mortality,
    washington_mortality,
    texas_mortality,
]
df_list_ship = [
    florida_shipment_annual,
    washington_shipment_annual,
    texas_shipment_annual,
    florida_shipment_monthly,
    texas_shipment_monthly,
    washington_shipment_monthly,
]


# %%
# giving dataframes string names
florida_mortality.Name = "Florida Mortality Distribution"
florida_shipment_annual.Name = "Florida Annual Opioid Shipment Distribution"
florida_shipment_monthly.Name = "Florida Monthly Shipment Distribution"
washington_mortality.Name = "Washington Mortality Distribution"
washington_shipment_annual.Name = "Washington Annual Opioid Shipment Distribution"
washington_shipment_monthly.Name = "Washington Monthly Shipment Distribution"
texas_mortality.Name = "Texas Mortality Distribution"
texas_shipment_annual.Name = "Texas Annual Opioid Shipment Distribution"
texas_shipment_monthly.Name = "Texas Monthly Shipment Distribution"
pop_clean.Name = "Population Distribution"


# %%
from IPython.display import display

for i in df_list:
    display(i.head())


# %%
# calculating statistics summary for mortality dataframes
for a in df_list_mort:
    print("Data Statistics for", a.Name, ":")
    fd = a[["Deaths", "deaths_per_100k"]].describe()
    print(fd.to_markdown())


# %%
# calculating summary statistics for shipment dataframes
for a in df_list_ship:
    print("Data Statistics for", a.Name, ":")
    dl = a[["shipment", "shipment_per_resident"]].describe()
    print(dl.to_markdown())


# %%
print("Data Statistics for the population dataset: ")
dfg = pop_clean["population"].describe()
print(dfg.to_markdown())


# %%
import altair as alt

alt.data_transformers.disable_max_rows()

# plotting county population data
pop_chart = (
    alt.Chart(pop_clean, title="County Population Histogram")
    .mark_bar(size=5)
    .encode(
        alt.X(
            "population", bin=alt.Bin(step=40000), scale=alt.Scale(domain=[0, 2000000])
        ),
        y="count()",
    )
)

pop_chart


# %%
alt.data_transformers.disable_max_rows()

# defining a function to make histogram plotting easier
# x is dataframe, y is second number in graph x range, z is step size
def plotting(x, y, z, col_name):
    s = (
        alt.Chart(x, title=str(x.Name))
        .mark_bar()
        .encode(
            alt.X(str(col_name), bin=alt.Bin(step=z), scale=alt.Scale(domain=[0, y])),
            alt.Y("count()"),
        )
    )
    return s.display()


plotting(florida_shipment_annual, 2800, 100, "shipment_per_resident")
plotting(washington_shipment_annual, 2800, 100, "shipment_per_resident")
plotting(texas_shipment_annual, 2800, 100, "shipment_per_resident")
plotting(florida_shipment_monthly, 300, 20, "shipment_per_resident")
plotting(washington_shipment_monthly, 300, 20, "shipment_per_resident")
plotting(texas_shipment_monthly, 300, 20, "shipment_per_resident")
plotting(florida_mortality, 100, 5, "deaths_per_100k")
plotting(washington_mortality, 100, 5, "deaths_per_100k")
plotting(texas_mortality, 100, 5, "deaths_per_100k")
