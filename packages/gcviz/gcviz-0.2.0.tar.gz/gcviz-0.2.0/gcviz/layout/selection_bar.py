from gcviz.flags import Flags
from gcviz.layout.sites_selection import create_site_selection

from datetime import date
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, callback, dash_table, dcc, html

from gcviz.view import View
from gcviz.components import CompoundDropdown
from gcviz.stats import Statistics
import gcviz.style as style


def make_info_div(elements: list[html.Div], title: str) -> html.Div:
    return html.Div(
        elements,
        title=title,
    )


def create_selection_bar(
    views: list[View], sites: list[str], config: dict[str, any]
) -> list[html.Div]:

    view_selection = dbc.DropdownMenu(
        children=dcc.Checklist(
            [
                {
                    "label": html.Div([view.name]),
                    "value": view.name,
                }
                for view in views
            ],
            value=[view.name for view in views],
            labelStyle={"display": "flex"},
            id="checklist-views",
        ),
        label="Views",
        id="dropdown-views",
    )

    layout = html.Div(
        [
            view_selection,
            create_site_selection(sites),
            CompoundDropdown(
                id="dropdown-compounds",
                value="cfc-11",
            ),
            dcc.DatePickerRange(
                id="date-range",
                start_date=date(1980, 1, 1),
                end_date_placeholder_text="End Period",
                display_format="YYYY-MM",
                clearable=True,
            ),
            make_info_div(
                dbc.DropdownMenu(
                    children=dcc.Checklist(
                        [
                            {"label": html.Div([flag.value]), "value": flag.value}
                            for flag in Flags
                        ],
                        value=[],
                        labelStyle={"display": "flex"},
                        id="checklist-flags",
                    ),
                    label="Flags",
                    id="dropdown-flags",
                ),
                title="Select the flags to filter the data",
            ),
            make_info_div(
                dcc.Dropdown(
                    id="dropdown-symbols",
                    options=[
                        {"label": s.capitalize(), "value": s} for s in style.symbols
                    ],
                    value="cross",
                    style={"width": "100px"},
                    clearable=False,
                ),
                title="Select the symbol of the markers in the plots",
            ),
            make_info_div(
                dcc.Dropdown(
                    id="dropdown-scatter-mode",
                    options=[
                        {"label": s.capitalize(), "value": s}
                        for s in style.scatter_modes
                    ],
                    value="markers",
                    style={"width": "150px"},
                    clearable=False,
                ),
                title="Select wether to have markers, lines or both",
            ),
            make_info_div(
                dcc.Dropdown(
                    id="dropdown-datastatistics",
                    options=[
                        {
                            "label": stat.value.replace("-", " ").capitalize(),
                            "value": stat.value,
                        }
                        for stat in Statistics
                    ],
                    value=Statistics.MEAN_MONTHS.value,
                    style={"width": "150px"},
                    clearable=False,
                ),
                title="Statistics to apply to the data. "
                "If you want to see each measurement, select `event` but this "
                "might be slow because of the amount of data",
            ),
            # Button that triggers the plot
            dbc.Button("plot", id="ploting-button"),
            # Sipmple text
            html.Div(id="selecteddata-text"),
        ],
        style={
            "display": "flex",
            "flexWrap": "wrap",
            "justifyContent": "space-around",
            "alignItems": "center",
        },
    )

    @callback(
        Output("selecteddata-text", "children"),
        Input("graph-content", "clickData"),
    )
    def update_selected_data(clickData):
        if clickData is None:
            return "Click on a point to select data"
        datapoint = clickData["points"][0]
        return f"Selected data: {datapoint['x']}, {datapoint['y']:0.2f}"

    @callback(
        Output("checklist-sites", "value"),
        Input("checklist-sites-all", "value"),
        prevent_initial_call=True,
    )
    def select_all_sites(all_sites):
        if "all_sites" in all_sites:
            return sites
        return []

    for view in views:
        # Enable or disable the views
        @callback(
            Output(component_id=view.id, component_property="style"),
            Input(component_id="checklist-views", component_property="value"),
        )
        def show_hide_view(selected_view, view=view):
            if view.name in selected_view:
                return {"display": "block"}
            return {"display": "none"}

    return layout
