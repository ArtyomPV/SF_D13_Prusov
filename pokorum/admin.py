from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Post, Comments, Category
# Register your models here.

admin.site.register(
    (Post,
     Comments,
     Category)
)