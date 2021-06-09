from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('signup', views.signup),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('success', views.success),
    path('news', views.news),
    path('reviews', views.reviews),
    path('forum', views.forum),
    path('process_message', views.post_mess),
    path('like/<int:id>', views.add_like),
    path('delete/<int:id>', views.delete_comment),    
    path('edit/<int:id>', views.edit),
]