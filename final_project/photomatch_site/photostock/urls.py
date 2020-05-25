from django.urls import include, path
from rest_framework import routers
from . import views

#router = routers.DefaultRouter()
#router.register(r'human', views.HumanViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    # path('api/', include(router.urls)), 
    # path('api/req/', include('rest_framework.urls', namespace='rest_framework')),
]
