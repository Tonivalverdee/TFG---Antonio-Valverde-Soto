import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

# Conexión a la base de datos con SQLAlchemy
engine = create_engine("mysql+pymysql://root:1234@localhost/instituto")

# Función para ejecutar consultas y devolver DataFrame
def obtener_datos(query):
    return pd.read_sql(query, engine)

# Crear app Dash
app = dash.Dash(__name__)
app.title = "Gráficas Instituto"

# Consultas SQL
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
        GROUP BY profesor;
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
    "Nota Media por Asignatura": '''
        SELECT cursos.nombre, COUNT(DISTINCT matriculas.id_alumno) AS num_alumnos
        FROM matriculas
        JOIN asignaturas ON matriculas.id_asignatura = asignaturas.id
        JOIN cursos ON asignaturas.id_curso = cursos.id
        GROUP BY cursos.nombre;
    '''
}

# Gráfica Alumnos por Curso
df_alumnos = obtener_datos(queries["alumnos_por_curso"])
grafica_alumnos = px.bar(
    df_alumnos,
    x="Curso",
    y="Alumnos",
    color="Curso",
    color_discrete_sequence=[ "#FFADAD", "#FFD6A5", "#FDFFB6", "#CAFFBF"],
    title="Alumnos por Curso"
)

# Gráfica de quesitos Alumnos por Curso
df_alumnos_quesitos = obtener_datos(queries["alumnos_por_curso"])
quesitos_alumnos = px.pie(
    df_alumnos_quesitos,
    names="Curso",
    values="Alumnos",
    color="Curso",
    color_discrete_sequence=[ "#FFADAD", "#FFD6A5", "#FDFFB6", "#CAFFBF"],
    title="Alumnos por Curso"
)

# Gráfica Asignaturas por Profesor
df_profesores = obtener_datos(queries["asignaturas_por_profesor"])
grafica_profesores = px.bar(
    df_profesores,
    x="Profesor",
    y="Asignaturas",
    color="Profesor",
    color_discrete_sequence=["#9BF6FF", "#A0C4FF", "#BDB2FF", "#FFC6FF", "#FFFFFC", "#FDCBCA", "#FEE1E8", "#F4D1AE", "#D3F8E2"],
    title="Asignaturas por Profesor"
)

# Gráfica de quesitos Asignaturas por Profesor
df_profesores_quesitos = obtener_datos(queries["asignaturas_por_profesor"])
quesitos_profesores = px.pie(
    df_profesores_quesitos,
    names="Profesor",
    values="Asignaturas",
    color="Profesor",
    color_discrete_sequence=["#9BF6FF", "#A0C4FF", "#BDB2FF", "#FFC6FF", "#FFFFFC", "#FDCBCA", "#FEE1E8", "#F4D1AE", "#D3F8E2"],
    title="Asignaturas por Profesor"
)

# Gráfica Nota Media por Curso
df_nota_media = obtener_datos(queries["nota_media_por_curso"])
grafica_nota_media = px.bar(
    df_nota_media,
    x="Curso",
    y="Media",
    color="Curso",
    color_discrete_sequence=["#E4C1F9", "#FAEDCB", "#C9F2C7", "#B5EAD7"],
    title="Nota Media por Curso"
)

# Gráfica de quesitos Nota Media por Curso
df_nota_media_quesitos = obtener_datos(queries["nota_media_por_curso"])
quesitos_nota_media = px.pie(
    df_nota_media_quesitos,
    names="Curso",
    values="Media",
    color="Curso",
    color_discrete_sequence=["#E4C1F9", "#FAEDCB", "#C9F2C7", "#B5EAD7"],
    title="Nota Media por Curso"
)

# Gráfica Alumnos por Asignatura
df_alumnos_asignaturas = obtener_datos(queries["alumnos_por_asignatura"])
grafica_alumnos_asignaturas = px.bar(
    df_alumnos_asignaturas,
    x="Asignatura",
    y="Alumnos",
    color="Asignatura",
    color_discrete_sequence=["#FFDAC1", "#E2F0CB", "#FFCBC1", "#C2FAFF", "#E0BBE4", "#FFDFD3", "#FFFACD", "#FFDEE9", "#E0F7FA", "#F0F4C3", "#C8E6C9", "#FFCCBC", "#D1C4E9", "#F8BBD0", "#DCEDC8"],
    title="Número de Alumnos por Asignatura"
)

# Gráfica de quesitos Alumnos por Asignatura
df_alumnos_asignaturas_quesitos = obtener_datos(queries["alumnos_por_asignatura"])
quesitos_alumnos_asignaturas = px.pie(
    df_alumnos_asignaturas_quesitos,
    names="Asignatura",
    values="Alumnos",
    color="Asignatura",
    color_discrete_sequence=["#FFDAC1", "#E2F0CB", "#FFCBC1", "#C2FAFF", "#E0BBE4", "#FFDFD3", "#FFFACD", "#FFDEE9", "#E0F7FA", "#F0F4C3", "#C8E6C9", "#FFCCBC", "#D1C4E9", "#F8BBD0", "#DCEDC8"],
    title="Número de Alumnos por Asignatura"
)

# Grafica Asignaturas por Curso
df_asignaturas_por_curso = obtener_datos(queries["asignaturas_por_curso"])
grafica_asignaturas_por_curso = px.bar(
    df_asignaturas_por_curso,
    x="Curso",
    y="Asignaturas",
    color="Curso",
    color_discrete_sequence=["#F0E5DE", "#FFD1DC", "#B5FFF9", "#FFF1C9"],
    title="Asignaturas por Curso"
)

# Gráfica de quesitos Asignaturas por Curso
df_asignaturas_por_curso_quesitos = obtener_datos(queries["asignaturas_por_curso"])
quesitos_asignaturas_por_curso = px.pie(
    df_asignaturas_por_curso_quesitos,
    names="Curso",
    values="Asignaturas",
    color="Curso",
    color_discrete_sequence=["#F0E5DE", "#FFD1DC", "#B5FFF9", "#FFF1C9"],
    title="Asignaturas por Curso"
)

# Graficas
figs = {
    "Alumnos por Curso": grafica_alumnos,
    "Alumnos por Curso (Quesitos)": quesitos_alumnos,
    "Asignaturas por Profesor": grafica_profesores,
    "Asignaturas por Profesor (Quesitos)": quesitos_profesores,
    "Nota Media por Curso": grafica_nota_media,
    "Nota Media por Curso (Quesitos)": quesitos_nota_media,
    "Alumnos por Asignatura": grafica_alumnos_asignaturas,
    "Alumnos por Asignatura (Quesitos)": quesitos_alumnos_asignaturas,
    "Alumnos y Asignaturas por Curso": grafica_asignaturas_por_curso,
    "Alumnos y Asignaturas por Curso (Quesitos)": quesitos_asignaturas_por_curso
}

# Layout
app.layout = html.Div([
    html.H1("Gráficas del Instituto", style={"textAlign": "center"}),
    html.Div([dcc.Graph(figure=fig) for fig in figs.values()], className="graph-container")
])

# Ejecutar app
if __name__ == "__main__":
    app.run(debug=True)