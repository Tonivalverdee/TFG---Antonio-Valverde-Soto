import dash
from dash import html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

dash.register_page(__name__, path="/asignaturas", name="Instituto")

with open(".venv/password.txt", "r") as f:
    db_password = f.read().strip()
engine = create_engine(f"mysql+pymysql://root:" + db_password + "@localhost/instituto")

card_style = {"borderRadius": "20px", "border": "none", "background": "#fff", "color": "#23253a", "boxShadow": "0 0 16px 0 rgba(76, 78, 100, 0.07)"}

layout = html.Div([
    dcc.Interval(id="interval-asignaturas", interval=3*1000, n_intervals=0),
    dbc.Button("← Volver al resumen", href="/", color="primary", outline=True, className="mb-4 fw-semibold", style={"borderRadius": "8px"}),
    html.H1("Gráficas de Asignaturas", className="my-4 fw-bold text-center", style={"fontSize": "2.1rem", "color": "#6366f1"}),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Alumnos por asignatura", className="card-title fw-semibold", style={"color": "#23253a"}),
                dcc.Graph(id="grafica-alumnos-por-asignatura-asignaturas"),
            ])
        ], className="mb-4 shadow-sm", style=card_style), width=12),
    ]),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Nota media por asignatura", className="card-title fw-semibold", style={"color": "#23253a"}),
                dcc.Graph(id="grafica-nota-por-asignatura-asignaturas"),
            ])
        ], className="mb-4 shadow-sm", style=card_style), width=12),
    ]),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Asignaturas por curso", className="card-title fw-semibold", style={"color": "#23253a"}),
                dcc.Graph(id="grafica-asignaturas-por-curso-asignaturas"),
            ])
        ], className="mb-4 shadow-sm", style=card_style), width=12),
    ]),
], style={"padding": "28px 0 0 0", "background": "#f4f6fb"})

@callback(
    Output("grafica-alumnos-por-asignatura-asignaturas", "figure"),
    Output("grafica-nota-por-asignatura-asignaturas", "figure"),
    Output("grafica-asignaturas-por-curso-asignaturas", "figure"),
    Input("interval-asignaturas", "n_intervals")
)
def refrescar_graficas(n):
    df_alum_asig = pd.read_sql("""
        SELECT asignaturas.nombre AS Asignatura, COUNT(matriculas.id_alumno) AS Alumnos
        FROM asignaturas
        LEFT JOIN matriculas ON asignaturas.id = matriculas.id_asignatura
        GROUP BY asignaturas.nombre;
    """, engine)
    df_nota_asig = pd.read_sql("""
        SELECT asignaturas.nombre AS Asignatura, ROUND(AVG(matriculas.nota),2) AS NotaMedia
        FROM asignaturas
        JOIN matriculas ON asignaturas.id = matriculas.id_asignatura
        GROUP BY asignaturas.nombre;
    """, engine)
    df_asig_curso = pd.read_sql("""
        SELECT cursos.nombre AS Curso, COUNT(asignaturas.id) AS Asignaturas
        FROM cursos
        LEFT JOIN asignaturas ON cursos.id = asignaturas.id_curso
        GROUP BY cursos.nombre;
    """, engine)

    fig1 = px.bar(df_alum_asig, x="Asignatura", y="Alumnos", color="Asignatura", title="Alumnos por asignatura", labels={"Asignatura": "Asignatura", "Alumnos": "Alumnos"}, template="plotly_white")
    fig2 = px.bar(df_nota_asig, x="Asignatura", y="NotaMedia", color="Asignatura", title="Nota media por asignatura", labels={"Asignatura": "Asignatura", "NotaMedia": "Nota media"}, template="plotly_white")
    fig3 = px.bar(df_asig_curso, x="Curso", y="Asignaturas", color="Curso", title="Asignaturas por curso", labels={"Curso": "Curso", "Asignaturas": "Asignaturas"}, template="plotly_white")
    return fig1, fig2, fig3
