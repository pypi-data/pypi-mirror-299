# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AyScatter(Component):
    """An AyScatter component.
An Ant Chart component
See https://ant-design-charts.antgroup.com/examples/statistics/pie/#outer-label

Keyword arguments:

- id (string; optional):
    ID.

- data (list of dicts; optional):
    Data.

- groupbyField (string; optional):
    Group by fied.

- height (string | number; optional):
    Height.

- legend (boolean | dict | string; optional):
    Whether to show legend.

- showGrid (boolean; default True):
    Whether to show grid.

- showRegression (boolean; default True):
    Whether to show regression lines.

- xField (string; default 'x'):
    X Field (Catgories).

- xFieldTitle (string; optional):
    X Axis Title.

- yField (string; default 'y'):
    Y Field (value).

- yFieldTitle (string; optional):
    Y Axis Title."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'ay_charts'
    _type = 'AyScatter'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, xField=Component.UNDEFINED, yField=Component.UNDEFINED, groupbyField=Component.UNDEFINED, legend=Component.UNDEFINED, height=Component.UNDEFINED, showGrid=Component.UNDEFINED, showRegression=Component.UNDEFINED, xFieldTitle=Component.UNDEFINED, yFieldTitle=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'data', 'groupbyField', 'height', 'legend', 'showGrid', 'showRegression', 'xField', 'xFieldTitle', 'yField', 'yFieldTitle']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data', 'groupbyField', 'height', 'legend', 'showGrid', 'showRegression', 'xField', 'xFieldTitle', 'yField', 'yFieldTitle']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(AyScatter, self).__init__(**args)
