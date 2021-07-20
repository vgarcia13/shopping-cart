from django.urls import path

from rest_framework.authtoken import views
from api.views import LogoutViewSet, ProductViewSet, CartViewSet, BuyCartViewSet

urlpatterns = [
    path('login/', views.obtain_auth_token, name='login'),
    path('logout/', LogoutViewSet.as_view({'get': 'list'})),
    path('products/', ProductViewSet.as_view()),
    path('cart/', CartViewSet.as_view()),
    path('cart/checkout/', BuyCartViewSet.as_view()),

]