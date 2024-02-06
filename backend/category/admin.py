from django.contrib import admin

from .models import Category, Phrase


# Register your models here.
class PhraseInline(admin.TabularInline):
    model = Phrase
    readonly_fields = ('phrase', 'active')
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', 'created']
    readonly_fields = ['created']
    search_fields = ['name']
    list_filter = ['active', 'created']
    inlines = [PhraseInline]


class PhraseAdmin(admin.ModelAdmin):
    list_display = ['phrase', 'category', 'active', 'created']
    readonly_fields = ['created']
    search_fields = ['phrase']
    list_filter = ['active', 'created']


admin.site.register(Phrase, PhraseAdmin)
admin.site.register(Category, CategoryAdmin)
