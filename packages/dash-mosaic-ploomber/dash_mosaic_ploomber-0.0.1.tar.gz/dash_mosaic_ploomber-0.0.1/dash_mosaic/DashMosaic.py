# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashMosaic(Component):
    """A DashMosaic component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- spec (dict; optional):
    The spec object to be visualized.

- uri (string; default ''):
    The URI for the database connector. If empty, uses wasmConnector.
    If starts with 'ws', uses socketConnector. If starts with 'http',
    uses restConnector."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mosaic'
    _type = 'DashMosaic'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, spec=Component.UNDEFINED, uri=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'spec', 'uri']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'spec', 'uri']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DashMosaic, self).__init__(**args)
