from django.contrib import admin
from .models import Member, Tag, Article
admin.site.register(Member)
admin.site.register(Tag)
admin.site.register(Article)