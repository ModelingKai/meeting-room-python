from rest_framework import viewsets, views, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from shop.models import Book
from .serializers import BookSerializer


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
        serializer.save()
        # レスポンスオブジェクトを作成して返す
        return Response(serializer.data, status.HTTP_201_CREATED)
