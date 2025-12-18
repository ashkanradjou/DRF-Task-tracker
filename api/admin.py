from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'priority', 'is_done', 'due_date', 'created_at')
    list_filter = ('priority', 'is_done')
    search_fields = ('title', 'description', 'owner__username')
