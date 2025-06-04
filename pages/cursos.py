import dash
from dash import html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

dash.register_page(__name__, path="/cursos", name="Instituto")

with open(".venv/password.txt", "r") as f:
    db_password = f.read().strip()
engine = create_engine(f"mysql+pymysql://root:" + db_password + "@localhost/instituto")

card_style = {"borderRadius": "20px", "border": "none", "background": "#fff", "color": "#23253a", "boxShadow": "0 0 16px 0 rgba(76, 78, 100, 0.07)"}

layout = html.Div([
    dcc.Interval(id="interval-cursos", interval=3*1000, n_intervals=0),
    dbc.Button("← Volver al resumen", href="/", color="primary", outline=True, className="mb-4 fw-semibold", style={"borderRadius": "8px"}),
    html.H1("Gráficas de Cursos", className="my-4 fw-bold text-center", style={"fontSize": "2.1rem", "color": "#6366f1"}),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Asignaturas por curso", className="card-title fw-semibold", style={"color": "#23253a"}),
                dcc.Graph(id="grafica-asig-por-curso-cursos"),
            ])
        ], className="mb-4 shadow-sm", style=card_style), md=4),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Nota media de los alumnos por curso", className="card-title fw-semibold", style={"color": "#23253a"}),
                dcc.Graph(id="grafica-nota-por-curso-cursos"),
            ])
        ], className="mb-4 shadow-sm", style=card_style), md=4),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Alumnos por curso", className="card-title fw-semibold", style={"color": "#23253a"}),
                dcc.Graph(id="grafica-alumnos-por-curso-cursos"),
            ])
        ], className="mb-4 shadow-sm", style=card_style), md=4),
    ]),
], style={"padding": "28px 0 0 0", "background": "#f4f6fb"})

@callback(
    Output("grafica-asig-por-curso-cursos", "figure"),
    Output("grafica-nota-por-curso-cursos", "figure"),
    Output("grafica-alumnos-por-curso-cursos", "figure"),
    Input("interval-cursos", "n_intervals")
)
def refrescar_graficas(n):
    df_asig_curso = pd.read_sql("""
        SELECT cursos.nombre AS Curso, COUNT(asignaturas.id) AS Asignaturas
        FROM cursos
        LEFT JOIN asignaturas ON cursos.id = asignaturas.id_curso
        GROUP BY cursos.nombre;
    """, engine)
    df_media_curso = pd.read_sql("""
        SELECT cursos.nombre AS Curso, ROUND(AVG(matriculas.nota),2) AS NotaMedia
        FROM matriculas
        JOIN asignaturas ON matriculas.id_asignatura = asignaturas.id
        JOIN cursos ON asignaturas.id_curso = cursos.id
        GROUP BY cursos.nombre;
    """, engine)
    df_alumnos_curso = pd.read_sql("""
        SELECT cursos.nombre AS Curso, COUNT(alumnos.id) AS Alumnos
        FROM alumnos
        JOIN cursos ON alumnos.id_curso = cursos.id
        GROUP BY cursos.nombre;
    """, engine)

    fig1 = px.bar(df_asig_curso, x="Curso", y="Asignaturas", color="Curso", title="Número de asignaturas por curso", labels={"Curso": "Curso", "Asignaturas": "Asignaturas"}, template="plotly_white")
    fig2 = px.bar(df_media_curso, x="Curso", y="NotaMedia", color="Curso", title="Nota media por curso", labels={"Curso": "Curso", "NotaMedia": "Nota media"}, template="plotly_white")
    fig3 = px.pie(df_alumnos_curso, names="Curso", values="Alumnos", color="Curso", title="Número de alumnos por curso", labels={"Curso": "Curso", "Alumnos": "Alumnos"}, template="plotly_white")
    return fig1, fig2, fig3
