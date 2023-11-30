from django.contrib import admin
from .models import Post, Major, Comment

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)


class MajorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Major, MajorAdmin)
