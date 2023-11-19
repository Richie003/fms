from django.contrib import admin
from .models import *

class ShareAdmin(admin.ModelAdmin):
    list_display = ('sharer', 'file', 'folder', 'access_link', 'created')
    search_fields = ('sharer', 'file', 'folder', 'access_link')
    list_filter = ('sharer', 'file', 'folder')
    readonly_fields = ('access_link', 'created')


admin.site.register(Share, ShareAdmin)
admin.site.register(FileData)
admin.site.register(Folder)
