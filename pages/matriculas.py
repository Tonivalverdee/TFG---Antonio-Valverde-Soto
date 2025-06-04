import dash
from dash import html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

dash.register_page(__name__, path="/matriculas", name="Instituto")

with open(".venv/password.txt", "r") as f:
    db_password = f.read().strip()
engine = create_engine(f"mysql+pymysql://root:" + db_password + "@localhost/instituto")

card_style = {
    "borderRadius": "20px",
    "border": "none",
    "background": "#fff",
    "color": "#23253a",
    "boxShadow": "0 0 16px 0 rgba(76, 78, 100, 0.07)"
}

layout = html.Div([
    dcc.Interval(id="interval-matriculas", interval=3*1000, n_intervals=0),
    dbc.Button("← Volver al resumen", href="/", color="primary", outline=True, className="mb-4 fw-semibold", style={"borderRadius": "8px"}),
    html.H1("Gráficas de Matrículas", className="my-4 fw-bold text-center", style={"fontSize": "2.1rem", "color": "#6366f1"}),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Distribución de notas", className="card-title fw-semibold", style={"color": "#23253a"}),
                dcc.Graph(id="grafica-distribucion-notas-matriculas"),
            ])
        ], className="mb-4 shadow-sm", style=card_style), width=12),
    ]),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Top 10 alumnos con mejor nota media", className="card-title fw-semibold", style={"color": "#23253a"}),
                dcc.Graph(id="grafica-top-alumnos-matriculas"),
            ])
        ], className="mb-4 shadow-sm", style=card_style), width=12),
    ]),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Asignaturas con más matrículas", className="card-title fw-semibold", style={"color": "#23253a"}),
                dcc.Graph(id="grafica-asig-mas-matriculas-matriculas"),
            ])
        ], className="mb-4 shadow-sm", style=card_style), width=12),
    ]),
], style={"padding": "28px 0 0 0", "background": "#f4f6fb"})

@callback(
    Output("grafica-distribucion-notas-matriculas", "figure"),
    Output("grafica-top-alumnos-matriculas", "figure"),
    Output("grafica-asig-mas-matriculas-matriculas", "figure"),
    Input("interval-matriculas", "n_intervals")
)
def refrescar_graficas(n):
    df_notas = pd.read_sql("SELECT nota FROM matriculas", engine)
    df_top_alumnos = pd.read_sql("""
        SELECT alumnos.nombre AS Alumno, alumnos.apellidos AS Apellidos, ROUND(AVG(matriculas.nota),2) AS NotaMedia
        FROM alumnos
        JOIN matriculas ON alumnos.id = matriculas.id_alumno
        GROUP BY alumnos.id
        ORDER BY NotaMedia DESC
        LIMIT 10;
    """, engine)
    df_asig_mas_matriculas = pd.read_sql("""
        SELECT asignaturas.nombre AS Asignatura, COUNT(matriculas.id) AS NumMatriculas
        FROM asignaturas
        JOIN matriculas ON asignaturas.id = matriculas.id_asignatura
        GROUP BY asignaturas.id
        ORDER BY NumMatriculas DESC
        LIMIT 10;
    """, engine)

    df_notas["nota_redondeada"] = df_notas["nota"].round(1)
    serie = df_notas.groupby("nota_redondeada").size().reset_index(name="frecuencia")
    serie["suavizado"] = serie["frecuencia"].rolling(window=3, center=True, min_periods=1).mean()

    fig_linea = px.line(
        serie,
        x="nota_redondeada",
        y="suavizado",
        markers=False,
        title="Distribución de notas",
        labels={"nota_redondeada": "Nota", "suavizado": "Nº Matrículas"},
        line_shape="spline"
    )
    fig_linea.update_traces(line=dict(color="#6366f1", width=3))
    fig_linea.update_layout(
        plot_bgcolor="#fff",
        paper_bgcolor="#fff",
        font_color="#23253a",
        title_x=0.5,
        xaxis_title="Nota",
        yaxis_title="Nº Matrículas"
    )

    fig_top_alumnos = px.bar(
        df_top_alumnos,
        x="Alumno",
        y="NotaMedia",
        color="Alumno",
        title="Top 10 alumnos con mejor nota media",
        labels={"Alumno": "Alumno", "NotaMedia": "Nota media"},
        template="plotly_white"
    )
    fig_top_alumnos.update_layout(
        plot_bgcolor="#fff",
        paper_bgcolor="#fff",
        font_color="#23253a",
        title_x=0.5,
        xaxis_title="Alumno",
        yaxis_title="Nota media"
    )

    fig_asig_mas_matriculas = px.bar(
        df_asig_mas_matriculas,
        x="Asignatura",
        y="NumMatriculas",
        color="Asignatura",
        title="Asignaturas con más matrículas",
        labels={"Asignatura": "Asignatura", "NumMatriculas": "Nº Matrículas"},
        template="plotly_white"
    )
    fig_asig_mas_matriculas.update_layout(
        plot_bgcolor="#fff",
        paper_bgcolor="#fff",
        font_color="#23253a",
        title_x=0.5,
        xaxis_title="Asignatura",
        yaxis_title="Nº Matrículas"
    )

    return fig_linea, fig_top_alumnos, fig_asig_mas_matriculas
