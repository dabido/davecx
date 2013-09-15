from django.contrib import admin
from blog.models import *

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'publish_date')
    prepopulated_fields = {"slug": ("title",)}

class BlogTagAndCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {"slug": ("name", )}

admin.site.register(Post, BlogPostAdmin)
admin.site.register(Category, BlogTagAndCategoryAdmin)
admin.site.register(Tag, BlogTagAndCategoryAdmin)