from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField



class Announcement(models.Model):
    POSITIONS = [('Танки', 'Танки'),
                 ('Целители', 'Целители'),
                 ('ДД', 'ДД'),
                 ('Торговцы', 'Торговцы'),
                 ('Гильдмастеры', 'Гильдмастеры'),
                 ('Квестгиверы', 'Квестгиверы'),
                 ('Кузнецы', 'Кузнецы'),
                 ('Кожевники', 'Кожевники'),
                 ('Зельевары', 'Зельевары'),
                 ('Мастера заклинаний', 'Мастера заклинаний')]

    category = models.CharField(max_length=20, choices=POSITIONS, verbose_name='Категория')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    title = models.CharField(max_length=255, unique=True, verbose_name='Название')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    announcement = RichTextUploadingField(null=True, default=None)


    def __str__(self):
        return f'{self.title} (Автор: {self.author.username})'

    def get_absolute_url(self):
        return reverse('anons_detail', args=[str(self.id)])



class Comment(models.Model):
    text = models.CharField(max_length=255, unique=False, verbose_name='Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    anons = models.ForeignKey(Announcement, on_delete=models.CASCADE, default=1, verbose_name='Объявление')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    accepted = models.BooleanField(verbose_name='Одобрение заявки', default=None, null=True)


    def __str__(self):
        return f'comment pk={self.pk} by {self.author.username}'













# from announcement.models import *
# a = Announcement.objects.all().first()



