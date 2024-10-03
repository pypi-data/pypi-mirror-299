import logging
from datetime import datetime

import boto3
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import _dash_renderer
import polars as pl
from dash_extensions.enrich import Output, Input, State, html, dcc, Trigger, Serverside, no_update, MATCH, ALL, \
    DashProxy, LogTransform, NoOutputTransform, TriggerTransform, MultiplexerTransform, ServersideOutputTransform

from dash_blueprints.ag_common import ag_options
from dash_blueprints.aio.dropdown_checkbox import DropdownCheckList
from dash_blueprints.aio.favourites import FavouritesS3
from swarkn.helpers import init_logger
import dash_blueprints.dynamic_callbacks as dcbs
from dash_blueprints.aio.ag_grid import AGTable
from dash_blueprints.utils import init_stores
_dash_renderer._set_react_version("18.2.0") #for dmc 0.14

boto3.setup_default_session(profile_name='default', region_name="eu-west-2")
FavouritesS3.BUCKET = 'esop-testbucket'

__ALL__ = [
    dcbs #register dynamic pattern match CBs
]

init_logger()
logger = logging.getLogger(__name__)
Div = html.Div
dt = datetime.fromisoformat

app = DashProxy(__name__,
    transforms=[LogTransform(), NoOutputTransform(), TriggerTransform(), MultiplexerTransform(), ServersideOutputTransform()],
    external_stylesheets=[dbc.themes.BOOTSTRAP, dmc.styles.ALL],
    prevent_initial_callbacks=True,
    # assets_folder='../assets',
)

# dl = dcc.Loading
table = AGTable(app, 'publish', 'in-df',  ag_options())

app.layout = dmc.MantineProvider([
    table.layout,
    html.Button('clickme', 'button'),
    DropdownCheckList(id='ddcl', options=['aa', 'bb'], dropdown_kwargs={'label': 'dropdowncl'})
])

@app.callback(Output('in-df', 'data'), Trigger('button', 'n_clicks'))
def set_grid():
    df = pl.DataFrame({
        'hello': [1, 2, 3],
        'world': ['a', 'b', 'c'],
    })
    return Serverside(df)

init_stores(app)
if __name__ == '__main__':
    app.run_server('0.0.0.0', 8050, debug=True) #debug=True
