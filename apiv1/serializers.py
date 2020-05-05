from rest_framework import serializers

from meeting_room.models import Reserve
from shop.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'price']


class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = ['id', 'meeting_room_id', 'reserver_id',
                  'status', 'number_of_participants',
                  'start_datetime', 'end_datetime', ]
