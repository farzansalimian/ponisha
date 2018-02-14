from django.contrib import admin
from .models import posts, categories, Profile, PostComments, HomePageSlideShow, CategorySlideShow
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

# Register your models here.
admin.site.register(posts)
admin.site.register(PostComments)
admin.site.register(categories)
admin.site.register(HomePageSlideShow)
admin.site.register(CategorySlideShow)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)