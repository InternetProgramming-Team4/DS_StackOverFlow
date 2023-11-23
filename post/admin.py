from django.contrib import admin
from .models import Post, Major

# Register your models here.

admin.site.register(Post)


class MajorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Major, MajorAdmin)