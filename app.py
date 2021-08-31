from flask import flask, render_template, request
from bs4 import beautiful_soup
import requests
import lxml
import pandas as pd


app = flask(__name__)


skater_results = pd.data_frame()
url = "https://www.hockey-reference.com/leagues/nhl_2021_skaters.html"
df = pd.read_html(url, header=1)[0]
skater_results = skater_results.append(df, sort=false)

skater_results = skater_results[~skater_results["age"].str.contains("age")]
skater_results = skater_results.reset_index(drop=true)


goalie_results = pd.data_frame()
url = "https://www.hockey-reference.com/leagues/nhl_2021_goalies.html"
df = pd.read_html(url, header=1)[0]
goalie_results = goalie_results.append(df, sort=false)

goalie_results = goalie_results[~goalie_results["age"].str.contains("age")]
goalie_results = goalie_results.reset_index(drop=true)


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route("/compare/skaters", methods=["get", "post"])
@app.route("/compare/goalies", methods=["get", "post"])
def compare_players():
    if request.method == "post":
        return 0
    else:
        render_template("compare.html")


@app.route("/stats/skaters")
def skater_stats():
    return render_template(
        "stats.html", column_names=skater_results.columns.values, row_data=list(skater_results.values.tolist()), zip=zip
    )


@app.route("/stats/goalies")
def goalies_stats():
    return render_template(
        "stats.html", column_names=goalie_results.columns.values, row_data=list(goalie_results.values.tolist()), zip=zip
    )


@app.route("/about")
def about_page():
    return render_template("about.html")
