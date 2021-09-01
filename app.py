from flask import Flask, render_template, request, flash
from bs4 import BeautifulSoup
import pandas as pd


app = Flask(__name__)
app.secret_key = "b'bi\xa8|\x02\x01\xea\t\xc9&|\xd8"


skater_results = pd.DataFrame()
url = "https://www.hockey-reference.com/leagues/NHL_2021_skaters.html"
df = pd.read_html(url, header=1)[0]
skater_results = skater_results.append(df, sort=False)

skater_results = skater_results[~skater_results["Age"].str.contains("Age")]
skater_results = skater_results.reset_index(drop=True)

skater_names = list(skater_results["Player"].values)


goalie_results = pd.DataFrame()
url = "https://www.hockey-reference.com/leagues/NHL_2021_goalies.html"
df = pd.read_html(url, header=1)[0]
goalie_results = goalie_results.append(df, sort=False)

goalie_results = goalie_results[~goalie_results["Age"].str.contains("Age")]
goalie_results = goalie_results.reset_index(drop=True)

goalie_names = list(goalie_results["Player"].values)


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route("/compare/<player_type>", methods=["GET", "POST"])
def compare_players(player_type):
    if request.method == "POST":
        if player_type == "skaters":
            if validate_players(request.form["player1"], request.form["player2"], skater_names):
                return "All players are valid."
            else:
                flash("One or more players were invalid.")
                return render_template("compare.html", player_names=skater_names)
        else:
            if validate_players(request.form["player1"], request.form["player2"], goalie_names):
                return "All players are valid."
            else:
                flash("One or more players were invalid.")
                return render_template("compare.html", player_names=goalie_names)

    else:
        if player_type == "skaters":
            return render_template("compare.html", player_names=skater_names)
        else:
            return render_template("compare.html", player_names=goalie_names)


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


def validate_players(player1, player2, players):
    return player1 in players and player2 in players
