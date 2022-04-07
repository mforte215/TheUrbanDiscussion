from django.contrib import admin
from .models import Member, Tag, Article, Thread, Comment
admin.site.register(Member)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(Thread)
admin.site.register(Comment)