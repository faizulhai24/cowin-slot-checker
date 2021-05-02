import logging

from django.conf import settings
from django.http import JsonResponse
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR, is_client_error, is_server_error
)
from rest_framework.views import exception_handler
from rest_framework.views import set_rollback

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    data = {}
    headers = {}

    response = exception_handler(exc, context)
    if response is not None:
        headers = response.serialize_headers()
        status = response.status_code
        if is_client_error(response.status_code):
            data['status'] = 'fail'
            data['message'] = response.data
        elif is_server_error(response.status_code):
            data['status'] = 'error'
            data['message'] = response.data
            set_rollback()
            logger.exception('Status:{} Response:{} Headers: {}'.format(status, data, headers))
    elif settings.DEBUG:
        raise
    else:
        data['status'] = 'error'
        data['message'] = {'Error': 'Internal Server Error'}
        status = HTTP_500_INTERNAL_SERVER_ERROR
        set_rollback()
        logger.exception('Status:{} Response:{} Headers: {}'.format(status, data, headers))
    return JsonResponse(data, status=status)
