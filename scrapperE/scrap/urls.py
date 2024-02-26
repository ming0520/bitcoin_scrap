from django.urls import path
from . import views

urlpatterns = [
    path("all_post/", views.all_post, name="all_post"),
    path("scrap_today/", views.scrap_today, name="scrap_today"),
    path("error_post/", views.scrap_today, name="error_post"),

    path("api/bitstamp/add", views.add_bitstamp, name="add_bitstamp"),
    path("api/bitstamphour/add", views.add_bitstamphour, name="add_bitstamphour"),
    path("api/bitstampminute/add", views.add_bitstampminute, name="add_bitstampminute"),

    path("api/bitstamp/save_daily", views.save_bitstamp_daily, name="save_bitstamp_daily"),
    path("api/bitstamp/save_hourly", views.save_bitstamp_hourly, name="save_bitstamp_hourly"),
    path("api/bitstamp/save_minutely", views.save_bitstamp_minutely, name="save_bitstamp_minutely"),

    path("api/post/<str:post_id>/", views.get_post_by_id, name="get_post_by_id"),
    path("api/error_log/add/", views.add_error_log, name="add_error_log"),

    # Bitstamp Crud
    # path('', views.bitstamp_list, name='bitstamp_list'),
    # path('create/', views.bitstamp_create, name='bitstamp_create'),
    # path('<int:pk>/', views.bitstamp_detail, name='bitstamp_detail'),
    # path('<int:pk>/update/', views.bitstamp_update, name='bitstamp_update'),
    # path('<int:pk>/delete/', views.bitstamp_delete, name='bitstamp_delete'),
]

