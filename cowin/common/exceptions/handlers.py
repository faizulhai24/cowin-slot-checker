from rest_framework.response import Response
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR, is_client_error, is_server_error
)
from rest_framework.views import exception_handler
from rest_framework.views import set_rollback


def custom_exception_handler(exc, context):
    data = {}

    response = exception_handler(exc, context)
    if response is not None:
        status = response.status_code
        if is_client_error(status):
            data['status'] = u'fail'
            data['message'] = response.data
        elif is_server_error(status):
            data['status'] = u'error'
            data['message'] = response.data
            set_rollback()
    else:
        data['status'] = u'error'
        data['message'] = u'Internal Server Error'
        status = HTTP_500_INTERNAL_SERVER_ERROR
        set_rollback()

    return Response(data, status=status)
