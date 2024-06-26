# cards/forms.py

from django import forms
from .models import Category, Card, Tag
from django.core.exceptions import ValidationError
import re

class CodeBlockValidator:
    def __call__(self, value):
        # Проверяем, содержит ли текст маркер начала блока кода
        if '```' not in value:
            return  # Если нет, то дальше не проверяем

        # Ищем все блоки кода, заключенные в ```
        code_blocks = re.findall(r'```[\s\S]+?```', value)
        # Если не нашли закрывающие ```, генерируем ошибку
        if not code_blocks:
            raise ValidationError("Нет закрывающей пары ```.")

        # Проверяем каждый найденный блок кода на соответствие правилам
        for block in code_blocks:
            self.validate_code_block(block)

    def validate_code_block(self, block):
        # Находим индексы открывающих и закрывающих ```
        opening_tick_index = block.find('```')
        closing_tick_index = block.rfind('```')
        # Если индексы совпадают, значит закрывающие ``` отсутствуют
        if opening_tick_index == closing_tick_index:
            raise ValidationError("Нет закрывающей пары ```.")

        # Проверяем, есть ли пробел перед открывающими ```
        if block[opening_tick_index - 1] == ' ':
            raise ValidationError("Уберите пробел перед открывающими ```.")

        # Определяем начало содержимого после ```
        content_start = opening_tick_index + 3

        # Проверяем, есть ли пробел сразу после открывающих ```
        if block[content_start] == ' ':
            raise ValidationError("Уберите пробел после открывающих ```.")

        # Ищем конец строки с названием языка программирования (первый перенос строки после ```)
        language_name_end = block.find('\n', content_start)
        # Проверяем, есть ли название языка и достаточно ли оно длинное
        if language_name_end == -1 or language_name_end - content_start < 2:
            raise ValidationError("Добавьте название языка программирования после открывающих ```.")

        # Проверяем, есть ли перенос строки после названия языка
        if block[language_name_end + 1] != '\n':
            raise ValidationError("Проверьте, что нет пробелов перед открытием блока кода, и есть перенос строки после названия языка.")

        # Проверяем, нет ли пробелов перед закрывающими ```
        if block[closing_tick_index - 1] == ' ':
            raise ValidationError("Уберите пробел перед закрывающими ```.")

class TagStringValidator:
    def __call__(self, value):
        # Проверяем, что в строке нет пробелов
        if ' ' in value:
            raise ValidationError("Теги не должны содержать пробелов.")


class CardForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label='Категория', widget=forms.Select(attrs={'class': 'form-select'}))
    tags = forms.CharField(label='Теги', required=False, help_text='Перечислите теги через запятую', widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[TagStringValidator()])

    class Meta:
        model = Card
        fields = ['question', 'answer', 'category', 'tags']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 40}),
        }
        labels = {
            'question': 'Вопрос',
            'answer': 'Ответ',
        }

    def clean_tags(self):
        tags_str = self.cleaned_data['tags'].lower()
        tag_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        return tag_list

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        instance.save()

        for tag_name in self.cleaned_data['tags']:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            instance.tags.add(tag)
        return instance
