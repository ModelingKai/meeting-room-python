from rest_framework import viewsets, views, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from shop.models import Book
from src.usecase.reservation.reserve_meeting_room_usecase import ReserveMeetingRoomUsecase
from .serializers import BookSerializer, ReserveSerializer


class BookViewSet(viewsets.ModelViewSet):
    """BookオブジェクトのCRUDをおこなうAPI"""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateAPIView(views.APIView):
    """
    本モデルの登録API
    """

    def post(self, request, *args, **kwargs):
        """本モデル登録APIに対応するハンドラメソッド"""

        # シリアライザオブジェクトを作成
        serializer = BookSerializer(data=request.data)
        # バリデーションを実行
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを登録
        # この時点でDatabaseに保存されるらしい
        serializer.save()
        # レスポンスオブジェクトを作成して返す
        return Response(serializer.data, status.HTTP_201_CREATED)


class ReserveMeetingroomAPIView(views.APIView):
    """
    予約モデルの登録API
    """

    def post(self, request, *args, **kwargs):
        input_date = '20200505'  # input('日付は？')
        input_start_time = '1100'  # input('開始時刻は？')
        input_end_time = '1200'  # input('終了時刻は？')
        input_meeting_room_id = 'A'  # input('会議室は？')
        input_reserver_id = 'Bob'  # input('あなたはだれ？')
        input_number_of_participants = '4'

        # リポジトリを用意する必要があるけど、誰に任せるか
        # Oratorにまかせてみて、こっちのシリアライザとかは全く使わない？
        # もしくは、中身でSerializerを使うRepositoryを作って、差し込むか？

        # ユースケースを呼ぶ
        usecase = ReserveMeetingRoomUsecase()
        usecase.reserve_meeting_room(reservation)

        # シリアライザオブジェクトを作成
        serializer = ReserveSerializer(data=request.data)
