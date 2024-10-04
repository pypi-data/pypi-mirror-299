from dataclasses import dataclass, field

from dash import html
from dash.development.base_component import Component


@dataclass
class View:

    name: str
    dash_component: Component
    tools: list[Component] = field(default_factory=list)

    def __post_init__(self):
        self.id = f"div-{self.name}"
        self.div = html.Div(
            [
                html.Div(
                    [
                        html.H3(self.name.capitalize()),
                        html.Div(
                            self.tools,
                            style={
                                "display": "flex",
                                "flexWrap": "wrap",
                                "justifyContent": "space-between",
                                "alignItems": "center",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flexWrap": "wrap",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                    },
                ),
                self.dash_component,
            ],
            id=self.id,
        )
