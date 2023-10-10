from django.contrib import admin

from comment.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "content",
        "date_posted",
    ]
    search_fields = ("content",)
    list_filter = ("content",)
