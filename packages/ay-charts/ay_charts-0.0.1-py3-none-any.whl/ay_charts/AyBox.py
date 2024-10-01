# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AyBox(Component):
    """An AyBox component.
An Ant Chart component
See https://ant-design-charts.antgroup.com/zh/examples/statistics/box/#basic

Keyword arguments:

- id (string; optional):
    ID.

- data (list of dicts; default [{name: 'Oceania', value: [1, 9, 16, 22, 24]}]):
    Data.

- direction (a value equal to: 'vertical', 'horizontal'; default 'horizontal'):
    Direction.

- groupbyField (string; optional):
    Group by/Stratified field.

- height (string | number; optional):
    Height.

- legend (boolean | dict; optional):
    Whether to show legend.

- raw (boolean; default False):
    Whether the data is raw.

- showAxis (boolean; default True):
    Whether to show axis.

- showGrid (boolean; default True):
    Whether to show grid.

- xField (string; default 'name'):
    X Field (Catgories).

- xFieldTitle (string; optional):
    X Axis Title.

- yField (string; default 'value'):
    Y Field (value).

- yFieldTitle (string; optional):
    Y Axis Title."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'ay_charts'
    _type = 'AyBox'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, xField=Component.UNDEFINED, yField=Component.UNDEFINED, xFieldTitle=Component.UNDEFINED, yFieldTitle=Component.UNDEFINED, groupbyField=Component.UNDEFINED, direction=Component.UNDEFINED, legend=Component.UNDEFINED, showAxis=Component.UNDEFINED, height=Component.UNDEFINED, raw=Component.UNDEFINED, showGrid=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'data', 'direction', 'groupbyField', 'height', 'legend', 'raw', 'showAxis', 'showGrid', 'xField', 'xFieldTitle', 'yField', 'yFieldTitle']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data', 'direction', 'groupbyField', 'height', 'legend', 'raw', 'showAxis', 'showGrid', 'xField', 'xFieldTitle', 'yField', 'yFieldTitle']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(AyBox, self).__init__(**args)
