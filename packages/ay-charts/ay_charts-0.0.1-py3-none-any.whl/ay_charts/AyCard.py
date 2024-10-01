# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AyCard(Component):
    """An AyCard component.
A chart wrapper based on the Ant Design card component
See https://ant.design/components/card

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Content to be displayed on the tag.

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- backgroundColor (string; default '#fff'):
    Background color.

- border (boolean; optional):
    Border.

- height (string | number; optional):
    Height.

- title (a list of or a singular dash component, string or number; optional):
    Title.

- width (string | number; default '100%'):
    Width."""
    _children_props = ['title']
    _base_nodes = ['title', 'children']
    _namespace = 'ay_charts'
    _type = 'AyCard'
    @_explicitize_args
    def __init__(self, children=None, title=Component.UNDEFINED, id=Component.UNDEFINED, height=Component.UNDEFINED, width=Component.UNDEFINED, border=Component.UNDEFINED, backgroundColor=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'backgroundColor', 'border', 'height', 'title', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'backgroundColor', 'border', 'height', 'title', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(AyCard, self).__init__(children=children, **args)
