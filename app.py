import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

SIDEBAR_WIDTH = "240px"

def make_sidebar():
    return html.Div([
        html.Div([
            html.Img(
                src="https://api.iconify.design/mdi/school-outline.svg?color=%236366f1",
                height="32px",
                style={"marginRight": "10px"}
            ),
            html.Span("Instituto", style={
                "fontWeight": "bold", "fontSize": "1.6rem",
                "letterSpacing": "2px", "color": "#6366f1",
                "verticalAlign": "middle"
            }),
        ], style={"marginBottom": "30px", "display": "flex", "alignItems": "center"}),
        html.Hr(style={"borderColor": "#e5e7eb"}),
        dbc.Nav([
            dbc.NavItem(
                dbc.DropdownMenu(
                    label="Dashboards",
                    nav=True,
                    in_navbar=True,
                    toggle_style={"fontWeight": "600", "fontSize": "18px", "color": "#23253a"},
                    children=[
                        dbc.DropdownMenuItem("Alumnos", href="/alumnos"),
                        dbc.DropdownMenuItem("Cursos", href="/cursos"),
                        dbc.DropdownMenuItem("Profesores", href="/profesores"),
                        dbc.DropdownMenuItem("Asignaturas", href="/asignaturas"),
                        dbc.DropdownMenuItem("Matriculas", href="/matriculas"),
                    ],
                    className="mb-2"
                )
            ),
        ], vertical=True, pills=True),
    ], style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": SIDEBAR_WIDTH,
        "padding": "32px 18px 10px 22px",
        "background": "#fff",
        "borderRight": "1.5px solid #e5e7eb",
        "height": "100vh",
        "zIndex": 2,
        "boxShadow": "0 0 24px 0 rgba(76, 78, 100, 0.14)",
        "transition": "background 0.3s"
    })

def make_topbar():
    return html.Div([], style={
        "height": "60px",
        "background": "transparent",
        "marginLeft": SIDEBAR_WIDTH,
        "position": "sticky",
        "top": 0,
        "zIndex": 9,
        "paddingRight": "20px",
        "boxShadow": "none"
    })

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Public+Sans:wght@300;400;500;600;700&display=swap"
    ],
    suppress_callback_exceptions=True,
)
app.title = "Instituto Dashboard"

app.layout = html.Div([
    html.Div(make_sidebar(), id="sidebar"),
    html.Div(make_topbar(), id="topbar"),
    dcc.Location(id="url", refresh=False),
    html.Div(
        dash.page_container,
        id="page-content",
        style={
            "marginLeft": SIDEBAR_WIDTH,
            "padding": "0 24px 24px 24px",
            "minHeight": "100vh",
            "fontFamily": "Public Sans, sans-serif",
            "backgroundColor": "#f4f6fb",
            "transition": "background 0.3s"
        }
    ),
])

if __name__ == "__main__":
    app.run(debug=True)
