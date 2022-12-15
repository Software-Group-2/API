from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Place,Comment,Rating


# Register your models here.
admin.site.unregister(Group)
admin.site.register(Place)
admin.site.register(Comment)
admin.site.register(Rating)

admin.site.site_header = "Unreveal Database"
