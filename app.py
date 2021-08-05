from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
