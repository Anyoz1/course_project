from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Course(models.Model):
    category = models.ForeignKey(
        'Category', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='courses', 
        verbose_name="Категория"
    )
    title = models.CharField(max_length=200, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание")
    author_contacts = models.CharField(max_length=200, blank=True, verbose_name="Контакты автора")
    course_url = models.URLField(blank=True, verbose_name="Ссылка на курс (YT/Сайт)")
    
    # НОВОЕ ПОЛЕ:
    is_recommended = models.BooleanField(default=False, verbose_name="Рекомендовать на главной")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    video_url = models.URLField(blank=True) # Ссылка на видео
    content = models.TextField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} на {self.course.title}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course') # Чтобы нельзя было добавить один курс дважды


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    # Новые поля
    is_pinned = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'course')
        # Сначала закрепленные, затем по порядку, затем по дате
        ordering = ['-is_pinned', 'order', '-enrolled_at']