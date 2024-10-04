"""Custom Dash components"""

from dash import dcc, html

from gcviz.compounds import compounds_beautify
from gcviz.netcdf import GlobalLoader


class CompoundDropdown(dcc.Dropdown):
    """A dropdown for selecting compounds."""

    def __init__(self, **kwargs):
        loader = GlobalLoader.get()
        kwargs["options"] = [
            {
                "label": html.Span(compounds_beautify(c, as_dash=True)),
                "value": c,
            }
            for c in sorted(loader.compounds)
        ]
        if "value" not in kwargs:
            kwargs["value"] = loader.compounds[0]
        kwargs["searchable"] = True
        kwargs["clearable"] = False
        # Make it long enough to see long compound names
        if "style" not in kwargs:
            kwargs["style"] = {}
        kwargs["style"].update({"width": "200px"})
        super().__init__(**kwargs)
