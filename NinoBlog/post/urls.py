from django.urls import path, include
from . import views


urlpatterns =[

    path("", views.post_list, name='post_list'),
    path("post/<int:pk>", views.readmore, name='readmore'),
    path("form", views.form, name='form'),
    path("comment/<int:pk>", views.add_comment, name='comment'),
    path("accounts/", include('django.contrib.auth.urls')),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('edit/<pk>', views.edit, name='edit'),


]