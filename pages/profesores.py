import dash
from dash import html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

dash.register_page(__name__, path="/profesores", name="Instituto")

with open(".venv/password.txt", "r") as f:
    db_password = f.read().strip()
engine = create_engine(f"mysql+pymysql://root:" + db_password + "@localhost/instituto")

card_style = {"borderRadius": "20px", "border": "none", "background": "#fff", "color": "#23253a", "boxShadow": "0 0 16px 0 rgba(76, 78, 100, 0.07)"}

layout = html.Div([
    dcc.Interval(id="interval-profesores", interval=3*1000, n_intervals=0),
    dbc.Button("← Volver al resumen", href="/", color="primary", outline=True, className="mb-4 fw-semibold", style={"borderRadius": "8px"}),
    html.H1("Gráficas de Profesores", className="my-4 fw-bold text-center", style={"fontSize": "2.1rem", "color": "#6366f1"}),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Asignaturas por profesor", className="card-title fw-semibold", style={"color": "#23253a"}),
                dcc.Graph(id="grafica-asig-por-profesor-profesores"),
            ])
        ], className="mb-4 shadow-sm", style=card_style), width=12),
    ]),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Nota media por profesor", className="card-title fw-semibold", style={"color": "#23253a"}),
                dcc.Graph(id="grafica-nota-por-profesor-profesores"),
            ])
        ], className="mb-4 shadow-sm", style=card_style), width=12),
    ]),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Cursos asignados por profesor", className="card-title fw-semibold", style={"color": "#23253a"}),
                dcc.Graph(id="grafica-cursos-por-profesor-profesores"),
            ])
        ], className="mb-4 shadow-sm", style=card_style), width=12),
    ]),
], style={"padding": "28px 0 0 0", "background": "#f4f6fb"})

@callback(
    Output("grafica-asig-por-profesor-profesores", "figure"),
    Output("grafica-nota-por-profesor-profesores", "figure"),
    Output("grafica-cursos-por-profesor-profesores", "figure"),
    Input("interval-profesores", "n_intervals")
)
def refrescar_graficas(n):
    df_asig_prof = pd.read_sql("""
        SELECT CONCAT(profesores.nombre, ' ', profesores.apellidos) AS Profesor, COUNT(asignaturas.id) AS Asignaturas
        FROM profesores
        LEFT JOIN asignaturas ON profesores.id = asignaturas.id_profesor
        GROUP BY profesores.id;
    """, engine)
    df_nota_prof = pd.read_sql("""
        SELECT CONCAT(p.nombre, ' ', p.apellidos) AS Profesor, ROUND(AVG(m.nota),2) AS NotaMedia
        FROM profesores p
        JOIN asignaturas a ON p.id = a.id_profesor
        JOIN matriculas m ON a.id = m.id_asignatura
        GROUP BY p.id;
    """, engine)
    df_cursos_prof = pd.read_sql("""
        SELECT CONCAT(p.nombre, ' ', p.apellidos) AS Profesor, COUNT(DISTINCT c.id) AS Cursos
        FROM profesores p
        JOIN asignaturas a ON p.id = a.id_profesor
        JOIN cursos c ON a.id_curso = c.id
        GROUP BY p.id;
    """, engine)

    fig1 = px.bar(df_asig_prof, x="Profesor", y="Asignaturas", color="Profesor", title="Asignaturas por profesor", labels={"Profesor": "Profesor", "Asignaturas": "Asignaturas"}, template="plotly_white")
    fig2 = px.bar(df_nota_prof, x="Profesor", y="NotaMedia", color="Profesor", title="Nota media por profesor", labels={"Profesor": "Profesor", "NotaMedia": "Nota media"}, template="plotly_white")
    fig3 = px.bar(df_cursos_prof, x="Profesor", y="Cursos", color="Profesor", title="Cursos asignados por profesor", labels={"Profesor": "Profesor", "Cursos": "Cursos"}, template="plotly_white")
    return fig1, fig2, fig3
