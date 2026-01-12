from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Course, Comment, Category, Favorite, Enrollment
from django.http import JsonResponse

# 1. ГЛАВНАЯ: Рекомендуемые курсы
def home(request):
    courses = Course.objects.filter(is_recommended=True)
    
    if request.user.is_authenticated:
        favorite_ids = list(Favorite.objects.filter(user=request.user).values_list('course_id', flat=True))
    else:
        favorite_ids = request.session.get('favorites', [])

    return render(request, 'courses/home.html', {
        'courses': courses,
        'favorite_ids': favorite_ids
    })

# 2. КАТАЛОГ: Поиск и категории
def course_list(request, category_id=None):
    categories = Category.objects.all()
    current_category = None
    query = request.GET.get('q')
    
    if request.user.is_authenticated:
        favorite_ids = list(Favorite.objects.filter(user=request.user).values_list('course_id', flat=True))
    else:
        favorite_ids = request.session.get('favorites', [])

    if query:
        courses = Course.objects.filter(title__icontains=query)
    elif category_id:
        current_category = get_object_or_404(Category, id=category_id)
        courses = Course.objects.filter(category=current_category)
    else:
        courses = Course.objects.all()
    
    return render(request, 'courses/list.html', {
        'courses': courses,
        'categories': categories,
        'current_category': current_category,
        'favorite_ids': favorite_ids,
        'query': query
    })

# 3. ДЕТАЛИ КУРСА
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_favorite = False
    is_enrolled = False
    
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, course=course).exists()
        is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    else:
        is_favorite = course.id in request.session.get('favorites', [])

    return render(request, 'courses/detail.html', {
        'course': course,
        'is_favorite': is_favorite,
        'is_enrolled': is_enrolled
    })

# 4. ПРОФИЛЬ (Теперь доступен гостям без ошибки)
def profile_view(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        # Сортировка: новые подписки сверху
        enrollments = Enrollment.objects.filter(user=request.user).order_by('-enrolled_at')
    else:
        favorites = []
        enrollments = []
    
    return render(request, 'courses/profile.html', {
        'favorites': favorites,
        'enrollments': enrollments
    })

# 5. УПРАВЛЕНИЕ ОБУЧЕНИЕМ

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('profile')

@login_required
def delete_enrollment(request, enrollment_id):
    # Удаление курса из "Моего обучения"
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, user=request.user)
    enrollment.delete()
    return redirect('profile')

# 6. КОММЕНТАРИИ, ИЗБРАННОЕ И РЕГИСТРАЦИЯ

def add_comment(request, course_id):
    if request.method == "POST" and request.user.is_authenticated:
        course = get_object_or_404(Course, id=course_id)
        text = request.POST.get('comment_text')
        if text:
            Comment.objects.create(course=course, user=request.user, text=text)
    return redirect('course_detail', course_id=course_id)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Синхронизация избранного из сессии (для гостей) в базу данных при регистрации
            session_favs = request.session.get('favorites', [])
            for c_id in session_favs:
                try:
                    c = Course.objects.get(id=c_id)
                    Favorite.objects.get_or_create(user=user, course=c)
                except Course.DoesNotExist: 
                    continue
            request.session['favorites'] = []
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'courses/signup.html', {'form': form})

def toggle_favorite(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.user.is_authenticated:
        fav, created = Favorite.objects.get_or_create(user=request.user, course=course)
        if not created:
            fav.delete()
            status = 'removed'
        else:
            status = 'added'
    else:
        favorites = request.session.get('favorites', [])
        if course_id in favorites:
            favorites.remove(course_id)
            status = 'removed'
        else:
            favorites.append(course_id)
            status = 'added'
        request.session['favorites'] = favorites
        request.session.modified = True
        
    # Если это AJAX запрос, возвращаем JSON, иначе — обычный редирект
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': status})
        
    return redirect(request.META.get('HTTP_REFERER', 'home'))

    
def favorites_list(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        fav_ids = Favorite.objects.filter(user=request.user).values_list('course_id', flat=True)
    else:
        fav_ids = request.session.get('favorites', [])
    courses = Course.objects.filter(id__in=fav_ids)
    return render(request, 'courses/favorites.html', {'courses': courses, 'categories': categories})