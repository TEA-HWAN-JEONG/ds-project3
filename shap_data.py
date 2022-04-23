import shap
from shap.plots._force_matplotlib import draw_additive_plot
from flask import Flask
from flask_app.model import give_shap_plot

app = Flask(__name__)

@app.route('/')
def displayshap():

    explainer, shap_values = give_shap_plot()

    def _force_plot_html(explainer, shap_values):
        force_plot = shap.plots.force(shap_values, matplotlib=False)
        shap_html = f"<head>{shap.getjs()}</head><body>{force_plot.html()}</body>"
        return shap_html

    shap_plots = _force_plot_html(explainer, shap_values)
    return shap.render_template('index.html', shap_plots = shap_plots)

if __name__ == '__main__':
    app.run(debug=True)
