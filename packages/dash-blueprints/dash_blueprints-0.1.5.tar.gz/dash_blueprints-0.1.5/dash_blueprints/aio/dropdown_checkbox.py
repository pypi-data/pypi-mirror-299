import dash_bootstrap_components as dbc
from dash import dcc

def DropdownCheckList(*args, dropdown_kwargs=None, **kwargs):
    """
    TODO: not yet working as expected :(
    """
    dropdown_kwargs = dropdown_kwargs or {}
    return dbc.DropdownMenu(children=[
        dcc.Checklist(*args, **kwargs)
    ], **dropdown_kwargs)
