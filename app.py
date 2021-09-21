from flask import Flask, json, render_template, request, flash
from bs4 import BeautifulSoup
import pandas as pd


app = Flask(__name__)
app.secret_key = "b133057c1b014cd945db7a8207501732a3fbf5a6c97fce8f"


skater_results = pd.DataFrame()
url = "https://www.hockey-reference.com/leagues/NHL_2021_skaters.html"
df = pd.read_html(url, header=1)[0]
skater_results = skater_results.append(df, sort=False)

skater_results = skater_results[~skater_results["Age"].str.contains("Age")]
skater_results = skater_results.reset_index(drop=True)

skater_teams = skater_results["Tm"].values

just_skater_names = skater_results["Player"].values
skater_names_and_teams = []
for i in range(0, len(just_skater_names)):
    player = just_skater_names[i] + " - " + skater_teams[i]
    skater_names_and_teams.append(player)

skaters_and_reference_index = dict(zip(skater_names_and_teams, skater_results.index.tolist()))


goalie_results = pd.DataFrame()
url = "https://www.hockey-reference.com/leagues/NHL_2021_goalies.html"
df = pd.read_html(url, header=1)[0]
goalie_results = goalie_results.append(df, sort=False)

goalie_results = goalie_results[~goalie_results["Age"].str.contains("Age")]
goalie_results = goalie_results.reset_index(drop=True)

goalie_teams = goalie_results["Tm"].values

just_goalie_names = goalie_results["Player"].values
goalie_names_and_teams = []
for i in range(0, len(just_goalie_names)):
    player = just_goalie_names[i] + " - " + goalie_teams[i]
    goalie_names_and_teams.append(player)

goalies_and_reference_index = dict(zip(goalie_names_and_teams, skater_results.index.tolist()))


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route("/compare/<player_type>", methods=["GET", "POST"])
def compare_players(player_type):
    if request.method == "POST":
        if player_type == "skaters":
            if validate_players(request.form["player1"], request.form["player2"], skaters_and_reference_index):
                player1_id = skaters_and_reference_index[request.form["player1"]]
                player2_id = skaters_and_reference_index[request.form["player2"]]

                player1_stats = skater_results.loc[skater_results["Player"] == just_skater_names[player1_id]].to_json()
                player2_stats = skater_results.loc[skater_results["Player"] == just_skater_names[player2_id]].to_json()

                player1_json = json.loads(player1_stats)
                player2_json = json.loads(player2_stats)
                return render_template(
                    "compare.html",
                    player_names=skaters_and_reference_index.keys(),
                    player1=player1_json,
                    player2=player2_json,
                    id1=player1_id,
                    id2=player2_id,
                )
            else:
                flash("One or more players were invalid.")
                return render_template(
                    "compare.html", player_names=skaters_and_reference_index.keys(), player1={}, player2={}
                )
        else:
            if validate_players(request.form["player1"], request.form["player2"], goalies_and_reference_index):
                player1_id = goalies_and_reference_index[request.form["player1"]]
                player2_id = goalies_and_reference_index[request.form["player2"]]

                player1_stats = goalie_results.loc[goalie_results["Player"] == just_goalie_names[player1_id]].to_json()
                player2_stats = goalie_results.loc[goalie_results["Player"] == just_goalie_names[player2_id]].to_json()

                player1_json = json.loads(player1_stats)
                player2_json = json.loads(player2_stats)
                return render_template(
                    "compare.html",
                    player_names=goalies_and_reference_index.keys(),
                    player1=player1_json,
                    player2=player2_json,
                    id1=player1_id,
                    id2=player2_id,
                )
            else:
                flash("One or more players were invalid.")
                return render_template(
                    "compare.html", player_names=goalies_and_reference_index.keys(), player1={}, player2={}
                )

    else:
        if player_type == "skaters":
            return render_template(
                "compare.html", player_names=skaters_and_reference_index.keys(), player1={}, player2={}
            )
        else:
            return render_template(
                "compare.html", player_names=goalies_and_reference_index.keys(), player1={}, player2={}
            )


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
