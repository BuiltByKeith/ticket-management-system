# apps/utils/responses.py

from rest_framework.response import Response
from rest_framework import status


def success_response(message, data=None, status_code=status.HTTP_200_OK):
    """
    Standard success response wrapper.
    All successful API responses go through this.
    """
    return Response(
        {
            'success': True,
            'message': message,
            'data': data,
        },
        status=status_code,
    )


def error_response(message, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Standard error response wrapper.
    All error API responses go through this.
    """
    return Response(
        {
            'success': False,
            'message': message,
            'errors': errors,
        },
        status=status_code,
    )