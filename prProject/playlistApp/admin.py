from django.contrib import admin
from .models import Recommend, Request, Curation, Popular, MyBookmark

# Register your models here.
admin.site.register(Recommend)
admin.site.register(Request)
admin.site.register(Curation)
admin.site.register(Popular)
admin.site.register(MyBookmark)

