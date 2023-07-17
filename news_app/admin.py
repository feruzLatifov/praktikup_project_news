from django.contrib import admin
from .models import News, Category, Contact, Comment

# Register your models here.

# admin.site.register(News)
# admin.site.register(Category)
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "publish_time", "status"]
    list_filter = ["category", "status", "created_time", "publish_time"]
    prepopulated_fields = {"slug": ('title',),}
    date_hierarchy = 'publish_time'
    search_fields = ['title', 'body']
    ordering = ['status', 'publish_time']

@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ['id', "name"]

admin.site.register(Contact)

#2-usul
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user__username', 'body']
    actions = ['disable_comments', 'active_comments']

    def disable_comments(self, request, queryset):
        queryset.update(active=False)

    def active_comments(self, request, queryset):
        queryset.update(active=True)
#1-usul
# admin.site.register(Comment, CommentAdmin)