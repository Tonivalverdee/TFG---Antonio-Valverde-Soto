import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Datos de ejemplo
df = pd.DataFrame({
    "Fecha": pd.date_range("2024-01-01", periods=10),
    "Temperatura": [22, 23, 24, 26, 25, 24, 23, 22, 21, 20]
})

# Crear app Dash
app = dash.Dash(__name__)

fig = px.line(df, x="Fecha", y="Temperatura", title="Temperatura diaria")

app.layout = html.Div([
    html.H1("Gráfica de Temperatura"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    print("Arrancando Dash...")
    app.run(debug=True)
    print("Dash arrancado.")
