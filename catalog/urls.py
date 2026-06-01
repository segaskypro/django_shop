from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('create/', views.ProductCreateView.as_view(), name='product_create'),
    path('update/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('unpublish/<int:pk>/', views.unpublish_product, name='unpublish_product'),
    path('contacts/', views.contacts, name='contacts'),
]