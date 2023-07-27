from django.contrib import admin
from .models import Review, Comment

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=(
        'pk','text','score'
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=(
        'pk','text','author', 'pub_date'
    )
    

