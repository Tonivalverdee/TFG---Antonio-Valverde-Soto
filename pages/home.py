import dash
from dash import html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

dash.register_page(__name__, path="/", name="Instituto", order=0)

with open(".venv/password.txt", "r") as f:
    db_password = f.read().strip()
engine = create_engine(f"mysql+pymysql://root:" + db_password + "@localhost/instituto")

card_style = {"borderRadius": "20px", "border": "none", "background": "#fff", "color": "#23253a", "boxShadow": "0 0 16px 0 rgba(76, 78, 100, 0.07)"}
kpi_style = {"fontSize": "2.4rem", "fontWeight": "bold", "color": "#6366f1"}

layout = html.Div([
    dcc.Interval(id="interval-home", interval=3*1000, n_intervals=0),
    html.H1("Resumen del Instituto", className="my-4 fw-bold text-center", style={"fontSize": "2.4rem", "color": "#6366f1"}),
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.Div("Alumnos", className="fw-semibold"),
            html.Div(id="kpi-alumnos", style=kpi_style)
        ]), className="mb-4", style=card_style), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.Div("Profesores", className="fw-semibold"),
            html.Div(id="kpi-profesores", style=kpi_style)
        ]), className="mb-4", style=card_style), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.Div("Cursos", className="fw-semibold"),
            html.Div(id="kpi-cursos", style=kpi_style)
        ]), className="mb-4", style=card_style), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.Div("Nota media global", className="fw-semibold"),
            html.Div(id="kpi-notamedia", style=kpi_style)
        ]), className="mb-4", style=card_style), md=3),
    ], className="mb-2"),
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Alumnos por curso", className="card-title fw-semibold"),
            dcc.Graph(id="grafica-alumnos-por-curso-home")
        ]), style=card_style), md=4),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Nota media por curso", className="card-title fw-semibold"),
            dcc.Graph(id="grafica-nota-por-curso-home")
        ]), style=card_style), md=4),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Asignaturas por curso", className="card-title fw-semibold"),
            dcc.Graph(id="grafica-asig-por-curso-home")
        ]), style=card_style), md=4),
    ])
], style={"padding": "28px 0 0 0", "background": "#f4f6fb"})

@callback(
    Output("kpi-alumnos", "children"),
    Output("kpi-profesores", "children"),
    Output("kpi-cursos", "children"),
    Output("kpi-notamedia", "children"),
    Output("grafica-alumnos-por-curso-home", "figure"),
    Output("grafica-nota-por-curso-home", "figure"),
    Output("grafica-asig-por-curso-home", "figure"),
    Input("interval-home", "n_intervals")
)
def refrescar_home(n):
    n_alumnos = pd.read_sql("SELECT COUNT(*) AS n FROM alumnos", engine).iloc[0,0]
    n_cursos = pd.read_sql("SELECT COUNT(*) AS n FROM cursos", engine).iloc[0,0]
    n_profesores = pd.read_sql("SELECT COUNT(*) AS n FROM profesores", engine).iloc[0,0]
    nota_media = pd.read_sql("SELECT ROUND(AVG(nota),2) AS media FROM matriculas", engine).iloc[0,0]

    df_alum_curso = pd.read_sql("""
        SELECT cursos.nombre AS Curso, COUNT(alumnos.id) AS Alumnos
        FROM alumnos
        JOIN cursos ON alumnos.id_curso = cursos.id
        GROUP BY cursos.nombre;
    """, engine)
    df_media_curso = pd.read_sql("""
        SELECT cursos.nombre AS Curso, ROUND(AVG(matriculas.nota),2) AS NotaMedia
        FROM matriculas
        JOIN asignaturas ON matriculas.id_asignatura = asignaturas.id
        JOIN cursos ON asignaturas.id_curso = cursos.id
        GROUP BY cursos.nombre;
    """, engine)
    df_asig_curso = pd.read_sql("""
        SELECT cursos.nombre AS Curso, COUNT(asignaturas.id) AS Asignaturas
        FROM cursos
        LEFT JOIN asignaturas ON cursos.id = asignaturas.id_curso
        GROUP BY cursos.nombre;
    """, engine)

    fig1 = px.bar(df_alum_curso, x="Curso", y="Alumnos", color="Curso", title="Alumnos por curso", labels={"Curso": "Curso", "Alumnos": "Alumnos"}, template="plotly_white")
    fig2 = px.bar(df_media_curso, x="Curso", y="NotaMedia", color="Curso", title="Nota media por curso", labels={"Curso": "Curso", "NotaMedia": "Nota media"}, template="plotly_white")
    fig3 = px.pie(df_asig_curso, names="Curso", values="Asignaturas", color="Curso", title="Asignaturas por curso", labels={"Curso": "Curso", "Asignaturas": "Asignaturas"}, template="plotly_white")

    return n_alumnos, n_profesores, n_cursos, nota_media, fig1, fig2, fig3
