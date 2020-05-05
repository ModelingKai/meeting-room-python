from django.http.response import JsonResponse


def json_reserve(request):
    input_date = '20200505'  # input('日付は？')
    input_start_time = '1100'  # input('開始時刻は？')
    input_end_time = '1200'  # input('終了時刻は？')
    input_meeting_room_id = 'A'  # input('会議室は？')
    input_reserver_id = 'Bob'  # input('あなたはだれ？')
    input_number_of_participants = '4'

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
