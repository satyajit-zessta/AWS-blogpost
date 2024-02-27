"""
URL configuration for blogpost_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blogging import views
from blogapi import urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.home, name='home'),


    path('user/', views.user_info, name='user_info'),
    path('user/<int:user_id>', views.user_view, name='user_view'),
    path('user/<int:user_id>/verification/', views.user_verification, name='user_verification'),
    path('user/<int:user_id>/update', views.user_update_profile, name='user_update_profile'),
    path('user/<int:user_id>/delete/', views.user_delete_profile, name='user_delete_profile'),
    path('user/admin/verification/', views.admin_verification, name='admin_verification'),
    path('user/admin/add/', views.add_user, name='add_user'),


    path('post/', views.view_posts, name = "view_posts"),
    path('post/<int:post_id>', views.post_info, name = "post_info"),
    path('post/add/', views.add_post, name = "add_post"),
    path('post/<int:post_id>/verification/', views.update_post, name = "update_post"),
    path('post/<int:post_id>/edit/', views.edit_post, name = "edit_post"),
    path('post/<int:post_id>/delete/', views.delete_post, name = "delete_post"),
    path('post/verification', views.verification_for_add_post, name = 'verification_for_add_post'),
    path('post/add', views.add_post, name = 'add_post'),


    path('tag/', views.view_tags, name = "view_tags"),
    path('tag/<int:tag_id>/verification/', views.update_tag, name = "update_tag"),
    path('tag/<int:tag_id>/edit/', views.edit_tag, name = "edit_tag"),
    path('tag/<int:tag_id>/delete/', views.delete_tag, name = "delete_tag"),
    path('tag/verification', views.verification_for_add_tag, name = 'verification_for_add_tag'),
    path('tag/add', views.add_tag, name = 'add_tag'),

    path('comment/', views.view_comments, name = "view_comments"),
    path('comment/<int:comment_id>', views.comment_info, name = "comment_info"),
    path('comment/<int:comment_id>/verification/', views.update_comment, name = "update_comment"),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name = "edit_comment"),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name = "delete_comment"),
    path('comment/verification', views.verification_for_add_comment, name = 'verification_for_add_comment'),
    path('comment/add', views.add_comment, name = 'add_comment'),


    path('api/', include(urls)),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

