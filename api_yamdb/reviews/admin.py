from django.contrib import admin

from .models import Category, Comment, Genre, Title, Review, TitleGenre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category'
    )
    search_fields = ('name', 'description')
    list_filter = ('name', 'year')
    empty_value_display = '-empty-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "score",
        "title",
        "author",
        "pub_date"
    )
    search_fields = ("text",)
    list_filter = ("pub_date", "title")
    empty_value_display = "-empty-"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "review",
        "author",
        "pub_date"
    )
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-empty-"


admin.site.register(TitleGenre)
