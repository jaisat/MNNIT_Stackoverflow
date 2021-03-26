from django.contrib import admin
from .models import *
# Register your models here.\
class QuestionAdmin(admin.ModelAdmin):
    list_display =('title','user')
    search_fields = ('title','detail')
admin.site.register(Question,QuestionAdmin)

class CommentAdmin(admin.ModelAdmin):
     list_display=('answer','comment')

admin.site.register(Comment,CommentAdmin)

admin.site.register(Answer)
class UpvoteAdmin(admin.ModelAdmin):
    list_display=('answer','user')
admin.site.register(Upvote,UpvoteAdmin)
class DownvoteAdmin(admin.ModelAdmin):
    list_display=('answer','user')
admin.site.register(Downvote,DownvoteAdmin)