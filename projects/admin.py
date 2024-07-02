from django.contrib import admin

from . models import Movies, Review, Tags
# Register your models here.

admin.site.register(Movies)
admin.site.register(Review)
admin.site.register(Tags)