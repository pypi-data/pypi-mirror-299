# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class _DashPdf(Component):
    """A _DashPdf component.
_DashPdf is a component that renders a PDF.
It takes a property, `data`, which is the PDF file to be rendered.
It allows navigation through the pages of the PDF.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- buttonClassName (string; default ''):
    CSS class name for the Previous and Next buttons.

- controlsClassName (string; default ''):
    CSS class name for the parent div of label and buttons.

- data (string; required):
    The PDF data to be rendered.

- labelClassName (string; default ''):
    CSS class name for the \"Page X of Y\" label."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_pdf'
    _type = '_DashPdf'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.REQUIRED, buttonClassName=Component.UNDEFINED, labelClassName=Component.UNDEFINED, controlsClassName=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'buttonClassName', 'controlsClassName', 'data', 'labelClassName']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'buttonClassName', 'controlsClassName', 'data', 'labelClassName']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(_DashPdf, self).__init__(**args)
