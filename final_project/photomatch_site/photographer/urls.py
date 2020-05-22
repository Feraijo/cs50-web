from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'human', views.HumanViewSet)

urlpatterns = [
    #path("", views.index, name="index"),  
    path('', include(router.urls)),
    path('qweqwe/', include('rest_framework.urls', namespace='rest_framework')) 
]
