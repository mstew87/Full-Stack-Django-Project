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
    path('add_comment/<int:id>', views.post_comment),
    path('like/<int:id>', views.add_like),
    path('delete/<int:id>', views.delete_comment),
    path('delete_mess/<int:id>', views.delete_post),
    path('edit/<int:id>', views.edit),
    path('edit-post/<int:post_id>', views.edit_post_template),
    path('edit-post', views.edit_post),
    path('add-image', views.add_img)
]