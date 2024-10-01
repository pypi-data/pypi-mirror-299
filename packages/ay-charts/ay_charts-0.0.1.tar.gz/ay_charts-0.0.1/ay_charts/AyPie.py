# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AyPie(Component):
    """An AyPie component.
An Ant Chart component
See https://ant-design-charts.antgroup.com/examples/statistics/pie/#outer-label

Keyword arguments:

- id (string; optional):
    ID.

- data (list of dicts; optional):
    Data.

- donut (boolean; default False):
    If the pie is a donut.

- height (string | number; optional):
    Height.

- legend (boolean | dict | string; optional):
    Whether to show legend.

- showLabel (boolean; default True):
    Whether to show label.

- tooltipName (string; default 'No. of Subjects'):
    Name of tooltip.

- xField (string; default 'name'):
    X Field (Catgories).

- yField (string; default 'value'):
    Y Field (value)."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'ay_charts'
    _type = 'AyPie'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, xField=Component.UNDEFINED, yField=Component.UNDEFINED, legend=Component.UNDEFINED, showLabel=Component.UNDEFINED, tooltipName=Component.UNDEFINED, height=Component.UNDEFINED, donut=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'data', 'donut', 'height', 'legend', 'showLabel', 'tooltipName', 'xField', 'yField']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data', 'donut', 'height', 'legend', 'showLabel', 'tooltipName', 'xField', 'yField']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(AyPie, self).__init__(**args)
