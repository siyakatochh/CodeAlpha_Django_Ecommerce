from django.urls import path
from . import views

urlpatterns = [
    # HOME
    path('', views.home, name='home'),

    # PRODUCT DETAILS
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # AUTH
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # CART
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('increase/<int:cart_id>/', views.increase_quantity, name='increase'),
    path('decrease/<int:cart_id>/', views.decrease_quantity, name='decrease'),
    path('remove/<int:cart_id>/', views.remove_cart, name='remove'),

    # ORDERS
    path('orders/', views.my_orders, name='orders'),

    # WISHLIST
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-wishlist/<int:wishlist_id>/', views.remove_wishlist, name='remove_wishlist'),
]