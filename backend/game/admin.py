from django.contrib import admin

from .models import Guess, Game, GameMap

print("again")


class GuessInline(admin.TabularInline):
    model = Guess
    readonly_fields = ("guess", "correct", "created", "is_word")


class GuessAdmin(admin.ModelAdmin):
    list_filter = ["created", "correct", "is_word", "game"]
    list_display = ["guess", "game", "correct", "created", "is_word"]
    search_fields = ["guess"]
    readonly_fields = ["created"]


class GameAdmin(admin.ModelAdmin):
    list_filter = ["created", "modified"]
    list_display = ["word", "created", "modified", "num_guesses"]
    search_fields = ["word"]
    readonly_fields = [
        "created",
        "modified",
        "num_guesses",
        "num_correct_guesses",
        "num_incorrect_guesses",
    ]
    inlines = [GuessInline]

    @admin.display(description="guesses")
    def num_guesses(self, obj):
        return obj.guesses.count()

    @admin.display(description="correct guesses")
    def num_correct_guesses(self, obj):
        return obj.guesses.filter(correct=True).count()

    @admin.display(description="incorrect guesses")
    def num_incorrect_guesses(self, obj):
        return obj.guesses.filter(correct=False).count()


class GameMapAdmin(admin.ModelAdmin):
    list_filter = ["created", "full"]
    list_display = [
        "game_slug",
        "player_1",
        "player_2",
        "game_1",
        "game_2",
        "created",
        "full",
    ]
    search_fields = ["game_slug"]
    readonly_fields = ["created"]


admin.site.register(Guess, GuessAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(GameMap, GameMapAdmin)
