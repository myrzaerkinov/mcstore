from django.urls import path

from products import views

urlpatterns = [
    path('api/v1/products/', views.product_list_view),
    path('api/v1/products/<int:id>', views.product_detail_view),
    path('api/v1/register/', views.register),
    path('api/v1/login/', views.login),
    path('api/v1/user_reviews/', views.user_reviews),
    path('api/v1/reviews/', views.reviews_list),
    path('api/v1/reviews/<int:id>', views.reviews_detail),
    path('api/v1/categories/', views.categories),
    path('api/v1/categories/<int:id>', views.categories_id),

]
