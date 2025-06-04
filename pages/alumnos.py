import dash
from dash import html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

dash.register_page(__name__, path="/alumnos", name="Instituto")

with open(".venv/password.txt", "r") as f:
    db_password = f.read().strip()
engine = create_engine(f"mysql+pymysql://root:" + db_password + "@localhost/instituto")

card_style = {"borderRadius": "20px", "border": "none", "background": "#fff", "color": "#23253a", "boxShadow": "0 0 16px 0 rgba(76, 78, 100, 0.07)"}

layout = html.Div([
    dcc.Interval(id="interval-alumnos", interval=3*1000, n_intervals=0),
    dbc.Button("← Volver al resumen", href="/", color="primary", outline=True, className="mb-4 fw-semibold", style={"borderRadius": "8px"}),
    html.H1("Gráficas de Alumnos", className="my-4 fw-bold text-center", style={"fontSize": "2.1rem", "color": "#6366f1"}),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Alumnos por curso", className="card-title fw-semibold", style={"color": "#23253a"}),
                dcc.Graph(id="grafica-alumnos-por-curso-alumnos"),
            ])
        ], className="mb-4 shadow-sm", style=card_style), md=4),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Alumnos por año de nacimiento", className="card-title fw-semibold", style={"color": "#23253a"}),
                dcc.Graph(id="grafica-alumnos-por-anio-alumnos"),
            ])
        ], className="mb-4 shadow-sm", style=card_style), md=4),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Distribución de edades", className="card-title fw-semibold", style={"color": "#23253a"}),
                dcc.Graph(id="grafica-alumnos-edades-alumnos"),
            ])
        ], className="mb-4 shadow-sm", style=card_style), md=4),
    ]),
], style={"padding": "28px 0 0 0", "background": "#f4f6fb"})

@callback(
    Output("grafica-alumnos-por-curso-alumnos", "figure"),
    Output("grafica-alumnos-por-anio-alumnos", "figure"),
    Output("grafica-alumnos-edades-alumnos", "figure"),
    Input("interval-alumnos", "n_intervals")
)
def refrescar_graficas(n):
    df_alumnos_curso = pd.read_sql("""
        SELECT cursos.nombre AS Curso, COUNT(alumnos.id) AS Alumnos
        FROM alumnos
        JOIN cursos ON alumnos.id_curso = cursos.id
        GROUP BY cursos.nombre;
    """, engine)
    df_alumnos_anio = pd.read_sql("""
        SELECT YEAR(fecha_nacimiento) AS Año, COUNT(*) AS Alumnos
        FROM alumnos
        GROUP BY Año
        ORDER BY Año;
    """, engine)
    df_edades = pd.read_sql("""
        SELECT TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE()) AS Edad, COUNT(*) AS Alumnos
        FROM alumnos
        GROUP BY Edad
        ORDER BY Edad;
    """, engine)

    fig1 = px.bar(df_alumnos_curso, x="Curso", y="Alumnos", color="Curso", title="Número de alumnos por curso", labels={"Curso": "Curso", "Alumnos": "Alumnos"}, template="plotly_white")
    fig2 = px.bar(df_alumnos_anio, x="Año", y="Alumnos", color=df_alumnos_anio["Año"].astype(str), title="Alumnos por año de nacimiento", labels={"Año": "Año", "Alumnos": "Alumnos", "color": "Año"}, template="plotly_white")
    fig3 = px.bar(df_edades, x="Edad", y="Alumnos", color=df_edades["Edad"].astype(str), title="Distribución de edades", labels={"Edad": "Edad", "Alumnos": "Alumnos", "color": "Edad"}, template="plotly_white")
    return fig1, fig2, fig3
