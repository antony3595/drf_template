import json
from collections import OrderedDict

from rest_framework.compat import SHORT_SEPARATORS, LONG_SEPARATORS, INDENT_SEPARATORS
from rest_framework.renderers import JSONRenderer

from main.response.status import SUCCESS


class CustomJSONResponseRenderer(JSONRenderer):
    media_type = 'application/json'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS

        response_dict = OrderedDict({
            'status': SUCCESS,
            'data': data,
            'error': None,
            'errors': None,
        }
        )
        data = response_dict

        ret = json.dumps(
            data, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii,
            allow_nan=not self.strict, separators=separators
        )

        ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
        return ret.encode()
