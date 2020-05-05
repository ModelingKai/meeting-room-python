import logging

from django.http.response import JsonResponse


def json_reserve(request):


    id_ = 'datades'
    return JsonResponse(
        data={
            "question": "結果ですよpost"
        },
        status=200
    )


def json_get_reserve():
    return JsonResponse(
        data={
            "question": "結果だよ"
        },
        status=200
    )
