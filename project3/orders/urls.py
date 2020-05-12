from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("menu/<str:menu_id>", views.menu_view, name="menu"),
    path("cart", views.cart_view, name="cart"),
]
