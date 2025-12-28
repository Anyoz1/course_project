from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Course, Comment, Category, Favorite

# 1. Главная страница с категориями и проверкой избранного
def course_list(request, category_id=None):
    categories = Category.objects.all()
    current_category = None
    
    if request.user.is_authenticated:
        favorite_ids = list(Favorite.objects.filter(user=request.user).values_list('course_id', flat=True))
    else:
        favorite_ids = request.session.get('favorites', [])

    if category_id:
        current_category = get_object_or_404(Category, id=category_id)
        courses = Course.objects.filter(category=current_category)
    else:
        courses = Course.objects.all()
    
    return render(request, 'courses/list.html', {
        'courses': courses,
        'categories': categories,
        'current_category': current_category,
        'favorite_ids': favorite_ids
    })

# 2. Страница курса
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, course=course).exists()
    else:
        is_favorite = course.id in request.session.get('favorites', [])

    return render(request, 'courses/detail.html', {
        'course': course,
        'is_favorite': is_favorite
    })

# 3. ТА САМАЯ ФУНКЦИЯ КОММЕНТАРИЕВ (которой не хватало)
def add_comment(request, course_id):
    if request.method == "POST" and request.user.is_authenticated:
        course = get_object_or_404(Course, id=course_id)
        text = request.POST.get('comment_text')
        if text:
            Comment.objects.create(course=course, user=request.user, text=text)
    return redirect('course_detail', course_id=course_id)

# 4. Регистрация
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('course_list')
    else:
        form = UserCreationForm()
    return render(request, 'courses/signup.html', {'form': form})

# 5. Переключатель избранного
def toggle_favorite(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.user.is_authenticated:
        fav, created = Favorite.objects.get_or_create(user=request.user, course=course)
        if not created:
            fav.delete()
    else:
        favorites = request.session.get('favorites', [])
        if course_id in favorites:
            favorites.remove(course_id)
        else:
            favorites.append(course_id)
        request.session['favorites'] = favorites
        request.session.modified = True
        
    return redirect(request.META.get('HTTP_REFERER', 'course_list'))

# 6. Страница списка избранного
def favorites_list(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        fav_ids = Favorite.objects.filter(user=request.user).values_list('course_id', flat=True)
        courses = Course.objects.filter(id__in=fav_ids)
    else:
        fav_ids = request.session.get('favorites', [])
        courses = Course.objects.filter(id__in=fav_ids)
        
    return render(request, 'courses/favorites.html', {
        'courses': courses, 
        'categories': categories
    })