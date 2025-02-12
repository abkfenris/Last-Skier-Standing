import marimo

__generated_with = "0.11.2"
app = marimo.App(width="medium")


@app.cell
def _():
    from collections import defaultdict

    import marimo as mo
    import pandas as pd
    import altair as alt
    return alt, defaultdict, mo, pd


@app.cell
def _():
    result_urls = {
        "2020": "https://ultrasignup.com/service/events.svc/results/73799/1/json?_search=false&nd=1739358474053&rows=9007199254740991&page=1&sidx=status%20asc%2C%20&sord=asc",
        "2021": "https://ultrasignup.com/service/events.svc/results/81154/1/json?_search=false&nd=1739358502846&rows=9007199254740991&page=1&sidx=status%20asc%2C%20&sord=asc",
        "2022": "https://ultrasignup.com/service/events.svc/results/89227/1/json?_search=false&nd=1739358523451&rows=9007199254740991&page=1&sidx=status%20asc%2C%20&sord=asc",
        "2023": "https://ultrasignup.com/service/events.svc/results/98254/1/json?_search=false&nd=1739358550033&rows=9007199254740991&page=1&sidx=status%20asc%2C%20&sord=asc",
        "2024": "https://ultrasignup.com/service/events.svc/results/107643/1/json?_search=false&nd=1739358563650&rows=9007199254740991&page=1&sidx=status%20asc%2C%20&sord=asc",
        "2025": "https://ultrasignup.com/service/events.svc/results/118801/1/json?_search=false&nd=1739275858047&rows=9007199254740991&page=1&sidx=status%20asc%2C%20&sord=asc",
    }
    return (result_urls,)


@app.cell
def _():
    # Download JSON files
    # import requests

    # for _year, _url in result_urls.items():
    #     _r = requests.get(_url)
    #     with open(f"{_year}.json", "w") as _f:
    #         _f.write(_r.text)
    return


@app.cell
def _(pd, result_urls):
    yearly_results = {}

    # Load remote files
    # for _year, _url in result_urls.items():
    #     yearly_results[_year] = pd.read_json(_url)

    # Load local data
    for _year in result_urls:
        yearly_results[_year] = pd.read_json(f"{_year}.json")
    return (yearly_results,)


@app.cell
def _(defaultdict, yearly_results):
    yearly_lap_participants = {}

    for _year, _df in yearly_results.items():
        _lap_participants = defaultdict(list)
        for _, _row in _df.iterrows():
            _laps = _row["time"]
            for _lap in range(1, _laps + 1):
                _lap_participants[_lap].append(
                    f"{_row['firstname']} {_row['lastname']}"
                )
        yearly_lap_participants[_year] = _lap_participants
    return (yearly_lap_participants,)


@app.cell
def _(pd, yearly_lap_participants):
    _laps_list = []

    for _year, _lap_participants in yearly_lap_participants.items():
        for _key, _value in _lap_participants.items():
            _laps_list.append(
                {
                    "Year": _year,
                    "Hour": _key,
                    "Participants": len(_value),
                    "names": _value,
                    "Lap Ascent": 1150 * len(_value),
                }
            )
    yearly_laps = pd.DataFrame(_laps_list)
    return (yearly_laps,)


@app.cell
def _(yearly_laps):
    total_ascent = yearly_laps["Lap Ascent"].sum()
    return (total_ascent,)


@app.cell
def _(mo, total_ascent):
    mo.md(f"# {total_ascent:,} vertical feet of Last Skier Standing")
    return


@app.cell
def _(alt, mo, pd, yearly_laps):
    _lines = (
        alt.Chart(yearly_laps)
        .mark_line()
        .encode(alt.X("Hour"), alt.Y("Participants"), alt.Color("Year"))
        .interactive()
    )

    _night_hours = pd.DataFrame({"Sunset": [7, 31, 55], "Sunrise": [19, 43, 67]})

    _night_areas = (
        alt.Chart(_night_hours)
        .mark_rect(opacity=0.3)
        .encode(alt.X("Sunset"), alt.X2("Sunrise"))
    )

    _chart = _lines + _night_areas
    attrition_chart = mo.ui.altair_chart(_chart)
    return (attrition_chart,)


@app.cell
def _(alt, mo, yearly_laps):
    ascent_chart = mo.ui.altair_chart(
        alt.Chart(yearly_laps)
        .mark_bar()
        .encode(
            alt.X("Year"),
            alt.Y("sum(Lap Ascent)", title="Feet of Ascent"),
            alt.Color("Year"),
        )
    )
    return (ascent_chart,)


@app.cell
def _(ascent_chart, attrition_chart, mo):
    mo.hstack([attrition_chart, ascent_chart])
    return


@app.cell
def _(mo, yearly_laps, yearly_results):
    mo.accordion({"Yearly lap summary": yearly_laps, **yearly_results})
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
