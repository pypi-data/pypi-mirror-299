import logging
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dcc, html

from gcviz.compounds import compounds_beautify
import gcviz.defaults as defaults
import gcviz.fit as fit
from gcviz.components import CompoundDropdown
from gcviz.flags import get_flags_from_checklist
from gcviz.netcdf import GlobalLoader
from gcviz.stats import Statistics, apply_statistics
from gcviz.view import View

logger = logging.getLogger("gcviz.views.correlation_view")
loader = GlobalLoader.get()

correlation_graph = View(
    name="correlation graph",
    dash_component=dcc.Graph(id="graph-correlation"),
    tools=[
        html.Div(
            [
                html.A("Reference compound"),
                CompoundDropdown(id="dropdown-refcompound", value="cfc-12"),
            ]
        ),
        # checkbox for the statistics
        html.Div(
            [
                html.A("Fit functions"),
                dcc.Checklist(
                    [method.value for method in fit.FittingMethods],
                    inline=True,
                    id="checklist-correlation-fit",
                ),
            ],
        ),
    ],
)


@callback(
    Output("graph-correlation", "figure"),
    Input("ploting-button", "n_clicks"),
    State("date-range", "start_date"),
    State("date-range", "end_date"),
    State("dropdown-compounds", "value"),
    Input("dropdown-refcompound", "value"),
    State("dropdown-symbols", "value"),
    State("checklist-sites", "value"),
    State("checklist-flags", "value"),
    State("dropdown-datastatistics", "value"),
    Input("checklist-correlation-fit", "value"),
    prevent_initial_call=True,
)
def update_correlation_plot(
    n_clicks: int,
    start_date: str,
    end_date: str,
    selected_compound: str,
    reference_compound: str,
    symbol: str,
    selected_sites: list[str],
    flags: list[str],
    statistics: list[str],
    correlation_fit: list[str] | None,
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

        read_kwargs = {
            "site": site,
            "date_interval": dt_interval,
            "flags_selected": get_flags_from_checklist(flags),
        }

        serie = loader.read_data(compound=selected_compound, **read_kwargs)
        serie_ref = loader.read_data(compound=reference_compound, **read_kwargs)

        if serie is None:
            logger.debug(f"No data found for {site=} {selected_compound=}")
            continue
        if serie_ref is None:
            logger.debug(f"No data found for {site=} {reference_compound=}")
            continue

        serie = apply_statistics(serie, Statistics(statistics))
        serie_ref = apply_statistics(serie_ref, Statistics(statistics))

        # Keep only the common index
        y = serie.loc[serie.index.isin(serie_ref.index)].values
        x = serie_ref.loc[serie_ref.index.isin(serie.index)].values

        mask_valid = ~(np.isnan(x) | np.isnan(y))

        # Remove the nan values
        serie_xy: pd.Series = pd.Series(y[mask_valid], index=x[mask_valid])

        # Calculate the pearson correlation
        bias = lambda x: x.values - x.values.mean()
        x_res = bias(serie_xy.index)
        y_res = bias(serie_xy)

        r = np.sum(x_res * y_res) / np.sqrt(np.sum(x_res**2) * np.sum(y_res**2))

        fig.add_trace(
            go.Scatter(
                x=serie_xy.index,
                y=serie_xy.values,
                mode="markers",
                marker_symbol=symbol,
                marker_color=defaults.sites_colors.get(site, "black"),
                name=f"{site} R={r:.3f}",
            )
        )

        if correlation_fit is None:
            continue
        for method in correlation_fit:
            method = fit.FittingMethods(method)
            # Fit the baseline
            func = fit.fit_function(serie_xy, method)
            x = np.linspace(serie_xy.index.min(), serie_xy.index.max(), 100)
            y = func(x)

            # using pandas
            ss_res = ((serie_xy - func(serie_xy.index)) ** 2).sum()
            ss_tot = ((serie_xy - serie_xy.mean()) ** 2).sum()
            r2 = 1 - (ss_res / ss_tot)

            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    mode="lines",
                    line_color=defaults.sites_colors.get(site, "black"),
                    name=f"{method} fit R^2={r2:.3f}",
                )
            )

    fig.update_layout(
        xaxis_title=f"{defaults.conc_name} of {compounds_beautify(reference_compound)} [ppt]",
        yaxis_title=f"{defaults.conc_name} of {compounds_beautify(selected_compound)} [ppt]",
    )
    logger.info(f"Figure Ready")
    return fig
