from django.contrib import admin
from .models import Post, Tag, Comment
# Register your models here.







class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": (
            "title",
        )
    }
    list_display = ['title','published','post_date']
    list_filter = ('published', )
    search_fields = ("title__startswith", )

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": (
            "name",
        )
    }
    list_display = ['name']
    list_filter = ("name",)


# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {
#         "slug": (
#             "name",
#         )
#     }
#     list_display = ['name']
#     list_filter = ("name",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'post_time', 'active', 'name', 'body']

admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
# admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
