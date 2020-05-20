from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("menu/<str:menu_id>", views.menu_view, name="menu"),
    # path("cart", views.cart_view, name="cart"),
]