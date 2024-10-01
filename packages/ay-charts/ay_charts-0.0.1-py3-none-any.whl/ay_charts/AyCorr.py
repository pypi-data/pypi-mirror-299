# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AyCorr(Component):
    """An AyCorr component.
An Ant Chart component
See https://ant-design-charts.antgroup.com/examples/statistics/heatmap/#cell-aggregated

Keyword arguments:

- id (string; optional):
    ID.

- colorField (string; default 'value'):
    Color Field (value).

- data (list of dicts; default [    {        x: 'A',        y: 'B',        value: -0.66,        p: 0.03,    },    {        x: 'A',        y: 'D',        value: 0.04,        p: 0.5,    },    {        x: 'A',        y: 'E',        value: 0.04,        p: 0.9,    },    {        x: 'A',        y: 'C',        value: 0.1,        p: 0.2,    },    {        x: 'C',        y: 'B',        value: 0.08,        p: 0.05,    },    {        x: 'C',        y: 'D',        value: 0.15,        p: 0.01,    },    {        x: 'C',        y: 'E',        value: 0.39,        p: 0.1,    },    {        x: 'C',        y: 'A',        value: 0.1,        p: 0.01,    },    {        x: 'E',        y: 'B',        value: 0.09,        p: 0.01,    },    {        x: 'E',        y: 'D',        value: 0.24,        p: 0.5,    },]):
    Data.

- height (string | number; optional):
    Height.

- legend (boolean | dict | string; optional):
    Whether to show legend.

- legend_title (string; default 'r'):
    Legend title.

- showGrid (boolean; default True):
    Whether to show grid.

- showLabel (boolean; default True):
    Whether to show label.

- step (number; default 0.01):
    Step.

- xField (string; default 'x'):
    X Field (Catgories).

- yField (string; default 'y'):
    Y Field (value)."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'ay_charts'
    _type = 'AyCorr'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, xField=Component.UNDEFINED, yField=Component.UNDEFINED, colorField=Component.UNDEFINED, legend=Component.UNDEFINED, showLabel=Component.UNDEFINED, height=Component.UNDEFINED, step=Component.UNDEFINED, legend_title=Component.UNDEFINED, showGrid=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'colorField', 'data', 'height', 'legend', 'legend_title', 'showGrid', 'showLabel', 'step', 'xField', 'yField']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'colorField', 'data', 'height', 'legend', 'legend_title', 'showGrid', 'showLabel', 'step', 'xField', 'yField']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(AyCorr, self).__init__(**args)
