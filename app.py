from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd


app = Flask(__name__)


@app.route("/")
def index():
    source = requests.get("https://www.hockey-reference.com/leagues/NHL_2021_skaters.html").text
    soup = BeautifulSoup(source, "lxml")

    result = pd.DataFrame()
    url = "https://www.hockey-reference.com/leagues/NHL_2021_skaters.html"
    df = pd.read_html(url, header=1)[0]
    result = result.append(df, sort=False)

    result = result[~result["Age"].str.contains("Age")]
    result = result.reset_index(drop=True)

    table = pd.DataFrame.to_html(result)

    return render_template("index.html", tables=[result.to_html(classes="data")], titles=result.columns.values)
