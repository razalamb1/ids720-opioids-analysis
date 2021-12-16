from altair.vegalite.v4.schema.channels import StrokeWidth
import pandas as pd
import numpy as np
import altair as alt
import statsmodels.formula.api as smf
import altair_saver
from find_control_module import find_controls


def read_in(state, kind):
    state_data = pd.read_parquet(f"../20_intermediate_files/{state}_{kind}.parquet")
    control_data = pd.read_parquet(f"../20_intermediate_files/other_{kind}.parquet")
    return state_data, control_data


def prepare_data(state_data, control_data, state, kind):
    years = {"Florida": 2010, "Texas": 2007, "Washington": 2012}
    cut_year = years[state]
    category = f"category_{state[0:3].lower()}"
    control_data[category] = np.where(control_data["year"] >= cut_year, "post", "pre")
    control_data["type"] = "Control States"
    state_data["type"] = f"{state}"
    state_pre = state_data[state_data[category] == "pre"]
    state_post = state_data[state_data[category] == "post"]
    control_pre = control_data[control_data[category] == "pre"]
    control_post = control_data[control_data[category] == "post"]

    # now that we have state_pre, control_pre, we use them to find similar control counties
    # duplicates are allowed here, so that we weight more frequently selected counties more heavily
    selected_control_data = find_controls(
        kind, state_pre, control_pre, control_data, n=2
    )

    selected_control_pre = selected_control_data[
        selected_control_data[category] == "pre"
    ]
    selected_control_post = selected_control_data[
        selected_control_data[category] == "post"
    ]

    # now that we have selected control counties, build pre and post data sets
    pre = pd.concat([state_pre, selected_control_pre])
    post = pd.concat([state_post, selected_control_post])
    return pre, post, cut_year


def get_reg_fit(data, yvar, xvar, color, alpha=0.05):
    import statsmodels.formula.api as smf

    # Grid for predicted values
    x = data.loc[pd.notnull(data[yvar]), xvar]
    xmin = x.min()
    xmax = x.max()
    step = 1
    grid = np.arange(xmin, xmax + step, step)
    predictions = pd.DataFrame({xvar: grid})

    # Fit model, get predictions
    model = smf.ols(f"{yvar} ~ {xvar}", data=data).fit()
    model_predict = model.get_prediction(predictions[xvar])
    predictions[yvar] = model_predict.summary_frame()["mean"]
    predictions[["ci_low", "ci_high"]] = model_predict.conf_int(alpha=alpha)

    # Build chart
    reg = alt.Chart(predictions).mark_line().encode(x=xvar, y=yvar)
    ci = (
        alt.Chart(predictions)
        .mark_errorband(color=color)
        .encode(
            x=f"{xvar}:O",
            y=alt.Y("ci_low", title=""),
            y2="ci_high",
        )
    )
    chart = ci + reg
    return ci


def main_chart(data, kind, state):
    kind_coding = {
        "shipment": [
            f"Opioid Shipments per County per Year, {state} vs. Controls",
            "shipment_per_resident",
            "Opioid Shipments per Resident (MME)",
        ],
        "mortality": [
            f"Opioid Mortality per County per Year, {state} vs. Controls",
            "deaths_per_100k",
            "Opioid Mortality per 100,000 Residents)",
        ],
    }
    encodings = kind_coding[kind]
    line_mark = data[encodings[1]].median()
    data2 = pd.DataFrame(
        {
            "year": [2006, 2007, 2008, 2009, 2010, 2011, 2012],
            "line": [
                line_mark,
                line_mark,
                line_mark,
                line_mark,
                line_mark,
                line_mark,
                line_mark,
            ],
        }
    )
    invis_line = (
        alt.Chart(data2).mark_line(color="transparent").encode(x="year:O", y="line")
    )
    chart = (
        alt.Chart(data, title=encodings[0])
        .mark_point()
        .encode(
            x=alt.X("year:O", scale=alt.Scale(zero=False), title="Year"),
            y=alt.Y(encodings[1], scale=alt.Scale(zero=False), title=encodings[2]),
            color="type",
        )
    )
    regression = chart.transform_regression(
        "year", encodings[1], groupby=["type"]
    ).mark_line()
    ci_control = get_reg_fit(
        data[data["type"] == "Control States"], encodings[1], "year", "blue", alpha=0.05
    )
    ci_state = get_reg_fit(
        data[data["type"] == f"{state}"],
        encodings[1],
        "year",
        "orange",
        alpha=0.05,
    )
    return regression + ci_control + ci_state + invis_line
    pass


def get_plot_object(
    state,
    kind,
):
    state_data, control_data = read_in(state, kind)
    pre, post, cut_year = prepare_data(state_data, control_data, state, kind)
    data = pd.DataFrame({"a": [cut_year]})
    sep_line = (
        alt.Chart(data).mark_rule(color="black", strokeDash=[10, 10]).encode(x="a:O")
    )

    pre_chart = main_chart(pre, kind, state)
    post_chart = main_chart(post, kind, state)

    return (
        (pre_chart + post_chart + sep_line)
        .properties(height=500, width=1000)
        .configure_axis(labelFontSize=20, titleFontSize=20)
        .configure_title(fontSize=30)
        .configure_legend(titleFontSize=20, labelFontSize=18)
    )


def save_chart(state, kind):
    chart = get_plot_object(state, kind)
    altair_saver.save(chart, f"../30_results/{state}_{kind}.png")
    pass


if __name__ == "__main__":
    alt.data_transformers.disable_max_rows()
    save_chart("Florida", "mortality")
    save_chart("Florida", "shipment")
    save_chart("Washington", "mortality")
    save_chart("Texas", "mortality")
