from django.contrib.auth import get_user_model
from django.db import models


class Card(models.Model):
    class Status(models.IntegerChoices):
        UNCHECKED = 0, 'Не проверено'
        CHECKED = 1, 'Проверено'

    id = models.AutoField(primary_key=True, db_column='CardID', verbose_name='ID')
    question = models.CharField(max_length=255, db_column='Question', verbose_name='Вопрос')
    answer = models.TextField(max_length=5000, db_column='Answer', verbose_name='Ответ')
    upload_date = models.DateTimeField(auto_now_add=True, db_column='UploadDate', verbose_name='Дата загрузки')
    views = models.IntegerField(default=0, db_column='Views', verbose_name='Просмотры')
    adds = models.IntegerField(default=0, db_column='Favorites', verbose_name='В избранном')
    # tags = models.ManyToManyField('Tag', through='CardTag', related_name='cards', db_column='Tags', verbose_name='Теги')
    tags = models.ManyToManyField('Tag', related_name='cards', blank=True, db_column='Tags', verbose_name='Теги')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='cards', null=True, blank=True, default=None, verbose_name='Категория')
    status = models.BooleanField(default=False, choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), verbose_name='Проверено')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='cards', null=True, default=None, verbose_name='Автор')

    class Meta:
        db_table = 'Cards'  # имя таблицы в базе данных
        verbose_name = 'Карточка'  # имя модели в единственном числе
        verbose_name_plural = 'Карточки'  # имя модели во множественном числе

    def __str__(self):
        return f'Карточка {self.question} - {self.answer[:50]}'

    def get_absolute_url(self):
        return f'/cards/{self.id}/detail/'


class Tag(models.Model):
    id = models.AutoField(primary_key=True, db_column='TagID')
    name = models.CharField(max_length=100, db_column='Name', verbose_name='Название')

    class Meta:
        db_table = 'Tags'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'Тег {self.name}'


# class CardTag(models.Model):
#     id = models.AutoField(primary_key=True, db_column='CardTagID', verbose_name='ID')
#     card = models.ForeignKey(Card, on_delete=models.CASCADE, db_column='Card_ID', verbose_name='Карточка')
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE, db_column='Tag_ID', verbose_name='Тег')

#     class Meta:
#         db_table = 'Cards_Tags'
#         verbose_name = 'Тег карточки'
#         verbose_name_plural = 'Теги карточек'
#         # Уникальные пары карточки и тег
#         unique_together = ('card', 'tag')

#     def __str__(self):
#         return f'Тег {self.tag.name} для карточки {self.card.question}'

#     def __str__(self):
#         return f'Тег {self.tag.name} для карточки {self.card.question}'


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True, db_column='Name', verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Категория {self.name}'
