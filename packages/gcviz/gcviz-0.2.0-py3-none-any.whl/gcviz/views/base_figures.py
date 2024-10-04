from datetime import datetime
import logging

import numpy as np
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dcc, html

from gcviz.compounds import compounds_beautify
import gcviz.defaults as defaults
from gcviz.flags import get_flags_from_checklist
import gcviz.stats as stats
from gcviz.components import CompoundDropdown
from gcviz.stats import Statistics, TimeAverageType, apply_statistics, fit_baseline
from gcviz.view import View
from gcviz.netcdf import GlobalLoader


logger = logging.getLogger("gcviz.views.base_figures")
loader = GlobalLoader.get()

timeseries = View(
    name="timeseries",
    dash_component=dcc.Graph(id="graph-content"),
    tools=[
        dcc.Checklist(
            [{"label": "Fit a baseline to the data", "value": "baseline"}],
            value=[],
            labelStyle={"display": "flex"},
            id="checklist-baseline",
        )
    ],
)


@callback(
    Output("graph-content", "figure"),
    Input("ploting-button", "n_clicks"),
    State("date-range", "start_date"),
    State("date-range", "end_date"),
    State("dropdown-compounds", "value"),
    State("dropdown-symbols", "value"),
    State("checklist-sites", "value"),
    State("checklist-flags", "value"),
    State("dropdown-datastatistics", "value"),
    State("dropdown-scatter-mode", "value"),
    Input("checklist-baseline", "value"),
    prevent_initial_call=True,
)
def update_base_plot(
    n_clicks,
    start_date,
    end_date,
    selected_compound,
    symbol,
    selected_sites,
    flags: list[str],
    statistics,
    scatter_mode,
    baseline: list[str],
):

    logger.info(
        f"Plotting {selected_compound=} from {start_date=} to {end_date=} on {selected_sites=} with {flags=}"
    )

    dt_interval = (
        datetime.strptime(start_date, "%Y-%m-%d") if start_date else None,
        datetime.strptime(end_date, "%Y-%m-%d") if end_date else None,
    )
    fig = go.Figure()

    for site in selected_sites:

        serie = loader.read_data(
            site,
            selected_compound,
            date_interval=dt_interval,
            flags_selected=get_flags_from_checklist(flags),
        )

        if serie is None:
            logger.debug(f"No data found for {site=} {selected_compound=}")
            continue

        serie_to_plot = apply_statistics(serie, Statistics(statistics))

        site_color = defaults.sites_colors.get(site, "black")

        fig.add_trace(
            go.Scatter(
                x=serie_to_plot.index,
                y=serie_to_plot.values,
                mode=scatter_mode,
                marker_symbol=symbol,
                marker_color=site_color,
                name=site,
            )
        )

        if baseline and "baseline" in baseline:
            serie_baseline = fit_baseline(serie)
            if serie_baseline is None:
                logger.warning(
                    f"Could not fit baseline for {site=} {selected_compound=}"
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=serie_baseline.index,
                        y=serie_baseline.values,
                        mode="lines",
                        marker_color=site_color,
                        name=f"{site} baseline",
                    )
                )

    fig.update_layout(
        # xaxis_title="Time",
        yaxis_title=f"{defaults.conc_name} of {compounds_beautify(selected_compound)} [ppt]",
    )
    logger.info(f"Figure Ready")
    return fig
