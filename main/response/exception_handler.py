from collections import OrderedDict

from django.utils.translation import gettext_lazy as _
from rest_framework import renderers
from rest_framework.exceptions import ErrorDetail
from rest_framework.views import exception_handler

from main.response.renderer import CustomJSONResponseRenderer
from main.response.status import FAIL, ERROR


def prepare_errors(errors):
    prepared_error = None

    if isinstance(errors, dict):
        if bool(errors):
            prepared_error = {field: prepare_errors(value) for field, value in errors.items()}
        else:
            prepared_error = None

    elif isinstance(errors, list):
        if any([isinstance(v, str) for v in errors]):
            prepared_error = "\n".join(errors)
        else:
            prepared_error = [prepare_errors(value) for value in errors]

    elif isinstance(errors, ErrorDetail):
        prepared_error = str(errors)
    return prepared_error


def custom_exception_handler(exc, context):
    if isinstance(context['request'].accepted_renderer, CustomJSONResponseRenderer):
        context['request'].accepted_renderer = renderers.JSONRenderer()

    response = exception_handler(exc, context)

    if response is not None:
        if response.has_header("WWW-Authenticate"):
            response.headers["www-authenticate"] = ("WWW-Authenticate", "Custom")

        message = response.data.get('detail') if isinstance(response.data, dict) else "\n".join(response.data)

        if not message:
            errors = prepare_errors(response.data)
            response.data = OrderedDict({
                'status': FAIL,
                'data': None,
                'error': _('Validation Error'),
                'errors': errors,
            })
        else:
            response.data = OrderedDict({
                'status': ERROR,
                'data': None,
                'error': message,
                'errors': None,
            })

    return response
