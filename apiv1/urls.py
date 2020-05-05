from django.urls import path, include
from rest_framework import routers

# from . import views
from . import api

router = routers.DefaultRouter()

app_name = 'apiv1'
urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path(
        'api/reserve/', api.json_reserve, name='reserve_api'
    ),
    path(
        'api/get_reserve/', api.json_get_reserve, name='get_reserve_api'
    ),
]
