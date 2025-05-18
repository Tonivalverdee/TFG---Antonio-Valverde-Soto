# Para ejecutar este programa, asegúrate de tener instaladas las librerías necesarias:
# pip install -r librerias.txt

# Lo primero que hacemos es importar las librerías necesarias para la ejecución del programa
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
from dash.dependencies import Input, Output
from cryptography.fernet import Fernet
import getpass
import os
from sqlalchemy.exc import OperationalError

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    while True:
        db_password = getpass.getpass("Introduce la contraseña de MySQL: ")
        try:
            engine = create_engine(f"mysql+pymysql://root:{db_password}@localhost/instituto")
            with engine.connect() as conn:
                print("✅ Contraseña introducida correctamente.")
            break
        except OperationalError:
            print("❌ Contraseña incorrecta. Inténtalo de nuevo.")

# La conexión ya se ha establecido correctamente dentro del bloque principal

# Creamos una función para obtener los datos de la base de datos
def obtener_datos(query):
    return pd.read_sql(query, engine)

# Creamos la app de Dash
app = dash.Dash(__name__)
app.title = "Gráficas del Instituto"

# Realizamos las consultas SQL que vamos a utilizar para obtener los datos
queries = {
    "alumnos_por_curso": '''
        SELECT c.nombre AS Curso, COUNT(a.id) AS Alumnos
        FROM alumnos a
        JOIN cursos c ON a.id_curso = c.id
        GROUP BY c.nombre;
    ''',
    "asignaturas_por_profesor": '''
        SELECT CONCAT(p.nombre, ' ', p.apellidos) AS Profesor, COUNT(asig.id) AS Asignaturas
        FROM profesores p
        JOIN asignaturas asig ON p.id = asig.id_profesor
        GROUP BY Profesor;
    ''',
    "nota_media_por_curso": '''
        SELECT c.nombre AS Curso, ROUND(AVG(m.nota), 2) AS Media
        FROM matriculas m
        JOIN alumnos a ON m.id_alumno = a.id
        JOIN cursos c ON a.id_curso = c.id
        GROUP BY c.nombre;
    ''',
    "alumnos_por_asignatura": '''
        SELECT asig.nombre AS Asignatura, COUNT(m.id_alumno) AS Alumnos
        FROM matriculas m
        JOIN asignaturas asig ON m.id_asignatura = asig.id
        GROUP BY asig.nombre;
    ''',
    "asignaturas_por_curso": '''
        SELECT c.nombre AS Curso,
        COUNT(DISTINCT s.id) AS Asignaturas
        FROM cursos c
        LEFT JOIN asignaturas s ON s.id_curso = c.id
        GROUP BY c.nombre;
    ''',
    "nota_media_por_asignatura": '''
        SELECT cursos.nombre AS Curso, COUNT(DISTINCT matriculas.id_alumno) AS num_alumnos
        FROM matriculas
        JOIN asignaturas ON matriculas.id_asignatura = asignaturas.id
        JOIN cursos ON asignaturas.id_curso = cursos.id
        GROUP BY cursos.nombre;
    '''
}

# Deinimos los colores que vamos a utilizar en las gráficas en una variable
colores = {
    "alumnos": ["#FFADAD", "#FFD6A5", "#FDFFB6", "#CAFFBF"],
    "profesores": ["#9BF6FF", "#A0C4FF", "#BDB2FF", "#FFC6FF", "#FFFFFC", "#FDCBCA", "#FEE1E8", "#F4D1AE", "#D3F8E2"],
    "nota_media": ["#E4C1F9", "#FAEDCB", "#C9F2C7", "#B5EAD7"],
    "asignaturas": ["#FFDAC1", "#E2F0CB", "#FFCBC1", "#C2FAFF", "#E0BBE4", "#FFDFD3", "#FFFACD", "#FFDEE9", "#E0F7FA", "#F0F4C3", "#C8E6C9", "#FFCCBC", "#D1C4E9", "#F8BBD0", "#DCEDC8"],
    "asignaturas_curso": ["#F0E5DE", "#FFD1DC", "#B5FFF9", "#FFF1C9"],
    "nota_media_asig": ["#C1FBA4", "#FFBCBC", "#B5EAD7", "#FFDAC1"]
}

# Ahora, definimos la estructura de la página, además con dcc.Interval vamos a actualizar las gráficas cada 3 segundos
app.layout = html.Div([
    html.H1("Gráficas del Instituto", style={"textAlign": "center"}),
    dcc.Interval(id="interval", interval=3*1000, n_intervals=0),
    html.Div([
        dcc.Graph(id="grafica-alumnos"),
        dcc.Graph(id="quesito-alumnos"),
        dcc.Graph(id="grafica-profesores"),
        dcc.Graph(id="quesito-profesores"),
        dcc.Graph(id="grafica-nota-media"),
        dcc.Graph(id="quesito-nota-media"),
        dcc.Graph(id="grafica-alumnos-asignatura"),
        dcc.Graph(id="quesito-alumnos-asignatura"),
        dcc.Graph(id="grafica-asignaturas-curso"),
        dcc.Graph(id="quesito-asignaturas-curso"),
        dcc.Graph(id="grafica-nota-media-asignatura"),
        dcc.Graph(id="quesito-nota-media-asignatura")
    ], id="contenedor-graficas", className="graph-container")
])

# Eliminado el uso de archivos para la contraseña; ahora se introduce en tiempo de ejecución

@app.callback(Output("grafica-alumnos", "figure"), Input("interval", "n_intervals"))
def actualizar_grafica_alumnos(n):
    df = obtener_datos(queries["alumnos_por_curso"])
    return px.bar(df, x="Curso", y="Alumnos", color="Curso",
        color_discrete_sequence=colores["alumnos"],
        title="Alumnos por Curso")

@app.callback(Output("quesito-alumnos", "figure"), Input("interval", "n_intervals"))
def actualizar_quesito_alumnos(n):
    df = obtener_datos(queries["alumnos_por_curso"])
    return px.pie(df, names="Curso", values="Alumnos", color="Curso",
        color_discrete_sequence=colores["alumnos"],
        title="Alumnos por Curso (Quesito)")

@app.callback(Output("grafica-profesores", "figure"), Input("interval", "n_intervals"))
def actualizar_grafica_profesores(n):
    df = obtener_datos(queries["asignaturas_por_profesor"])
    return px.bar(df, x="Profesor", y="Asignaturas", color="Profesor",
        color_discrete_sequence=colores["profesores"],
        title="Asignaturas por Profesor")

@app.callback(Output("quesito-profesores", "figure"), Input("interval", "n_intervals"))
def actualizar_quesito_profesores(n):
    df = obtener_datos(queries["asignaturas_por_profesor"])
    return px.pie(df, names="Profesor", values="Asignaturas", color="Profesor",
        color_discrete_sequence=colores["profesores"],
        title="Asignaturas por Profesor (Quesito)")

@app.callback(Output("grafica-nota-media", "figure"), Input("interval", "n_intervals"))
def actualizar_grafica_nota_media(n):
    df = obtener_datos(queries["nota_media_por_curso"])
    return px.bar(df, x="Curso", y="Media", color="Curso",
        color_discrete_sequence=colores["nota_media"],
        title="Nota Media por Curso")

@app.callback(Output("quesito-nota-media", "figure"), Input("interval", "n_intervals"))
def actualizar_quesito_nota_media(n):
    df = obtener_datos(queries["nota_media_por_curso"])
    return px.pie(df, names="Curso", values="Media", color="Curso",
        color_discrete_sequence=colores["nota_media"],
        title="Nota Media por Curso (Quesito)")

@app.callback(Output("grafica-alumnos-asignatura", "figure"), Input("interval", "n_intervals"))
def actualizar_grafica_alumnos_asignatura(n):
    df = obtener_datos(queries["alumnos_por_asignatura"])
    return px.bar(df, x="Asignatura", y="Alumnos", color="Asignatura",
        color_discrete_sequence=colores["asignaturas"],
        title="Número de Alumnos por Asignatura")

@app.callback(Output("quesito-alumnos-asignatura", "figure"), Input("interval", "n_intervals"))
def actualizar_quesito_alumnos_asignatura(n):
    df = obtener_datos(queries["alumnos_por_asignatura"])
    return px.pie(df, names="Asignatura", values="Alumnos", color="Asignatura",
        color_discrete_sequence=colores["asignaturas"],
        title="Alumnos por Asignatura (Quesito)")

@app.callback(Output("grafica-asignaturas-curso", "figure"), Input("interval", "n_intervals"))
def actualizar_grafica_asignaturas_curso(n):
    df = obtener_datos(queries["asignaturas_por_curso"])
    return px.bar(df, x="Curso", y="Asignaturas", color="Curso",
        color_discrete_sequence=colores["asignaturas_curso"],
        title="Asignaturas por Curso")

@app.callback(Output("quesito-asignaturas-curso", "figure"), Input("interval", "n_intervals"))
def actualizar_quesito_asignaturas_curso(n):
    df = obtener_datos(queries["asignaturas_por_curso"])
    return px.pie(df, names="Curso", values="Asignaturas", color="Curso",
        color_discrete_sequence=colores["asignaturas_curso"],
        title="Asignaturas por Curso (Quesito)")

@app.callback(Output("grafica-nota-media-asignatura", "figure"), Input("interval", "n_intervals"))
def actualizar_grafica_nota_media_asignatura(n):
    df = obtener_datos(queries["nota_media_por_asignatura"])
    return px.bar(df, x="Curso", y="num_alumnos", color="Curso",
        color_discrete_sequence=colores["nota_media_asig"],
        title="Nota Media por Asignatura")

@app.callback(Output("quesito-nota-media-asignatura", "figure"), Input("interval", "n_intervals"))
def actualizar_quesito_nota_media_asignatura(n):
    df = obtener_datos(queries["nota_media_por_asignatura"])
    return px.pie(df, names="Curso", values="num_alumnos", color="Curso",
        color_discrete_sequence=colores["nota_media_asig"],
        title="Nota Media por Asignatura (Quesito)")

if __name__ == "__main__":
    app.run(debug=True)
