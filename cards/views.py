from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Card
from .forms import CardForm


info = {
    "menu": [
        {"title": "Главная",
         "url": "/",
         "url_name": "index"},
        {"title": "Каталог",
         "url": "/cards/catalog/",
         "url_name": "catalog"},
        {"title": "Администрирование",
         "url": "/admin:index/",
         "url_name": "admin:index"},
        {"title": "Добавление карточки",
         "url": "/add/",
         "url_name": "add_card"},
        {"title": "О проекте",
         "url": "/about/",
         "url_name": "about"},
    ]
}


class MenuMixin:
    """
    Миксин для вставки меню в шаблон
    """
    timeout = 30  # Время хранения в кэше (в секундах)

    def get_menu(self):
        """
        Возвращает меню из кэша
        return: menu - возвращаем меню
        """
        menu = cache.get('menu')  # получаем меню из кэша
        if not menu:  # если меню нет в кэше
            menu = info['menu']  # то возвращаем меню
            cache.set('menu', menu, timeout=self.timeout)  # сохраняем меню в кэше
        return menu

    def get_cards_count(self):
        """
        Возвращает количество карточек из кэша
        return: cards_count - возвращаем количество карточек
        """
        cards_count = cache.get('cards_count')  # получаем количество карточек из кэша
        if not cards_count:  # если количество карточек нет в кэше
            cards_count = Card.objects.count()  # то возвращаем количество карточек
            cache.set('cards_count', cards_count, timeout=self.timeout)  # сохраняем количество карточек в кэше
        return cards_count

    def get_users_count(self):
        """
        Возвращает количество пользователей из кэша
        return: users_count - возвращаем количество пользователей
        """
        users_count = cache.get('users_count')  # получаем количество пользователей из кэша
        if not users_count:  # если количество пользователей нет в кэше
            users_count = get_user_model().objects.count()  # то возвращаем количество пользователей
            cache.set('users_count', users_count, timeout=self.timeout)  # сохраняем количество пользователей в кэше
        return users_count

    def get_context_data(self, **kwargs):
        """
        Метод для модификации контекста для шаблона
        return: context - возвращаем контекст
        """
        context = super().get_context_data(**kwargs)  # вызываем метод родительского класса. Получаем контекст
        context['menu'] = self.get_menu()  # добавляем в контекст меню
        context['cards_count'] = self.get_cards_count()  # добавляем в контекст количество карточек
        context['users_count'] = self.get_users_count()  # добавляем в контекст количество пользователей
        return context


class AboutView(MenuMixin, TemplateView):
    """
    Выводим страницу о проекте
    """
    template_name = 'about.html'
    extra_context = {'title': 'О проекте'}


class IndexView(MenuMixin, TemplateView):
    """
    Выводим главную страницу
    """
    template_name = 'main.html'


class PageNotFoundView(MenuMixin, TemplateView):
    template_name = '404.html'


class CatalogView(MenuMixin, ListView):
    """
    Выводим каталог карточек
    """
    model = Card  # Указываем модель, данные которой мы хотим отобразить
    template_name = 'cards/catalog.html'  # Путь к шаблону, который будет использоваться для отображения страницы
    context_object_name = 'cards'  # Имя переменной контекста, которую будем использовать в шаблоне
    paginate_by = 10  # Количество объектов на странице

    # Метод для модификации начального запроса к БД
    def get_queryset(self):
        # Получение параметров сортировки из GET-запроса
        sort = self.request.GET.get('sort', 'upload_date')
        order = self.request.GET.get('order', 'desc')
        search_query = self.request.GET.get('search_query', '')

        # Определение направления сортировки
        if order == 'asc':
            order_by = sort
        else:
            order_by = f'-{sort}'

        # Фильтрация карточек по поисковому запросу и сортировка
        if search_query:
            queryset = Card.objects.filter(
                Q(question__iregex=search_query) |
                Q(answer__iregex=search_query) |
                Q(tags__name__iregex=search_query)
            ).select_related('category').prefetch_related('tags').order_by(order_by).distinct()
        else:
            queryset = Card.objects.select_related('category').prefetch_related('tags').order_by(order_by)
        return queryset

    def get_context_data(self, **kwargs):
        # Получение существующего контекста из базового класса
        context = super().get_context_data(**kwargs)
        # добавить номер страницы в контекст
        # context['page'] = self.request.GET.get('page')
        # Добавление дополнительных данных в контекст
        context['sort'] = self.request.GET.get('sort', 'upload_date')
        context['order'] = self.request.GET.get('order', 'desc')
        context['search_query'] = self.request.GET.get('search_query', '')
        return context
        # response = render(request, 'cards/catalog.html', context)
        # response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # - кэш не используется
        # response['Expires'] = '0'  # Перестраховка - устаревание кэша
        # return response
        # return render(request, 'cards/catalog.html', context)


def get_categories(request):
    """
    Возвращает все категории для представления в каталоге
    """
    # Проверка работы базового шаблона
    return render(request, 'base.html', info)


def get_cards_by_category(request, category_id):
    """
    Возвращает карточки по категории для представления в каталоге
    """
    # Добываем карточки из БД по категории
    cards_all = Card.objects.filter(category__id=category_id)
    # Подготавливаем контекст и отображаем шаблон
    # Пагинация
    paginator = Paginator(cards_all, 10)
    page_number = request.GET.get('page', 1)
    cards = paginator.get_page(page_number)

    context = {
        'cards': cards,
        'cards_count': len(cards_all),
        'menu': info['menu'],
    }

    return render(request, 'cards/catalog.html', context)


def get_cards_by_tag(request, tag_id):
    """
    Возвращает карточки по тегу для представления в каталоге
    """
    # Добываем карточки из БД по тегу
    cards_all = Card.objects.filter(tags__id=tag_id)
    # Подготавливаем контекст и отображаем шаблон
    # Пагинация
    paginator = Paginator(cards_all, 10)
    page_number = request.GET.get('page', 1)
    cards = paginator.get_page(page_number)

    context = {
        'cards': cards,
        'cards_count': len(cards_all),
        'menu': info['menu'],
    }
    return render(request, 'cards/catalog.html', context)


class CardDeleteView(DeleteView):
    model = Card  # Указываем модель, с которой работает представление
    success_url = reverse_lazy('catalog')  # URL для перенаправления после успешного удаления карточки
    template_name = 'cards/delete_card.html'  # Указываем шаблон, который будет использоваться для отображения формы подтверждения удаления


def preview_card_ajax(request):
    if request.method == "POST":
        question = request.POST.get('question', '')
        answer = request.POST.get('answer', '')
        category = request.POST.get('category', '')

        # Генерация HTML для предварительного просмотра
        html_content = render_to_string('cards/card_detail.html', {
            'card': {
                'question': question,
                'answer': answer,
                'category': category,
                'tags': ['тест', 'тег'],

            }
        }
                                        )

        return JsonResponse({'html': html_content})
    return JsonResponse({'error': 'Invalid request'}, status=400)


class AddCardCreateView(MenuMixin, LoginRequiredMixin,  CreateView):
    """
    Класс представления для создания карточки
    """
    model = Card  # Указываем модель, с которой работает представление
    form_class = CardForm  # Указываем класс формы для создания карточки
    template_name = 'cards/add_card.html'  # Указываем шаблон, который будет использоваться для отображения формы
    success_url = reverse_lazy('catalog')  # URL для перенаправления после успешного создания карточки
    login_url = reverse_lazy('users:login')  # указываем  URL для входа в систему, который будет использоваться для перенаправления пользователя на страницу аутентификации.
    redirect_field_name = 'next'  # имя параметра запроса, в котором хранится URL-адрес, на который пользователь должен быть перенаправлен после успешного входа в систему.
    
    def form_valid(self, form):
        # Добавляем автора к карточке перед сохранением
        form.instance.author = self.request.user
        # Логика обработки данных формы перед сохранением объекта
        return super().form_valid(form)


class EditCardUpdateView(MenuMixin, LoginRequiredMixin, UpdateView):
    model = Card  # Указываем модель, с которой работает представление
    form_class = CardForm  # Указываем класс формы для редактирования карточки
    template_name = 'cards/add_card.html'  # Указываем шаблон, который будет использоваться для отображения формы
    context_object_name = 'card'  # Имя переменной контекста для карточки
    success_url = reverse_lazy('catalog')  # URL для перенаправления после успешного редактирования карточки


class CardDetailView(MenuMixin, DetailView):
    """
    Класс представления для отображения детальной страницы карточки
    """
    model = Card  # Указываем, что моделью для этого представления является Card
    template_name = 'cards/card_detail.html'  # Указываем путь к шаблону для детального отображения карточки
    context_object_name = 'card'  # Переопределяем имя переменной в контексте шаблона на 'card'

    # Метод для обновления счетчика просмотров при каждом отображении детальной страницы карточки
    def get_object(self, queryset=None):
        # Получаем объект с учетом переданных в URL параметров (в данном случае, pk или id карточки)
        obj = super().get_object(queryset=queryset)
        # Увеличиваем счетчик просмотров на 1 с помощью F-выражения для избежания гонки условий
        Card.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        return obj
