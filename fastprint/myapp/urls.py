from django.urls import path
from . import views
from .views import ProdukListAPIView, ProdukDetailAPIView, ProdukFilterByStatusAPIView, login_page, logout_view

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', login_page, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create/', views.produk_create_view, name='produk_create'),
    path('list/', views.produk_list_view, name='produk_list'),
    path('update/<int:id_produk>/', views.produk_update_view, name='produk_update'),
    path('delete/<int:id_produk>/', views.produk_delete_view, name='produk_delete'),

    path('api/produks/', ProdukListAPIView.as_view(), name='api_produk_list'),
    path('api/produks/<int:id_produk>/', ProdukDetailAPIView.as_view(), name='api_produk_detail'),
    path('api/produks/filter/status/', ProdukFilterByStatusAPIView.as_view(), name='api_produk_filter_by_status'),

]
