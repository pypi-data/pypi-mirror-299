# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AyBar(Component):
    """An AyBar component.
An Ant Chart component
See https://ant-design-charts.antgroup.com/en/examples/statistics/bar/#bar

Keyword arguments:

- id (string; optional):
    ID.

- data (list of dicts; default [    {        label: 'Blue',        value: 110,    },    {        label: 'White',        value: 220,    },    {        label: 'Pink',        value: 330,    },    {        label: 'Green',        value: 440,    },]):
    Data.

- groupbyField (string; optional):
    Group by/Stratified field.

- height (string | number; optional):
    Height.

- legend (boolean | dict; optional):
    Whether to show legend.

- normalize (boolean; default False):
    Wether to normalize/show percentages.

- showGrid (boolean; default True):
    Whether to show grid.

- showLabel (boolean; default False):
    Whether to show label.

- stack (boolean; default True):
    Whether to stack groups.

- tooltipName (string; default 'No. of Subjects'):
    Name of tooltip.

- width (string | number; optional):
    Width.

- xField (string; default 'label'):
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
    _type = 'AyBar'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, xField=Component.UNDEFINED, yField=Component.UNDEFINED, groupbyField=Component.UNDEFINED, normalize=Component.UNDEFINED, tooltipName=Component.UNDEFINED, showLabel=Component.UNDEFINED, legend=Component.UNDEFINED, xFieldTitle=Component.UNDEFINED, yFieldTitle=Component.UNDEFINED, stack=Component.UNDEFINED, height=Component.UNDEFINED, width=Component.UNDEFINED, showGrid=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'data', 'groupbyField', 'height', 'legend', 'normalize', 'showGrid', 'showLabel', 'stack', 'tooltipName', 'width', 'xField', 'xFieldTitle', 'yField', 'yFieldTitle']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data', 'groupbyField', 'height', 'legend', 'normalize', 'showGrid', 'showLabel', 'stack', 'tooltipName', 'width', 'xField', 'xFieldTitle', 'yField', 'yFieldTitle']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(AyBar, self).__init__(**args)
