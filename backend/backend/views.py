import functools
import logging
import traceback

from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.views import View

logger = logging.getLogger('main')

JSON_DUMBS_PARAMS = {
    'ensure_ascii': False,
}


def _response(data, status=200):

    return JsonResponse(
        data,
        status=status,
        safe=not isinstance(data, list),
        json_dumps_params=JSON_DUMBS_PARAMS
    )


def error_response(exception):
    result = {
        'errorMessage': str(exception),
    }

    _traceback = traceback.format_exc()

    if settings.DEBUG:
        result['traceback'] = _traceback

    logger.error(str(exception) + _traceback)

    return _response(result, status=400)


def base_view(fn):
    @functools.wraps(fn)
    def inner(request, *args, **kwargs):
        try:
            with transaction.atomic():
                return fn(request, *args, **kwargs)
        except Exception as e:
            return error_response(e)

    return inner


class BaseView(View):

    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            return self._response({'errorMessage': str(e)}, status=400)

        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response

    @staticmethod
    def _response(data, *, status=200):
        return _response(data, status)
