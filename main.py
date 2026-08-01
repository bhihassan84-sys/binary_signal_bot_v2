from flask import Flask, render_template
from data import get_market_data

app = Flask(__name__)

@app.route("/")
def home():
    market = get_market_data()
    return render_template("index.html", market=market)

if __name__ == "__main__":
    app.run(debug=True)