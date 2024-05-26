from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>', views.get_title, name='url_title_name'),
    path('search/', views.search, name='url_search'),
    path('new/', views.new_page, name='url_new_page'),
    path('random/', views.random_page, name='url_random_page'),
    path('edit/', views.edit, name='url_edit_page'),
    path('save_edit_page/', views.save_edit_page, name='url_save_edit_page'),
]