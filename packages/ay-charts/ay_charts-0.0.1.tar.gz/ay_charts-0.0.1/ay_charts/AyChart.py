# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AyChart(Component):
    """An AyChart component.
A chart wrapper based on the Ant Design card component
See https://ant.design/components/card

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Content to be displayed on the tag.

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- axis (boolean | dict; optional):
    Whether to show axis (applies to boxes).

- backgroundColor (string; default '#fff'):
    Background color.

- border (boolean; optional):
    Border.

- box (boolean; default False):
    Whether to show box.

- chart (a value equal to: 'bar', 'box', 'histogram', 'pie', 'corr', 'scatter'; optional):
    Type of chart.

- colorField (string; optional):
    Color Field (applies to correlation matrix only).

- data (list of dicts; optional):
    Data.

- direction (a value equal to: 'vertical', 'horizontal'; default 'horizontal'):
    Direction of chart (applies to bars only).

- grid (boolean; default True):
    Whether to show grid.

- groupbyField (string; optional):
    Group by/Stratified field.

- height (string | number; optional):
    Height.

- isCard (boolean; default False):
    Whether to wrap the chart in a card.

- isDonut (boolean; default False):
    Whether the pie is a donut.

- label (boolean; optional):
    Label.

- legend (a value equal to: true, false, 'top', 'right'; optional):
    Legend setting.

- nBins (number; default 10):
    No. of bins (applies to histograms only).

- normalize (boolean; default False):
    Wether to normalize/show percentages (applies to bars only).

- raw (boolean; default False):
    Whether the data is raw (applies to boxes only).

- regression (boolean; default True):
    Whether to show regression lines (applies to scatter plot only).

- stack (boolean; optional):
    Whether to stack groups.

- title (a list of or a singular dash component, string or number; optional):
    Title.

- tooltipName (string; optional):
    Name of tooltip.

- width (string | number; default '100%'):
    Width.

- xField (string; optional):
    X Field (Catgories).

- xFieldTitle (string; optional):
    X Axis Title.

- yField (string; optional):
    Y Field (value).

- yFieldTitle (string; optional):
    Y Axis Title."""
    _children_props = ['title']
    _base_nodes = ['title', 'children']
    _namespace = 'ay_charts'
    _type = 'AyChart'
    @_explicitize_args
    def __init__(self, children=None, data=Component.UNDEFINED, xField=Component.UNDEFINED, yField=Component.UNDEFINED, groupbyField=Component.UNDEFINED, colorField=Component.UNDEFINED, stack=Component.UNDEFINED, nBins=Component.UNDEFINED, normalize=Component.UNDEFINED, chart=Component.UNDEFINED, direction=Component.UNDEFINED, legend=Component.UNDEFINED, axis=Component.UNDEFINED, xFieldTitle=Component.UNDEFINED, yFieldTitle=Component.UNDEFINED, label=Component.UNDEFINED, box=Component.UNDEFINED, raw=Component.UNDEFINED, isDonut=Component.UNDEFINED, id=Component.UNDEFINED, title=Component.UNDEFINED, tooltipName=Component.UNDEFINED, height=Component.UNDEFINED, width=Component.UNDEFINED, border=Component.UNDEFINED, backgroundColor=Component.UNDEFINED, isCard=Component.UNDEFINED, grid=Component.UNDEFINED, regression=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'axis', 'backgroundColor', 'border', 'box', 'chart', 'colorField', 'data', 'direction', 'grid', 'groupbyField', 'height', 'isCard', 'isDonut', 'label', 'legend', 'nBins', 'normalize', 'raw', 'regression', 'stack', 'title', 'tooltipName', 'width', 'xField', 'xFieldTitle', 'yField', 'yFieldTitle']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'axis', 'backgroundColor', 'border', 'box', 'chart', 'colorField', 'data', 'direction', 'grid', 'groupbyField', 'height', 'isCard', 'isDonut', 'label', 'legend', 'nBins', 'normalize', 'raw', 'regression', 'stack', 'title', 'tooltipName', 'width', 'xField', 'xFieldTitle', 'yField', 'yFieldTitle']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(AyChart, self).__init__(children=children, **args)
