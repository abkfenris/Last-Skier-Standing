import marimo

__generated_with = "0.11.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell
def _(pd):
    df = pd.read_json("https://ultrasignup.com/service/events.svc/results/118801/1/json?_search=false&nd=1739275858047&rows=9007199254740991&page=1&sidx=status%20asc%2C%20&sord=asc")
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell
def _():
    from collections import defaultdict
    return (defaultdict,)


@app.cell
def _(defaultdict, df):
    lap_participants = defaultdict(list)

    for _, row in df.iterrows():
        # print(row[1])
        laps = row["time"]
        for lap in range(1, laps + 1):
            lap_participants[lap].append(f"{row['firstname']} {row['lastname']}")

    lap_participants
    return lap, lap_participants, laps, row


@app.cell
def _(lap_participants, pd):
    laps_list = [{'hour': key, 'participant names': value, 'participants': len(value)} for key, value in lap_participants.items()]
    laps_df = pd.DataFrame(laps_list)
    laps_df
    return laps_df, laps_list


@app.cell
def _():
    import altair as alt
    return (alt,)


@app.cell
def _(alt, laps_df):
    alt.Chart(laps_df).mark_line().encode(alt.X("hour"), alt.Y("participants"))
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
