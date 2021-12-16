import pandas as pd
import numpy as np
import altair as alt
import statsmodels.formula.api as smf
import altair_saver


def read_in(state, kind):
    state_data = pd.read_parquet(f"../20_intermediate_files/{state}_{kind}.parquet")
    return state_data


def prepare_data(state_data, state):
    years = {"Florida": 2010, "Texas": 2007, "Washington": 2011}
    cut_year = years[state]
    return cut_year


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
    reg = alt.Chart(predictions).mark_line(color="orange").encode(x=xvar + ":O", y=yvar)
    ci = (
        alt.Chart(predictions)
        .mark_errorband(color="orange")
        .encode(
            x=f"{xvar}:O",
            y=alt.Y("ci_low", title=""),
            y2="ci_high",
        )
    )
    chart = ci + reg
    return chart


def main_chart(data, kind, state):
    data["Pre Post"] = data[f"category_{state[0:3].lower()}"]
    kind_coding = {
        "shipment": [
            f"Opioid Shipments per County per Year in {state}",
            "shipment_per_resident",
            "Opioid Shipments per Resident (MME)",
        ],
        "mortality": [
            f"Opioid Mortality per County per Year in {state}",
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
            color=alt.Color("Pre Post", legend=None),
        )
    )
    regression = chart.transform_regression(
        "year", encodings[1], groupby=["Pre Post"]
    ).mark_line(color="yellow")
    ci_before = get_reg_fit(
        data[data["Pre Post"] == "pre"],
        encodings[1],
        "year",
        "orange",
        alpha=0.05,
    )
    ci_after = get_reg_fit(
        data[data[f"category_{state[0:3].lower()}"] == "post"],
        encodings[1],
        "year",
        "blue",
        alpha=0.05,
    )
    return regression + ci_before + ci_after + invis_line
    pass


def get_plot_object(
    state,
    kind,
):
    state_data = read_in(state, kind)
    cut_year = prepare_data(state_data, state)
    data = pd.DataFrame({"a": [cut_year]})
    sep_line = (
        alt.Chart(data).mark_rule(color="black", strokeDash=[10, 10]).encode(x="a:O")
    )

    chart = main_chart(state_data, kind, state)
    return (
        (chart + sep_line)
        .properties(height=500, width=1000)
        .configure_axis(labelFontSize=20, titleFontSize=20)
        .configure_title(fontSize=30)
        .configure_legend(titleFontSize=20, labelFontSize=18)
    )


def save_chart(state, kind):
    chart = get_plot_object(state, kind)
    altair_saver.save(chart, f"../30_results/prepost_{state}_{kind}.png")
    pass


if __name__ == "__main__":
    alt.data_transformers.disable_max_rows()
    save_chart("Florida", "mortality")
    save_chart("Florida", "shipment")
    save_chart("Washington", "mortality")
    save_chart("Texas", "mortality")
