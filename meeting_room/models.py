import uuid

from django.db import models
from django.utils import timezone


class Reserve(models.Model):
    """
    予約モデル
    """

    class Meta:
        db_table = 'reserve'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meeting_room_id = models.CharField(verbose_name='会議室ID', max_length=1000)
    reserver_id = models.CharField(verbose_name='予約者ID', max_length=1000)
    status = models.CharField(verbose_name='ステータス', max_length=100)
    number_of_participants = models.IntegerField(verbose_name='想定人数')
    start_datetime = models.DateTimeField(verbose_name='開始日時')
    end_datetime = models.DateTimeField(verbose_name='終了日時')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.status
