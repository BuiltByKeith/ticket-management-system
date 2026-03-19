# apps/utils/exceptions.py

from rest_framework.views import exception_handler
from rest_framework import status
from .responses import error_response


def custom_exception_handler(exc, context):
    """
    Overrides DRF's default exception handler to return all errors
    in our standard response format.
    """

    # Call DRF's default handler first to get the standard response
    response = exception_handler(exc, context)

    if response is not None:
        status_code = response.status_code

        # Map common status codes to clean messages
        default_messages = {
            status.HTTP_400_BAD_REQUEST: 'Bad request.',
            status.HTTP_401_UNAUTHORIZED: 'Authentication credentials were not provided or are invalid.',
            status.HTTP_403_FORBIDDEN: 'You do not have permission to perform this action.',
            status.HTTP_404_NOT_FOUND: 'The requested resource was not found.',
            status.HTTP_405_METHOD_NOT_ALLOWED: 'Method not allowed.',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'An internal server error occurred.',
        }

        # Extract the actual error detail from DRF's response
        data = response.data

        # DRF wraps single errors in {"detail": "..."} — extract that
        if 'detail' in data:
            # Use your custom message if defined, otherwise fall back to DRF's
            message = default_messages.get(status_code, str(data['detail']))
            errors = None
        else:
            # Validation errors come as field-level dicts
            message = default_messages.get(status_code, 'An error occurred.')
            errors = data

        return error_response(
            message=message,
            errors=errors,
            status_code=status_code,
        )

    # If response is None, DRF couldn't handle it (unhandled exception)
    # Let Django handle it (500 error)
    return response