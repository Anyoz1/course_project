from django.core.management.base import BaseCommand
from courses.models import Category, Course, Lesson
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write('Начинаю заполнение данных...')

        # 1. Создаем категории
        cat_it, _ = Category.objects.get_or_create(name='Программирование')
        cat_math, _ = Category.objects.get_or_create(name='Математика')
        cat_design, _ = Category.objects.get_or_create(name='Дизайн')

        # 2. Создаем курсы (с пометкой is_recommended)
        # Рекомендуемые (будут на главной)
        Course.objects.get_or_create(
            title='Python для Arch Linux',
            description='Углубленный курс по автоматизации твоей любимой системы.',
            category=cat_it,
            is_recommended=True,
            author_contacts='@arch_python',
            course_url='https://youtube.com'
        )

        Course.objects.get_or_create(
            title='Высшая математика',
            description='Разбираем производные и интегралы с нуля.',
            category=cat_math,
            is_recommended=True,
            author_contacts='@math_pro',
            course_url='https://youtube.com'
        )

        # Обычные курсы (будут в каталоге)
        c3, _ = Course.objects.get_or_create(
            title='Основы Figma',
            description='Как рисовать красивые интерфейсы для веб-приложений.',
            category=cat_design,
            is_recommended=False,
            author_contacts='@design_hub'
        )

        Course.objects.get_or_create(
            title='C++ для профи',
            description='Сложный курс для тех, кто хочет понять, как работает память.',
            category=cat_it,
            is_recommended=False
        )

        # 3. Добавим пару уроков для примера
        Lesson.objects.get_or_create(
            course=c3,
            title='Введение в слои',
            video_url='https://youtube.com/watch?v=example'
        )

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))