# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AyHistogram(Component):
    """An AyHistogram component.
An Ant Chart component
See https://ant-design-charts.antgroup.com/en/examples/statistics/bar/#bar

Keyword arguments:

- id (string; optional):
    ID.

- binField (string; default 'value'):
    Bin Field (value).

- binFieldTitle (string; optional):
    X Axis Title.

- data (list of dicts; default [    {value: 12.0},    {value: 12.9},    {value: 12.9},    {value: 13.3},    {value: 13.7},    {value: 13.8},    {value: 13.9},    {value: 14.0},    {value: 14.2},    {value: 14.5},    {value: 15},    {value: 15.2},    {value: 15.6},    {value: 16.0},    {value: 16.3},    {value: 17.3},    {value: 17.5},    {value: 17.9},    {value: 18.0},    {value: 18.0},    {value: 20.6},    {value: 21},    {value: 23.4},]):
    Data.

- groupbyField (string; optional):
    Group by/Stratified field.

- height (string | number; optional):
    Height.

- legend (boolean | dict; optional):
    Whether to show legend.

- nBins (number; default 10):
    No. of bins.

- normalize (boolean; default False):
    Wether to normalize/show percentages.

- showAxis (boolean; default True):
    Whether to show axis.

- showGrid (boolean; default True):
    Whether to show grid.

- stack (boolean; default True):
    Whether to stack groups.

- tooltipName (string; optional):
    Name of tooltip.

- valueFieldTitle (string; optional):
    Y Axis Title."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'ay_charts'
    _type = 'AyHistogram'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, binField=Component.UNDEFINED, nBins=Component.UNDEFINED, groupbyField=Component.UNDEFINED, normalize=Component.UNDEFINED, tooltipName=Component.UNDEFINED, legend=Component.UNDEFINED, binFieldTitle=Component.UNDEFINED, valueFieldTitle=Component.UNDEFINED, showAxis=Component.UNDEFINED, stack=Component.UNDEFINED, height=Component.UNDEFINED, showGrid=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'binField', 'binFieldTitle', 'data', 'groupbyField', 'height', 'legend', 'nBins', 'normalize', 'showAxis', 'showGrid', 'stack', 'tooltipName', 'valueFieldTitle']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'binField', 'binFieldTitle', 'data', 'groupbyField', 'height', 'legend', 'nBins', 'normalize', 'showAxis', 'showGrid', 'stack', 'tooltipName', 'valueFieldTitle']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(AyHistogram, self).__init__(**args)
