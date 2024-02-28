from django.contrib import admin
from.models import PostRaw, CommentRaw,ErrorPost,BitstampData,BitstampDataHour,BitstampDataMinute,ErrorLog

# Register your models here.
admin.site.register(PostRaw)
admin.site.register(CommentRaw)
admin.site.register(ErrorPost)
admin.site.register(BitstampData)
admin.site.register(BitstampDataHour)
admin.site.register(BitstampDataMinute)
admin.site.register(ErrorLog)

