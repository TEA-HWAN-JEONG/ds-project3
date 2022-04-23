from flask import Flask, render_template, request, redirect
import os
import sys
import pandas as pd
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from flask_app.model import get_model, get_dataframe, get_row, shap_plot

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        summoner = request.form["summoner"]
        return redirect(f'/{summoner}')
    else:
        return render_template("index.html")

@app.route('/<summoner>', methods = ['POST', 'GET'])
def index2(summoner):
    df = pd.read_csv('flask_app/data2.csv')
    data = get_dataframe(df, summoner)
    p_index = data.index
    html = data.to_html()
    if request.method == 'POST':
        i = request.form["button"]
        return redirect(f'/{summoner}/{i}')
    else:
        return render_template("index2.html", html=html, p_index=p_index, name=summoner)

@app.route('/<summoner>/<i>')
def index3(summoner, i):
    model, x_preprocess = get_model()
    row = get_row(x_preprocess, i)
    explainer, shap_values = shap_plot(model, row)
    return render_template("index3.html")

if __name__=='__main__':
    app.run(debug=True)