from django.contrib import admin
from .models import *

class ShareAdmin(admin.ModelAdmin):
    list_display = ('sharer', 'file', 'folder', 'access_link', 'created')
    search_fields = ('sharer', 'file', 'folder', 'access_link')
    list_filter = ('sharer', 'file', 'folder')
    readonly_fields = ('access_link', 'created')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('to_user', 'message', 'read_receipt', 'read')
    search_fields = ('to_user', 'message')
    list_filter = ('to_user', 'read_receipt')
    readonly_fields = ('read',)


class FolderAdmin(admin.ModelAdmin):
    list_display = ('user', 'folder', 'created', 'updated')
    list_filter = ('user', 'folder')
    search_fields = ('user', 'folder')

class SubFolderAdmin(admin.ModelAdmin):
    list_display = ('user', 'parent_folder', 'folder', 'created', 'updated')
    list_filter = ('user', 'parent_folder')
    search_fields = ('user', 'folder')

class TrashAdmin(admin.ModelAdmin):
    list_display = ('user', 'from_folder', 'from_folder', 'deleted_on', 'delete_on')
    
admin.site.register(Share, ShareAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(SubFolder, SubFolderAdmin)
admin.site.register(Trash, TrashAdmin)
admin.site.register(FileTable)
admin.site.register(FileData)
admin.site.register(Folder, FolderAdmin)
