from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()

app_name = 'apiv1'
urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path(
        'api/books/', views.BookCreateAPIView.as_view()
    ),
    path(
        'api/reserve/', views.ReserveMeetingRoomAPIView.as_view(), name='reserve_api'
    ),
    path(
        'api/get_reserve/', api.json_get_reserve, name='get_reserve_api'
    ),
]
