from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORIES = (
    ('Tanks', 'Танки'),
    ('Hill', 'Хилы'),
    ('DD', 'ДД'),
    ('Merchants', 'Торговцы'),
    ('Guildmaster', 'Гилдмастеры'),
    ('Questgivers', 'Квестгиверы'),
    ('Blacksmith', 'Кузнецы'),
    ('Leatherman', 'Кожевники'),
    ('Potionist', 'Зельевары'),
    ('SpellMaster', 'Мастера заклинаний'),

)


# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=250, choices=CATEGORIES, blank=False, default=None)

    def __str__(self):
        return dict(CATEGORIES)[self.category]

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Post(models.Model):
    """
    Модель объявлений
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    picture = models.ImageField(verbose_name='Изображение', blank=True, null=True, upload_to='media')
    videoLink = models.CharField(max_length=255, verbose_name='Ссылка на видео', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категории',
                                 blank=False,
                                 null=False)
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def get_absolute_url(self):
        return f'post/{self.pk}'

    def __str__(self):
        return self.text[:20] + '...'


class Comments(models.Model):
    """
    Модель комментариев
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    comment = models.TextField(verbose_name='Комментарий')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.comment[:20] + ' ...'
