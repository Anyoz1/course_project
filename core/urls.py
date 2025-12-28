from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
# Импортируем все функции из нашего файла views.py
from courses.views import (
    course_list, 
    course_detail, 
    add_comment, 
    signup, 
    favorites_list,  # Добавили это
    toggle_favorite  # И это
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', course_list, name='course_list'),
    path('category/<int:category_id>/', course_list, name='category_filter'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('add_comment/<int:course_id>/', add_comment, name='add_comment'),
    
    # Регистрация и вход
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='courses/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='course_list'), name='logout'),

    # Избранное (favorites)
    # Здесь мы убрали приставку "views.", так как импортировали функции напрямую
    path('favorites/', favorites_list, name='favorites_list'),
    path('favorite/toggle/<int:course_id>/', toggle_favorite, name='toggle_favorite'),
]