import pickle
import pandas as pd
import shap
import streamlit as st
import matplotlib.pyplot as plt

def get_model():
    with open("flask_app/model.pkl", "rb") as pickle_file:
        clf = pickle.load(pickle_file)

    df = pd.read_csv('flask_app/data2.csv')

    target = 'result'
    x = df.drop(target, axis= 1)

    model = clf.named_steps['gradientboostingclassifier']
    x_preprocess = clf.named_steps['ordinalencoder'].transform(x)
    return model, x_preprocess

def get_dataframe(df, name):
    return df[df['summoners'] == name]

def get_row(x_preprocess, i):
    return x_preprocess.iloc[[i]]

def shap_plot(model, row):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(row)

    shap.initjs()
    shap.force_plot(
        base_value=explainer.expected_value, 
        shap_values=shap_values,
        features=row,
        show=False,
        matplotlib=True
    ).savefig('flask_app/templates/shap.png')
    return explainer, shap_values