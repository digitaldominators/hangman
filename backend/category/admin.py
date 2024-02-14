from django.contrib import admin

from .models import Category, Phrase


# Register your models here.
class PhraseInline(admin.TabularInline):
    model = Phrase
    readonly_fields = ("phrase", "active")
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "active", "created", "phrases"]
    readonly_fields = ["created", "phrases"]
    search_fields = ["name"]
    list_filter = ["active", "created"]

    # takes too long to load
    # inlines = [PhraseInline]

    @admin.display(description="phrases")
    def phrases(self, obj):
        return Phrase.objects.filter(category=obj, active=True).count()


class PhraseAdmin(admin.ModelAdmin):
    list_display = ["phrase", "category", "active", "created"]
    readonly_fields = ["created"]
    search_fields = ["phrase"]
    list_filter = ["active", "created", "category"]


admin.site.register(Phrase, PhraseAdmin)
admin.site.register(Category, CategoryAdmin)
