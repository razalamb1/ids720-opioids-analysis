import pandas as pd
from scipy import stats

# grab encodings based on kind of data
def grab_encodings(kind):
    kind_coding = {
        "shipment": [
            "Opioid Shipments per County per Year",
            "shipment_kg_per_100k",
            "Opioid Shipments per 100,000 Residents (Kg)",
        ],
        "mortality": [
            "Opioid Mortality per County per Year",
            "deaths_per_100k",
            "Opioid Mortality per 100,000 Residents)",
        ],
    }
    encodings = kind_coding[kind]
    return encodings


# calculate slope for each county
def calulate_slope_by_county(df_pre):
    # helper function for running regression
    def reg(df, x, y):
        slope, _, _, _, _ = stats.linregress(df[x], df[y])
        return slope

    # calculate slopes for mortality for each county
    slopes_mortality = (
        df_pre.groupby(["state", "county"])
        .apply(reg, "year", "deaths_per_100k")
        .reset_index(name="slope_mortality")
    )
    df_pre = pd.merge(df_pre, slopes_mortality, on=["state", "county"], how="left")

    # calculate slopes for shipment for each county
    slopes_shipment= (
        df_pre.groupby(["state", "county"])
        .apply(reg, "year", "shipment_kg_per_100k")
        .reset_index(name="slope_shipment")
    )
    df_pre = pd.merge(df_pre, slopes_shipment, on=["state", "county"], how="left")

    return df_pre


# calculate average population in pre-period for each county
def calculate_avg_population(df_pre):
    avg_pops = (
        df_pre.groupby(["state", "county"])["population"]
        .mean()
        .reset_index(name="avg_population")
    )
    df_pre = pd.merge(df_pre, avg_pops, on=["state", "county"], how="left")

    return df_pre


# find control counties based on slope

# for each county in state_pre, choose n most similar counties in control
#   # similarity is determined by 1) similar slope, 2) similar population
# return a DF with full data for the control counties selected

# duplicates in the DF is allowed so that we give more frequently selected counties higher weights
def grab_control_counties(state_pre, control_pre, control_data, n):
    # pull out these columns and dedupe to compare each test county to control counties
    state_pre_for_comparison = state_pre[
        ["state", "county", "slope_mortality", "slope_shipment", "avg_population"]
    ].drop_duplicates()
    control_pre_for_comparison = control_pre[
        ["state", "county", "slope_mortality", "slope_shipment", "avg_population"]
    ].drop_duplicates()

    # initiate DF to store data for selected controls
    selected_control = pd.DataFrame()
    # use a loop to find similar control counties
    for idx, row in state_pre.iterrows():
        # pull values for the test county we're currently on
        current_county = row["county"]
        current_data = state_pre_for_comparison.loc[
            state_pre_for_comparison.county == current_county
        ]
        current_slope_mortality = current_data["slope_mortality"].values
        current_slope_shipment = current_data["slope_shipment"].values
        current_avg_population = current_data["avg_population"].values

        # calculate differences between current county and all control counties
        control_pre_for_comparison["slope_mortality_diff"] = (
            control_pre_for_comparison["slope_mortality"] - current_slope_mortality
        ).abs()
        control_pre_for_comparison["slope_shipment_diff"] = (
            control_pre_for_comparison["slope_shipment"] - current_slope_shipment
        ).abs()
        control_pre_for_comparison["avg_pop_diff"] = (
            control_pre_for_comparison["avg_population"] - current_avg_population
        ).abs()
        # sort by difference, then select the top n counties
        selected_control_counties = control_pre_for_comparison.sort_values(
            ["slope_mortality_diff", "slope_shipment_diff", "avg_pop_diff"]
        )[["state", "county"]][0:n]

        # add data for the 4 selected counties into the data frame we initiated
        additional_control_data = control_data[
            control_data["state"].isin(selected_control_counties["state"])
            & (control_data["county"].isin(selected_control_counties["county"]))
        ]
        selected_control = pd.concat([selected_control, additional_control_data])
        pass

    return selected_control


# a final function to sum it all up - to be called by graphing_function.py
def find_controls(state_pre, control_pre, control_data, n=2):
    state_pre = calulate_slope_by_county(state_pre)
    control_pre = calulate_slope_by_county(control_pre)
    state_pre = calculate_avg_population(state_pre)
    control_pre = calculate_avg_population(control_pre)
    selected_control_data = grab_control_counties(
        state_pre, control_pre, control_data, n
    )
    return selected_control_data

