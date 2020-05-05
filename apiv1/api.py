import logging

from django.http.response import JsonResponse


def json_reserve(self, request):
    logging.debug("Whatever to log")


def json_get_reserve(self):
    return JsonResponse(
        data={
            "question": "結果だよ"
        },
        status=200
    )
