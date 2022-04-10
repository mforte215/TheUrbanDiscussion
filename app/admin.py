from django.contrib import admin
from .models import Member, Tag, Article, Thread, Comment


class ThreadAdmin(admin.ModelAdmin):
    readonly_fields = ('latest_comment_date',)




admin.site.register(Member)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Comment)