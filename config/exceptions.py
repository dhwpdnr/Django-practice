from rest_framework.exceptions import Throttled
from rest_framework.views import exception_handler
from rest_framework.response import Response


class CustomThrottled(Throttled):
    default_detail = "요청이 너무 많습니다. 나중에 다시 시도하세요."
    default_code = "throttled"


def custom_exception_handler(exc, context):
    if isinstance(exc, CustomThrottled):
        return Response(
            {
                "error": "Too many requests",
                "message": "요청이 너무 많습니다. 나중에 다시 시도하세요.",
            },
            status=429,
        )
    return exception_handler(exc, context)
