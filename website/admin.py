from django.contrib import admin
from .models import posts, categories

# Register your models here.
admin.site.register(posts)
admin.site.register(categories)
