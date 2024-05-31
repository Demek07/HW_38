from django.contrib import admin
from .models import Card, Tag, Category


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в админке
    list_display = ('question', 'category', 'views', 'upload_date', 'status')
    # Поля, которые будут ссылками
    list_display_links = ('question',)
    # Поля по которым будет поиск
    search_fields = ('question', 'answer')
    # Поля по которым будет фильтрация
    list_filter = ('status',)
    # Ordering - сортировка
    ordering = ('-upload_date',)
    # List_per_page - количество элементов на странице
    list_per_page = 12
    # Поля, которые можно редактировать
    list_editable = ('status', 'category')
    actions = ['set_checked', 'set_unchecked']
    # fields = ('question', 'answer', 'category', 'status','tags')
    save_on_top = True
    search_fields = ('question',)
    change_form_template = 'admin/cards/change_form_custom.html'


    @admin.action(description="Пометить как проверенное")
    def set_checked(self, request, queryset):
        updated_count = queryset.update(status=Card.Status.CHECKED)
        self.message_user(request, f"{updated_count} записей было помечено как проверенное")

    @admin.action(description="Пометить как непроверенное")
    def set_unchecked(self, request, queryset):
        updated_count = queryset.update(status=Card.Status.UNCHECKED)
        self.message_user(request, f"{updated_count} записей было помечено как непроверенное")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_editable = ('name',)
    search_fields = ('name',)


# @admin.register(CardTag)
# class CardTagAdmin(admin.ModelAdmin):
#     pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_editable = ('name',)
    search_fields = ('name',)
