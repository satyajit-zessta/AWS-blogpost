from django.contrib import admin
from .models import *
from .resources import *
from  import_export.admin import ImportExportModelAdmin
# Register your models here.

class UserImportExportModelAdmin(ImportExportModelAdmin):
    resource_class = UserResource
class PostImportExportModelAdmin(ImportExportModelAdmin):
    resource_class = PostResource
class TagImportExportModelAdmin(ImportExportModelAdmin):
    resource_class = TagResource
class CommentImportExportModelAdmin(ImportExportModelAdmin):
    resource_class = CommentResource

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_display = ('id','first_name', 'last_name', 'email','user_name')
# admin.site.register(User,UserAdmin)

@admin.register(Post)
class PostDetails(PostImportExportModelAdmin):
    list_display = ('id', 'title','content', 'author', 'date')

admin.site.register(Tagging, TagImportExportModelAdmin)
admin.site.register(Comment,CommentImportExportModelAdmin)

