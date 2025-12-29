from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
# Импортируем только нужные функции
from courses.views import (
    home, 
    course_list, 
    course_detail, 
    add_comment, 
    signup, 
    favorites_list,
    toggle_favorite,
    profile_view,
    enroll_course,
    delete_enrollment  # Оставили только удаление
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- ПРОФИЛЬ И УПРАВЛЕНИЕ ОБУЧЕНИЕМ ---
    path('profile/', profile_view, name='profile'),
    path('course/enroll/<int:course_id>/', enroll_course, name='enroll_course'),
    
    # Путь только для удаления курса из профиля
    path('enrollment/delete/<int:enrollment_id>/', delete_enrollment, name='delete_enrollment'),
    
    # --- ГЛАВНАЯ И КАТАЛОГ ---
    path('', home, name='home'),
    path('explore/', course_list, name='course_list'),
    path('category/<int:category_id>/', course_list, name='category_filter'),
    
    # --- ДЕТАЛИ И КОММЕНТАРИИ ---
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('add_comment/<int:course_id>/', add_comment, name='add_comment'),
    
    # --- АУТЕНТИФИКАЦИЯ ---
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='courses/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # --- ИЗБРАННОЕ ---
    path('favorites/', favorites_list, name='favorites_list'),
    path('favorite/toggle/<int:course_id>/', toggle_favorite, name='toggle_favorite'),
]