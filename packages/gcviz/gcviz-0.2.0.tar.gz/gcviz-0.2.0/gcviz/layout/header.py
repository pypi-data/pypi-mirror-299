from dash import html
import dash_bootstrap_components as dbc


def create_header():
    title = html.H1(children="gcviz", style={"textAlign": "center"})
    description = html.P(
        children="A web application for visualizing atmospheric measurements.",
        style={"textAlign": "center"},
    )
    instruction = html.P(
        children=(
            "Try to select parameters below and click on the 'plot' button to"
            " create the first plot. Different plots are available by selecting"
            " the different views."
        )
    )
    dev_alert = dbc.Container(
        dbc.Alert(
            [
                html.H4("Get started"),
                instruction,
                html.Hr(),
                html.Div(
                    [
                        html.A(
                            "This is currently in developpement. If you have a problem, please report on "
                        ),
                        html.A(
                            "our Gitlab",
                            href="https://gitlab.com/empa503/atmospheric-measurements/gcviz/-/issues",
                        ),
                    ]
                ),
            ],
            color="info",
        ),
        class_name="developpement-alert",
    )
    return html.Div([title, description, dev_alert])
