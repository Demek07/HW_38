from django import template
from django.utils.safestring import mark_safe
import markdown

# в Django это регистрация библиотеки шаблонов, которая позволяет использовать пользовательские теги
# и фильтры в шаблонах Django.
register = template.Library()

# @register это декоратор, который используется в Django для создания простых пользовательских тегов шаблонов.
# simple_tag - это декоратор, который используется для создания простых пользовательских тегов шаблонов.


@register.simple_tag
def markdown_to_html(markdown_text: str) -> str:
    # Включение расширений для улучшеной обработки
    md_extensions = ['extra', 'fenced_code', 'tables']

    # Преобразование Markdown в HTML c расширениями
    html_content = markdown.markdown(markdown_text, extensions=md_extensions)

    return mark_safe(html_content)

# можем менять параметры в запросах (URL)
# @register.simple_tag
# def add_query_params(request, **kwargs):
#     updated = request.GET.copy()
#     for k, v in kwargs.items():
#         updated[k] = v
#     return request.build_absolute_uri('?'+updated.urlencode())
